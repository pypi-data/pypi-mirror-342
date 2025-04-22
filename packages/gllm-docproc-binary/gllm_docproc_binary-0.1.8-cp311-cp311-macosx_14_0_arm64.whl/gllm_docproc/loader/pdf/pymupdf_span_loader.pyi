from gllm_docproc.loader.base_loader import BaseLoader as BaseLoader
from gllm_docproc.loader.loader_utils import create_base_element_metadata as create_base_element_metadata, validate_file_extension as validate_file_extension
from gllm_docproc.loader.pdf.pymupdf_utils import bbox_to_coordinates as bbox_to_coordinates, extract_image_element as extract_image_element, find_related_link as find_related_link
from gllm_docproc.model.element import Element as Element, UNCATEGORIZED_TEXT as UNCATEGORIZED_TEXT
from gllm_docproc.model.element_metadata import ElementMetadata as ElementMetadata, PDF as PDF
from typing import Any

class PyMuPDFSpanLoader(BaseLoader):
    """PyMuPDFSpanLoader class to extract text per span from a PDF file using PyMuPDF.

    This class defines the structure for extracting text per span from a PDF file using PyMuPDF.
    It implements the load method to extract information from a PDF file from a given source.

    PyMuPDFLoader is used to extract the TEXT, HYPERLINK, and IMAGE in base64 format from the PDF document.
    Text loader have to be the first loader in the pipeline. This prioritization is because subsequent
    loaders like the Table Loader may contain overlapping information with the Text Loader.
    Therefore, these subsequent loaders rely on the output from the Text Loader. They merge the
    loaded elements and filter out any duplicates by using the information provided by the Text Loader.

    Methods:
        load(source, loaded_elements, **kwargs): Load a PDF document.
    """
    def load(self, source: str, loaded_elements: list[dict[str, Any]] | None = None, **kwargs: Any) -> list[dict[str, Any]]:
        """Load a PDF file using PyMuPDF and extract text span.

        This method loads a PDF file using PyMuPDF and extracts text per span. It will return
        a list of loaded elements. Span is a segment of text within a document, representing a
        continuous sequence of characters with the same formatting (such as font, size, and color).

        Args:
            source (str): The path to the PDF file.
            loaded_elements (list[dict[str, Any]] | None): A list of loaded elements. Defaults to None.
            **kwargs (Any): Additional keyword arguments.

        Kwargs:
            original_source (str, optional): The original source of the document.
            hyperlink_as_markdown (bool, optional): A boolean to determine if the hyperlink should be in
                markdown format. Defaults to True.
            sort_elements (Callable, optional): A callable function to sort the elements in every page.
                Defaults to None. Means no sorting will be done.

        Returns:
            list[dict[str, Any]]: A list of loaded elements.
        """
