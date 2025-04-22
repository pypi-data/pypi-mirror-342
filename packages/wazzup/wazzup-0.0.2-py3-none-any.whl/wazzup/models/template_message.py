from dataclasses import asdict, dataclass

from .template_componenets import TemplateComponent


@dataclass
class TemplateMessage:
    to: str
    template: dict[str, str]
    messaging_product: str = "whatsapp"
    type: str = "template"

    def __init__(
        self,
        to: str,
        template_name: str,
        components: list[TemplateComponent],
    ):
        self.to = to
        self.template = {
            'name': template_name,
            "language": {"code": "pt_BR"},
            'components': [asdict(component) for component in components]
        }
