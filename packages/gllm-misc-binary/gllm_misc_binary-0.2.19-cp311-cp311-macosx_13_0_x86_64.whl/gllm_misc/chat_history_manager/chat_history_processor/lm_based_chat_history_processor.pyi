from _typeshed import Incomplete
from dataclasses import dataclass
from gllm_inference.request_processor import LMRequestProcessor as LMRequestProcessor, UsesLM
from gllm_inference.schema import UnimodalPrompt as UnimodalPrompt
from gllm_misc.chat_history_manager.chat_history_processor.chat_history_processor import BaseChatHistoryProcessor as BaseChatHistoryProcessor
from typing import Callable

DEFAULT_LM_OUTPUT_KEY: str

@dataclass
class MessagePair:
    """Represents a user-assistant message pair.

    Attributes:
        id (str): Unique identifier for the message pair.
        user (str): User message content.
        assistant (str): Assistant response content.
    """
    id: str
    user: str
    assistant: str

class LMBasedChatHistoryProcessor(BaseChatHistoryProcessor, UsesLM):
    '''A chat history processor which uses a language model.

    This class provides a chat history processor which uses a language model to perform the
    post-processing of chat histories by selecting relevant message pairs.

    This approach prevents hallucination by constraining the LM to select only from existing
    message pairs, rather than generating new content. It also ensures that user messages
    and their corresponding assistant responses are kept together, preserving the conversational flow.

    Attributes:
        lm_request_processor (LMRequestProcessor): The request processor that handles requests to the language model.
        lm_output_key (str): The key in the language model\'s output that contains the selected pair IDs.
            Defaults to DEFAULT_LM_OUTPUT_KEY.
        preserve_history_on_error (bool): If True, returns the original history when processing fails.
            If False, returns an empty list. Defaults to True.
        formatter_fn (Callable[[list[MessagePair]], str]): A function that formats message pairs to a string.
            If None, _format_message_pairs_as_string will be used.
        logger (Logger): The logger for this class.

    Notes:
        When defining the `lm_request_processor`, you must carefully consider the input and output formats:

        The `lm_request_processor` must be configured to:
           - Take the following keys as input:
             - `message_pairs`: The chat history organized as message pairs.
             - `user_message`: Latest user message to add context for the processing.
           - Return a JSON object with the IDs of relevant message pairs.

        If no `formatter_fn` is given, the default format of the message_pairs will be
        sent to the `lm_request_processor`:
           ```
           [PAIR]
           id: <pair_id_1>
           user: <user_message_1>
           assistant: <assistant_response_1>

           [PAIR]
           id: <pair_id_2>
           user: <user_message_2>
           assistant: <assistant_response_2>
           ```

        Expected output from the `lm_request_processor`:
           ```
           {
               "selected_pairs": ["<pair_id_1>", "<pair_id_3>"]
           }
           ```
        Where "selected_pairs" is the value specified by `lm_output_key`.
    '''
    lm_request_processor: Incomplete
    lm_output_key: Incomplete
    preserve_history_on_error: Incomplete
    formatter_fn: Incomplete
    logger: Incomplete
    def __init__(self, lm_request_processor: LMRequestProcessor, lm_output_key: str = ..., preserve_history_on_error: bool = True, formatter_fn: Callable[[list[MessagePair]], str] | None = None) -> None:
        """Initializes a new instance of the LMBasedChatHistoryProcessor class.

        Args:
            lm_request_processor (LMRequestProcessor): The request processor that
                handles requests to the language model.
            lm_output_key (str, optional): The key in the language model's output that contains the message IDs.
                Defaults to DEFAULT_LM_OUTPUT_KEY.
            preserve_history_on_error (bool, optional): If True, returns the original history when processing fails.
                If False, returns an empty list. Defaults to True.
            formatter_fn (Callable[[list[MessagePair]], str] | None, optional): A function to format message pairs
                into string. Defaults to None. If None, _format_message_pairs_as_string will be used.
        """
    async def process(self, history: UnimodalPrompt, user_message: str | None = None) -> UnimodalPrompt:
        """Preprocesses the chat history using language model.

        This method preprocesses the chat history using the language model. The history is organized
        into message pairs, and the model selects which pairs to keep based on relevance.

        Args:
            history (UnimodalPrompt): The chat history to be processed. This should be a list of tuples
                containing the role (user or assistant) and the message content.
            user_message (str): The user message to process the history.

        Returns:
            UnimodalPrompt: The processed chat history in the same format as the input.
        """
