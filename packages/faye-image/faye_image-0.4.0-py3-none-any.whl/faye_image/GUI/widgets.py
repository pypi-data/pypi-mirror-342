# Define widget interface and implementations

import imgui
import abc
import os
from typing import Any, Dict, Optional, Tuple, Callable

from .inputs import FyInputType, FyINT, FyFLOAT, FySTR, FyBOOL, FyCHOICE, FyPATH, FyIMAGE
from .utils import open_path_dialog, truncate_path, load_image_as_texture, release_texture
from .exceptions import ValidationError, ImageLoadError

# --- Widget State & Interface ---

class WidgetState:
    """Holds the current value and error state for a widget."""
    def __init__(self, initial_value: Any):
        self.value: Any = initial_value
        self.error_message: Optional[str] = None
        self.last_validated_value: Any = initial_value # For reverting on error

    def update_value(self, new_value: Any, validator: Callable[[Any], Any]):
        """Updates the value, validates it, and stores error state."""
        try:
            validated_value = validator(new_value)
            # If validation passes, update the value and clear error
            self.value = validated_value
            self.last_validated_value = validated_value # Update snapshot on success
            self.error_message = None
            return True # Indicates value potentially changed and is valid
        except ValidationError as e:
            # If validation fails, keep the old value, store error
            self.error_message = str(e)
            # Do not update self.value, effectively reverting the change attempt
            # self.value = self.last_validated_value # Revert immediately? Or let caller handle?
            return False # Indicates value change was rejected

    def revert_value(self):
        """Reverts the value to the last known valid state."""
        self.value = self.last_validated_value
        self.error_message = None # Clear error on revert


class BaseWidget(abc.ABC):
    """Abstract base class for all input widgets."""
    def __init__(self, label: str, definition: FyInputType, initial_value: Any):
        self.label = label
        self.definition = definition
        self.state = WidgetState(initial_value)
        self._changed_last_frame = False # Internal flag for change detection

    @abc.abstractmethod
    def render(self) -> bool:
        """
        Renders the widget using ImGui.
        Returns True if the value was changed *and validated* successfully in this frame, False otherwise.
        Handles validation internally and updates self.state.
        """
        pass

    def get_value(self) -> Any:
        """
        Returns the current validated value.
        """
        return self.state.value

    def _handle_change(self, changed: bool, current_imgui_value: Any) -> bool:
        """
        Internal helper to manage validation and state update on change.
        """
        value_updated_and_valid = False
        if changed:
            # Attempt to update the state with the new value from ImGui
            is_valid = self.state.update_value(current_imgui_value, self.definition.validate)
            if is_valid:
                value_updated_and_valid = True # Change accepted
            else:
                # Value is invalid, state.value remains unchanged (reverted implicitly)
                # Error message is stored in self.state.error_message
                pass # Keep changed=False as the change was rejected

        # Display error message if any
        if self.state.error_message:
            imgui.same_line()
            imgui.push_style_color(imgui.COLOR_TEXT, 1.0, 0.0, 0.0, 1.0) # Red text
            imgui.text(f"Error: {self.state.error_message}")
            imgui.pop_style_color()
            if imgui.is_item_hovered():
                imgui.set_tooltip(self.state.error_message)

        self._changed_last_frame = value_updated_and_valid
        return value_updated_and_valid


# --- Concrete Widget Implementations ---

class IntWidget(BaseWidget):
    def __init__(self, label: str, definition: FyINT, initial_value: int):
        super().__init__(label, definition, initial_value)
        # Ensure definition is the correct type
        assert isinstance(definition, FyINT)
        self.definition: FyINT = definition # For type hinting

    def render(self) -> bool:
        changed = False
        current_value = int(self.state.value) # ImGui expects native types

        # Use slider if range is defined, otherwise just input box
        if self.definition.min_val is not None and self.definition.max_val is not None:
            # Slider + Input combo
            imgui.push_item_width(imgui.get_content_region_available_width() * 0.6) # Adjust width as needed
            slider_changed, current_value = imgui.slider_int(
                f"##{self.label}_slider", # Hide label for slider part
                current_value,
                self.definition.min_val,
                self.definition.max_val,
                format=f"{self.label}: %d" # Show label here
            )
            imgui.pop_item_width()
            imgui.same_line()
            imgui.push_item_width(imgui.get_content_region_available_width() * 0.3)
            input_changed, current_value = imgui.input_int(f"##{self.label}_input", current_value, step=self.definition.step)
            imgui.pop_item_width()
            changed = slider_changed or input_changed
        else:
            # Just input box
            imgui.push_item_width(-1) # Use full available width
            changed, current_value = imgui.input_int(self.label, current_value, step=self.definition.step)
            imgui.pop_item_width()

        return self._handle_change(changed, current_value)


