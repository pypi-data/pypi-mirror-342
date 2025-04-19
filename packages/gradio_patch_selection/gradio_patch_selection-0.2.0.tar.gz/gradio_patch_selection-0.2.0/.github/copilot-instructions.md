# Project

## Description

PatchSelector is an input gradio component that allows the user to select a patch from an image. It takes an image, a patch size and an image size as input and overlays a grid based on those parameters for the user to click on.

For example, if the image size is 224x224 and the patch size is 16, a grid of 14x14 will be overlayed on the image. The user can then select a patch by clicking on it, and the component will return the patch index.

This is meant to be used as an input gradio component for visualization of attention maps in ViT models. The component will return the patch index, which can then be used to visualize the attention map for that patch.


## Project Structure

- frontend: Svelte frontend components, uses TypeScript.
- backend: contains the backend logic for the component. It uses Gradio to create the input component and handle the image processing.
- demo: `demo/app.py` contains the Gradio demo for the component. 
- Generated code (don't edit these files)
    - `backend/{package}/templates/**`
    - `dist/**`

The full stack for this project is:
- Svelte/TypeScript/JavaScript: for frontend development
- Python: for backend development
- uv: for python package management
    - To run python commands in the environment you can do `uv run {cmd}`. For example, `uv run gradio cc build` will build the gradio component.

## Coding Instructions

- If you want to debug the backend or frontend, just insert print statements wherever you want and ask me to run the code. Tell me if you want the browser console or the python console or both. I'll copy its outputs to you.
- Don't add comments on the svelte files, they mess up the compilation.