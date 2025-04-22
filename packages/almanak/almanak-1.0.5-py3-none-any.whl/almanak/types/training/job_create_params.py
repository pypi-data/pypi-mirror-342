from __future__ import annotations

from collections.abc import Iterable
from typing import Literal, Required

from typing_extensions import TypedDict

__all__ = ["JobCreateParams", "Hyperparameters", "Integration", "IntegrationWandb"]


class JobCreateParams(TypedDict, total=False):
    model: Required[str]
    """The name of the model to train.

    You can select one of the
    
    """

    training_file: Required[str]
    """The ID of an uploaded file that contains training data.

    See [upload file](https://platform.almanak.com/docs/api-reference/files/create)
    for how to upload a file.

    Your dataset must be formatted as a JSONL file. Additionally, you must upload
    your file with the purpose `train`.

    See the [training guide](https://platform.almanak.com/docs/guides/training)
    for more details.
    """

    hyperparameters: Hyperparameters
    """The hyperparameters used for the training job."""

    integrations: Iterable[Integration] | None
    """A list of integrations to enable for your training job."""

    seed: int | None
    """The seed controls the reproducibility of the job.

    Passing in the same seed and job parameters should produce the same results, but
    may differ in rare cases. If a seed is not specified, one will be generated for
    you.
    """

    suffix: str | None
    """
    A string of up to 18 characters that will be added to your traind model
    name.

    For example, a `suffix` of "custom-model-name" would produce a model name like
    `ft:gpt-3.5-turbo:almanak:custom-model-name:7p4lURel`.
    """

    validation_file: str | None
    """The ID of an uploaded file that contains validation data.

    If you provide this file, the data is used to generate validation metrics
    periodically during training. These metrics can be viewed in the training
    results file. The same data should not be present in both train and validation
    files.

    Your dataset must be formatted as a JSONL file. You must upload your file with
    the purpose `train`.

    See the [training guide](https://platform.almanak.com/docs/guides/training)
    for more details.
    """


class Hyperparameters(TypedDict, total=False):
    batch_size: Literal["auto"] | int
    """Number of examples in each batch.

    A larger batch size means that model parameters are updated less frequently, but
    with lower variance.
    """

    learning_rate_multiplier: Literal["auto"] | float
    """Scaling factor for the learning rate.

    A smaller learning rate may be useful to avoid overfitting.
    """

    n_epochs: Literal["auto"] | int
    """The number of epochs to train the model for.

    An epoch refers to one full cycle through the training dataset.
    """


class IntegrationWandb(TypedDict, total=False):
    project: Required[str]
    """The name of the project that the new run will be created under."""

    entity: str | None
    """The entity to use for the run.

    This allows you to set the team or username of the WandB user that you would
    like associated with the run. If not set, the default entity for the registered
    WandB API key is used.
    """

    name: str | None
    """A display name to set for the run.

    If not set, we will use the Job ID as the name.
    """

    tags: list[str]
    """A list of tags to be attached to the newly created run.

    These tags are passed through directly to WandB. Some default tags are generated
    by Almanak: "almanak/training", "almanak/{base-model}", "almanak/{ftjob-abcdef}".
    """


class Integration(TypedDict, total=False):
    type: Required[Literal["wandb"]]
    """The type of integration to enable.

    Currently, only "wandb" (Weights and Biases) is supported.
    """

    wandb: Required[IntegrationWandb]
    """The settings for your integration with Weights and Biases.

    This payload specifies the project that metrics will be sent to. Optionally, you
    can set an explicit display name for your run, add tags to your run, and set a
    default entity (team, username, etc) to be associated with your run.
    """
