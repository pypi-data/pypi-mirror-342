from gllm_docproc.loader.pdf.pdf_loader_utils import bbox_to_coordinates as bbox_to_coordinates
from gllm_docproc.model.element import Element as Element, IMAGE as IMAGE
from gllm_docproc.model.element_metadata import ElementMetadata as ElementMetadata
from typing import Any

def extract_image_element(image_instance: dict[str, Any], page_idx: int, element_metadata: ElementMetadata, page_layout_width: int, page_layout_height: int) -> Element:
    """Extract value (image in base64 format and other metadata) from image element.

    This method defines the process of extracting Image value in base64 format from image element.

    Args:
        image_instance (dict): The image instance.
        page_idx (int): The number of the page index.
        element_metadata (ElementMetadata): The element metadata.
        page_layout_width (int): The width of the page layout.
        page_layout_height (int): The height of the page layout.

    Returns:
        Element: An Element object containing image in base64 format and metadata.
    """
def find_related_link(text_rect: list[float], links: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Find the related link for a text rectangle.

    This method finds the related link for a text rectangle. It will return the link if the text
    rectangle intersects with the link rectangle.

    Args:
        text_rect (list[float]): The text rectangle.
        links (list[dict[str, Any]]): A list of links.

    Returns:
        dict[str, Any] | None: The related link if the text rectangle intersects with the link rectangle
            or None if the text rectangle does not intersect with the link rectangle.
    """
