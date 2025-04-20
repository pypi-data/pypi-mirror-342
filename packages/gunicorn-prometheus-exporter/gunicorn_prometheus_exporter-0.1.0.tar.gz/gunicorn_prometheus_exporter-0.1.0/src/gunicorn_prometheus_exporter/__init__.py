"""
Gunicorn Prometheus Exporter - A worker plugin for Gunicorn that exports
Prometheus metrics.
"""

from .metrics import registry
from .plugin import PrometheusWorker

__version__ = "0.1.0"
__all__ = [
    "PrometheusWorker",
    "registry",
]