class FloatWidget(BaseWidget):
    def __init__(self, label: str, definition: FyFLOAT, initial_value: float):
        super().__init__(label, definition, initial_value)
        assert isinstance(definition, FyFLOAT)
        self.definition: FyFLOAT = definition

    def render(self) -> bool:
        changed = False
        current_value = float(self.state.value) # ImGui expects native types
        format_str = "%.3f" # Default format, can be customized

        if self.definition.min_val is not None and self.definition.max_val is not None:
            # Slider + Input combo
            imgui.push_item_width(imgui.get_content_region_available_width() * 0.6)
            slider_changed, current_value = imgui.slider_float(
                f"##{self.label}_slider",
                current_value,
                self.definition.min_val,
                self.definition.max_val,
                format=f"{self.label}: {format_str}" # Show label on slider
            )
            imgui.pop_item_width()
            imgui.same_line()
            imgui.push_item_width(imgui.get_content_region_available_width() * 0.3)
            input_changed, current_value = imgui.input_float(f"##{self.label}_input", current_value, step=self.definition.step, format=format_str)
            imgui.pop_item_width()
            changed = slider_changed or input_changed
        else:
            # Just input box
            imgui.push_item_width(-1)
            changed, current_value = imgui.input_float(self.label, current_value, step=self.definition.step, format=format_str)
            imgui.pop_item_width()

        return self._handle_change(changed, current_value)


class StringWidget(BaseWidget):
    def __init__(self, label: str, definition: FySTR, initial_value: str):
        # Ensure initial_value is a string
        super().__init__(label, definition, str(initial_value))
        assert isinstance(definition, FySTR)
        self.definition: FySTR = definition
        # No longer need self.buffer or self.buffer_size

    def render(self) -> bool:
        # Get the current string value from the state
        current_value_str = str(self.state.value)

        imgui.push_item_width(-1)
        # Pass the string directly to input_text
        # It returns (changed, new_value_str)
        changed, new_value_str = imgui.input_text(
            self.label,
            current_value_str,
            256 # Still need to provide a max buffer size hint for ImGui
        )
        imgui.pop_item_width()

        # No need to decode from buffer anymore
        # current_imgui_value is the new_value_str returned by input_text
        current_imgui_value = new_value_str

        # Handle change needs the potentially updated string
        value_changed_and_valid = self._handle_change(changed, current_imgui_value)

        # No need to update self.buffer anymore
        # self.state.value is updated within _handle_change if validation passes

        return value_changed_and_valid


class BoolWidget(BaseWidget):
    def __init__(self, label: str, definition: FyBOOL, initial_value: bool):
        super().__init__(label, definition, initial_value)
        assert isinstance(definition, FyBOOL)
        self.definition: FyBOOL = definition

    def render(self) -> bool:
        current_value = bool(self.state.value)
        changed, current_value = imgui.checkbox(self.label, current_value)
        return self._handle_change(changed, current_value)


class ChoiceWidget(BaseWidget):
    def __init__(self, label: str, definition: FyCHOICE, initial_value: str):
        super().__init__(label, definition, initial_value)
        assert isinstance(definition, FyCHOICE)
        self.definition: FyCHOICE = definition
        # Find the index of the initial value
        try:
            self.current_index = self.definition.choices.index(initial_value)
        except ValueError:
            print(f"Warning: Initial value '{initial_value}' for ChoiceWidget '{label}' not found in choices. Defaulting to first choice.")
            self.current_index = 0
            # Update state to reflect the actual initial value being used
            self.state.value = self.definition.choices[0]
            self.state.last_validated_value = self.state.value


    def render(self) -> bool:
        # Ensure current_index reflects state.value (e.g., after revert)
        try:
            current_value_str = str(self.state.value)
            if self.definition.choices[self.current_index] != current_value_str:
                 self.current_index = self.definition.choices.index(current_value_str)
        except (ValueError, IndexError):
             # Handle cases where state.value is somehow invalid, reset to default
             print(f"Warning: Invalid state value '{self.state.value}' for ChoiceWidget '{self.label}'. Resetting.")
             self.current_index = self.definition.choices.index(self.definition.default)
             self.state.value = self.definition.choices[self.current_index]
             self.state.last_validated_value = self.state.value


        imgui.push_item_width(-1)
        changed, self.current_index = imgui.combo(
            self.label, self.current_index, self.definition.choices
        )
        imgui.pop_item_width()

        # Get the string value corresponding to the selected index
        current_imgui_value = self.definition.choices[self.current_index]

        # Handle change expects the actual value, not the index
        return self._handle_change(changed, current_imgui_value)


class PathWidget(BaseWidget):
    def __init__(self, label: str, definition: FyPATH, initial_value: str):
        super().__init__(label, definition, initial_value)
        assert isinstance(definition, FyPATH)
        self.definition: FyPATH = definition
        self.display_path_cache = "" # Cache for truncated path

    def _update_display_path(self):
        self.display_path_cache = truncate_path(str(self.state.value), max_len=40) # Adjust max_len

    def render(self) -> bool:
        changed = False
        current_value = str(self.state.value)
        self._update_display_path() # Update truncated path cache

        # Display area for the path
        imgui.text(self.label + ":") # Label on its own line
        imgui.push_item_width(imgui.get_content_region_available_width() * 0.75) # Adjust width
        # Use InputText with read-only flag to allow hover tooltip
        imgui.input_text(f"##{self.label}_display", self.display_path_cache, flags=imgui.INPUT_TEXT_READ_ONLY)
        if imgui.is_item_hovered() and current_value:
            imgui.set_tooltip(current_value)
        imgui.pop_item_width()

        # Select button
        imgui.same_line()
        if imgui.button(f"Select##{self.label}"):
            selected_path = open_path_dialog(
                title=f"Select {self.label}",
                is_dir=self.definition.is_dir
            )
            if selected_path:
                # User selected a path, treat this as a change
                changed = True
                current_value = selected_path # Update value to be validated

        # Handle change if button was clicked and path selected
        value_changed_and_valid = self._handle_change(changed, current_value)

        # If validation failed after selecting a path, the error message will be shown.
        # If validation passed, state.value is updated, and display cache will refresh next frame.

        return value_changed_and_valid


