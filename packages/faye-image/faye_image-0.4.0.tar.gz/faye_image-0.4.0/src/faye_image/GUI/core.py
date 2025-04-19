"""
Define the interactive input of the GUI

We want to simplify the input definition for developers to convinently create their own interactive visualizer gui.
The syntax is as follows:
```python

@FyINPUT
class MyInput:
    attr1 = FyINT(0, 100, default=1, step=2) # The range is [0, 100], the later two arguments are optional
    attr2 = FyFLOAT(0.0, 1.0, default=0.5, step=0.1) # The range is [0.0, 1.0], the later two arguments are optional
    attr3 = FySTR(default='Hello, World!') # The default value is 'Hello, World!'
    attr4 = FyBOOL(default=True) # The default value is True
    attr5 = FyCHOICE(['A', 'B', 'C'], default='A') # The default value is 'A'
    attr6 = FyPATH(default='./test.png') # The default value is './test.png'
    attr7 = FyIMAGE(default='./test.png') # The default value is './test.png'

```
"""

import imgui
import time
import copy
import sys
from typing import Type, Callable, Optional, Dict, Any, List, Tuple

# Import local modules
from .inputs import FyInputType, get_registered_inputs, FyIMAGE
from .widgets import BaseWidget, create_widget, WidgetState
from .context import FyContext
from .backends.glfw_backend import create_glfw_window, run_glfw_loop
from .utils import release_all_textures, load_image_as_texture, release_texture
from .exceptions import ValidationError, ImageLoadError

# Placeholder for the user's callback result (image data)
CallbackResult = Any # Could be PIL Image, numpy array, etc.

