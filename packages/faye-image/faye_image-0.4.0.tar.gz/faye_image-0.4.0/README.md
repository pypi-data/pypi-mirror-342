# FaYE-image
A image toolkit designed to convert the image file from `any supported type` to `another one` with **only one line code**.

current supported file types:
- .png
- .jpg / .jpeg
- .exr
- .gif
- .npy

current supported runtime data types:
- numpy.ndarray
- torch.Tensor
- cv2.Mat
- PIL.Image.Image
- matplotlib.pyplot.Figure

## News
- **2024.10.12**: [FaYE 0.2.0](update_record/v0.2.0.md) is released, bringing a totally new version of FaYE-image, with more operations and easier interfaces.
- **2024.10.14**: [FaYE 0.2.1](update_record/v0.2.1.md) is released, fixing the bug of unexpected image data shape management.
- **2024.10.20**: [FaYE 0.2.2](update_record/v0.2.2.md) is released, fixing the bug of potential data type incompatibility during image resizing.
- **2024.11.07**: [FaYE 0.3.0](update_record/v0.3.0.md) is released, introducing FaYE Visualizer, an interactive visualizer for any image formation algorithm.
- **2024.04.19**: [FaYE 0.4.0](update_record/v0.4.0.md) is released, FaYE Visualizer is deprecated, and introducing the novel FyGUI.

## Requirement
### Necessary packages
- numpy
- imgui[glfw]
- PyOpenGL
### Optional packages
- matplotlib
- PIL
- opencv-python
- torch
- OpenEXR

## Usage
**Installation**:
```bash
pip install faye-image
```

To achieve this easy and uniform image data IO operations, you only need to add:
```python
from faye_image import *
```
at the beginning of your code.

If you want to load a PNG image file into a torch tensor, you can simply call:
```python
tensor = Convert('path/to/image.png', from_type=PNG_FILE, to_type=TORCH)
```
Or precisely version:
```python
intermediate = From('path/to/image.png', data_type=PNG_FILE)
tensor = To(intermediate, data_type=TORCH)
```

If you want to save a torch tensor to a PNG image file, you can simply call:
```python
Convert(tensor, from_type=TORCH, to_type=PNG_FILE, save_path='path/to/image.png', save_mode='RGB')
```
Or precisely version:
```python
intermediate = From(tensor, data_type=TORCH)
To(intermediate, data_type=PNG_FILE, save_path='path/to/image.png', save_mode='RGB')
```

If you want to convert a numpy image data to a cv::Mat, you can simply call:
```python
mat = Convert(numpy_image, from_type=NUMPY, to_type=CV_MAT)
```
Or precisely version:
```python
intermediate = From(numpy_image, data_type=NUMPY)
mat = To(intermediate, data_type=CV_MAT)
```

## Extension
If you want to make this module compatible with more image data types of your interest,
     you just need to implement a corresponding builder class inherited from the `ImageDataBuilder` class.

Then, call the `RegisterBuilders(builder1, builder2, ...)` at the end of your .py file to add the builder to the image factory.


The builder class should implement the following methods:
- `CanBuild(data) -> bool`: Check if the builder can build the data.
- `GetTag() -> str`: Get the tag of the builder.
- `BuildIntermediate(data) -> ImageIntermediate`: Build the image intermediate from the data.
    For current version, the image intermediate is a numpy array in `[BxCxHxW]` in `float32`.
- `BuildData(intermediate: ImageIntermediate, **kwargs)`: Build the data from the image intermediate.
    Since the `B` maybe not 1, the batch dimension should be considered in the implementation.
    Returning a list of data is also supported.

## Usage Example of FyGUI:

1.  **Define Input Parameters:**
    Use the `@FyINPUT` decorator on a class and define attributes using `Fy` input types.

    ```python
    from faye_image.GUI import FyINPUT, FyINT, FySTR, FyBOOL, FyCHOICE, FyContext

    @FyINPUT
    class MyInputs:
        seed = FyINT(0, 10000, default=42)
        width = FyINT(min_val=50, max_val=500, default=200)
        height = FyINT(min_val=50, max_val=500, default=150)
        message = FySTR(default="Hello FyGUI!")
        color = FyCHOICE(['Red', 'Green', 'Blue', 'Yellow'], default='Blue')
        use_border = FyBOOL(default=True)
    ```

2.  **Define Callback Function:**
    Create a function that takes the parameter object (an instance reflecting `MyInputs`) and a `FyContext` object. It should return the result to visualize (e.g., a PIL Image).

    ```python
    from PIL import Image, ImageDraw, ImageFont
    import time

    def generate_image(params: MyInputs, context: FyContext) -> Image.Image:
        """Callback that generates a simple image based on inputs."""
        print(f"Generating image with seed={params.seed}, size=({params.width}x{params.height})")
        frame = context.get('frame_count', 0)
        context['last_seed'] = params.seed

        img = Image.new('RGB', (params.width, params.height), color='white')
        draw = ImageDraw.Draw(img)
        text = f"{params.message}\nSeed: {params.seed}\nFrame: {frame}"
        text_color = params.color.lower()

        try:
            font = ImageFont.load_default()
            draw.text((10, 10), text, fill=text_color, font=font)
        except ImportError:
            draw.text((10, 10), text, fill=text_color)

        if params.use_border:
            draw.rectangle([(0, 0), (params.width - 1, params.height - 1)], outline=(0,0,0), width=2)

        time.sleep(0.1) # Simulate work
        context['frame_count'] = frame + 1
        return img
    ```

3.  **Initialize and Run FyGUI:**
    Instantiate `FyGUI` with your input class and run it with your callback function.

    ```python
    from faye_image.GUI import FyGUI

    # Initialize FyGUI, optionally passing initial context
    gui = FyGUI(MyInputs, window_title="Simple Image Generator", frame_count=0)
    # Run the GUI, providing the callback function
    gui.run(generate_image)
    ```

This will launch an interactive window where you can modify the parameters defined in `MyInputs` and see the generated image update in real-time.