from _typeshed import Incomplete
from gllm_docproc.model.element import Element as Element
from gllm_docproc.utils.html_constants import HTMLTags as HTMLTags, ItemDataKeys as ItemDataKeys, TableConstants as TableConstants

class FlatTableUtils:
    """A utility class providing methods for extracting data from HTML tables."""
    colcount: int
    rowspans: Incomplete
    def __init__(self) -> None:
        """Initialize the FlatTableUtils."""
    def generate_tables(self, content: list[Element]) -> list[list[str]]:
        """Generate tables from HTML content.

        Args:
            content (List[Element]): The list of Element instances representing the HTML content.

        Returns:
            List[List[str]]: A list containing the generated tables.
        """
    def filter_table(self, table_content: list[Element]) -> tuple[list[Element], list[Element]]:
        """Filter the HTML table content.

        Args:
            table_content (List[Element]): The list of Element instances representing the HTML table.

        Returns:
            tuple[List[Element], List[Element]]: A tuple containing the filtered table content
                and the removed elements.
        """
