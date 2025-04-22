from time import sleep
from typing import TYPE_CHECKING

from src.almanak_library.models.action_bundle import ActionBundle

if TYPE_CHECKING:
    from ..strategy import StrategyTemplateHelloWorld


def initialization(strategy: "StrategyTemplateHelloWorld") -> ActionBundle:
    """
    Initializes the strategy by preparing assets and opening positions.

    The initialization process may involve swapping assets, wrapping ETH, and opening liquidity positions.
    It operates in several substates to manage the sequence of actions.

    Returns:
        ActionBundle: An action bundle representing the actions required to initialize
        the strategy, or None if no actions are required.

    Notes:
        - This method should only be called at the start of the strategy lifecycle.
        - The process is divided into substates to handle complex initialization steps.
    """
    print("Initializing the strategy")
    print("Sleeping for 2 seconds\n")
    sleep(2)
