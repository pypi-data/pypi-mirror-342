from typing import Literal

from ..._models import BaseModel
from .training_job_wandb_integration import TrainingJobWandbIntegration

__all__ = ["TrainingJobWandbIntegrationObject"]


class TrainingJobWandbIntegrationObject(BaseModel):
    type: Literal["wandb"]
    """The type of the integration being enabled for the training job"""

    wandb: TrainingJobWandbIntegration
    """The settings for your integration with Weights and Biases.

    This payload specifies the project that metrics will be sent to. Optionally, you
    can set an explicit display name for your run, add tags to your run, and set a
    default entity (team, username, etc) to be associated with your run.
    """
