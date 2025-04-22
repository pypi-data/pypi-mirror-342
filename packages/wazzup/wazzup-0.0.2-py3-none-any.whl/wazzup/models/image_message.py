from dataclasses import dataclass


@dataclass
class ImageMessage:

    to: str
    image: dict[str, str]
    messaging_product: str = "whatsapp"
    recipient_type: str = "individual"
    type: str = "image"

    def __init__(self, id: str, to: str):
        """
        Args:
            message_id: The ID of the message to react to.
            emoji: The emoji to use for the image.
            to: The recipient's phone number in the format 1234567890'.
        """
        self.to = to
        self.image = {
            "id": id,
        }
