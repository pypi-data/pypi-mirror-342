from _typeshed import Incomplete
from gllm_misc.knowledge_graph.graph_store.llama_index_graph_store import LlamaIndexGraphStore as LlamaIndexGraphStore
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from typing import Any

class LlamaIndexNeo4jGraphStore(LlamaIndexGraphStore, Neo4jPropertyGraphStore):
    """Graph store for Neo4j. This class extends the Neo4jPropertyGraphStore class from LlamaIndex."""
    neo4j_version_tuple: Incomplete
    def __init__(self, *args, **kwargs) -> None:
        """Initialize the LlamaIndexNeo4jGraphStore.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
    def cascade_delete(self, element_ids: list[str], **kwargs: Any) -> None:
        """Perform cascade deletion of elements (chunks) and their related entities in the graph.

        Args:
            element_ids (list[str]): List of element (chunk) IDs to be deleted.
            **kwargs (Any): Additional keyword arguments.
        """
