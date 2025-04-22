import abc
from abc import ABC, abstractmethod

class BaseDownloader(ABC, metaclass=abc.ABCMeta):
    """Base class for document converter."""
    @abstractmethod
    def download(self, source: str, output: str) -> None:
        """Converts a document.

        Args:
            source (str): The source of the document (could be JSON-formatted or URL)
            output (str): The output where we put the downloaded content (usually a folder path).

        Returns:
            None
        """