class ImageWidget(PathWidget):
    def __init__(self, label: str, definition: FyIMAGE, initial_value: str):
        super().__init__(label, definition, initial_value)
        assert isinstance(definition, FyIMAGE)
        self.definition: FyIMAGE = definition
        self.texture_id: Optional[int] = None
        self.texture_width: int = 0
        self.texture_height: int = 0
        self.preview_load_error: Optional[str] = None
        self._load_texture_for_preview() # Initial texture load

    def _load_texture_for_preview(self):
        # Release previous texture if any
        if self.texture_id is not None:
            release_texture(texture_id=self.texture_id)
            self.texture_id = None
            self.texture_width = 0
            self.texture_height = 0
            self.preview_load_error = None

        current_path = str(self.state.value)
        if current_path and os.path.exists(current_path):
            try:
                result = load_image_as_texture(current_path)
                if result:
                    self.texture_id, self.texture_width, self.texture_height = result
                else:
                    self.preview_load_error = "Unsupported format or GL unavailable."
            except ImageLoadError as e:
                self.preview_load_error = str(e)
            except Exception as e:
                self.preview_load_error = f"Unexpected error loading preview: {e}"
        # else: path is empty or doesn't exist, no preview

    def render(self) -> bool:
        # Render the path selection part using the parent method
        value_changed_and_valid = super().render()

        # If the path changed and was validated, reload the texture
        if value_changed_and_valid:
            self._load_texture_for_preview()

        # Render the image preview area below the path widget
        imgui.begin_child(f"##{self.label}_preview_area", height=120, border=True) # Adjust height

        if self.texture_id is not None and self.texture_width > 0 and self.texture_height > 0:
            # Calculate preview size, maintaining aspect ratio
            max_preview_height = 100 # Max height inside the child window
            aspect_ratio = self.texture_width / self.texture_height
            preview_height = min(max_preview_height, self.texture_height)
            preview_width = preview_height * aspect_ratio

            # Center the image horizontally (optional)
            cursor_x = (imgui.get_content_region_available_width() - preview_width) / 2
            if cursor_x > 0:
                imgui.set_cursor_pos_x(imgui.get_cursor_pos_x() + cursor_x)

            imgui.image(self.texture_id, preview_width, preview_height)
            if imgui.is_item_hovered():
                 imgui.set_tooltip(f"{os.path.basename(str(self.state.value))}\\n{self.texture_width}x{self.texture_height}")

        elif self.preview_load_error:
            imgui.text_colored(f"Preview Error:", 1.0, 0.5, 0.5, 1.0)
            imgui.text_wrapped(self.preview_load_error)
        elif str(self.state.value):
             imgui.text(f"No preview available.")
             if not os.path.exists(str(self.state.value)):
                 imgui.text_colored("File not found.", 1.0, 0.5, 0.5, 1.0)

        else:
            imgui.text("Select an image file.")

        imgui.end_child()

        # Return the result from the path widget rendering
        return value_changed_and_valid

    def __del__(self):
        # Ensure texture is released when widget is destroyed
        if self.texture_id is not None:
            # This might be called after GL context is gone, wrap in try-except
            try:
                release_texture(texture_id=self.texture_id)
            except Exception as e:
                print(f"Warning: Error releasing texture for {self.label} during deletion: {e}")


# --- Widget Factory ---

def create_widget(label: str, definition: FyInputType, initial_value: Any) -> BaseWidget:
    """
    Factory function to create the appropriate widget based on the definition type.
    """
    if isinstance(definition, FyINT):
        return IntWidget(label, definition, initial_value)
    elif isinstance(definition, FyFLOAT):
        return FloatWidget(label, definition, initial_value)
    elif isinstance(definition, FySTR):
        return StringWidget(label, definition, initial_value)
    elif isinstance(definition, FyBOOL):
        return BoolWidget(label, definition, initial_value)
    elif isinstance(definition, FyCHOICE):
        return ChoiceWidget(label, definition, initial_value)
    elif isinstance(definition, FyIMAGE): # Check FyIMAGE before FyPATH
        return ImageWidget(label, definition, initial_value)
    elif isinstance(definition, FyPATH):
        return PathWidget(label, definition, initial_value)
    else:
        raise TypeError(f"Unsupported FyInputType: {type(definition).__name__}")
