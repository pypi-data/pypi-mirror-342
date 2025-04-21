from __future__ import annotations

__codegen__ = True

from nshtrainer.callbacks.distributed_prediction_writer import (
    CallbackConfigBase as CallbackConfigBase,
)
from nshtrainer.callbacks.distributed_prediction_writer import (
    DistributedPredictionWriterConfig as DistributedPredictionWriterConfig,
)
from nshtrainer.callbacks.distributed_prediction_writer import (
    callback_registry as callback_registry,
)

__all__ = [
    "CallbackConfigBase",
    "DistributedPredictionWriterConfig",
    "callback_registry",
]
