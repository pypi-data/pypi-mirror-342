import json
from dataclasses import asdict, dataclass

from almanak._hasura import HasuraClient


@dataclass
class RequestMixin:
    @classmethod
    def from_request(cls, request):
        values = request.get("input")
        return cls(**values)

    def to_json(self):
        return json.dumps(asdict(self))


@dataclass
class ModelTrainingInput(RequestMixin):
    gcs_directory: str
    setup_command: str | None
    run_command: str | None


@dataclass
class ModelTrainingKafkaResponse(RequestMixin):
    response: str


@dataclass
class Mutation(RequestMixin):
    createModelTrainingRun: ModelTrainingKafkaResponse | None


@dataclass
class createModelTrainingRunArgs(RequestMixin):
    modelTrainingInput: ModelTrainingInput


def create_model_training(
    hasura_client: HasuraClient,
    gcs_directory: str,
    setup_command: str | None,
    run_command: str | None,
):
    query = """
        mutation CreateModelTrainingRun($modelTrainingInput: model_training_input_insert_input = {}) {
            createModelTrainingRun(object: $modelTrainingInput) {
                response
            }
        }
    """
    response = hasura_client.graphql_client.execute(
        query,
        {"modelTrainingInput": ModelTrainingInput(gcs_directory, setup_command, run_command).to_json()},
    )

    if response.get("errors"):
        raise ValueError(response.get("errors"))

    if response == "200":
        return

    raise RuntimeError(f"Failed to create model training run: {response}")