class FyGUI:
    """
    Core class for the interactive ImGui-based visualization tool.
    """
    def __init__(self,
                 input_cls: Type,
                 window_size: Optional[List[int]] = None,
                 window_title: str = "FyGUI Interactive Tool",
                 **kwargs):
        """
        Initializes the FyGUI application.

        Args:
            input_cls: The user-defined class decorated with @FyINPUT.
            window_size: Optional list [width, height] for the window. Defaults to fullscreen-like size.
            window_title: The title for the application window.
            **kwargs: Initial key-value pairs for the shared FyContext.
        """
        self.input_cls = input_cls
        self.window_title = window_title
        self.context = FyContext(**kwargs)

        # --- Window Setup ---
        # Determine window size (use a large default, not true fullscreen yet)
        # TODO: Implement actual fullscreen or better default sizing
        self.width = (window_size[0] if window_size and len(window_size) > 0 else 1600)
        self.height = (window_size[1] if window_size and len(window_size) > 1 else 900)
        self.window = None # Will be initialized in run()

        # --- Input Parameter Handling ---
        self.input_definitions: Dict[str, FyInputType] = get_registered_inputs(input_cls)
        self.param_state: Dict[str, Any] = self._get_initial_param_state()
        self.param_snapshot: Dict[str, Any] = copy.deepcopy(self.param_state) # Snapshot for revert
        self.widgets: Dict[str, BaseWidget] = self._create_widgets()
        self.params_changed: bool = True # Start dirty to run callback initially
        self.validation_errors: Dict[str, str] = {} # Store validation errors per widget

        # --- Callback & Result Handling ---
        self.callback: Optional[Callable[[Any, FyContext], CallbackResult]] = None
        self.callback_result: Optional[CallbackResult] = None
        self.result_texture_id: Optional[int] = None
        self.result_texture_width: int = 0
        self.result_texture_height: int = 0
        self.callback_error: Optional[str] = None
        self.last_callback_time = 0.0
        self.callback_debounce_time = 0.1 # Debounce callback calls (seconds)

        # --- Internal State ---
        self._is_running = False

        # --- Const ---
        self.initial_param_width = 300
        self.param_start_pos = (5, 5) # Initial position for the parameter window
        self.param_result_gap = 10 # Gap between parameter and result windows

    def _get_initial_param_state(self) -> Dict[str, Any]:
        """Gets the default values from the input definitions."""
        defaults = {}
        for name, definition in self.input_definitions.items():
            try:
                # Validate the default value itself
                defaults[name] = definition.validate(definition.default)
            except ValidationError as e:
                print(f"Warning: Default value for '{name}' is invalid: {e}. Using raw default.")
                defaults[name] = definition.default # Use raw default if validation fails
        return defaults

    def _create_widgets(self) -> Dict[str, BaseWidget]:
        """Creates widget instances based on input definitions and initial state."""
        widgets = {}
        for name, definition in self.input_definitions.items():
            initial_value = self.param_state.get(name) # Should always exist
            widgets[name] = create_widget(name, definition, initial_value)
        return widgets

    def _create_param_instance(self) -> Any:
        """Creates an object to pass to the callback, holding current param values."""
        # Create a simple namespace object or a dynamic class instance
        # Using a simple class for attribute access feels more Pythonic
        class ParamContainer:
            pass

        instance = ParamContainer()
        for name, value in self.param_state.items():
            setattr(instance, name, value)

        # Optionally, add the original definition class for reference?
        # setattr(instance, '_definition_cls', self.input_cls)
        return instance

    def _update_param_state_from_widgets(self) -> bool:
        """Updates self.param_state based on widget values and returns True if any changed."""
        changed = False
        self.validation_errors.clear()
        for name, widget in self.widgets.items():
            current_widget_value = widget.get_value()
            # Check for validation errors stored in the widget's state
            if widget.state.error_message:
                 self.validation_errors[name] = widget.state.error_message
                 # If a widget has an error, we might not want to trigger the callback
                 # or revert the specific change? The widget handles revert internally now.

            # Update the central param_state
            if name not in self.param_state or self.param_state[name] != current_widget_value:
                # Check if the change was actually accepted by the widget (valid)
                if not widget.state.error_message:
                    self.param_state[name] = current_widget_value
                    changed = True
                # else: change was rejected by widget due to validation, state not updated

        return changed

    def _take_snapshot(self):
        """Stores the current valid parameter state."""
        # Snapshot only if there are no current validation errors?
        # Or snapshot regardless, and revert logic handles errors?
        # Let's snapshot the current state, revert logic will use it if needed.
        self.param_snapshot = copy.deepcopy(self.param_state)
        # print("Snapshot taken:", self.param_snapshot)


    def _run_callback_if_needed(self):
        """Checks if parameters changed and runs the user callback."""
        if self.params_changed and self.callback and not self.validation_errors:
            current_time = time.monotonic()
            # Debounce the callback
            if current_time - self.last_callback_time > self.callback_debounce_time:
                print("Parameters changed, running callback...")
                param_instance = self._create_param_instance()
                try:
                    self.callback_error = None
                    result = self.callback(param_instance, self.context)
                    self._update_result_texture(result)
                    self.last_callback_time = current_time
                except Exception as e:
                    self.callback_error = f"Error in callback function: {type(e).__name__}: {e}"
                    print(f"Error: {self.callback_error}")
                    import traceback
                    traceback.print_exc() # Log full traceback
                    # Clear previous result on error?
                    self._update_result_texture(None)

                self.params_changed = False # Reset flag after running
                self._take_snapshot() # Take snapshot after successful callback run? Or after any change? After change.

    def _update_result_texture(self, result_data: Optional[CallbackResult]):
        """Converts callback result (e.g., PIL Image) to an OpenGL texture for display."""
        # Release previous texture
        if self.result_texture_id is not None:
            release_texture(texture_id=self.result_texture_id)
            self.result_texture_id = None
            self.result_texture_width = 0
            self.result_texture_height = 0

        self.callback_result = result_data # Store raw result

        if result_data is None:
            return # No result to display

        # --- Convert result_data to texture ---
        # This part depends heavily on the expected format of result_data
        # Example: Assuming result_data is a PIL Image
        try:
            from PIL import Image
            if isinstance(result_data, Image.Image):
                # Need a way to save PIL image to bytes or temp file to use load_image_as_texture
                # Or adapt load_image_as_texture to take PIL image directly
                # Let's try adapting the texture loading logic here for simplicity

                import OpenGL.GL as gl # Ensure gl is available
                if not gl:
                     raise RuntimeError("PyOpenGL not available for texture creation.")

                img = result_data
                img_format = img.mode
                width, height = img.size

                # Convert image format to OpenGL format constants
                if img_format == 'RGB':
                    gl_format = gl.GL_RGB
                    internal_format = gl.GL_RGB
                    pixel_type = gl.GL_UNSIGNED_BYTE
                    img_data = img.tobytes("raw", "RGB", 0, -1)
                elif img_format == 'RGBA':
                    gl_format = gl.GL_RGBA
                    internal_format = gl.GL_RGBA
                    pixel_type = gl.GL_UNSIGNED_BYTE
                    img_data = img.tobytes("raw", "RGBA", 0, -1)
                elif img_format == 'L': # Grayscale
                    gl_format = gl.GL_LUMINANCE
                    internal_format = gl.GL_LUMINANCE
                    pixel_type = gl.GL_UNSIGNED_BYTE
                    img_data = img.tobytes("raw", "L", 0, -1)
                else:
                    print(f"Warning: Result image format {img_format} not directly supported, converting to RGBA.")
                    img = img.convert('RGBA')
                    gl_format = gl.GL_RGBA
                    internal_format = gl.GL_RGBA
                    pixel_type = gl.GL_UNSIGNED_BYTE
                    img_data = img.tobytes("raw", "RGBA", 0, -1)
                    width, height = img.size

                # Create OpenGL texture
                texture_id = gl.glGenTextures(1)
                gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id)
                gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
                gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
                gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
                gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
                gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
                gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, internal_format, width, height, 0,
                                  gl_format, pixel_type, img_data)
                gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

                self.result_texture_id = texture_id
                self.result_texture_width = width
                self.result_texture_height = height
                print(f"Result texture updated: ID={texture_id}, Size={width}x{height}")

            # Add handlers for other types (e.g., numpy arrays) here
            # elif isinstance(result_data, np.ndarray):
            #    ... handle numpy array ...
            else:
                 raise TypeError(f"Unsupported callback result type: {type(result_data)}. Expected PIL Image or similar.")

        except ImportError:
             self.callback_error = "Pillow library not found, cannot process image result."
             print(f"Error: {self.callback_error}")
        except Exception as e:
             self.callback_error = f"Error processing callback result: {e}"
             print(f"Error: {self.callback_error}")
             import traceback
             traceback.print_exc()
             # Ensure texture ID is cleared on error
             if self.result_texture_id is not None:
                 release_texture(texture_id=self.result_texture_id)
                 self.result_texture_id = None
                 self.result_texture_width = 0
                 self.result_texture_height = 0


    def _render_parameter_window(self):
        """Renders the floating window with input widgets."""
        # Explicitly set an initial position for the parameter window
        # Using APPEARING condition means it only sets the position the first time
        # or when the window hasn't been seen for a while. User can move it later.
        viewport = imgui.get_main_viewport()
        window_size = (self.initial_param_width, viewport.size.y)
        window_pos = self.param_start_pos
        imgui.set_next_window_position(window_pos[0], window_pos[1], condition=imgui.APPEARING)
        imgui.set_next_window_size(window_size[0], window_size[1], condition=imgui.APPEARING)

        # Make parameter window floating and potentially resizable/movable
        imgui.begin("Parameters", closable=False)

        widget_changed = False
        for name, widget in self.widgets.items():
            # Render widget and check if its value changed *and* was validated
            if widget.render():
                widget_changed = True
                # No need to update self.param_state here, _update_param_state_from_widgets does that

            # Add spacing between widgets
            imgui.separator()

        # If any widget reported a validated change, mark parameters as dirty
        if widget_changed:
            # Update the central state from all widgets
            # This ensures self.param_state is consistent before snapshot/callback
            self._update_param_state_from_widgets()
            self.params_changed = True
            self._take_snapshot() # Take snapshot immediately after a valid change is detected


        # Display general validation errors or callback errors at the bottom
        if self.validation_errors:
             imgui.push_style_color(imgui.COLOR_TEXT, 1.0, 0.0, 0.0, 1.0)
             imgui.text_wrapped("Input errors detected. Please correct the highlighted fields.")
             imgui.pop_style_color()

        imgui.end()

    def _render_result_window(self):
        """Renders the main area displaying the callback result (image)."""

        # --- Set position and size for the *next* window ---
        viewport = imgui.get_main_viewport()
        window_pos = (self.initial_param_width + self.param_result_gap, 0)
        # Take remaining width, full height
        window_size = (viewport.size.x - window_pos[0], viewport.size.y)
        imgui.set_next_window_position(window_pos[0], window_pos[1], condition=imgui.APPEARING)
        imgui.set_next_window_size(window_size[0], window_size[1], condition=imgui.APPEARING)
        # --- End setting next window ---

        imgui.begin("Result", closable=False)

        if self.callback_error:
            imgui.push_style_color(imgui.COLOR_TEXT, 1.0, 0.0, 0.0, 1.0)
            imgui.text_wrapped(f"Callback Error: {self.callback_error}")
            imgui.pop_style_color()
        elif self.result_texture_id is not None:
            # Get available content region size (width, height)
            available_w, available_h = imgui.get_content_region_available() # Use the correct function

            # Calculate display size, maintaining aspect ratio
            aspect_ratio = self.result_texture_width / self.result_texture_height if self.result_texture_height else 1
            display_w = available_w
            display_h = display_w / aspect_ratio

            if display_h > available_h:
                display_h = available_h
                display_w = display_h * aspect_ratio

            # Center the image
            cursor_x = (available_w - display_w) / 2
            cursor_y = (available_h - display_h) / 2
            cursor_x = max(0, cursor_x)
            cursor_y = max(0, cursor_y)
            # Get current cursor pos to add offset, don't just set absolute offset
            current_cursor_pos = imgui.get_cursor_pos()
            imgui.set_cursor_pos((current_cursor_pos.x + cursor_x, current_cursor_pos.y + cursor_y))


            imgui.image(self.result_texture_id, display_w, display_h)
        else:
            imgui.text("Result will be displayed here.")

        imgui.end()


    def _main_loop_iteration(self) -> bool:
        """Performs rendering for one frame. Returns True to continue, False to exit."""
        # Check for parameter changes from widgets
        # self._update_param_state_from_widgets() # Moved inside _render_parameter_window logic

        # Run callback if parameters changed and are valid
        self._run_callback_if_needed()

        # Render UI elements
        self._render_parameter_window()
        self._render_result_window()

        # Handle window closing or other exit conditions if needed
        # The backend loop handles glfw.window_should_close()

        return True # Return True to keep the loop running


    def run(self, callback: Callable[[Any, FyContext], CallbackResult]):
        """
        Starts the FyGUI application window and runs the main loop.

        Args:
            callback: The user-defined function to call when parameters change.
                      It receives the parameter state object and the FyContext.
                      It should return the data to be visualized (e.g., a PIL Image).
        """
        if self._is_running:
            print("Error: FyGUI is already running.")
            return

        self.callback = callback
        self._is_running = True
        self.params_changed = True # Ensure callback runs on first frame

        try:
            print("Initializing FyGUI window...")
            self.window = create_glfw_window(self.width, self.height, self.window_title)
            if not self.window:
                raise RuntimeError("Failed to create GLFW window.")

            print("Starting main loop...")
            # Pass the instance method as the loop function
            run_glfw_loop(self.window, self._main_loop_iteration)

        except Exception as e:
            print(f"Fatal error during FyGUI execution: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
        finally:
            print("FyGUI shutting down...")
            # Cleanup OpenGL resources
            release_all_textures()
            if self.result_texture_id is not None:
                 try:
                     release_texture(texture_id=self.result_texture_id)
                 except Exception as e:
                     print(f"Warning: Error releasing result texture during shutdown: {e}")

            # Backend cleanup is handled within run_glfw_loop's finally block
            self._is_running = False
            self.window = None
            print("FyGUI shutdown complete.")


# --- Example Usage ---
if __name__ == '__main__':
    # Need to run this from the root directory or adjust imports
    # Example requires Pillow: pip install Pillow
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("Please install Pillow to run the example: pip install Pillow")
        exit()
    from .inputs import FyINPUT, FyINT, FySTR, FyBOOL, FyCHOICE

    # 1. Define Input Structure
    @FyINPUT
    class MyInputs:
        seed = FyINT(0, 10000, default=42)
        width = FyINT(min_val=50, max_val=500, default=200)
        height = FyINT(min_val=50, max_val=500, default=150)
        message = FySTR(default="Hello FyGUI!")
        color = FyCHOICE(['Red', 'Green', 'Blue', 'Yellow'], default='Blue')
        use_border = FyBOOL(default=True)
        # image_path = FyIMAGE(default="", must_exist=True) # Example image input

    # 2. Define Callback Function
    def generate_image(params: MyInputs, context: FyContext) -> Image.Image:
        """Callback that generates a simple image based on inputs."""
        print(f"Generating image with seed={params.seed}, size=({params.width}x{params.height})")
        # Access context
        frame = context.get('frame_count', 0) # Example of reading from context
        context['last_seed'] = params.seed   # Example of writing to context

        img = Image.new('RGB', (params.width, params.height), color='white')
        draw = ImageDraw.Draw(img)

        text = f"{params.message}\\nSeed: {params.seed}\\nFrame: {frame}"
        text_color = params.color.lower()

        # Simple text drawing
        try:
             # Use a basic font if possible, otherwise default
             from PIL import ImageFont
             try:
                 # font = ImageFont.truetype("arial.ttf", 15) # Try loading a common font
                 font = ImageFont.load_default() # Fallback
             except IOError:
                 font = ImageFont.load_default()
             draw.text((10, 10), text, fill=text_color, font=font)
        except ImportError:
             draw.text((10, 10), text, fill=text_color) # Fallback without ImageFont


        if params.use_border:
            border_color = (0,0,0) # Black border
            draw.rectangle([(0, 0), (params.width - 1, params.height - 1)], outline=border_color, width=2)

        # Simulate some work
        time.sleep(0.1)

        # Update context (example)
        context['frame_count'] = frame + 1

        return img

    # 3. Initialize and Run FyGUI
    gui = FyGUI(MyInputs, window_title="Simple Image Generator", frame_count=0) # Pass initial context
    gui.run(generate_image)
