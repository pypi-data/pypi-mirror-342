from tinyml4all.configurations.Configuration import Configuration
from tinyml4all.tabular.features.PowerTransform import PowerTransform


class YeoJohnson(PowerTransform):
    """
    Yeo-Johnson power transformation.
    See https://en.wikipedia.org/wiki/Power_transform
    """
    def method(self) -> str:
        """

        :return:
        """
        return "yeo-johnson"

    def get_configuration(self) -> Configuration:
        """

        :return:
        """
        return Configuration(
            title="Yeo Johnson",
            description="Yeo-Johnson power transform"
        )