from typing import TYPE_CHECKING

from src.almanak_library.models.action_bundle import ActionBundle

if TYPE_CHECKING:
    from ..strategy import StrategyTemplateHelloWorld


def display_message(strategy: "StrategyTemplateHelloWorld") -> ActionBundle:
    # Get the message from the config
    message = strategy.config.message

    # Display the message.
    print(message + "\n")

    # Save the last displayed message into the persistent state (this is just an example! a bit useless here).
    strategy.persistent_state.last_message = message

    # Normally other part of the code would handle that, but here we'll force a save on disk.
    strategy.save_persistent_state()
