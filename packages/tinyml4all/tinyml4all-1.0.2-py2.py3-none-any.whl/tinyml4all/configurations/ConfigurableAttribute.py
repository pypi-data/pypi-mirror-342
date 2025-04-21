from typing import Any

from tinyml4all.transpile.Jsonable import Jsonable
from tinyml4all.transpile.jinja.JSONEncoder import JSONEncoder


class ConfigurableAttribute(Jsonable):
    """
    An attribute that can be configured
    """
    def __init__(
            self,
            name: str,
            value: Any = None,
            label: str = None,
            description: str = None,
            warning: str = None
    ):
        """
        Constructor
        :param name:
        :param label:
        """
        self.type = self.__class__.__name__
        self.name = name
        self.description = description
        self.warning = warning
        self.value = value
        self.label = label or (name[0].upper() + name[1:])
        self.custom = {}

    def to_json(self) -> dict:
        """
        Convert to JSON
        :return:
        """
        return {
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "warning": self.warning,
            "label": self.label,
            "value": JSONEncoder().eval(self.value),
            **self.custom
        }