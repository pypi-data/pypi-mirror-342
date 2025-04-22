"""
This module provides the RESTClient class for interacting with RESTful APIs.
"""

import json
from typing import Any

import requests

from .._exceptions import APIStatusError


class RESTClient:
    """
    A client for interacting with RESTful APIs.
    """

    def __init__(self, base_url: str, jwt: str):
        """
        Initialize the RESTClient with the base URL and JWT.
        """
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {jwt}",
            "Content-Type": "application/json",
        }

    def get(self, endpoint: str, params: dict[str, Any] | None = None, timeout=30) -> Any:
        """
        Send a GET request to the specified endpoint.
        """
        response = requests.get(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            params=params,
            timeout=timeout,
        )

        return self._handle_response(response)

    def post(self, endpoint: str, data: dict[str, Any], timeout=30) -> Any:
        """
        Send a POST request to the specified endpoint.
        """
        response = requests.post(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            data=json.dumps(data),
            timeout=timeout,
        )
        return self._handle_response(response)

    def put(self, endpoint: str, data: dict[str, Any], timeout=30) -> Any:
        """
        Send a PUT request to the specified endpoint.
        """
        response = requests.put(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            data=json.dumps(data),
            timeout=timeout,
        )
        return self._handle_response(response)

    def delete(self, endpoint: str, timeout=30) -> Any:
        """
        Send a DELETE request to the specified endpoint.
        """
        response = requests.delete(f"{self.base_url}{endpoint}", headers=self.headers, timeout=timeout)
        return self._handle_response(response)

    def _handle_response(self, response: requests.Response) -> Any:
        """
        Handle the response, raising an error for non-success statuses.
        """
        if response.status_code not in {200, 201, 204}:
            raise APIStatusError(
                message=f"REST request failed with status {response.status_code}",
                response=response,
                body=None,
            )  # TODO: Be more specific each time with error handling

        try:
            return response
        except json.JSONDecodeError:
            return response.content
