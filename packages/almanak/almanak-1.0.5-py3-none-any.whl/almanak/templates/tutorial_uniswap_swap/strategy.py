import os

from src.almanak_library.models.action_bundle import ActionBundle
from src.strategy.strategies.tutorial_uniswap_swap.models import (
    PersistentState,
    State,
    StrategyConfig,
    SubState,
)
from src.strategy.strategy_base import StrategyUniV3
from src.strategy.utils.pool_token import pooltoken_service
from src.utils.utils import get_protocol_sdk, get_web3_by_network_and_chain

from .states.initialization import initialization
from .states.swap import swap
from .states.teardown import teardown


class StrategyTutorialUniswapSwap(StrategyUniV3):
    STRATEGY_NAME = "Tutorial_Uniswap_Swap"

    def __init__(self, **kwargs):
        """
        Initialize the strategy with given configuration parameters.

        Args:
            **kwargs: Strategy-specific configuration parameters.
        """
        super().__init__()
        self.name = self.STRATEGY_NAME.replace("_", " ")

        # Overwrite the States and SubStates for this Strategy
        self.State = State
        self.SubState = SubState

        # Get configuration from kwargs
        try:
            self.config = StrategyConfig(**kwargs)
        except Exception as e:
            raise ValueError(f"Invalid Strategy Configuration. {e}")

        self.id = self.config.id
        self.chain = self.config.chain
        self.network = self.config.network
        self.protocol = self.config.protocol
        self.wallet_address = self.config.wallet_address
        self.pool_address = self.config.pool_address

        self.web3 = get_web3_by_network_and_chain(self.network, self.chain)
        self.uniswap_v3 = get_protocol_sdk(self.protocol, self.network, self.chain)
        self.pooltoken = pooltoken_service.get_registry(
            protocol=self.protocol,
            chain=self.chain,
            network=self.network,
            web3=self.web3,
            pool_abi=self.uniswap_v3.POOL_ABI,
            token_abi=self.uniswap_v3.ERC20_ABI,
        )
        self.pool = self.pooltoken.get_pool(self.pool_address)
        self.token0 = self.pool.token0
        self.token1 = self.pool.token1
        self.fee = self.pool.fee

        self.slippage_swap = self.config.slippage_swap

        print(self.pool)

        if self.token0.address.lower() == self.config.token_in_address.lower():
            self.token_in = self.token0
            self.token_out = self.token1
        else:
            self.token_in = self.token1
            self.token_out = self.token0

        self.amount_in = self.config.token_in_amount

        self.initialize_persistent_state()

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, chain={self.chain}, network={self.network}, protocol={self.protocol}, wallet_address={self.wallet_address})"

    @classmethod
    def get_persistent_state_model(cls):
        return PersistentState

    @classmethod
    def get_config_model(cls):
        return StrategyConfig

    def initialize_persistent_state(self):
        """
        Initialize the persistent state by uploading the JSON template.
        """
        template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "persistent_state_template.json")
        super().initialize_persistent_state(template_path)

    def restart_cycle(self) -> None:
        """A Strategy should only be restarted when the full cycle is completed."""
        if self.persistent_state.current_state == self.State.COMPLETED:
            # Properly restart the cycle
            self.persistent_state.current_flowstatus = self.InternalFlowStatus.PREPARING_ACTION
            self.persistent_state.current_state = self.State.SWAP
            self.persistent_state.completed = False

            # Dump the state to the persistent state because we load it when called.
            self.save_persistent_state()
        elif self.persistent_state.current_state == self.State.TERMINATED:
            print("Strategy is terminated, nothing to restart.")
        else:
            raise ValueError("The strategy is not completed yet, can't restart.")

    def run(self):
        """
        Executes the strategy by progressing through its state machine based on the current state.

        This method orchestrates the transitions between different states of the strategy,
        performing actions as defined in each state, and moves to the next state based on the
        actions' results and strategy's configuration.

        Returns:
            dict: A dictionary containing the current state, next state, and actions taken or
                recommended, depending on the execution mode.

        Raises:
            ValueError: If an unknown state is encountered, indicating a potential issue in state management.

        Notes:
            - This method is central to the strategy's operational logic, calling other methods
            associated with specific states like initialization, rebalancing, or closing positions.
            - It integrates debugging features to display balances and positions if enabled.
        """
        print("Running the strategy")
        if self.config.pause_strategy:
            print("Strategy is paused.")
            return None

        try:
            self.load_persistent_state()
        except Exception as e:
            raise ValueError(f"Unable to load persistent state. {e}")

        # Check if initiate_teardown (this has to happen after loading the persistent state or it will be overwritten)
        self.check_teardown()

        # NOTE: Here we are cheating a little by changing the state directly from here.
        #       Usually, the state change would be handled in the state's function/file.
        actions = None
        while self.is_locked and not actions:
            match self.persistent_state.current_state:
                case State.INITIALIZATION:
                    actions = initialization(self)
                case State.SWAP:
                    actions = swap(self)
                case State.COMPLETED:
                    self.complete()
                case State.TEARDOWN:
                    actions = teardown(self)
                case self.State.TERMINATED:
                    print("Strategy is terminated.")
                    actions = None
                case _:
                    raise ValueError(f"Unknown state: {self.persistent_state.current_state}")

        # Save actions to current state to load the executioner status from them when re-entering.
        if actions is None:
            self.persistent_state.current_actions = []
        elif isinstance(actions, ActionBundle):
            self.persistent_state.current_actions = [actions.id]
        else:
            raise ValueError(f"Invalid actions type. {type(actions)} : {actions}")

        # Always save the persistent state before leaving the Strategy's state machine
        self.save_persistent_state()
        return actions

    def complete(self) -> None:
        self.persistent_state.current_state = self.State.COMPLETED
        self.persistent_state.current_flowstatus = self.InternalFlowStatus.PREPARING_ACTION
        self.persistent_state.completed = True

        # Check if a teardown might be required. (before the main restart the cycle)
        self.check_teardown()

    def check_teardown(self) -> None:
        if self.config.initiate_teardown and (self.persistent_state.current_state == self.State.COMPLETED):
            self.persistent_state.current_state = self.State.TEARDOWN
            self.persistent_state.current_flowstatus = self.InternalFlowStatus.PREPARING_ACTION
            self.persistent_state.completed = False

    def log_strategy_balance_metrics(self, action_id: str):
        """Logs strategy balance metrics per action. It is called in the StrategyBase class."""
        pass
