from __future__ import annotations

import re
import warnings
from pathlib import Path
from typing import Any, List, Literal, cast

import numpy as np
import PIL.Image
from PIL import ImageOps

from gradio import image_utils, utils
from gradio.components.base import Component
from gradio.data_classes import FileData, GradioModel
from gradio.events import Events, EventListener

PIL.Image.init()  # fixes https://github.com/gradio-app/gradio/issues/2843


class AnnotatedImageData(GradioModel):
    image: FileData
    patchIndex: int | None = None
    imgSize: int | None = None
    patchSize: int | None = None




class PatchSelector(Component):
    """
    Creates a component that allows the user to select a patch from an image. 
    The image is divided into a grid based on the patch_size parameter, and the user can click on a patch to select it.
    This is useful for visualizing attention maps in Vision Transformer models.
    """

    EVENTS = [
        Events.clear,
        Events.change,
        Events.upload,
        EventListener(
            "patch_select",
            doc="Triggered when a patch is selected by the user. Returns the patch index.",
        )
    ]

    data_model = AnnotatedImageData

    def __init__(
        self,
        value: dict | None = None,
        *,
        height: int | str | None = None,
        width: int | str | None = None,
        img_size: int | None = None,
        patch_size: int = 16,
        show_grid: bool = True,
        grid_color: str = "rgba(200, 200, 200, 0.5)",
        image_mode: Literal[
            "1", "L", "P", "RGB", "RGBA", "CMYK", "YCbCr", "LAB", "HSV", "I", "F"
        ] = "RGB",
        sources: list[Literal["upload", "webcam", "clipboard"]] | None = [
            "upload",
            "webcam",
            "clipboard",
        ],
        image_type: Literal["numpy", "pil", "filepath"] = "numpy",
        label: str | None = None,
        container: bool = True,
        scale: int | None = None,
        min_width: int = 160,
        interactive: bool | None = True,
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        show_label: bool | None = None,
        show_download_button: bool = True,
        show_share_button: bool | None = None,
        show_clear_button: bool | None = True,
        show_remove_button: bool | None = None,
        handles_cursor: bool | None = True,
    ):
        """
        Parameters:
            value: A dict or None. The dictionary must contain a key 'image' with either an URL to an image, a numpy image or a PIL image. It may also contain a key 'patchIndex' with the index of the selected patch.
            patch_size: The size of each patch in pixels. For a 224x224 image with patch_size=16, there will be a 14x14 grid (196 patches).
            show_grid: If True, will display the grid overlay on the image.
            grid_color: The color of the grid overlay lines, specified as a CSS color string.
            height: The height of the displayed image, specified in pixels if a number is passed, or in CSS units if a string is passed.
            width: The width of the displayed image, specified in pixels if a number is passed, or in CSS units if a string is passed.
            img_size: If provided, will resize the displayed image to this fixed dimension (img_size × img_size). This takes precedence over height and width parameters. Recommended for ViT models, which typically use square images of fixed dimensions (e.g., 224x224).
            patch_size: The size of each patch in pixels. For a 224x224 image with patch_size=16, there will be a 14x14 grid (196 patches).
            show_grid: If True, will display the grid overlay on the image.
            grid_color: The color of the grid overlay lines, specified as a CSS color string (e.g., 'rgba(200, 200, 200, 0.5)').
            image_mode: "RGB" if color, or "L" if black and white. See https://pillow.readthedocs.io/en/stable/handbook/concepts.html for other supported image modes and their meaning.
            sources: List of sources for the image. "upload" creates a box where user can drop an image file, "webcam" allows user to take snapshot from their webcam, "clipboard" allows users to paste an image from the clipboard. If None, defaults to ["upload", "webcam", "clipboard"].
            image_type: The format the image is converted before being passed into the prediction function. "numpy" converts the image to a numpy array with shape (height, width, 3) and values from 0 to 255, "pil" converts the image to a PIL image object, "filepath" passes a str path to a temporary file containing the image. If the image is SVG, the `type` is ignored and the filepath of the SVG is returned.
            label: The label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.
            container: If True, will place the component in a container - providing some extra padding around the border.
            scale: relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.
            min_width: minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.
            interactive: if True, will allow users to upload and annotate an image; if False, can only be used to display annotated images.
            visible: If False, component will be hidden.
            elem_id: An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.
            elem_classes: An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.
            render: If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.
            show_label: if True, will display label.
            show_download_button: If True, will show a button to download the image.
            show_share_button: If True, will show a share icon in the corner of the component that allows user to share outputs to Hugging Face Spaces Discussions. If False, icon does not appear. If set to None (default behavior), then the icon appears if this Gradio app is launched on Spaces, but not otherwise.
            show_clear_button: If True, will show a button to clear the current image.
            show_remove_button: If True, will show a button to remove the selected bounding box.
            handles_cursor: If True, the cursor will change when hovering over box handles in drag mode. Can be CPU-intensive.
        """

        valid_types = ["numpy", "pil", "filepath"]
        if image_type not in valid_types:
            raise ValueError(
                f"Invalid value for parameter `type`: {type}. Please choose from one of: {valid_types}"
            )
        self.image_type = image_type
        self.height = height
        self.width = width
        self.image_mode = image_mode
        
        self.sources = sources
        valid_sources = ["upload", "clipboard", "webcam", None]
        if isinstance(sources, str):
            self.sources = [sources]
        if self.sources is None:
            self.sources = []
        if self.sources is not None:
            for source in self.sources:
                if source not in valid_sources:
                    raise ValueError(
                        f"`sources` must a list consisting of elements in {valid_sources}"
                    )
        
        self.show_download_button = show_download_button
        self.show_share_button = (
            (utils.get_space() is not None)
            if show_share_button is None
            else show_share_button
        )
        self.show_clear_button = show_clear_button
        self.show_remove_button = show_remove_button
        self.handles_cursor = handles_cursor

        self.img_size = img_size
        self.patch_size = patch_size
        self.show_grid = show_grid
        self.grid_color = grid_color
        
        super().__init__(
            label=label,
            every=None,
            show_label=show_label,
            container=container,
            scale=scale,
            min_width=min_width,
            interactive=interactive,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
            value=value,
        )

    def preprocess_image(self, image: FileData | None) -> str | None:
        if image is None:
            return None
        file_path = Path(image.path)
        if image.orig_name:
            p = Path(image.orig_name)
            name = p.stem
            suffix = p.suffix.replace(".", "")
            if suffix in ["jpg", "jpeg"]:
                suffix = "jpeg"
        else:
            name = "image"
            suffix = "png"

        if suffix.lower() == "svg":
            return str(file_path)
        
        im = PIL.Image.open(file_path)
        exif = im.getexif()
        # 274 is the code for image rotation and 1 means "correct orientation"
        if exif.get(274, 1) != 1 and hasattr(ImageOps, "exif_transpose"):
            try:
                im = ImageOps.exif_transpose(im)
            except Exception:
                warnings.warn(
                    f"Failed to transpose image {file_path} based on EXIF data."
                )
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            im = im.convert(self.image_mode)
        return image_utils.format_image(
            im,
            cast(Literal["numpy", "pil", "filepath"], self.image_type),
            self.GRADIO_CACHE,
            name=name,
            format=suffix,
        )


    def preprocess(self, payload: AnnotatedImageData | None) -> dict | None:
        """
        Parameters:
            payload: an AnnotatedImageData object.
        Returns:
            A dict with the image, patchIndex, imgSize, and patchSize or None.
        """
        if payload is None:
            return None
        
        print("payload", payload)
        
        ret_value = {
            "image": self.preprocess_image(payload.image),
            "patch_index": payload.patchIndex,
            "img_size": payload.imgSize,
            "patch_size": payload.patchSize
        }
        return ret_value

    def postprocess(self, value: dict | None) -> AnnotatedImageData | None:
        """
        Parameters:
            value: A dict with an image and an optional patchIndex or None.
        Returns:
            Returns an AnnotatedImageData object.
        """
        # Check value
        if value is None:
            return None
        print("postprocess value", value)
        if not isinstance(value, dict):
            raise ValueError(f"``value`` must be a dict. Got {type(value)}")
    
        # Check and parse image
        image = value.setdefault("image", None)
        if image is not None:
            if isinstance(image, str) and image.lower().endswith(".svg"):
                image = FileData(path=image, orig_name=Path(image).name)
            else:
                saved = image_utils.save_image(image, self.GRADIO_CACHE)
                orig_name = Path(saved).name if Path(saved).exists() else None
                image = FileData(path=saved, orig_name=orig_name)
        else:
            raise ValueError(f"An image must be provided. Got {value}")
        
        return AnnotatedImageData(
            image=image, 
            patchIndex=value.get("patch_index", None),
            imgSize=value.get("img_size", self.img_size),
            patchSize=value.get("patch_size", self.patch_size)
        )

    def process_example(self, value: dict | None) -> FileData | None:
        if value is None:
            return None
        if not isinstance(value, dict):
            raise ValueError(f"``value`` must be a dict. Got {type(value)}")

        image = value.setdefault("image", None)
        if image is not None:
            if isinstance(image, str) and image.lower().endswith(".svg"):
                image = FileData(path=image, orig_name=Path(image).name)
            else:
                saved = image_utils.save_image(image, self.GRADIO_CACHE)
                orig_name = Path(saved).name if Path(saved).exists() else None
                image = FileData(path=saved, orig_name=orig_name)
        else:
            raise ValueError(f"An image must be provided. Got {value}")

        return image

    def example_inputs(self) -> Any:
        return {
            "image": "https://raw.githubusercontent.com/gradio-app/gradio/main/guides/assets/logo.png",
            "patch_index": 42  # Example patch index
        }
