from time import sleep
from typing import TYPE_CHECKING

from src.almanak_library.models.action_bundle import ActionBundle

if TYPE_CHECKING:
    from ..strategy import StrategyTemplateHelloWorld


def teardown(strategy: "StrategyTemplateHelloWorld") -> ActionBundle:
    """
    Concludes the strategy by closing any active positions and preparing the system for a reset or shutdown.
    Leaves the system in a state where it can be cleanly initialized again.

    Returns:
        ActionBundle | None: An action bundle with the teardown actions.
    """
    print("Tearing down the strategy\n")
    print("Sleeping for 2 seconds\n")
    sleep(2)
