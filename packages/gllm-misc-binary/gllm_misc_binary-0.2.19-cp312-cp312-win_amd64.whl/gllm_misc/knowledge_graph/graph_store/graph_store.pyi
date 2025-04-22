import abc
from abc import ABC, abstractmethod
from typing import Any

class BaseGraphStore(ABC, metaclass=abc.ABCMeta):
    """Abstract base class for graph stores."""
    @abstractmethod
    def query(self, query: str, **kwargs: Any) -> Any:
        """Query the graph store.

        Args:
            query (str): The query to be executed.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            Any: The result of the query.
        """
    @abstractmethod
    def cascade_delete(self, element_ids: list[str], **kwargs: Any) -> None:
        """Perform cascade deletion.

        This method is used to delete a list of elements from the graph store given a list of chunk IDs.
        It is crucial to ensure that all elements and their associated data are deleted correctly in regard to the
        source documents.

        Args:
            element_ids (list[str]): List of element IDs to be deleted.
            **kwargs (Any): Additional keyword arguments.
        """
