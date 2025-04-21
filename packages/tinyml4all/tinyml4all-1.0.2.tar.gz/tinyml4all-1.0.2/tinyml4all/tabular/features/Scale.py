from typing import Self, Literal, List

import numpy as np

from tinyml4all.configurations.ConfigurableAttribute import ConfigurableAttribute
from tinyml4all.configurations.Configuration import Configuration
from tinyml4all.configurations.Hidden import Hidden
from tinyml4all.configurations.OneOf import OneOf
from tinyml4all.support import numeric
from tinyml4all.tabular.ProcessingBlock import ProcessingBlock


class Scale(ProcessingBlock):
    """
    Apply feature scaling
    """
    def __init__(
            self,
            method: Literal["minmax", "zscore", "maxabs", "robust", "l1", "l2", "l-max"] = "robust",
            **kwargs):
        """
        Constructor

        :param method: scaling method
        """
        super().__init__()

        self.method = method.lower().replace("norm", "").strip()
        self.offsets = None
        self.scales = None

    def __str__(self) -> str:
        """
        Get string representation
        :return:
        """
        if self.offsets is not None:
            return f"Scale(method={self.method}, offsets={self.offsets}, scales={self.scales})"

        return f"Scale(method={self.method})"

    def fit(self, dataset, *args, **kwargs) -> Self:
        """
        Fit
        :param dataset:
        :param args:
        :param kwargs:
        :return:
        """
        df = self.remember_working_variables(numeric(dataset.df))
        X = df.to_numpy()

        match self.method:
            case "zscore":
                self.offsets = X.mean(axis=0)
                self.scales = X.std(axis=0)
            case "minmax":
                self.offsets = X.min(axis=0)
                self.scales = X.max(axis=0) - self.offsets
            case "maxabs":
                self.offsets = np.zeros(X.shape[1])
                self.scales = np.abs(X).max(axis=0)
            case "robust":
                self.offsets = np.median(X, axis=0)
                self.scales = np.percentile(X, 75, axis=0) - np.percentile(X, 25, axis=0)
            case "l1" | "l2" | "l-max":
                # nothing to learn
                pass

        return self

    def transform(self, dataset, *args, **kwargs) -> dict:
        """
        Apply scaling

        :param dataset:
        :param args:
        :param kwargs:
        :return:
        """
        df = dataset.df
        working_columns = [var.name for var in self.working_dtypes]

        if self.scales is not None:
            for var, scale, offset in zip(self.working_dtypes, self.scales, self.offsets):
                df[var.name] = (df[var.name] - offset) / scale
        elif self.method == "l1":
            df[working_columns] = df[working_columns].apply(lambda x: x / x.sum(), axis=1)
        elif self.method == "l2":
            df[working_columns] = df[working_columns].apply(lambda x: x / np.sqrt(np.square(x).sum()), axis=1)
        elif self.method == "l-max":
            df[working_columns] = df[working_columns].apply(lambda x: x / np.abs(x).max(), axis=1)

        return {"df": df}

    def get_configuration(self) -> Configuration:
        """
        Get base configuration
        :return:
        """
        return Configuration(
            title="Scale",
            description="Apply feature scaling"
        )

    def get_configurables(self) -> List[ConfigurableAttribute]:
        """
        Get configurable options
        :return:
        """
        methods = ["MinMax", "ZScore", "MaxAbs", "Robust", "L1 Norm", "L2 Norm", "L-Max Norm"]
        method_options = [(method.lower(), method) for method in methods]

        return [
            OneOf(
                name="method",
                value=self.method,
                options=method_options),
            Hidden(name="offsets", value=self.offsets),
            Hidden(name="scales", value=self.scales)
        ]

    @classmethod
    def hydrate_from_dict(cls, attributes: dict) -> Self:
        """
        Convert attributes dict to object
        :param attributes:
        :return:
        """
        instance = cls(method=attributes["method"]["value"])

        if (offsets := attributes.get("offsets", {}).get("value", "")) != "":
            instance.offsets = np.asarray(offsets)

        if (scales := attributes.get("scales", {}).get("value", "")) != "":
            instance.scales = np.asarray(scales)

        return instance