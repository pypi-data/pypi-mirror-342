from typing import Literal

from ...._models import BaseModel

__all__ = ["FineTuningJobCheckpoint", "Metrics"]


class Metrics(BaseModel):
    full_valid_loss: float | None = None

    full_valid_mean_token_accuracy: float | None = None

    step: float | None = None

    train_loss: float | None = None

    train_mean_token_accuracy: float | None = None

    valid_loss: float | None = None

    valid_mean_token_accuracy: float | None = None


class FineTuningJobCheckpoint(BaseModel):
    id: str
    """The checkpoint identifier, which can be referenced in the API endpoints."""

    created_at: int
    """The Unix timestamp (in seconds) for when the checkpoint was created."""

    fine_tuned_model_checkpoint: str
    """The name of the traind checkpoint model that is created."""

    training_job_id: str
    """The name of the training job that this checkpoint was created from."""

    metrics: Metrics
    """Metrics at the step number during the training job."""

    object: Literal["training.job.checkpoint"]
    """The object type, which is always "training.job.checkpoint"."""

    step_number: int
    """The step number that the checkpoint was created at."""
