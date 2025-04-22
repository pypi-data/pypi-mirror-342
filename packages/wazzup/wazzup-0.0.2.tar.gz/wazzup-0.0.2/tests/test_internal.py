from src.wazzup import models
from src.wazzup.messaging import Messaging
from src.wazzup.models import template_componenets, template_parameters


class _Test_send_text_message:
    def test_xuxa(self):
        access_token = 'EAAan7AMfBDUBO7FmdB0p7cGLh28GD1SeZBgE4PCQT3RwNIqpbPYvAFDDp2EUwdBH2LugAb9ZCWW9iRVBTV4HfKetL2Pm4h9bs5sK1eP0mnbpQem3rPsxQPcT2TI7ZBghsZCWu9OQE8egCSqPtqZATJdz9mPlc63f9NqxKquLLnwfIjEwDfLkY8gnO4WyZAFTUIuR6DoSPHN7SEkdaVvyeUrmfrNAXrlfVap3wX'
        phone_number_id = '544908905382751'
        recipient_phone_number = '5545999229802'

        template_message = models.TemplateMessage(
            to=recipient_phone_number,
            template_name='lembrete_para_rafael',
            components=[
                template_componenets.ComponentHeader(
                    parameters=[
                        template_parameters.NamedTextParameter(
                            parameter_name='user_name',
                            value='Rafael'
                        )
                    ]
                ),
                template_componenets.ComponentBody(
                    parameters=[
                        template_parameters.NamedTextParameter(
                            parameter_name='rider_name',
                            value='Joana'
                        )
                    ]
                )
            ]
        )

        messaging = Messaging(access_token, phone_number_id)

        response = messaging.send_template_message(template_message)

        assert response.status_code == 200, response.data
