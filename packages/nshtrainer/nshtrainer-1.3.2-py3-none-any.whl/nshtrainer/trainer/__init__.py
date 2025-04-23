from __future__ import annotations

from ..callbacks import callback_registry as callback_registry
from ..callbacks.distributed_prediction_writer import (
    DistributedPredictionReader as DistributedPredictionReader,
)
from ._config import TrainerConfig as TrainerConfig
from ._distributed_prediction_result import (
    DistributedPredictionResult as DistributedPredictionResult,
)
from .accelerator import accelerator_registry as accelerator_registry
from .plugin import plugin_registry as plugin_registry
from .trainer import Trainer as Trainer
