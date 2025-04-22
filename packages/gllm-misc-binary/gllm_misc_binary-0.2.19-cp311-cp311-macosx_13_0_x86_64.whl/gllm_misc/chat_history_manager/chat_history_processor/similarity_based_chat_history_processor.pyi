from _typeshed import Incomplete
from gllm_inference.em_invoker.em_invoker import BaseEMInvoker as BaseEMInvoker
from gllm_inference.schema import UnimodalPrompt as UnimodalPrompt
from gllm_misc.chat_history_manager.chat_history_processor.chat_history_processor import BaseChatHistoryProcessor as BaseChatHistoryProcessor
from typing import Callable

class SimilarityBasedChatHistoryProcessor(BaseChatHistoryProcessor):
    """A chat history processor that preprocesses chat history based on sentence similarity.

    Attributes:
        em_invoker (BaseEMInvoker): An instance of the BaseEMInvoker class to embed text.
        threshold (float): The threshold to filter out the chat history.
    """
    em_invoker: Incomplete
    threshold: Incomplete
    similarity_func: Incomplete
    def __init__(self, em_invoker: BaseEMInvoker, threshold: float = 0.8, similarity_func: Callable[[list[float], list[list[float]]], list[float]] = ...) -> None:
        """Initializes the SimilarityBasedChatHistoryProcessor class.

        This constructor method initializes an instance of the SimilarityBasedChatHistoryProcessor class, setting up
        the embedding model and threshold that will be used to preprocess chat history based on similarity to a query.

        Args:
            em_invoker (BaseEMInvoker): An instance of the BaseEMInvoker class that will be used to calculate the
                embeddings of the query and the chat history.
            threshold (float): The threshold to filter out the chat history. Defaults to 0.8.
            similarity_func (callable): The function to calculate the similarity between embeddings.
                The function should take two arguments: a vector and a matrix of vectors.
                The function should return a list of similarity scores.
                Defaults to the `gllm_core.utils.similarity.cosine` similarity function.

        Raises:
            ValueError: If threshold is not between 0 and 1.
            TypeError: If similarity_func is not callable.
        """
    async def process(self, history: UnimodalPrompt, user_message: str) -> UnimodalPrompt:
        """Processes the chat history using embedding similarity.

        This method filters out irrelevant information from the chat history
        using the embedding model to produce the similarity of history and user message.
        It uses batch processing for calculating similarities between user message and chat history.

        Args:
            history (UnimodalPrompt): The chat history to be processed. This should be a list of tuples,
                where each tuple contains a role (PromptRole) and a message (str).
            user_message (str): The user message to filter out the irrelevant history.

        Returns:
            UnimodalPrompt: The processed chat history in the same format as the input.
        """
