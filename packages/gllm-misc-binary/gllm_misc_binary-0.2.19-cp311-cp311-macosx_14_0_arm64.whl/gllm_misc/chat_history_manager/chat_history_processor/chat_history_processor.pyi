import abc
from abc import ABC, abstractmethod
from gllm_inference.schema import UnimodalPrompt as UnimodalPrompt

class BaseChatHistoryProcessor(ABC, metaclass=abc.ABCMeta):
    """An abstract base class for processing chat history.

    This class provides a foundation for implementing different chat history processing strategies.
    Subclasses should implement the process method to define specific processing behavior.
    """
    @abstractmethod
    async def process(self, history: UnimodalPrompt, user_message: str | None = None) -> UnimodalPrompt:
        """Process the retrieved chat history.

        This method should be implemented by subclasses to define specific processing behavior.

        Args:
            history (list[tuple[PromptRole, str]): The retrieved chat history.
            user_message (str | None, optional): The user message. Defaults to None.

        Returns:
            UnimodalPrompt: The processed chat history. This should be a list of tuples
                where each tuple contains a PromptRole and a string representing the message.

        Raises:
            NotImplementedError: This method should be implemented by subclasses.
        """
