from ..._models import BaseModel

__all__ = ["TrainingJobWandbIntegration"]


class TrainingJobWandbIntegration(BaseModel):
    project: str
    """The name of the project that the new run will be created under."""

    entity: str | None = None
    """The entity to use for the run.

    This allows you to set the team or username of the WandB user that you would
    like associated with the run. If not set, the default entity for the registered
    WandB API key is used.
    """

    name: str | None = None
    """A display name to set for the run.

    If not set, we will use the Job ID as the name.
    """

    tags: list[str] | None = None
    """A list of tags to be attached to the newly created run.

    These tags are passed through directly to WandB. Some default tags are generated
    by Almanak: "almanak/training", "almanak/{base-model}", "almanak/{ftjob-abcdef}".
    """
