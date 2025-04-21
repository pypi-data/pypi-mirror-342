# Define utility functions

import tkinter as tk
from tkinter import filedialog
import os
from typing import Optional, Tuple, Dict

# --- File Dialog ---

def open_file_dialog(title: str = "Select File", filetypes: Optional[list[Tuple[str, str]]] = None) -> Optional[str]:
    """Opens a native file selection dialog. Returns the selected path or None."""
    root = tk.Tk()
    root.withdraw() # Hide the main tkinter window
    root.attributes('-topmost', True) # Bring the dialog to the front

    path = filedialog.askopenfilename(
        title=title,
        filetypes=filetypes or [("All Files", "*.*")]
    )
    root.destroy()
    return path if path else None

def open_directory_dialog(title: str = "Select Directory") -> Optional[str]:
    """Opens a native directory selection dialog. Returns the selected path or None."""
    root = tk.Tk()
    root.withdraw() # Hide the main tkinter window
    root.attributes('-topmost', True) # Bring the dialog to the front

    path = filedialog.askdirectory(
        title=title,
        mustexist=True # Usually, we want an existing directory
    )
    root.destroy()
    return path if path else None

def open_path_dialog(title: str = "Select Path", is_dir: Optional[bool] = None) -> Optional[str]:
    """Opens a file or directory dialog based on is_dir flag."""
    if is_dir is True:
        return open_directory_dialog(title)
    elif is_dir is False:
        return open_file_dialog(title)
    else:
        # Ask the user? Or provide a generic "select path" - difficult with standard dialogs.
        # Defaulting to file selection might be safer.
        # Or, we could try opening a file dialog first, and if cancelled, maybe offer dir? Complex.
        # Let's default to file dialog for now if type is unspecified.
        print("Warning: Path type (file/directory) not specified for dialog. Defaulting to file selection.")
        return open_file_dialog(title)


# --- Path Utils ---

def truncate_path(path: str, max_len: int = 50) -> str:
    """
    Truncates a path string, replacing the middle with ellipsis if too long.
    """
    if len(path) <= max_len:
        return path

    # Find the separator positions
    parts = path.split(os.sep)
    if len(parts) <= 2: # Not much to truncate if only root/filename or similar
        return path[:max_len-3] + "..."

    # Calculate how much to keep from start and end
    # Keep the first part (drive/root) and the last part (filename) fully
    start_part = parts[0]
    end_part = parts[-1]
    # Reserve space for separators and ellipsis
    reserved_len = len(start_part) + len(os.sep) + len(end_part) + len(os.sep) + 3 # ".../"

    if reserved_len >= max_len:
        # Even root and filename are too long, just truncate the end
        return path[:max_len-3] + "..."

    remaining_len = max_len - reserved_len

    # Try to fit middle parts
    middle_parts = parts[1:-1]
    truncated_middle = ""
    current_len = 0

    # Add parts from the beginning of the middle section
    for i, part in enumerate(middle_parts):
        part_len = len(part) + len(os.sep)
        if current_len + part_len <= remaining_len:
            truncated_middle += part + os.sep
            current_len += part_len
        else:
            # Cannot fit more full parts
            break

    return f"{start_part}{os.sep}{truncated_middle}...{os.sep}{end_part}"


# --- Image Loading & Texture Handling (Requires Pillow, OpenGL) ---
# These will be more complex and depend on the specific ImGui backend and OpenGL setup

try:
    from PIL import Image
except ImportError:
    print("Warning: Pillow library not found. Image loading features will be unavailable.")
    print("Install it using: pip install Pillow")
    Image = None

try:
    import OpenGL.GL as gl
except ImportError:
    print("Warning: PyOpenGL not found. OpenGL features (texture loading) will be unavailable.")
    print("Install it using: pip install PyOpenGL")
    gl = None

from .exceptions import ImageLoadError

_texture_cache: Dict[str, int] = {} # Cache loaded textures by path

