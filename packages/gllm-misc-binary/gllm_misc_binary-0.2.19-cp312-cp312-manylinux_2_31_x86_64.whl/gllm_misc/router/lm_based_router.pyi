from _typeshed import Incomplete
from gllm_inference.request_processor import LMRequestProcessor as LMRequestProcessor, UsesLM
from gllm_misc.router.router import BaseRouter as BaseRouter

DEFAULT_LM_OUTPUT_KEY: str

class LMBasedRouter(BaseRouter, UsesLM):
    '''A router that utilizes a language model to determine the appropriate route for an input text.

    This class routes a given input text to an appropriate path based on the output of a language model.
    If the determined route is not valid, it defaults to a predefined route.

    Attributes:
        lm_request_processor (LMRequestProcessor): The request processor that handles requests to the language model.
        default_route (str): The default route to be used if the language model\'s output is invalid.
        valid_routes (set[str]): A set of valid routes for the router.
        lm_output_key (str, optional): The key in the language model\'s output that contains the route.

    Notes:
        The `lm_request_processor` must be configured to:
        1. Take a "text" key as input. The input text of the router should be passed as the value of this "text" key.
        2. Return a JSON object which contains the selected route as a string. The key of the route is specified by the
        `lm_output_key` attribute. Furthermore, the selected route must be present in the `valid_routes` set.

        Output example, assuming the `lm_output_key` is "route":
        {
            "route": "<route_string>"
        }
    '''
    lm_request_processor: Incomplete
    lm_output_key: Incomplete
    def __init__(self, lm_request_processor: LMRequestProcessor, default_route: str, valid_routes: set[str], lm_output_key: str = ...) -> None:
        """Initializes a new instance of the LMBasedRouter class.

        Args:
            lm_request_processor (LMRequestProcessor): The request processor that handles requests to the
                language model.
            default_route (str): The default route to be used if the language model's output is invalid.
            valid_routes (set[str]): A set of valid routes for the router.
            lm_output_key (str): The key in the language model's output that contains the route.
                Defaults to DEFAULT_LM_OUTPUT_KEY.

        Raises:
            ValueError: If the provided default route is not in the set of valid routes.
        """
