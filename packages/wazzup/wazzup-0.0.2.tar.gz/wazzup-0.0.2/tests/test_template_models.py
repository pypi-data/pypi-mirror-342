from dataclasses import asdict

from src.wazzup.models import template_componenets, template_parameters


class Test_header_template_models:
    def test_with_image_component(self):
        # Prepare
        header = template_componenets.ComponentHeader(
            parameters=[
                template_parameters.ImageParameter('image_link')
            ]
        )

        # Call
        dict_header = asdict(header)

        # Assert
        assert dict_header == {
            "type": "header",
            "parameters": [
                {
                    "type": "image",
                    "image": {
                        "link": "image_link"
                    },
                },
            ],
        }

    def test_with_text_component(self):
        # Prepare
        header = template_componenets.ComponentHeader(
            parameters=[
                template_parameters.TextParameter('my text')
            ]
        )

        # Call
        dict_header = asdict(header)

        # Assert
        assert dict_header == {
            "type": "header",
            "parameters": [
                {
                    "type": "text",
                    "text": 'my text'
                },
            ],
        }


class Test_body_template_models:
    def test_with_text_and_image_component(self):
        # Prepare
        body = template_componenets.ComponentBody(
            parameters=[
                template_parameters.TextParameter('my text'),
                template_parameters.ImageParameter('image_link'),
            ]
        )

        # Call
        dict_body = asdict(body)

        # Assert
        assert dict_body == {
            "type": "body",
            "parameters": [
                {
                    "type": "text",
                    "text": 'my text'
                },
                {
                    "type": "image",
                    "image": {
                        "link": "image_link"
                    },
                },
            ],
        }


class Test_footer_template_models:
    def test_with_text_component(self):
        # Prepare
        footer = template_componenets.ComponentFooter(
            parameters=[
                template_parameters.TextParameter('my text'),
            ]
        )

        # Call
        dict_footer = asdict(footer)

        # Assert
        assert dict_footer == {
            "type": "footer",
            "parameters": [
                {
                    "type": "text",
                    "text": 'my text'
                },
            ],
        }


class Test_button_template_models:
    def test_with_payload_component(self):
        # Prepare
        payload = template_componenets.ComponentButton(
            parameters=[
                template_parameters.PayloadParameter('my payload'),
            ]
        )

        # Call
        dict_payload = asdict(payload)

        # Assert
        assert dict_payload == {
            "type": "button",
            "sub_type": "quick_reply",
            "index": "0",
            "parameters": [
                {
                    "type": "payload",
                    "payload": "my payload",
                },
            ],
        }
