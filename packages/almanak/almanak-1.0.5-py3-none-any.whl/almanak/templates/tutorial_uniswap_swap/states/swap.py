from functools import partial
from typing import TYPE_CHECKING

from src.almanak_library.enums import (
    ActionType,
    ExecutionStatus,
    SwapSide,
    TransactionType,
)
from src.almanak_library.models.action import Action
from src.almanak_library.models.action_bundle import ActionBundle
from src.almanak_library.models.params import ApproveParams, SwapParams

if TYPE_CHECKING:
    from ..strategy import StrategyTutorialUniswapSwap


def swap(strat: "StrategyTutorialUniswapSwap") -> ActionBundle | None:
    """
    Swaps a token from the pool provided in the config.

    Args:
        strat (StrategyTutorialUniswapSwap): The Strategy instance.

    Returns:
        ActionBundle or None: An ActionBundle containing the approve and swap.
    """
    return strat.handle_state_with_actions(
        prepare_fn=partial(prepare_swap, strat),
        validate_fn=partial(validate_swap, strat),
        sadflow_fn=partial(sadflow_swap, strat),
        next_state=strat.State.COMPLETED,
    )


def prepare_swap(strat: "StrategyTutorialUniswapSwap") -> ActionBundle | None:
    """
    Prepares the swap actions.

    Returns:
        ActionBundle or None: An ActionBundle containing the approve and swap actions if a swap is needed.
    """

    if strat.persistent_state.last_swap_amounts[0] != 0:
        # We have already swapped, no need to swap again.
        print("Skipping swap, already swapped.")
        return None

    print(f"Swap {strat.amount_in} {strat.token_in.symbol} for {strat.token_out.symbol}")

    action_approve = Action(
        type=ActionType.APPROVE,
        params=ApproveParams(
            token_address=strat.token_in.address,
            spender_address=strat.uniswap_v3.UNISWAP_V3_ROUTER_ADDRESS,
            from_address=strat.wallet_address,
            amount=int(strat.amount_in),
        ),
        protocol=strat.protocol,
    )

    action_swap = Action(
        type=ActionType.SWAP,
        params=SwapParams(
            side=SwapSide.SELL,
            tokenIn=strat.token_in.address,
            tokenOut=strat.token_out.address,
            fee=strat.fee,
            recipient=strat.wallet_address,
            amount=int(strat.amount_in),
            slippage=strat.slippage_swap,
        ),
        protocol=strat.protocol,
    )

    return ActionBundle(
        actions=[action_approve, action_swap],
        chain=strat.chain,
        network=strat.network,
        strategy_id=strat.id,
        config=strat.config,
        persistent_state=strat.persistent_state,
    )


def validate_swap(strat: "StrategyTutorialUniswapSwap") -> bool:
    """
    Validates the swap actions and retrieves the executed amounts using the execution details.

    Returns:
        bool: True if the swap actions were successful and the amounts were retrieved correctly.
              and we can move to the next state.
    """
    actions = strat.executioner_status["actions"]

    # If no actions, it means no wrap was needed.
    if not actions:
        print("Swap was skipped, nothing to validate. Moving to next state.")
        return True

    # At this point it should be a successful execution.
    if actions.status != ExecutionStatus.SUCCESS:
        raise ValueError(f"Validation failed (Swap): Expected SUCCESS, Received: {actions.status}")

    # Find the swap action
    swap_actions = [action for action in actions.actions if action.type == ActionType.SWAP]
    if len(swap_actions) != 1:
        raise ValueError(f"Validation failed (Swap): Expected 1 swap action, received: {len(swap_actions)}")
    swap_action = swap_actions[0]

    swap_executed = swap_action.get_execution_details()
    if not swap_executed:
        raise ValueError("Validation failed: No receipt found for swap")
    if swap_executed.type != ActionType.SWAP:
        raise ValueError(f"Validation failed: Expected SWAP, Received: {swap_executed.type}")

    # Confirm that the tokens in the receipt match the strategy tokens
    tokens_receipt = (
        swap_executed.tokenIn_symbol.lower(),
        swap_executed.tokenOut_symbol.lower(),
    )
    tokens_strat = (strat.token_in.symbol.lower(), strat.token_out.symbol.lower())
    if set(tokens_receipt) != set(tokens_strat):
        raise ValueError("Validation failed: Swap executed for wrong tokens")

    if swap_executed.tokenIn_symbol.lower() == strat.token0.symbol.lower():
        amount0 = swap_executed.amountIn * -1
        amount1 = swap_executed.amountOut
    else:
        amount0 = swap_executed.amountOut
        amount1 = swap_executed.amountIn * -1

    strat.persistent_state.last_swap_amounts = (int(amount0), int(amount1))
    print(swap_executed)
    return True


