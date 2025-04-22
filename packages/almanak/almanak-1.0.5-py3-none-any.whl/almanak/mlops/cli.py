from pathlib import Path

import click

from almanak.mlops.train._hasura import create_model_training
from almanak.mlops.train._upload_training_artifacts_to_gcs import (
    upload_training_artifacts,
)


@click.command()
@click.option(
    "--artifact-dir",
    default=None,
    help="The directory of training artifacts to upload.",
)
@click.option(
    "--setup-command",
    default=None,
    help="The command to run before training.",
)
@click.option(
    "--run-command",
    default=None,
    help="The command to run to start training.",
)
def train_model(artifact_dir, setup_command, run_command):
    from almanak.hasura import HasuraClient

    if artifact_dir is None:
        click.echo("No artifact directory provided, uploading current directory.")
        artifact_dir = Path(".")
    gcs_directory = upload_training_artifacts(Path(artifact_dir))
    print("Uploaded artifacts")

    model_training_args = {
        "hasura_client": HasuraClient(),
        "gcs_directory": gcs_directory,
    }
    if setup_command:
        model_training_args["setup_command"] = setup_command
    if run_command:
        model_training_args["run_command"] = run_command
    create_model_training(**model_training_args)
