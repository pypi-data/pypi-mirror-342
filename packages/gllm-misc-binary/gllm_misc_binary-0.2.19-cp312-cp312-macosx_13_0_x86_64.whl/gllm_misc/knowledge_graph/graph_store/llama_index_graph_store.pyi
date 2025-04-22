import abc
from abc import ABC
from gllm_misc.knowledge_graph.graph_store.graph_store import BaseGraphStore as BaseGraphStore
from llama_index.core.graph_stores.types import PropertyGraphStore
from typing import Any

class LlamaIndexGraphStore(PropertyGraphStore, BaseGraphStore, ABC, metaclass=abc.ABCMeta):
    """Abstract base class for a LlamaIndex graph store."""
    def query(self, query: str, **kwargs: Any) -> Any:
        """Query the graph store.

        Args:
            query (str): The query to be executed.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            Any: The result of the query.
        """