def sadflow_swap(strat: "StrategyTutorialUniswapSwap") -> ActionBundle:
    """
    Handles the sadflow for the swap state.
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
            raise ValueError("Sadflow swap with SUCCESS Status. Should not happen.")
        case _:
            raise ValueError(f"Invalid status for validate swap: {actions.status}")


def sadflow_retry(strat: "StrategyTutorialUniswapSwap") -> ActionBundle:
    """
    Handles the basic retry sadflow.
    """
    return prepare_swap(strat)  # Retrying the same state


def sadflow_partial_retry(strat: "StrategyTutorialUniswapSwap") -> ActionBundle:
    """
    Handles the complex partial retry sadflow.

    The Prepare Action sends: actions=[action_approve, action_swap]
    - Failure #1: The Approves failed -> We retry the same state as is.
    - Failure #2: Swap failed -> We check the revert reason.
                              -> For now we simply retry the same state as is (updating values),
                                 because we don't care too much double approving.
                  Known revert reasons:
                    - STF: Retry the same state for now.
                    - Slippage: Retry the same state for now.
    """
    # Only support 1 retry attempt.
    if strat.persistent_state.sadflow_actions and len(strat.persistent_state.sadflow_actions) > 0:
        raise ValueError("Partial Retry (Swap): Sadflow Partial Retry already attempted. Halting strategy for human intervention.")

    actions = strat.executioner_status["actions"]
    if actions.status != ExecutionStatus.PARTIAL_EXECUTION:
        raise ValueError("Partial Retry (Swap): Expected PARTIAL_EXECUTION status.")

    print("Entering Partial Retry (Swap) - last attempted actions:", actions)

    # --------------------------------------------
    # Failure #1: The Approve failed
    # --------------------------------------------
    # Find the approve transactions
    approve_tx = [tx for tx in actions.transactions if tx.type == TransactionType.APPROVE]
    if len(approve_tx) != 1:
        raise ValueError(f"Partial Retry (Swap): Expected 1 approve transaction, received: {len(approve_tx)}")

    # Check if the approve transactions failed
    if approve_tx[0].tx_status != ExecutionStatus.SUCCESS:
        print("Partial Retry: Approve failed, restarting the state.")
        strat.persistent_state.current_flowstatus = strat.InternalFlowStatus.PREPARING_ACTION
        return prepare_swap(strat)  # Prepare the same actions and return them as part of sadflow.

    # --------------------------------------------
    # Failure #2: The Swap failed
    # --------------------------------------------
    # Find the swap transaction
    swap_txs = [tx for tx in actions.transactions if tx.type == TransactionType.SWAP]
    if len(swap_txs) != 1:
        raise ValueError(f"Partial Retry (Swap): Expected 1 swap transaction, received: {len(swap_txs)}")
    swap_tx = swap_txs[0]

    # Check if the swap transaction failed
    if swap_tx.tx_status != ExecutionStatus.SUCCESS:
        try:
            revert_reason = str(strat.execution_manager.get_revert_reason(strat.web3, swap_tx.tx_hash))
        except Exception as e:
            print(f"Partial Retry: Failed to get revert reason. {e}")
            revert_reason = "Unknown"

        print(f"Partial Retry: Swap failed with revert reason: {revert_reason}")
        if "slippage" in revert_reason.lower():
            print("Partial Retry: Slippage error detected, restarting the state.")
        elif "stf" in revert_reason.lower():
            print("Partial Retry: STF error detected, restarting the state.")
        else:
            print("Partial Retry: Unknown revert reason, restarting the state.")

        # For now, we simply retry re-prepare all actions, regardless of the revert reason.
        strat.persistent_state.current_flowstatus = strat.InternalFlowStatus.PREPARING_ACTION
        return prepare_swap(strat)  # Prepare the same actions and return them as part of sadflow.

    # We shouldn't reach this point.
    raise ValueError("Partial Retry (Swap): Unknown partial flow status.")
