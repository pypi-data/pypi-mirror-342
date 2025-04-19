# -*- coding: utf-8 -*-
"""Client for the Koolnova REST API."""

import logging
import time
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from dateutil.parser import parse

from .exceptions import KoolnovaError
from .session import KoolnovaClientSession

_LOGGER = logging.getLogger(__name__)


class KoolnovaAPIRestClient:
    """Proxy to the Koolnova REST API."""

    def __init__(self, username: str, password: str) -> None:
        """Initialize the API and authenticate so we can make requests.

        Args:
            username: string containing your Koolnova's app username
            password: string containing your Koolnova's app password
        """
        self.username = username
        self.password = password
        self.session: Optional[KoolnovaClientSession] = None

    def _get_session(self) -> KoolnovaClientSession:
        if self.session is None:
            self.session = KoolnovaClientSession(self.username, self.password)
        return self.session

    

   

    def get_project(self) -> Dict[str, Any]:
        
        response = self._get_session().rest_request("GET", "projects")
        response.raise_for_status()
        json_resp = response.json()
        if not json_resp:
            raise KoolnovaError(
                f"Error : No data received for Koolnova by the API. "
                + "You should test on Koolnova official app. "
                + "Or perhaps API has changed :(."
            )

        #_LOGGER.debug("Réponse brute  : %s", json_resp)

        if not json_resp["data"]:
            raise KoolnovaError(
                f"Error :  No data"
                )
        projects = []
        for project in json_resp["data"]:
            _LOGGER.debug("Project Name : %s", project["name"])
            _LOGGER.debug("Topic Name : %s", project["topic"]["name"])
            projects.append({
                "Project_Name": project["name"],
                "Topic_Name": project["topic"]["name"],
                "Topic_Id": project["topic"]["id"],
                "Mode": project["topic"]["mode"],
                "is_stop": project["topic"]["is_stop"],
                "is_online": project["topic"]["is_online"],
                "eco": project["topic"]["eco"],
                "last_sync": project["topic"]["last_sync"],


            })

        return projects

    def get_sensors(self) -> Dict[str, Any]:
        
        resp = self._get_session().rest_request("GET", "topics/sensors")
        json_resp = resp.json()
        if not json_resp:
            raise KoolnovaError(
                f"Error : No data received for Koolnova by the API. "
                + "You should test on Koolnova official app. "
                + "Or perhaps API has changed :(."
            )

        #_LOGGER.debug("Réponse brute  : %s", json_resp)

        if not json_resp["data"]:
            raise KoolnovaError(
                f"Error :  No data"
                )

        rooms = []
        for room in json_resp["data"]:
            _LOGGER.debug("Room Name : %s", room["name"])
            _LOGGER.debug("Room Room_actual_temp : %s", room["temperature"])
            _LOGGER.debug("Topic Info : %s", room.get("topic_info", {}))
            # Récupérer l'id de topic_info
            topic_id = room.get("topic_info", {}).get("id", "Unknown")

            rooms.append({
                "Room_Name": room["name"],
                "Room_id": room["id"],
                "Room_status": room["status"],
                "Room_update_at": room["updated_at"],
                "Room_actual_temp": room["temperature"],
                "Room_setpoint_temp": room["setpoint_temperature"],
                "Room_speed": room["speed"],
                "Topic_id": topic_id 
            })

        return rooms
       

    def update_sensor(self, sensor_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update specific attributes for a sensor.

        Args:
            sensor_id: The ID of the sensor to update.
            payload: A dictionary containing the attributes to update and their new values.

        Returns:
            The JSON response from the API.
        """
        url = f"topics/sensors/{sensor_id}/"
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json"
        }

        # Send the PATCH request
        response = self._get_session().rest_request("PATCH", url, json=payload, headers=headers)
        response.raise_for_status()

        _LOGGER.debug("Sensor %s updated successfully with payload %s: %s", sensor_id, payload, response.json())
        return response.json()
   
    def update_project(self, topic_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update specific attributes for a project (topic).

        Args:
            topic_id: The ID of the topic/project to update.
            payload: A dictionary containing the attributes to update and their new values.

        Returns:
            The JSON response from the API.
        """
        url = f"topics/{topic_id}/"
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "accept-language": "fr"
        }

        response = self._get_session().rest_request("PATCH", url, json=payload, headers=headers)
        response.raise_for_status()

        _LOGGER.debug("Project %s updated successfully with payload %s: %s", topic_id, payload, response.json())
        return response.json()