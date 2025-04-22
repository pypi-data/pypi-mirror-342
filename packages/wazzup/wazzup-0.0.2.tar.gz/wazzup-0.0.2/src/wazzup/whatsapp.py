from dataclasses import asdict
from urllib.parse import urljoin

import requests

from . import models


class WhatsAppDriver:
    BASE_URL = "https://graph.facebook.com/v22.0/"
    RESOURCE_PATH = "{phone_number}/messages"

    def __init__(self, access_token, phone_number_id):
        self.access_token = access_token
        self.url = urljoin(
            self.BASE_URL,
            self.RESOURCE_PATH.format(phone_number=phone_number_id),
        )

    def _get_common_headers(self) -> dict[str, str]:
        """
        Get standard headers for json response
        """
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }

        return headers

    def _make_request(
        self,
        method: str,
        url: str,
        data: dict[str, str],
    ) -> None:
        """
        Perform requests to PagBank API endpoints
        """
        headers = self._get_common_headers()
        response = requests.request(method, url, json=data, headers=headers)
        response.raise_for_status()
        return response

    def send_text_message(self, text_message: models.TextMessage):
        payload = asdict(text_message)

        response = self._make_request(
            method="POST",
            url=self.url,
            data=payload,
        )

        return response

    def reply_message(
        self,
        text_message: models.TextMessage,
        message_id,
    ):
        payload = asdict(text_message)
        payload["context"] = {"message_id": message_id}

        response = self._make_request(
            method="POST",
            url=self.url,
            data=payload,
        )

        return response

    def react_to_message(
        self,
        message_reactoin: models.MessageReaction,
    ):
        payload = asdict(message_reactoin)
        response = self._make_request(
            method="POST",
            url=self.url,
            data=payload,
        )

        return response

    def send_image_message(self, image_message: models.ImageMessage):
        payload = asdict(image_message)

        response = self._make_request(
            method="POST",
            url=self.url,
            data=payload,
        )

        return response

    def send_location_message(self, location_message: models.LocationMessage):
        payload = asdict(location_message)

        response = self._make_request(
            method="POST",
            url=self.url,
            data=payload,
        )

        return response

    def send_template_message(self, template: models.TemplateMessage):
        payload = asdict(template)

        response = self._make_request(
            method="POST",
            url=self.url,
            data=payload,
        )

        return response
