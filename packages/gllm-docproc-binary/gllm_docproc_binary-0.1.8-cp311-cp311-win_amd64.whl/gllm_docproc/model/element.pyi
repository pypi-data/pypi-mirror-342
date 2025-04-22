from _typeshed import Incomplete
from gllm_docproc.model.element_metadata import ElementMetadata as ElementMetadata
from pydantic import BaseModel
from typing import Any

UNCATEGORIZED_TEXT: str
HEADER: str
TITLE: str
HEADING: Incomplete
PARAGRAPH: str
TABLE: str
AUDIO: str
IMAGE: str
VIDEO: str
FOOTER: str
FOOTNOTE: str
MAX_HEADING_LEVEL: int

class Element(BaseModel):
    """An Element model.

    This class serves as the Element model for storing element text, structure, and metadata.

    Attributes:
        text (str): The element text.
        structure (str): The element structure.
        metadata (dict): The element metadata.
    """
    text: str
    structure: str
    metadata: ElementMetadata
    @staticmethod
    def to_list_dict(elements: list['Element']) -> list[dict[str, Any]]:
        """Convert a list of Element objects to a list of dictionaries."""
    @staticmethod
    def from_list_dict(elements: list[dict[str, Any]]) -> list['Element']:
        """Convert a list of dictionaries to a list of Element objects."""
