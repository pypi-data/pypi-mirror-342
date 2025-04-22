from functools import partial
from typing import TYPE_CHECKING

from src.almanak_library.constants import get_address_by_chain_and_network
from src.almanak_library.enums import ActionType, ExecutionStatus
from src.almanak_library.models.action import Action
from src.almanak_library.models.action_bundle import ActionBundle
from src.almanak_library.models.params import UnwrapParams

if TYPE_CHECKING:
    from ..strategy import StrategyTutorialUniswapSwap


def teardown(strat: "StrategyTutorialUniswapSwap") -> ActionBundle:
    """
    Concludes the strategy by closing any active positions and preparing the system for a reset or shutdown.
    Leaves the system in a state where it can be cleanly initialized again.

    Returns:
        ActionBundle | None: An action bundle with the teardown actions.
    """
    return strat.handle_state_with_actions(
        prepare_fn=partial(prepare_unwrap, strat),
        validate_fn=partial(validate_unwrap, strat),
        sadflow_fn=partial(sadflow_unwrap, strat),
        next_state=strat.State.TERMINATED,
    )


def prepare_unwrap(strat: "StrategyTutorialUniswapSwap") -> ActionBundle | None:
    """
    Prepares the swap actions.

    Returns:
        ActionBundle or None: An ActionBundle containing the approve and swap actions if a swap is needed.
    """
    # Check if UnWrap is needed.
    if strat.token_out.address.lower() != strat.uniswap_v3.WETH_ADDRESS.lower():
        print("UnWrap not needed. Moving to next state.")
        return None

    last_swap_amounts = strat.persistent_state.last_swap_amounts
    amount = int(last_swap_amounts[0] if last_swap_amounts[0] > 0 else last_swap_amounts[1])

    if amount <= 0:
        raise ValueError(f"Invalid amount to unwrap: {amount}")

    WETH_ADDRESS = get_address_by_chain_and_network(chain=strat.chain, network=strat.network, contract_name="WETH")

    action_unwrap = Action(
        type=ActionType.UNWRAP,
        params=UnwrapParams(
            from_address=strat.wallet_address,
            token_address=WETH_ADDRESS,
            amount=amount,
        ),
        protocol=strat.protocol,
    )

    return ActionBundle(
        actions=[action_unwrap],
        chain=strat.chain,
        network=strat.network,
        strategy_id=strat.id,
        config=strat.config,
        persistent_state=strat.persistent_state,
    )


def validate_unwrap(strat: "StrategyTutorialUniswapSwap") -> bool:
    """
    Validates the wrap action and retrieves the executed amount using the execution details.

    Returns:
        bool: True if the wrap action was successful and the amount was retrieved correctly.
              and we can move to the next state.
    """
    actions = strat.executioner_status["actions"]

    # If no actions, it means no wrap was needed.
    if not actions:
        print("Unwrap was skipped, nothing to validate. Moving to next state.")
        return True

    # At this point it should be a successful execution.
    if actions.status != ExecutionStatus.SUCCESS:
        raise ValueError(f"Validation failed (Unwrap): Expected SUCCESS, Received: {actions.status}")

    # Find the wrap action
    unwrap_actions = [action for action in actions.actions if action.type == ActionType.UNWRAP]
    if len(unwrap_actions) != 1:
        raise ValueError(f"Validation failed (Unwrap): Expected 1 unwrap action, received: {len(unwrap_actions)}")
    unwrap_action = unwrap_actions[0]

    unwrap_executed = unwrap_action.get_execution_details()
    if not unwrap_executed:
        raise ValueError("Validation failed: No receipt found for unwrap")
    if unwrap_executed.type != ActionType.UNWRAP:
        raise ValueError(f"Validation failed: Expected UNWRAP, Received: {unwrap_executed.type}")

    print(unwrap_executed)

    return True


def sadflow_unwrap(strat: "StrategyTutorialUniswapSwap") -> ActionBundle:
    """
    Handles the sadflow for the initialization unwrap state.
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
            raise ValueError("Sadflow unwrap with SUCCESS Status. Should not happen.")
        case _:
            raise ValueError(f"Invalid status for validate unwrap: {actions.status}")


def sadflow_retry(strat: "StrategyTutorialUniswapSwap") -> ActionBundle:
    """
    Handles the basic retry sadflow.
    """
    return prepare_unwrap(strat)  # Retrying the same state


def sadflow_partial_retry(strat: "StrategyTutorialUniswapSwap") -> ActionBundle:
    raise ValueError("Partial retry should not happen for only an unwrap.")
