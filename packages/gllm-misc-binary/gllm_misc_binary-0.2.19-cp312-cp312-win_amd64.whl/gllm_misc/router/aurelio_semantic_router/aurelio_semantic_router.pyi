from _typeshed import Incomplete
from gllm_misc.router.aurelio_semantic_router.index.aurelio_index import BaseAurelioIndex as BaseAurelioIndex
from gllm_misc.router.router import BaseRouter as BaseRouter
from semantic_router import Route
from semantic_router.encoders import BaseEncoder as BaseEncoder
from typing import Any

class AurelioSemanticRouter(BaseRouter):
    """A router that utilizes the Aurelio Labs library to route the input text to the appropriate path.

    The `AurelioSemanticRouter` utilizes the Aurelio Labs library to route a given input text to an appropriate path
    based on the similarity with existing samples. If the determined route is not valid, it defaults to a predefined
    route.

    Attributes:
        route_layer (RouteLayer): The Aurelio Labs route layer that handles the routing logic.
        default_route (str): The default route to be used if the input text is not similar to any of the routes.
        valid_routes (set[str]): A set of valid routes for the router.

    Notes:
        For more information about the Aurelio Labs library, please refer to
        https://github.com/aurelio-labs/semantic-router
    """
    route_layer: Incomplete
    def __init__(self, default_route: str, valid_routes: set[str], encoder: BaseEncoder, routes: list[Route] | dict[str, list[str]] | None = None, index: BaseAurelioIndex | None = None, **kwargs: Any) -> None:
        """Initializes a new instance of the AurelioSemanticRouter class.

        To define the routes, at least one of the `routes` or `index` parameters must be provided.
        When both parameters are provided, the `routes` parameter is ignored.

        Args:
            default_route (str): The default route to be used if the input text is not similar to any of the routes.
            valid_routes (set[str]): A set of valid routes for the router.
            encoder (BaseEncoder): An Aurelio Labs Encoder to encode the input text and the samples. The encoded
                vectors are used to calculate the similarity between the input text and the samples.
            routes (list[Route] | dict[str, list[str]] | None, optional): A list of Aurelio Labs Routes
                or a dictionary mapping route names to the list of samples. Ignored if `index` is provided.
                Defaults to None.
            index (BaseAurelioIndex | None, optional): A router index to retrieve the routes.
                If provided, it is prioritized over `routes`. Defaults to None.
            kwargs (Any): Additional keyword arguments to be passed to the Aurelio Labs Route Layer.

        Raises:
            ValueError:
                1. If neither `routes` nor `index` is provided.
                2. If the parsed routes contains routes that are not in the set of valid routes.
                3. If the provided default route is not in the set of valid routes.
        """
    @classmethod
    def from_file(cls, default_route: str, valid_routes: set[str], file_path: str) -> AurelioSemanticRouter:
        '''Creates a new instance of the AurelioSemanticRouter class from a file.

        This method creates a new instance of the AurelioSemanticRouter class from a file. It supports JSON and YAML
        file extensions.

        Args:
            default_route (str): The default route to be used if the input text is not similar to any of the routes.
            valid_routes (set[str]): A set of valid routes for the router.
            file_path (str): The path to the file containing the routes. The file extension must be either JSON or YAML.

        Returns:
            AurelioSemanticRouter: A new instance of the AurelioSemanticRouter class.

        Raises:
            ValueError: If the file extension is not ".json" or ".yaml".
        '''
