from typing import Generator

import numpy as np

from tinyml4all.support.types import TemplateDef
from tinyml4all.time.features.FeatureExtractor import FeatureExtractor
from tinyml4all.transpile.Convertible import Convertible
from tinyml4all.transpile.Variable import Variable


class Peaks(FeatureExtractor):
    """
    Compute count of peaks
    """
    def __str__(self):
        """
        Get string representation
        :return:
        """
        return "Peaks()"

    def __call__(self, data: np.ndarray[float, float]) -> Generator[float, None, None]:
        """
        Count peaks
        :param data:
        :return:
        """
        for column in self.save_count(data.T):
            mean = np.abs(column).mean()
            is_greater_than_prev = (np.abs(column[1:-1] - column[:-2]) > mean * 0.1)
            is_greater_than_next = (np.abs(column[1:-1] - column[2:]) > mean * 0.1)
            is_peak = np.logical_and(is_greater_than_prev, is_greater_than_next)

            yield is_peak.mean()

    def get_feature_names(self, columns: list[str]) -> Generator[str, None, None]:
        """
        Get feature names
        :param columns:
        :return:
        """
        for column in self.save_columns(columns):
            yield f"peaks({column})"
