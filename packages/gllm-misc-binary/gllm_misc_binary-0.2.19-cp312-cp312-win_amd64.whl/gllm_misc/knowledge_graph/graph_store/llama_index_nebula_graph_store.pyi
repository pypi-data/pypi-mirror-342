from gllm_misc.knowledge_graph.graph_store.llama_index_graph_store import LlamaIndexGraphStore as LlamaIndexGraphStore
from llama_index.graph_stores.nebula import NebulaPropertyGraphStore
from typing import Any

class LlamaIndexNebulaGraphStore(LlamaIndexGraphStore, NebulaPropertyGraphStore):
    """Graph store for Nebula. This class extends the NebulaPropertyGraphStore class from LlamaIndex."""
    def cascade_delete(self, element_ids: list[str], **kwargs: Any) -> None:
        """Perform cascade deletion of elements (chunks) and their related entities in the graph.

        Args:
            element_ids (list[str]): List of element (chunk) IDs to be deleted.
            **kwargs (Any): Additional keyword arguments.
        """
