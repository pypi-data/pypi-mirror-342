from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING

import urllib3
import urllib3.util

if TYPE_CHECKING:
    from ..._client import Almanak

from ..._resource import SyncAPIResource

__all__ = ["Agent"]


class Agent(SyncAPIResource):
    _client: Almanak

    def download_state(
        self,
        agent_id: str,
        output_dir: str,
    ) -> str | None:
        response = self._client._hasura_client.generate_sign_url_for_agent(agent_id)
        if "errors" in response:
            raise Exception(response["errors"])

        gcs_uris: list[str] = response["data"]["generateSignUrlForAgent"]["read_gcs_uri"]
        if len(gcs_uris) == 0:
            return None

        folder_dir = output_dir
        if output_dir == ".":
            folder_dir = os.path.join(output_dir, f"almanak-agent-{agent_id[0:5]}")

        for gcs in gcs_uris:
            result = self._get(gcs, cast_to=str)

            gcs_url = urllib3.util.parse_url(gcs)
            file_path = "/".join(gcs_url.path.split("/")[4:])

            full_path = os.path.join(folder_dir, file_path)

            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            result_json = json.loads(result)
            with open(full_path, "w") as f:
                f.write(json.dumps(result_json, indent=4))

        return os.path.abspath(folder_dir)

    def update_state(
        self,
        agent_id: str,
        persistent_state,
        config,
    ) -> dict:
        response = self._client._hasura_client.generate_sign_url_for_agent(agent_id)
        gcs_uris: list[str] = response["data"]["generateSignUrlForAgent"]["write_gcs_uri"]

        for gcs in gcs_uris:
            gcs_url = urllib3.util.parse_url(gcs)
            file_path = "/".join(gcs_url.path.split("/")[4:])

            if file_path.endswith("persistent_state.json") and persistent_state:
                with open(persistent_state) as f:
                    persistent_state_raw = f.read()
                    persistent_state_json = json.loads(persistent_state_raw)
                    self._put(gcs, body=persistent_state_json, cast_to=str)

            if file_path.endswith("config.json") and config:
                with open(config) as f:
                    config_raw = f.read()
                    config_json = json.loads(config_raw)
                    self._put(gcs, body=config_json, cast_to=str)

    def list(self):
        response = self._client._hasura_client.list_live_agents()

        if "errors" in response:
            raise Exception(response["errors"])
        return response["data"]["live_agent"]
