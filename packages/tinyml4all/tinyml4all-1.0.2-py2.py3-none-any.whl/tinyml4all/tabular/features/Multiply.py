from itertools import combinations
from typing import List, Literal, Self

import numpy as np

from tinyml4all.configurations.AnyOf import AnyOf
from tinyml4all.configurations.ConfigurableAttribute import ConfigurableAttribute
from tinyml4all.configurations.Configuration import Configuration
from tinyml4all.support import numeric
from tinyml4all.support.types import ArrayOfStrings, as_list_of_strings, coalesce, TemplateDef
from tinyml4all.support.userwarn import userwarn
from tinyml4all.tabular.ProcessingBlock import ProcessingBlock


class Multiply(ProcessingBlock):
    """
    Polynomial (2) features expansion
    """
    def __init__(self, columns: ArrayOfStrings = None,):
        """

        :param columns:
        """
        super().__init__()
        self.columns = as_list_of_strings(columns)

    def __str__(self) -> str:
        """

        :return:
        """
        return f"Multiply(columns={coalesce(self.columns, 'ALL')})"

    @property
    def get_template(self) -> TemplateDef:
        return {
            "columns": self.columns,
        }

    def fit(self, dataset, **kwargs) -> Self:
        """
        Fit
        :param dataset:
        :return:
        """
        df = self.remember_working_variables(numeric(dataset.df))
        self.columns = coalesce(self.columns, df.columns)

        return self

    def transform(self, dataset, **kwargs) -> dict:
        """
        Apply combinatorial multiplication

        :param dataset
        :return:
        """
        df = dataset.df.copy()

        # self multiply
        for col in self.columns:
            df[f"{col}_x_{col}"] = df[col].to_numpy() * df[col].to_numpy()

        for a, b in combinations(self.columns, 2):
            df[f"{a}_x_{b}"] = df[a].to_numpy() * df[b].to_numpy()

        return {"df": df}

    def get_configuration(self) -> Configuration:
        """
        Get base configuration
        :return:
        """
        return Configuration(
            title="Multiply",
            description="Multiply columns by each other"
        )

    def get_configurables(self) -> List[ConfigurableAttribute]:
        """
        Get configurable options
        :return:
        """
        return [
            AnyOf(
                name="columns",
                value=self.columns,
                options=self.all_columns
            )
        ]

    @classmethod
    def hydrate_from_dict(cls, attributes: dict) -> Self:
        """
        Convert attributes dict to object
        """
        columns = attributes.get("columns", {}).get("value", [])

        return cls(columns=columns)
