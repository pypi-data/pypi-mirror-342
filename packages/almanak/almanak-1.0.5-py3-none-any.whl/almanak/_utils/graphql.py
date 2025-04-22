"""
This module provides the GraphQLClient class for interacting with a GraphQL API.
"""

import json
from typing import Any

import requests

from .._exceptions import GraphQLQueryError


class GraphQLClient:
    """
    A client for interacting with a GraphQL API.
    """

    def __init__(self, url: str, jwt: str):
        """
        Initialize the GraphQLClient with the API URL and JWT.
        """
        self.url = url
        self.headers = {
            "Authorization": f"Bearer {jwt}",
            "Content-Type": "application/json",
        }

    def execute(self, query: dict, variables: dict[str, str] = None, timeout=90) -> Any:
        """
        Execute a GraphQL query.
        """
        data = {"query": query}
        if variables:
            data["variables"] = variables

        response = requests.post(self.url, headers=self.headers, data=json.dumps(data), timeout=timeout)

        if response.status_code != 200:
            raise GraphQLQueryError("GraphQL query failed")

        return response.json()
