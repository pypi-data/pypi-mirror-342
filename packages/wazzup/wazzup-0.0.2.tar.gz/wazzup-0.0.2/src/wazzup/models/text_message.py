from dataclasses import dataclass


@dataclass
class TextMessage:
    """
    Represents a text message in the WhatsApp application

    Attributes:
        sender (str): The sender of the message.
        recipient (str): The recipient of the message.
        content (str): The content of the message.
        timestamp (str): The time when the message was sent.
    """

    to: str
    text: dict[str, str]
    messaging_product: str = "whatsapp"
    recipient_type: str = "individual"
    type: str = "text"

    def __init__(self, message_content: str, to: str):
        """
        Args:
            message_content: The content of the message.
            to: The recipient of the message.
        """
        self.to = to
        self.text = {
            'preview_url': False,
            'body': message_content
        }
