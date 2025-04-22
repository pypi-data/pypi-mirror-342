from typing import List, Literal, Self

import numpy as np

from tinyml4all.configurations.AnyOf import AnyOf
from tinyml4all.configurations.ConfigurableAttribute import ConfigurableAttribute
from tinyml4all.configurations.Configuration import Configuration
from tinyml4all.support import numeric
from tinyml4all.support.types import ArrayOfStrings, as_list_of_strings, coalesce, TemplateDef
from tinyml4all.support.userwarn import userwarn
from tinyml4all.tabular.ProcessingBlock import ProcessingBlock


class Monotonic(ProcessingBlock):
    """
    Apply monotonic functions to inputs
    (power, exp, log, ...)
    """
    def __init__(
            self,
            columns: ArrayOfStrings = None,
            functions: ArrayOfStrings | List[
                Literal["square", "cube", "sqrt", "inverse", "log", "exp"]
            ] = None,
    ):
        """

        :param columns:
        :param functions:
        """
        super().__init__()

        self.all_columns = None
        self.columns = as_list_of_strings(columns)
        self.functions = as_list_of_strings(coalesce(functions, self.available_functions))

        if (unknown := set(self.functions) - set(self.available_functions)) and len(unknown) > 0:
            raise ValueError(f"Unknown function(s): {unknown}")

    def __str__(self) -> str:
        """

        :return:
        """
        return f"Monotonic(columns={coalesce(self.columns, 'ALL')} functions={self.functions})"

    @property
    def available_functions(self) -> List[str]:
        """
        Get list of supported functions
        :return:
        """
        return ["square", "cube", "sqrt", "inverse", "log", "exp"]

    def get_template(self) -> TemplateDef:
        return {
            "columns": self.columns,
            "functions": self.functions
        }

    def fit(self, dataset, **kwargs) -> Self:
        """
        Fit
        :param dataset:
        :return:
        """
        df = self.remember_working_variables(numeric(dataset.df))
        self.all_columns = df.columns.tolist()
        self.columns = [col for col in coalesce(self.columns, df.columns)]

        # warn user of potential overflow for exp
        if "exp" in self.functions:
            for col in self.columns:
                if np.max(np.abs(df[col].to_numpy())) > 30:
                    userwarn(f"exp({col}) will likely cause overflow on embedded hardware. Consider scaling your features first!")

        return self

    def transform(self, dataset, **kwargs) -> dict:
        """
        Apply functions

        :param dataset
        :return:
        """
        df = dataset.df.copy()

        for col in self.columns:
            series = df[col].to_numpy()

            for fn in self.functions:
                with np.errstate(divide="ignore", invalid="ignore"):
                    match fn:
                        case "square":
                            values = series ** 2
                        case "cube":
                            values = series ** 3
                        case "sqrt":
                            values = np.sqrt(np.abs(series))
                        case "inverse":
                            values = np.nan_to_num(1 / series, nan=series, posinf=series, neginf=series)
                        case "log":
                            values = np.log(np.abs(series) + 1)
                        case "exp":
                            values = np.where(np.abs(series) < 30, np.exp(series), 0)
                        case _:
                            raise ValueError(f"Unknown function {fn}")

                df[f"{fn}({col})"] = values

        return {"df": df}

    def get_configuration(self) -> Configuration:
        """
        Get base configuration
        :return:
        """
        return Configuration(
            title="Monotonic",
            description="Apply monotonic transforms (square, cube, sqrt...)"
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
            ),
            AnyOf(
                name="functions",
                value=self.functions,
                options=self.available_functions
            )
        ]

    def configure_columns(self, columns: ArrayOfStrings):
        """
        Configure columns.
        :param columns:
        :return:
        """
        self.all_columns = coalesce(self.all_columns, columns)
        self.columns = coalesce(self.columns, columns)

    @classmethod
    def hydrate_from_dict(cls, attributes: dict) -> Self:
        """
        Convert attributes dict to object
        """
        instance = cls()

        if columns := attributes.get("columns", {}).get("value", []):
            instance.columns = columns

        if functions := attributes.get("functions", {}).get("value", []):
            instance.functions = functions

        return instance

