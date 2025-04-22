"""
This module provides the HasuraClient class for interacting with the Almanak API.
"""

import logging
import time

import jwt
import requests

from ._utils.graphql import GraphQLClient
from ._utils.rest import RESTClient


class HasuraClient:
    """
    A client for interacting with the Almanak API.
    """

    graphql_client = GraphQLClient
    restful_client = RESTClient
    user_id = None
    team_id = None
    organisation_id = None
    api_key = None

    def __init__(self, graph_api_url, rest_api_url, platform_jwt):
        # Decode the JWT here
        try:
            decoded_jwt = jwt.decode(platform_jwt, options={"verify_signature": False})  # Assuming api_key is the JWT
            # check if JWT expired
            # if expired, throw error
            if decoded_jwt.get("exp") < time.time():
                raise jwt.exceptions.ExpiredSignatureError
            iss = decoded_jwt.get("iss")

            self.restful_client = RESTClient(rest_api_url, platform_jwt)
            self.check_jwt()

            self.graphql_client = GraphQLClient(graph_api_url, platform_jwt)
            if iss == "almanak-platform":
                self.api_key = decoded_jwt.get("apiKey")
                self.get_user_id()
            else:
                # Extract the hasura claims
                hasura_claims = decoded_jwt.get("https://hasura.io/jwt/claims")
                if hasura_claims:
                    # Extract the x-hasura-user-platform-id
                    self.user_id = hasura_claims.get("x-hasura-user-platform-id")
        except jwt.exceptions.ExpiredSignatureError:
            raise  # Reraise this error unchanged.
        except jwt.InvalidTokenError as exc:
            # Handle the error (e.g., invalid token)
            # return error
            raise ValueError("Invalid token, please re-authenticate") from exc

        # next time, else use the api key to get the user id, team id and organisation id
        # set the user id, team id and organisation id
        self.get_user_team()
        self.logger = logging.getLogger(__name__)

    def upload_zip_to_gcs(self, signed_url, file_path):
        """
        Uploads a ZIP file to Google Cloud Storage using a signed URL.

        Parameters:
            signed_url (str): The signed URL to which the file will be uploaded.
            file_path (str): The local path to the ZIP file that needs to be uploaded.

        Returns:
            bool: True if the upload was successful, False otherwise.
        """
        # Open the file in binary read mode
        with open(file_path, "rb") as file:
            headers = {"Content-Type": "application/octet-stream"}

            # POST request to upload the file
            response = requests.put(signed_url, data=file, headers=headers, timeout=180)

            # Check if the upload was successful
            if response.status_code == 200:
                print("File uploaded successfully.")
                return True
            else:
                print(f"Failed to upload file. Status code: {response.status_code}, Response: {response.text}")
                return False

    def check_jwt(self):
        """
        Check if the JWT is valid by calling auth service with the JWT
        """
        try:
            response: requests.Response = self.restful_client.post("/auth/check-jwt", None)
            if response.status_code == 200:
                logging.debug("JWT is valid.")
                return response
            else:
                logging.warning(f"Authentication failed with status code: {response.status_code}")
                return None

        except Exception as e:
            logging.error("Error checking JWT", exc_info=True)
            raise ValueError("Invalid token, please re-authenticate or get new token.") from e

    def get_user_id(self):
        """
        Get the user id from api_key object the graphql client
        """
        user_query = """
            query getUserApiKey($api_key: String) { 
            user_api_key(where: {api_key: {_eq: $api_key}}) {
            user_id
            created_at
            api_key
            active
            }
        }
        """
        response = self.graphql_client.execute(user_query, {"api_key": self.api_key})
        # print(response)
        self.user_id = response["data"]["user_api_key"][0]["user_id"]

        return response

    def get_user_team(self):
        """
        Get the user id, team id and organisation id from the graphql client
        """
        user_query = """
            query getUserTeam($userId: String) {
            user_team(where: {user_id: {_eq: $userId}}) {
                organisation_id
                team_id
                user {
                email
                notification_email
                }
                role
            }
            }

        """
        response = self.graphql_client.execute(user_query, {"userId": self.user_id})
        # print(response)
        self.team_id = response["data"]["user_team"][0]["team_id"]
        self.organisation_id = response["data"]["user_team"][0]["organisation_id"]
        return response

    def start_mc_simulation(self, group_simulation_id):
        start_query = """
        mutation StartGroupSimulation($simulationId: String!) {
            startGroupSimulation(arg1: {group_simulation_id: $simulationId, version:3}) {
              message
              valid,
            }
        }
        """
        start_query_response = self.graphql_client.execute(start_query, {"simulationId": group_simulation_id}, 300)

        if start_query_response["data"]["startGroupSimulation"]["valid"]:
            print("Simulation started successfully")
        else:
            print("Simulation failed to start")
            raise ValueError("Simulation failed to start: " + start_query_response["data"]["startGroupSimulation"]["message"])
        return group_simulation_id

    def validate_mc(self, group_simulation_id):
        start_query = """
        mutation MyMutation($simulationId: String!) {
            unzipValidateSimulationConfig(arg1: {group_simulation_id: $simulationId}) {
              message
              valid
              error
            }
        }
        """
        start_query_response = self.graphql_client.execute(start_query, {"simulationId": group_simulation_id})

        if start_query_response["data"]["unzipValidateSimulationConfig"]["valid"]:
            print("Simulation validated successfully")
        else:
            print("Simulation validation failed")
            print(start_query_response["data"]["unzipValidateSimulationConfig"]["message"])
            # do not raise error here, return the response to the user
        return start_query_response["data"]["unzipValidateSimulationConfig"]

    def generate_upload_link(self, group_simulation_id):
        query = """
            mutation GenerateUploadLink($id: String!) {
                generateGroupSimulationConfigUrl(arg1: {group_simulation_id: $id}) {
                    message
                    signed_url
                    valid
                }
            }
        """
        try:
            response = self.graphql_client.execute(query, {"id": group_simulation_id})
            data = response["data"]["generateGroupSimulationConfigUrl"]
            if data["valid"]:
                self.logger.info("Upload link generated successfully")
                return data["signed_url"]
            else:
                self.logger.error(f"Upload link generation failed: {data['message']}")
                raise ValueError(f"Upload link generation failed({group_simulation_id}): {data['message']}")
        except Exception as e:
            self.logger.error(f"Failed to generate upload link: {str(e)}")
            raise

    def create_mc_simulation_get_upload_link(self):
        """Creates a group simulation and generates an upload link."""

        update_payload = {
            "team_id": self.team_id,
            "organisation_id": self.organisation_id,
            "created_by": self.user_id,
            "status": "pending",
            "created_at": "now()",
            "description": "MC Simulation from CLI",
        }
        # create a group simulation via grapohql with the correct data
        query = """
            mutation CreateGroupSimulation($payload: group_simulations_insert_input = {}) {
                insert_group_simulations_one(object: $payload) {
                  id
                  created_at
                  status
                }
            }

        """
        response = self.graphql_client.execute(query, {"payload": update_payload})
        # print(response)
        group_simulation_id = response["data"]["insert_group_simulations_one"]["id"]
        # print(group_simulation_id + " is the group simulation id")

        # generate the upload link
        upload_link = self.generate_upload_link(group_simulation_id)
        return {"monte_carlo_id": group_simulation_id, "upload_link": upload_link}

    def get_simulation_status(self, group_simulation_id):
        query = """
            query GetGroupSimulationStatus($group_simulation_id: String!) {
                group_simulations_by_pk(id: $group_simulation_id) {
                    id
                    created_at
                    status
                }
            }
        """
        try:
            response = self.graphql_client.execute(query, {"group_simulation_id": group_simulation_id})
            return response
        except Exception as e:
            self.logger.error(f"Failed to get simulation status: {str(e)}")
            raise

    def get_mc_simulation_results(self, group_simulation_id):
        """get the results of the simulation"""
        query = """
            query GetGroupSimulationResults($group_simulation_id: String!) {
                group_simulations_by_pk(id: $group_simulation_id) {
                  id
                  created_at
                  status
                  results
                }
            }
        """
        response = self.graphql_client.execute(query, {"group_simulation_id": group_simulation_id})
        return response

    def get_mc_simulations_raw_metrics_gcs_uri(self, group_simulation_id):
        """get the raw metrics of the simulation"""
        query = """
          query MyQuery3($group_simulation_id: String!) {
            getRawSimulationMetricsURL(group_simulation_id: $group_simulation_id) {
              message
              valid
              data {
                data_uri
                simulation_id
                url
              }
            }
          }
        """
        response = self.graphql_client.execute(query, {"group_simulation_id": group_simulation_id})
        return response

    def generate_price_data_async(self, price_configs):
        """generate price data"""
        query = """
          mutation GeneratePriceData($price_configs: [price_configs_insert_input!]!) {
            generatePriceData(price_configs: $price_configs) {
              message
              valid
            }
          }
        """
        response = self.graphql_client.execute(query, {"price_configs": price_configs})
        return response

    def generate_sign_url_for_agent(self, agent_id: str):
        """generate signed url for agent"""
        query = """
          mutation GenerateSignUrlForAgent($agent_id: String!) {
            generateSignUrlForAgent(arg1: {agentId: $agent_id}) {
              message
              valid
              read_gcs_uri
              write_gcs_uri
            }
          }
        """
        return self.graphql_client.execute(query, {"agent_id": agent_id})

    def list_live_agents(self):
        """list live agents"""
        query = """
            query LiveAgents($user_id: String!) {
                live_agent(where: {user_id: {_eq: $user_id}}){
                    id
                    name
                    environment_metadata
                    user_id
                    config
                    status
                    strategy_version
                    updated_at
                }
            }
        """
        response = self.graphql_client.execute(query, {"user_id": self.user_id})
        return response

    def generate_strategy_download(self, strategy_name: str, version: str):
        """generate strategy download urls"""
        query = """
          mutation GenerateStrategyDownloadURL($strategy_name: String!, $version: String!) {
            generateStrategyDownloadUrl(strategyName: $strategy_name, version: $version) {
              files {
                presigned_url
                relative_path
              }
            }
          }
        """
        return self.graphql_client.execute(query, {"strategy_name": strategy_name, "version": version})

    def generate_strategy_download_by_strategy_id(self, strategy_id: str, version_id: str):
        """generate strategy download urls"""
        query = """
          query GenerateStrategyDownloadURL($artifactId: String!, $versionId: String!) {
            generateArtifactFilesDownloadUrl(artifactId: $artifactId, versionId: $versionId) {
              files
            }
          }
        """
        return self.graphql_client.execute(query, {"artifactId": strategy_id, "versionId": version_id})

    def generate_strategy_version_id_upload_url(self, strategy_id: str, files: list[str]):
        """generate strategy version id upload urls"""
        query = """
          mutation GenerateStrategyVersionIdUploadUrl($strategyId: String!, $files: [String!]!) {
            generateStrategyVersionIdUploadUrl(strategyId: $strategyId, files: $files) {
              success
              rootUri
              version
              versionId
              urls {
                presigned_url
                relative_path
              }
            }
          }
        """
        return self.graphql_client.execute(query, {"strategyId": strategy_id, "files": files})

    def trigger_scan(self, artifact_version_id: str):
        """trigger security scan"""
        query = """
          mutation ScanArtifactVersion($artifactVersionId: String!) {
            scanArtifactVersion(arg1: {artifactVersionId: $artifactVersionId}) {
              message
              success
            }
          }
        """
        return self.graphql_client.execute(query, {"artifactVersionId": artifact_version_id})

    def get_version_id_by_name(self, strategy_id: str, version: str):
        """get version id by version name and strategy id"""
        query = """
          query GetVersionId($strategyId: uuid!, $version: String!) {
            artifact_id_version(where: {name: {_eq: $version}, artifact_id_fk: {_eq: $strategyId}}) {
                id
            }
          }
        """
        return self.graphql_client.execute(query, {"strategyId": strategy_id, "version": version})

    def update_strategy_version(self, strategy_id: str, version_id: str, metadata: dict, description: str):
        """update strategy version"""
        query = """
          mutation UpdateStrategyVersion($strategyId: uuid!, $versionId: uuid!, $metadata: jsonb!, $description: String!) {
            update_artifact_id_version(where: {id: {_eq: $versionId}, _and: {artifact_id_fk: {_eq: $strategyId}}}, _set: {metadata: $metadata, description: $description}) {
                __typename
            }
          }
        """
        return self.graphql_client.execute(query, {"strategyId": strategy_id, "versionId": version_id, "metadata": metadata, "description": description})
