from functools import partial
from typing import TYPE_CHECKING

from src.almanak_library.enums import ActionType, ExecutionStatus
from src.almanak_library.models.action import Action
from src.almanak_library.models.action_bundle import ActionBundle
from src.almanak_library.models.params import WrapParams

if TYPE_CHECKING:
    from ..strategy import StrategyTutorialUniswapSwap


def initialization(strat: "StrategyTutorialUniswapSwap") -> ActionBundle:
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
    return strat.handle_state_with_actions(
        prepare_fn=partial(prepare_wrap, strat),
        validate_fn=partial(validate_wrap, strat),
        sadflow_fn=partial(sadflow_wrap, strat),
        next_state=strat.State.SWAP,
    )


def prepare_wrap(strat: "StrategyTutorialUniswapSwap") -> ActionBundle | None:
    """
    Prepares the swap actions.

    Returns:
        ActionBundle or None: An ActionBundle containing the approve and swap actions if a swap is needed.
    """

    # Check if Wrap is needed.
    if strat.token_in.address.lower() != strat.uniswap_v3.WETH_ADDRESS.lower():
        print("Wrap not needed. Moving to next state.")
        return None

    print(f"Wrap {strat.amount_in} WETH")

    action_wrap = Action(
        type=ActionType.WRAP,
        params=WrapParams(
            from_address=strat.wallet_address,
            amount=int(strat.amount_in),
        ),
        protocol=strat.protocol,
    )

    return ActionBundle(
        actions=[action_wrap],
        chain=strat.chain,
        network=strat.network,
        strategy_id=strat.id,
        config=strat.config,
        persistent_state=strat.persistent_state,
    )


def validate_wrap(strat: "StrategyTutorialUniswapSwap") -> bool:
    """
    Validates the wrap action and retrieves the executed amount using the execution details.

    Returns:
        bool: True if the wrap action was successful and the amount was retrieved correctly.
              and we can move to the next state.
    """
    actions = strat.executioner_status["actions"]

    # If no actions, it means no wrap was needed.
    if not actions:
        print("Wrap was skipped, nothing to validate. Moving to next state.")
        return True

    # At this point it should be a successful execution.
    if actions.status != ExecutionStatus.SUCCESS:
        raise ValueError(f"Validation failed (Wrap): Expected SUCCESS, Received: {actions.status}")

    # Find the wrap action
    wrap_actions = [action for action in actions.actions if action.type == ActionType.WRAP]
    if len(wrap_actions) != 1:
        raise ValueError(f"Validation failed (Wrap): Expected 1 wrap action, received: {len(wrap_actions)}")
    wrap_action = wrap_actions[0]

    wrap_executed = wrap_action.get_execution_details()
    if not wrap_executed:
        raise ValueError("Validation failed: No receipt found for wrap")
    if wrap_executed.type != ActionType.WRAP:
        raise ValueError(f"Validation failed: Expected WRAP, Received: {wrap_executed.type}")

    print(wrap_executed)

    if wrap_executed.amount != int(strat.amount_in):
        raise ValueError(f"Validation failed: Expected amount {strat.amount_in}, Received: {wrap_executed.amount}")

    return True


def sadflow_wrap(strat: "StrategyTutorialUniswapSwap") -> ActionBundle:
    """
    Handles the sadflow for the initialization wrap state.
    Calls the appropriate function based on the status of the actions.
    """
    actions = strat.executioner_status["actions"]
    match actions.status:
        case ExecutionStatus.FAILED | ExecutionStatus.CANCELLED | ExecutionStatus.NOT_INCLUDED:
            actions = sadflow_retry(strat)
            return actions
        case ExecutionStatus.PARTIAL_EXECUTION:
            actions = sadflow_partial_retry(strat)
            return actions
        case ExecutionStatus.SUCCESS:
            raise ValueError("Sadflow wrap with SUCCESS Status. Should not happen.")
        case _:
            raise ValueError(f"Invalid status for validate wrap: {actions.status}")


def sadflow_retry(strat: "StrategyTutorialUniswapSwap") -> ActionBundle:
    """
    Handles the basic retry sadflow.
    """
    return prepare_wrap(strat)  # Retrying the same state


def sadflow_partial_retry(strat: "StrategyTutorialUniswapSwap") -> ActionBundle:
    raise ValueError("Partial retry should not happen for only a wrap.")
