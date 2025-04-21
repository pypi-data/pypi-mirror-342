from typing import List, Self

from tinyml4all.configurations.ConfigurableAttribute import ConfigurableAttribute
from tinyml4all.configurations.Configuration import Configuration
from tinyml4all.support import override
from tinyml4all.support.types import ArrayOfStrings


class Configurable:
    """
    Interface for configurable objects
    """
    @classmethod
    def hydrate(cls, block: dict) -> Self:
        """
        Convert JSON representation to object
        :param block:
        :return:
        """
        assert "attributes" in block, "Missing attributes"
        # convert list of attributes into dict for easier access
        attributes = {attr["name"]: attr for attr in block["attributes"]}

        return cls.hydrate_from_dict(attributes)

    @classmethod
    def hydrate_from_dict(cls, attributes: dict) -> Self:
        """
        Convert attributes dict to object
        :param attributes:
        :return:
        """
        override(cls)

    def get_configuration(self) -> Configuration:
        """
        Get base configuration
        :return:
        """
        override(self)

    def get_configurables(self) -> List[ConfigurableAttribute]:
        """
        Get configurable options
        :return:
        """
        override(self)

    def to_config(self) -> dict:
        """

        :return:
        """
        conf = self.get_configuration()
        attributes = self.get_configurables()

        return {
            "type": f"{self.__class__.__module__}.{self.__class__.__name__}",
            "info": {
                "title": conf.title,
                "description": conf.description
            },
            "attributes": [attr.to_json() for attr in attributes]
        }