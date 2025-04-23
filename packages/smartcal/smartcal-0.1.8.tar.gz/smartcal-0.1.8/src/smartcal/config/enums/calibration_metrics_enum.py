from enum import Enum

from smartcal.metrics.conf_ece import ConfECE
from smartcal.metrics.ece import ECE
from smartcal.metrics.mce import MCE


class CalibrationMetricsEnum(Enum):
    """Enum to map metric names to their corresponding classes."""
    ECE = ECE
    MCE = MCE
    ConfECE = ConfECE

    @classmethod
    def get_metric_class(cls, metric_name: str):
        """Retrieve the metric class by name."""
        try:
            return cls[metric_name].value
        except KeyError:
            raise ValueError(f"Metric '{metric_name}' is not supported.")
