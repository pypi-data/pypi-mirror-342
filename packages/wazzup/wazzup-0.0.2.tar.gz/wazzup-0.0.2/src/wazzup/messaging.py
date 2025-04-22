from . import models
from .whatsapp import WhatsAppDriver


class Messaging:
    def __init__(self, access_token, phone_number_id):
        self.whatsapp_driver = WhatsAppDriver(access_token, phone_number_id)

    def send_text_message(self, text_message: 'models.TextMessage'):
        """
        Send a text message using the WhatsApp API
        """
        response = self.whatsapp_driver.send_text_message(
            text_message=text_message,
        )

        return response

    def reply_message(
        self,
        text_message: models.TextMessage,
        message_id,
    ):
        """
        Reply to a message using the WhatsApp API
        """
        response = self.whatsapp_driver.reply_message(text_message, message_id)

        return response

    def react_to_message(
        self,
        message_reaction: models.MessageReaction,
    ):
        """
        React to a message using the WhatsApp API
        """
        response = self.whatsapp_driver.react_to_message(message_reaction)

        return response

    def send_image_message(self, image_message: models.ImageMessage):
        """
        Send an image message using the WhatsApp API
        """
        response = self.whatsapp_driver.send_image_message(image_message)

        return response

    def send_location_message(self, location_message: models.LocationMessage):
        response = self.whatsapp_driver.send_location_message(location_message)

        return response

    def send_template_message(self, template: models.TemplateMessage):
        """
        Send a template message using the WhatsApp API

        :param recipient_phone_number: The phone number of the recipient.
        :param template_name: The name of the template to be sent.
        """
        response = self.whatsapp_driver.send_template_message(template)

        return response
