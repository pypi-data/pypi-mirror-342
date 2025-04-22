from dataclasses import dataclass


@dataclass
class LocationMessage:

    to: str
    location: dict[str, str]
    messaging_product: str = "whatsapp"
    type: str = "location"

    def __init__(
        self,
        to: str,
        longitude: str,
        latitude: str,
        name: str,
        address: str,
    ):
        """
        Args:
            message_id: The ID of the message to react to.
            emoji: The emoji to use for the image.
            to: The recipient's phone number in the format 1234567890'.
        """
        self.to = to
        self.location = {
            'latitude': latitude,
            'longitude': longitude,
            'name': name,
            'address': address,
        }
