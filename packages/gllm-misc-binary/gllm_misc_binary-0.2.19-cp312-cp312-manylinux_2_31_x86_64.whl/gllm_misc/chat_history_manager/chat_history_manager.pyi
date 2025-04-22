from _typeshed import Incomplete
from enum import StrEnum
from gllm_core.schema import Component
from gllm_datastore.sql_data_store.sql_data_store import BaseSQLDataStore as BaseSQLDataStore
from gllm_inference.schema import PromptRole
from gllm_misc.chat_history_manager.chat_history_processor.chat_history_processor import BaseChatHistoryProcessor as BaseChatHistoryProcessor
from typing import Any

Base: Incomplete

class Message(Base):
    """An SQLAlchemy declarative base for the message table.

    Attributes:
        id (Integer): Primary key for the message.
        conversation_id (String): Identifier for the conversation this message belongs to.
        role (String): Role of the entity sending the message (e.g., 'user', 'assistant').
        content (String): Actual content/text of the message.
        additional_data (String): Any additional data associated with the message.
        created_at (DateTime): Timestamp when the message was created. Defaults to the current time in UTC.
    """
    __tablename__: str
    id: Incomplete
    conversation_id: Incomplete
    role: Incomplete
    content: Incomplete
    additional_data: Incomplete
    created_at: Incomplete

class ChatHistoryOperationType(StrEnum):
    """The type of operation for the chat history manager.

    Attribute:
        RETRIEVE (str): The operation type for retrieving the chat history.
        STORE (str): The operation type for storing the chat history.
    """
    RETRIEVE = 'retrieve'
    STORE = 'store'

class ChatHistoryManager(Component):
    """A class for managing chat history in Gen AI applications.

    This class provides functionality for storing and retrieving chat history
    with optional processing via a ChatHistoryProcessor.

    Currently, this module only supports storing chat history in SQL databases.
    Database interactions are handled through the SQLAlchemy ORM via the SQLAlchemyDataStore class.

    Attributes:
        data_store (BaseSQLDataStore): Data store for storing and retrieving chat history.
        order_by (str): The column to order the chat history by.
        processor (BaseChatHistoryProcessor): Processor for chat history transformation.
    """
    data_store: Incomplete
    order_by: Incomplete
    processor: Incomplete
    def __init__(self, data_store: BaseSQLDataStore, order_by: str = 'created_at', processor: BaseChatHistoryProcessor | None = None) -> None:
        '''Initialize the chat history manager.

        Args:
            data_store (BaseSQLDataStore): Data store for storing and retrieving chat history. Currently only supports
                SQL-based data store.
            order_by (str, optional): The column to order the chat history by. Defaults to "created_at".
            processor (BaseChatHistoryProcessor | None, optional): Processor for chat history transformation.
                Defaults to None.
        '''
    async def retrieve(self, conversation_id: str, user_message: str | None = None, pair_limit: int = 5) -> list[tuple[PromptRole, str]]:
        """Retrieves the chat history of a given conversation ID.

        This method returns the chat history in the format of a list of tuples, where each tuple contains
        a `PromptRole` and a `str`.

        Args:
            conversation_id (str): The ID of the conversation.
            user_message (str | None, optional): The user message. Defaults to None.
            pair_limit (int, optional): The number of pairs of messages to retrieve. Defaults to 5.

        Returns:
            list[tuple[PromptRole, str]]: The retrieved and processed chat history.
                This list contains tuples of role and message content.
        """
    async def store(self, conversation_id: str, user_message: str, assistant_message: str, additional_data: dict[str, Any] | None = None) -> None:
        """Stores the chat history of a given conversation ID.

        Args:
            conversation_id (str): The ID of the conversation.
            user_message (str): The user message.
            assistant_message (str): The assistant message.
            additional_data (dict[str, Any] | None, optional): Additional data to store. Defaults to None.
        """
