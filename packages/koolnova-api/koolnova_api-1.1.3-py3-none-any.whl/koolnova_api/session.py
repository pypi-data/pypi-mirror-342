# -*- coding: utf-8 -*-
"""Session manager for the Koolnova REST API in order to maintain authentication token between calls."""

import logging
import json
from urllib.parse import quote_plus

from requests import Response
from requests import Session

#logging.basicConfig(level=logging.DEBUG)

from .const import KOOLNOVA_API_URL
from .const import KOOLNOVA_AUTH_URL

_LOGGER = logging.getLogger(__name__)

class KoolnovaClientSession(Session):
    """HTTP session manager for Koolnova api.

    This session object allows to manage the authentication
    in the API using a token.
    """

    host: str = KOOLNOVA_API_URL

    def __init__(self, username: str, password: str) -> None:
        """Initialize and authenticate.

        Args:
            username: the flipr registered user
            password: the flipr user's password
        """
        Session.__init__(self)

        _LOGGER.debug("Starting authentification with username '%s' and password '%s'", username, password)

        # Authenticate with user and pass and store bearer token
        #payload_token = "grant_type=password&username=" + quote_plus(username) + "&password=" + quote_plus(password)
        payload_token = json.dumps({
            "password": password,
            "email": username
        })
        _LOGGER.debug(payload_token)
        headers_token = {
            "accept":"application/json, text/plain, */*'", 
            "content-type": "application/json"   
        }
        response = super().request("POST", KOOLNOVA_AUTH_URL, data=payload_token, headers=headers_token)
        _LOGGER.debug(response)
        response.raise_for_status()

        self.bearerToken = str(response.json()["access_token"])
        _LOGGER.debug("BearerToken of authentication : %s", self.bearerToken)

    def rest_request(self, method: str, path: str, **kwargs) -> Response:
        """
        Make a request using token authentication.

        Args:
            method: HTTP method (e.g., "GET", "POST", "PATCH").
            path: Path of the REST API endpoint.
            **kwargs: Additional arguments for the request (e.g., headers, json, data).

        Returns:
            The Response object corresponding to the result of the API request.
        """
        headers_auth = {
            "Authorization": "Bearer " + self.bearerToken,
            "Cache-Control": "no-cache",
        }
        # Fusionner les headers passés en argument
        headers = kwargs.pop("headers", {})
        headers_auth.update(headers)

        response = super().request(method, f"{self.host}/{path}", headers=headers_auth, **kwargs)
        response.raise_for_status()
        return response
