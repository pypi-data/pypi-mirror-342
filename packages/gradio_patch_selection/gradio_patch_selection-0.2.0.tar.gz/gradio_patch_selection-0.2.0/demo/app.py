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
    """Get the selected patch index from annotations"""
    if annotations and annotations.get("patch_index") is not None:
        return f"Selected Patch Index: {annotations['patch_index']}"
    return "No patch selected"


def update_params(img_size, patch_size, current_annotation):
    """Update patch_size and img_size based on user inputs"""
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
