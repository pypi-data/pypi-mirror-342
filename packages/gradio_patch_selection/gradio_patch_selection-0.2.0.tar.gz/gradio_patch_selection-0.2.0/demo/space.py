
import gradio as gr
from app import demo as app
import os

_docs = {'PatchSelector': {'description': 'Creates a component that allows the user to select a patch from an image. \nThe image is divided into a grid based on the patch_size parameter, and the user can click on a patch to select it.\nThis is useful for visualizing attention maps in Vision Transformer models.', 'members': {'__init__': {'value': {'type': 'dict | None', 'default': 'None', 'description': "A dict or None. The dictionary must contain a key 'image' with either an URL to an image, a numpy image or a PIL image. It may also contain a key 'patchIndex' with the index of the selected patch."}, 'height': {'type': 'int | str | None', 'default': 'None', 'description': 'The height of the displayed image, specified in pixels if a number is passed, or in CSS units if a string is passed.'}, 'width': {'type': 'int | str | None', 'default': 'None', 'description': 'The width of the displayed image, specified in pixels if a number is passed, or in CSS units if a string is passed.'}, 'img_size': {'type': 'int | None', 'default': 'None', 'description': 'If provided, will resize the displayed image to this fixed dimension (img_size × img_size). This takes precedence over height and width parameters. Recommended for ViT models, which typically use square images of fixed dimensions (e.g., 224x224).'}, 'patch_size': {'type': 'int', 'default': '16', 'description': 'The size of each patch in pixels. For a 224x224 image with patch_size=16, there will be a 14x14 grid (196 patches).'}, 'show_grid': {'type': 'bool', 'default': 'True', 'description': 'If True, will display the grid overlay on the image.'}, 'grid_color': {'type': 'str', 'default': '"rgba(200, 200, 200, 0.5)"', 'description': 'The color of the grid overlay lines, specified as a CSS color string.'}, 'image_mode': {'type': '"1"\n    | "L"\n    | "P"\n    | "RGB"\n    | "RGBA"\n    | "CMYK"\n    | "YCbCr"\n    | "LAB"\n    | "HSV"\n    | "I"\n    | "F"', 'default': '"RGB"', 'description': '"RGB" if color, or "L" if black and white. See https://pillow.readthedocs.io/en/stable/handbook/concepts.html for other supported image modes and their meaning.'}, 'sources': {'type': 'list["upload" | "webcam" | "clipboard"] | None', 'default': '["upload", "webcam", "clipboard"]', 'description': 'List of sources for the image. "upload" creates a box where user can drop an image file, "webcam" allows user to take snapshot from their webcam, "clipboard" allows users to paste an image from the clipboard. If None, defaults to ["upload", "webcam", "clipboard"].'}, 'image_type': {'type': '"numpy" | "pil" | "filepath"', 'default': '"numpy"', 'description': 'The format the image is converted before being passed into the prediction function. "numpy" converts the image to a numpy array with shape (height, width, 3) and values from 0 to 255, "pil" converts the image to a PIL image object, "filepath" passes a str path to a temporary file containing the image. If the image is SVG, the `type` is ignored and the filepath of the SVG is returned.'}, 'label': {'type': 'str | None', 'default': 'None', 'description': 'The label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.'}, 'container': {'type': 'bool', 'default': 'True', 'description': 'If True, will place the component in a container - providing some extra padding around the border.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.'}, 'interactive': {'type': 'bool | None', 'default': 'True', 'description': 'if True, will allow users to upload and annotate an image; if False, can only be used to display annotated images.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.'}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will display label.'}, 'show_download_button': {'type': 'bool', 'default': 'True', 'description': 'If True, will show a button to download the image.'}, 'show_share_button': {'type': 'bool | None', 'default': 'None', 'description': 'If True, will show a share icon in the corner of the component that allows user to share outputs to Hugging Face Spaces Discussions. If False, icon does not appear. If set to None (default behavior), then the icon appears if this Gradio app is launched on Spaces, but not otherwise.'}, 'show_clear_button': {'type': 'bool | None', 'default': 'True', 'description': 'If True, will show a button to clear the current image.'}, 'show_remove_button': {'type': 'bool | None', 'default': 'None', 'description': 'If True, will show a button to remove the selected bounding box.'}, 'handles_cursor': {'type': 'bool | None', 'default': 'True', 'description': 'If True, the cursor will change when hovering over box handles in drag mode. Can be CPU-intensive.'}}, 'postprocess': {'value': {'type': 'dict | None', 'description': 'A dict with an image and an optional patchIndex or None.'}}, 'preprocess': {'return': {'type': 'dict | None', 'description': 'A dict with the image, patchIndex, imgSize, and patchSize or None.'}, 'value': None}}, 'events': {'clear': {'type': None, 'default': None, 'description': 'This listener is triggered when the user clears the PatchSelector using the clear button for the component.'}, 'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the PatchSelector changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'upload': {'type': None, 'default': None, 'description': 'This listener is triggered when the user uploads a file into the PatchSelector.'}, 'patch_select': {'type': None, 'default': None, 'description': 'Triggered when a patch is selected by the user. Returns the patch index.'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'PatchSelector': []}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_patch_selection`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.2.0%20-%20orange">  
</div>

A Gradio component that allows users to select patches from images by overlaying a customizable grid.
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_patch_selection
```

## Usage

```python
# filepath: /Users/dgcnz/development/playground/gradio_image_annotator/demo/app_dynamic_inputs.py
import gradio as gr
from gradio_patch_selection import PatchSelector


# Default values for image size and patch size
DEFAULT_IMG_SIZE = 224
DEFAULT_PATCH_SIZE = 16

example_annotation = {
    "image": "https://gradio-builds.s3.amazonaws.com/demo-files/base.png",
    "patch_index": 42,  # Example patch index
    "img_size": DEFAULT_IMG_SIZE,
    "patch_size": DEFAULT_PATCH_SIZE
}

examples = [
    {
        "image": "https://raw.githubusercontent.com/gradio-app/gradio/main/guides/assets/logo.png",
        "patch_index": 10,  # Example patch index
        "img_size": DEFAULT_IMG_SIZE,
        "patch_size": DEFAULT_PATCH_SIZE
    },
    {
        "image": "https://gradio-builds.s3.amazonaws.com/demo-files/base.png",
        "patch_index": 42,  # Example patch index
        "img_size": DEFAULT_IMG_SIZE,
        "patch_size": DEFAULT_PATCH_SIZE
    },
]


def get_patch_index(annotations):
    \"\"\"Get the selected patch index from annotations\"\"\"
    if annotations and annotations.get("patch_index") is not None:
        return f"Selected Patch Index: {annotations['patch_index']}"
    return "No patch selected"


def update_params(img_size, patch_size, current_annotation):
    \"\"\"Update patch_size and img_size based on user inputs\"\"\"
    if not current_annotation:
        current_annotation = {"image": None, "patch_index": None}
    
    # Ensure values are integers and within reasonable bounds
    img_size = max(32, min(1024, int(img_size)))
    patch_size = max(1, min(128, int(patch_size)))
    
    # Preserve the existing image and patch_index if they exist
    current_annotation["img_size"] = img_size
    current_annotation["patch_size"] = patch_size
    
    # Return updated annotation and parameter info string
    param_info = f"Image Size: {img_size}x{img_size}\nPatch Size: {patch_size}x{patch_size}"
    
    # Calculate grid dimensions
    grid_width = img_size // patch_size
    grid_height = img_size // patch_size 
    grid_info = f"Grid Dimensions: {grid_width}x{grid_height} ({grid_width * grid_height} patches)"
    
    return current_annotation, param_info, grid_info


with gr.Blocks() as demo:
    with gr.Tab("Dynamic Patch Selector", id="tab_dynamic_patch_selector"):
        gr.Markdown("# Dynamic Patch Selector Demo")
        gr.Markdown("This demo shows how to dynamically update the patch size and image size using number inputs.")
        
        with gr.Row():
            with gr.Column(scale=1):
                img_size_input = gr.Number(
                    value=DEFAULT_IMG_SIZE,
                    label="Image Size",
                    minimum=32,
                    maximum=1024,
                    step=16,
                    precision=0
                )
                patch_size_input = gr.Number(
                    value=DEFAULT_PATCH_SIZE,
                    label="Patch Size",
                    minimum=1,
                    maximum=128,
                    step=1,
                    precision=0
                )
                param_info = gr.Textbox(
                    value=f"Image Size: {DEFAULT_IMG_SIZE}x{DEFAULT_IMG_SIZE}\nPatch Size: {DEFAULT_PATCH_SIZE}x{DEFAULT_PATCH_SIZE}",
                    label="Parameters",
                    interactive=False
                )
                grid_info = gr.Textbox(
                    value=f"Grid Dimensions: {DEFAULT_IMG_SIZE//DEFAULT_PATCH_SIZE}x{DEFAULT_IMG_SIZE//DEFAULT_PATCH_SIZE} ({(DEFAULT_IMG_SIZE//DEFAULT_PATCH_SIZE)**2} patches)",
                    label="Grid Information",
                    interactive=False
                )
        
        with gr.Row():
            with gr.Column(scale=2):
                annotator = PatchSelector(
                    example_annotation,
                    img_size=DEFAULT_IMG_SIZE,  # Default image size
                    patch_size=DEFAULT_PATCH_SIZE,  # Default patch size
                    show_grid=True,
                    grid_color="rgba(200, 200, 200, 0.5)"
                )
            
            with gr.Column(scale=1):
                output = gr.Textbox(label="Selected Patch", value="No patch selected")
                gr.Markdown("### How it works")
                gr.Markdown("1. Adjust the image size and patch size using the number inputs")
                gr.Markdown("2. The grid will update automatically based on your inputs")
                gr.Markdown("3. Click on any patch to select it and get its index")
        
        # Handle the parameter change events
        img_size_input.change(
            update_params,
            inputs=[img_size_input, patch_size_input, annotator],
            outputs=[annotator, param_info, grid_info]
        )
        
        patch_size_input.change(
            update_params,
            inputs=[img_size_input, patch_size_input, annotator],
            outputs=[annotator, param_info, grid_info]
        )
        
        # Handle the patch selection event
        annotator.patch_select(get_patch_index, annotator, output)
        
        gr.Examples(examples, annotator)

if __name__ == "__main__":
    demo.launch()

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `PatchSelector`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["PatchSelector"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["PatchSelector"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, a dict with the image, patchIndex, imgSize, and patchSize or None.
- **As output:** Should return, a dict with an image and an optional patchIndex or None.

 ```python
def predict(
    value: dict | None
) -> dict | None:
    return value
```
""", elem_classes=["md-custom", "PatchSelector-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          PatchSelector: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
