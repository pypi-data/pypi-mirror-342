from models import (
    PersistentState,
    State,
    StrategyConfig,
    SubState,
)
from src.almanak_library.models.action_bundle import ActionBundle
from src.strategy.strategy_base import StrategyUniV3

from .states.display_message import display_message
from .states.initialization import initialization
from .states.teardown import teardown


class StrategyTutorialHelloWorld(StrategyUniV3):
    STRATEGY_NAME = "Tutorial_Hello_World"

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

        self.initialize_persistent_state()

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, chain={self.chain}, network={self.network}, protocol={self.protocol}, wallet_address={self.wallet_address}"

    @classmethod
    def get_persistent_state_model(cls):
        return PersistentState

    @classmethod
    def get_config_model(cls):
        return StrategyConfig

    def restart_cycle(self) -> None:
        """A Strategy should only be restarted when the full cycle is completed."""
        if self.persistent_state.current_state == self.State.COMPLETED:
            # Properly restart the cycle
            self.persistent_state.current_flowstatus = self.InternalFlowStatus.PREPARING_ACTION
            self.persistent_state.current_state = self.State.DISPLAY_MESSAGE
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
        if self.config.initiate_teardown and (self.persistent_state.current_state == self.State.COMPLETED or self.persistent_state.current_state == self.State.DISPLAY_MESSAGE):
            self.persistent_state.current_state = self.State.TEARDOWN
            self.persistent_state.current_flowstatus = self.InternalFlowStatus.PREPARING_ACTION

        print(self.persistent_state)

        # NOTE: Here we are cheating a little by changing the state directly from here.
        #       Usually, the state change would be handled in the state's function/file.
        actions = None
        while self.is_locked and not actions:
            match self.persistent_state.current_state:
                case State.INITIALIZATION:
                    actions = initialization(self)
                    self.persistent_state.current_state = State.DISPLAY_MESSAGE
                case State.DISPLAY_MESSAGE:
                    actions = display_message(self)
                    self.persistent_state.current_state = State.COMPLETED
                case State.COMPLETED:
                    self.complete()
                case State.TEARDOWN:
                    teardown(self)
                    self.persistent_state.current_state = State.TERMINATED
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

    def log_strategy_balance_metrics(self, action_id: str):
        """Logs strategy balance metrics per action. It is called in the StrategyBase class."""
        pass
