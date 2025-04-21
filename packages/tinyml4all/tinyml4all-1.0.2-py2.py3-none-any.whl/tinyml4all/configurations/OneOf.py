from typing import List, Tuple, Any

from tinyml4all.configurations.ConfigurableAttribute import ConfigurableAttribute


class OneOf(ConfigurableAttribute):
    """
    Array configuration (single choice)
    """
    def __init__(self, name: str, options: List[str|Tuple[str, str]], **kwargs):
        """

        :param name:
        :param options:
        :param label:
        """
        super().__init__(name, **kwargs)
        self.custom["options"] = self.format_options(options)

    def format_options(self, options: List[str|Tuple[str, str]]) -> List[dict]:
        """
        Format options
        :param options:
        :return:
        """
        options = [(opt, opt) if isinstance(opt, str) else opt for opt in options]

        return [{"label": label, "value": value} for value, label in options]