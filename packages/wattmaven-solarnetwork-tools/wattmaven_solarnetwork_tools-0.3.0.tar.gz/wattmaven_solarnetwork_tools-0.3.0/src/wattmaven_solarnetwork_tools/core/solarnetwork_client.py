import json
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional, Union
from urllib.parse import urlencode

import requests

from wattmaven_solarnetwork_tools.core.authentication import (
    generate_auth_header,
    get_x_sn_date,
)


class HTTPMethod(Enum):
    """The available SolarNetwork API methods."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


@dataclass
class SolarNetworkCredentials:
    """Credentials for authenticating with SolarNetwork."""

    token: str
    secret: str


class SolarNetworkClient:
    """Client for interacting with the SolarNetwork API."""

    def __init__(
        self,
        host: str = "data.solarnetwork.net",
        credentials: Optional[SolarNetworkCredentials] = None,
    ):
        """
        Initialize the SolarNetwork client.

        If credentials are provided, authentication will be handled automatically.

        See https://github.com/SolarNetwork/solarnetwork/wiki/SolarNet-API-authentication-scheme-V2

        Args:
            host: The host of the SolarNetwork API
            credentials: SolarNetwork authentication credentials
        """
        self.host = host
        self.credentials = credentials
        self._session = requests.Session()

    def _prepare_request(
        self,
        method: Union[str, HTTPMethod],
        path: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        accept: Optional[str] = "application/json",
    ) -> requests.Request:
        """Prepare a request with authentication headers.

        Args:
            method: HTTP method
            path: API endpoint path
            params: Query parameters
            data: Request body data
            accept: Accept header value, defaults to application/json

        Returns:
            Prepared request
        """
        now = datetime.now(timezone.utc)
        date = get_x_sn_date(now)

        headers = {
            "accept": accept,
            "host": self.host,
            "x-sn-date": date,
        }

        method_str = method.value if isinstance(method, HTTPMethod) else method.upper()

        # Generate auth header only if credentials are provided
        if self.credentials:
            auth = generate_auth_header(
                self.credentials.token,
                self.credentials.secret,
                method_str,
                path,
                urlencode(params) if params else "",
                headers,
                json.dumps(data) if data else "",
                now,
            )
            headers["Authorization"] = auth

        if isinstance(data, dict):
            headers["Content-Type"] = "application/json"

        return requests.Request(
            method=method_str,
            url=f"https://{self.host}{path}",
            params=params,
            headers=headers,
            json=data if isinstance(data, dict) else None,
        )

    def request(
        self,
        method: Union[str, HTTPMethod],
        path: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        accept: Optional[str] = "application/json",
    ) -> requests.Response:
        """
        Make an authenticated request to the SolarNetwork API.

        Args:
            method: HTTP method
            path: API endpoint path
            params: Query parameters
            data: Request body data
            accept: Accept header value, defaults to application/json
        Returns:
            API response
        """
        request = self._prepare_request(method, path, params, data, accept)
        prepared = request.prepare()
        return self._session.send(prepared)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()
