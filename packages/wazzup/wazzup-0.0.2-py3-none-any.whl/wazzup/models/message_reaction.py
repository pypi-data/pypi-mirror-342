from dataclasses import dataclass


@dataclass
class MessageReaction:

    to: str
    reaction: dict[str, str]
    messaging_product: str = "whatsapp"
    recipient_type: str = "individual"
    type: str = "reaction"

    def __init__(self, message_id: str, emoji, to: str):
        """
        Args:
            message_id: The ID of the message to react to.
            emoji: The emoji to use for the reaction.
            to: The recipient's phone number in the format 1234567890'.
        """
        self.to = to
        self.reaction = {
            "message_id": message_id,
            "emoji": emoji,
        }
