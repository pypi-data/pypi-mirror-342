from almanak._base_client import make_request_options
from almanak._utils import maybe_transform
from almanak.pagination import SyncPage
from almanak.types.deployment import (
    Deployment as DeploymentModel,
)
from almanak.types.deployment import (
    DeploymentCreated,
    DeploymentCreateParams,
    DeploymentHeartbeat,
    DeploymentLogs,
    DeploymentMetrics,
    DeploymentStopped,
)

from .._resource import SyncAPIResource


class AgentDeployment(SyncAPIResource):
    def create_deployment(
        self,
        *,
        strategy_name: str,
        strategy_version: str,
        wallet_id: str,  # This will be an id, not the exact wallet address or EOA address
        agent_name: str,
        config: dict | None = None,
    ) -> DeploymentCreated:
        """
        Deploy a strategy to an agent on the Almanak Platform.
        """
        body = {
            "strategy_name": strategy_name,
            "strategy_version": strategy_version,
            "wallet_id": wallet_id,
            "agent_name": agent_name,
            "config": config or {},
        }

        return self._post(
            "deployments",
            body=maybe_transform(body, DeploymentCreateParams),
            options=make_request_options(),
            cast_to=DeploymentCreated,
            unpack_by_keys=["data", "create_deployment"],
        )

    def start_agent(self, agent_name: str) -> DeploymentCreated:
        """
        Start a specific deployment.
        """
        return self._post(
            f"deployments/{agent_name}/start",
            options=make_request_options(),
            cast_to=DeploymentCreated,
            unpack_by_keys=["data", "deployment_started"],
        )

    def delete_deployment(self, agent_name: str) -> DeploymentStopped:
        """
        Delete a specific deployment.
        """
        return self._delete(
            f"deployments/{agent_name}",
            options=make_request_options(),
            cast_to=DeploymentStopped,
            unpack_by_keys=["data", "deployment_stopped"],
        )

    def get_logs(self, deployment_id: str) -> DeploymentLogs:
        """
        Get logs for a specific deployment.
        Logs are from GCP
        """
        return self._get(
            f"deployments/{deployment_id}/logs",
            options=make_request_options(),
            cast_to=DeploymentLogs,
            unpack_by_keys=["data", "deployment_logs"],
        )

    def get_metrics(self, deployment_id: str) -> DeploymentMetrics:
        """
        Get metrics for a specific deployment.

        """
        return self._get(
            f"deployments/{deployment_id}/metrics",
            options=make_request_options(),
            cast_to=DeploymentMetrics,
            unpack_by_keys=["data", "deployment_metrics"],
        )

    def get_heartbeat(self, deployment_id: str) -> DeploymentHeartbeat:
        """
        Get heartbeat information for a specific deployment.
        """
        return self._get(
            f"deployments/{deployment_id}/heartbeat",
            options=make_request_options(),
            cast_to=DeploymentHeartbeat,
            unpack_by_keys=["data", "deployment_heartbeat"],
        )

    def list_deployments(self, *, limit: int = 100, offset: int = 0) -> SyncPage[DeploymentModel]:
        """
        List all deployments.
        """
        return self._get_api_list(
            "/deployments",
            page=SyncPage[DeploymentModel],
            options=make_request_options(),
            model=DeploymentModel,
            body={"limit": limit, "offset": offset},
            unpack_by_keys=["data"],
            page_key="deployments",
        )

    def stop_deployment(self, deployment_id: str) -> DeploymentStopped:
        """
        Stop a specific deployment.
        """
        return self._post(
            f"deployments/{deployment_id}/stop",
            options=make_request_options(),
            cast_to=DeploymentStopped,
            unpack_by_keys=["data", "stop_deployment"],
        )
