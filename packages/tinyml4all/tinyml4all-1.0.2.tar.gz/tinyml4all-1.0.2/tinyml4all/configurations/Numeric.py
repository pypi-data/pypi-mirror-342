from tinyml4all.configurations.Text import Text


class Numeric(Text):
    """
    Text value
    """
    def __init__(self, name: str, min: float|None = 0, max: float|None = None, step: float = 0.01, **kwargs):
        """"
        Constructor
        :param name:
        :param label:
        """
        super().__init__(name, **kwargs)
        self.custom.update(dtype="number", min=min, max=max, step=step)

