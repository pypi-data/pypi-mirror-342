from enum import Enum
from uuid import UUID

from pydantic import validator
from src.almanak_library.enums import Chain, Network, Protocol
from src.strategy.models import (
    InternalFlowStatus,
    PersistentStateBase,
    StrategyConfigBase,
)
from web3 import Web3


class State(Enum):
    """Enum representing the state of the strategy."""

    INITIALIZATION = "INITIALIZATION"
    SWAP = "SWAP"
    COMPLETED = "COMPLETED"  # A "Cycle" is completed in between Checks for Rebalance
    TEARDOWN = "TEARDOWN"
    TERMINATED = "TERMINATED"  # The Strategy is terminated


class SubState(Enum):
    """Enum representing the substates of some of the strategy states. A state machine within a state machine."""

    NO_SUBSTATE = "NO_SUBSTATE"


class PersistentState(PersistentStateBase):
    # Strategy Framework variables
    current_state: State
    current_substate: SubState
    current_flowstatus: InternalFlowStatus
    current_actions: list[UUID]
    sadflow_counter: int
    sadflow_actions: list[UUID]
    not_included_counter: int

    # Strategy Specific variables
    last_swap_amounts: tuple[int, int]

    # Required for json dump of Enum
    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        data["current_state"] = self.current_state.value
        data["current_substate"] = self.current_substate.value
        data["current_flowstatus"] = self.current_flowstatus.value
        data["current_actions"] = [str(action) for action in self.current_actions]
        data["sadflow_actions"] = [str(action) for action in self.sadflow_actions]
        return data


class StrategyConfig(StrategyConfigBase):
    # Strategy Framework variables
    id: str
    network: Network
    chain: Chain
    protocol: Protocol
    initiate_teardown: bool
    pause_strategy: bool

    # Strategy Specific variables
    wallet_address: str
    pool_address: str
    token_in_address: str
    token_in_amount: int
    slippage_swap: float

    @validator(
        "wallet_address",
        "pool_address",
        check_fields=False,
    )
    def validate_ethereum_address(cls, value):
        if not Web3.is_address(value):
            raise ValueError("Invalid Ethereum address")
        return value

    # Required for json dump of Enum
    def model_dump(self, *args, **kwargs):
        d = super().model_dump(*args, **kwargs)
        d["network"] = self.network.value
        d["chain"] = self.chain.value
        d["protocol"] = self.protocol.value
        return d
