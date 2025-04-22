from typing import List

from tinyml4all.configurations.ConfigurableAttribute import ConfigurableAttribute


class Configuration:
    """
    Processing block configuration
    """
    def __init__(self, title: str, description: str = ""):
        """

        :param title:
        :param description:
        """
        self.title = title
        self.description = description
