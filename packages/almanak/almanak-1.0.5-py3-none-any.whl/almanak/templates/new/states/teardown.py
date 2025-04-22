from time import sleep
from typing import TYPE_CHECKING

from src.almanak_library.models.action_bundle import ActionBundle

if TYPE_CHECKING:
    from ..strategy import MyStrategy


def teardown(strategy: "MyStrategy") -> ActionBundle:
    """
    Concludes the strategy by closing any active positions and/or releasing any locked assets.

    Returns:
        ActionBundle | None: An action bundle with the teardown actions.
    """
    print("Tearing down the strategy\n")
    print("Sleeping for 2 seconds\n")
    sleep(2)
