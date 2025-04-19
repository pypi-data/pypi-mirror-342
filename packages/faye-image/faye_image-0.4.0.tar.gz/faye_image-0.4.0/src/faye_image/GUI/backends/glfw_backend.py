# GLFW backend implementation

import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer
import sys
from typing import Callable, Optional, Tuple, Any

# --- GLFW Window Management ---

def create_glfw_window(width: int = 1280, height: int = 720, title: str = "FyGUI Window") -> Optional[glfw._GLFWwindow]:
    """Initializes GLFW and creates a window with an OpenGL context."""
    if not glfw.init():
        print("Error: Could not initialize GLFW", file=sys.stderr)
        return None

    # Configure GLFW window hints (OpenGL version, etc.)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE) # Required on macOS

    # Create the window
    window = glfw.create_window(width, height, title, None, None)
    if not window:
        glfw.terminate()
        print("Error: Could not create GLFW window", file=sys.stderr)
        return None

    # Make the window's context current
    glfw.make_context_current(window)
    # Enable VSync (optional, but often desired)
    glfw.swap_interval(1)

    # Check OpenGL version (optional)
    print(f"OpenGL Vendor: {gl.glGetString(gl.GL_VENDOR).decode()}")
    print(f"OpenGL Renderer: {gl.glGetString(gl.GL_RENDERER).decode()}")
    print(f"OpenGL Version: {gl.glGetString(gl.GL_VERSION).decode()}")
    print(f"GLSL Version: {gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION).decode()}")


    return window

def shutdown_glfw(window: glfw._GLFWwindow):
    """Cleans up GLFW resources."""
    glfw.destroy_window(window)
    glfw.terminate()

# --- ImGui Integration ---

def setup_imgui(window: glfw._GLFWwindow) -> Tuple[Any, GlfwRenderer]:
    """Initializes ImGui context and the GLFW renderer integration."""
    imgui.create_context()
    impl = GlfwRenderer(window)
    # You might want to load fonts here if needed
    # io = imgui.get_io()
    # io.fonts.add_font_from_file_ttf("path/to/font.ttf", 16)
    # impl.refresh_font_texture()
    return imgui.get_current_context(), impl

def cleanup_imgui(impl: GlfwRenderer, context: Any):
    """Shuts down the ImGui GLFW renderer."""
    impl.shutdown()
    # Note: imgui.destroy_context() might be needed depending on ImGui version/usage
    # imgui.destroy_context(context) # Usually called automatically? Check docs.


# --- Main Loop Structure ---

def run_glfw_loop(window: glfw._GLFWwindow, loop_func: Callable[[], bool]):
    """
    Runs the main GLFW event loop.

    Args:
        window: The GLFW window object.
        loop_func: A callable that performs the rendering for one frame.
                   It should return True to continue the loop, False to exit.
    """
    impl = None
    context = None
    try:
        context, impl = setup_imgui(window)

        while not glfw.window_should_close(window):
            glfw.poll_events()
            impl.process_inputs()

            imgui.new_frame()

            # Call the user's rendering function
            if not loop_func():
                break # Exit loop if requested by loop_func

            imgui.render()

            # Clear screen (or render your scene behind ImGui)
            fb_width, fb_height = glfw.get_framebuffer_size(window)
            gl.glViewport(0, 0, fb_width, fb_height)
            gl.glClearColor(0.1, 0.1, 0.1, 1.0) # Dark grey background
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            # Render ImGui draw data
            impl.render(imgui.get_draw_data())

            glfw.swap_buffers(window)

    except Exception as e:
        print(f"Error during GLFW loop: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc() # Print full traceback for debugging
    finally:
        # Cleanup
        if impl and context:
            cleanup_imgui(impl, context)
        shutdown_glfw(window)


# --- Example Usage (Standalone Test) ---
if __name__ == "__main__":
    def simple_gui_loop():
        """A simple ImGui frame for testing the backend."""
        imgui.begin("GLFW Backend Test")
        imgui.text("Hello from ImGui via GLFW!")
        if imgui.button("Click Me"):
            print("Button clicked!")
        imgui.end()

        # Return True to keep running
        return True

    print("Initializing GLFW window...")
    window = create_glfw_window(title="GLFW Backend Test")

    if window:
        print("Running main loop...")
        run_glfw_loop(window, simple_gui_loop)
        print("Loop finished.")
    else:
        print("Failed to create window.")
