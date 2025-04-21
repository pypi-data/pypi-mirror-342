from typing import Any

from tinyml4all.configurations.ConfigurableAttribute import ConfigurableAttribute


class Hidden(ConfigurableAttribute):
    """
    Internal state config
    """
    def __init__(self, name: str, value: Any = None, label: str = None):
        """
        Constructor
        :param name:
        :param label:
        """
        super().__init__(name, value=value, label=label)
        self.custom["hidden"] = True
