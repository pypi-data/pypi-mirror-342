from gllm_docproc.loader.base_loader import BaseLoader as BaseLoader
from gllm_docproc.loader.loader_utils import create_base_element_metadata as create_base_element_metadata, validate_file_extension as validate_file_extension
from gllm_docproc.model.element import Element as Element, UNCATEGORIZED_TEXT as UNCATEGORIZED_TEXT
from gllm_docproc.model.element_metadata import TXT as TXT
from typing import Any

class TXTLoader(BaseLoader):
    """A class for loading text files (.txt) into a list of elements.

    Methods:
        load: Load a text file into a list of elements.
    """
    def load(self, source: str, loaded_elements: list[dict[str, Any]] | None = None, **kwargs: Any) -> list[dict[str, Any]]:
        """Load a text file into a list of elements.

        Args:
            source (str): The path to the text file.
            loaded_elements (list[dict[str, Any]]): The list of elements that have already been loaded.
            **kwargs: Additional keyword arguments.

        Kwargs:
            original_source (str, optional): The original source of the document.

        Returns:
            list[dict[str, Any]]: A list of elements.
        """