def load_image_as_texture(image_path: str) -> Optional[Tuple[int, int, int]]:
    """
    Loads an image file and converts it into an OpenGL texture.

    Returns:
        A tuple (texture_id, width, height) or None if loading fails or dependencies are missing.
    """
    if not Image or not gl:
        return None
    if not os.path.exists(image_path) or not os.path.isfile(image_path):
        return None # Don't try to load non-existent files

    # Use cache if available
    if image_path in _texture_cache:
        # We need width/height too, maybe cache that as well?
        # For now, re-opening to get dimensions is simpler than managing complex cache
        try:
            with Image.open(image_path) as img:
                 width, height = img.size
            return _texture_cache[image_path], width, height
        except Exception:
             # If reading dimensions fails, remove from cache and reload
             if image_path in _texture_cache:
                 gl.glDeleteTextures(1, [_texture_cache[image_path]])
                 del _texture_cache[image_path]
             # Proceed to load normally


    try:
        with Image.open(image_path) as img:
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
                # Attempt conversion to RGBA as a fallback
                print(f"Warning: Image format {img_format} not directly supported, converting to RGBA.")
                img = img.convert('RGBA')
                gl_format = gl.GL_RGBA
                internal_format = gl.GL_RGBA
                pixel_type = gl.GL_UNSIGNED_BYTE
                img_data = img.tobytes("raw", "RGBA", 0, -1)
                width, height = img.size # Update size after conversion

            # Create OpenGL texture
            texture_id = gl.glGenTextures(1)
            gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id)

            # Set texture parameters (important for ImGui)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)

            # Upload texture data
            # Ensure correct pixel alignment (Pillow default is usually fine)
            gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
            gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, internal_format, width, height, 0,
                              gl_format, pixel_type, img_data)

            gl.glBindTexture(gl.GL_TEXTURE_2D, 0) # Unbind texture

            # Add to cache
            _texture_cache[image_path] = texture_id

            return texture_id, width, height

    except FileNotFoundError:
        # This shouldn't happen due to the check above, but handle defensively
        print(f"Error: File not found during image load: {image_path}")
        return None
    except Exception as e:
        # Catch potential Pillow errors (corrupt file, unsupported format)
        raise ImageLoadError(f"Failed to load or process image '{image_path}': {e}") from e


def release_texture(image_path: Optional[str] = None, texture_id: Optional[int] = None):
    """
    Releases an OpenGL texture from the cache and GPU memory.
    """
    if not gl: return

    tex_id_to_delete = None
    path_to_remove = None

    if texture_id is not None:
        tex_id_to_delete = texture_id
        # Find the corresponding path in the cache to remove it
        for path, tid in _texture_cache.items():
            if tid == texture_id:
                path_to_remove = path
                break
    elif image_path is not None and image_path in _texture_cache:
        tex_id_to_delete = _texture_cache[image_path]
        path_to_remove = image_path

    if tex_id_to_delete is not None:
        try:
            gl.glDeleteTextures(1, [tex_id_to_delete])
            # print(f"Released texture ID: {tex_id_to_delete}")
        except Exception as e:
            # Can happen if OpenGL context is already destroyed
            print(f"Warning: Could not delete texture ID {tex_id_to_delete}: {e}")

        if path_to_remove and path_to_remove in _texture_cache:
            del _texture_cache[path_to_remove]

def release_all_textures():
    """
    Releases all cached OpenGL textures.
    """
    if not gl: return
    if not _texture_cache: return

    texture_ids = list(_texture_cache.values())
    if texture_ids:
        try:
            gl.glDeleteTextures(len(texture_ids), texture_ids)
            # print(f"Released {len(texture_ids)} cached textures.")
        except Exception as e:
            # Can happen if OpenGL context is already destroyed
            print(f"Warning: Could not delete all textures: {e}")
    _texture_cache.clear()


# Example Usage
if __name__ == '__main__':
    # Test path truncation
    long_path_unix = "/Users/username/Documents/Projects/VeryLongProjectName/src/core/utils/helpers/misc.py"
    long_path_win = "C:\\Users\\username\\Documents\\Projects\\VeryLongProjectName\\src\\core\\utils\\helpers\\misc.py"
    short_path = "/etc/hosts"

    print(f"Original: {long_path_unix}")
    print(f"Truncated (50): {truncate_path(long_path_unix, 50)}")
    print(f"Truncated (30): {truncate_path(long_path_unix, 30)}")

    print(f"Original: {long_path_win}")
    print(f"Truncated (60): {truncate_path(long_path_win, 60)}")

    print(f"Original: {short_path}")
    print(f"Truncated (50): {truncate_path(short_path, 50)}")


    # Test file dialog (will pop up windows)
    # print("Opening file dialog...")
    # selected_file = open_file_dialog()
    # print(f"Selected file: {selected_file}")

    # print("Opening directory dialog...")
    # selected_dir = open_directory_dialog()
    # print(f"Selected directory: {selected_dir}")

    # Image loading requires an OpenGL context, cannot be tested standalone easily.
    print("\nImage loading utilities defined (requires OpenGL context for testing).")
