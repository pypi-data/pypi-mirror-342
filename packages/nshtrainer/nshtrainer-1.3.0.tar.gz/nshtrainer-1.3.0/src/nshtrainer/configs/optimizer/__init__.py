from __future__ import annotations

__codegen__ = True

from nshtrainer.optimizer import AdadeltaConfig as AdadeltaConfig
from nshtrainer.optimizer import AdafactorConfig as AdafactorConfig
from nshtrainer.optimizer import AdagradConfig as AdagradConfig
from nshtrainer.optimizer import AdamaxConfig as AdamaxConfig
from nshtrainer.optimizer import AdamConfig as AdamConfig
from nshtrainer.optimizer import AdamWConfig as AdamWConfig
from nshtrainer.optimizer import ASGDConfig as ASGDConfig
from nshtrainer.optimizer import NAdamConfig as NAdamConfig
from nshtrainer.optimizer import OptimizerConfig as OptimizerConfig
from nshtrainer.optimizer import OptimizerConfigBase as OptimizerConfigBase
from nshtrainer.optimizer import RAdamConfig as RAdamConfig
from nshtrainer.optimizer import RMSpropConfig as RMSpropConfig
from nshtrainer.optimizer import RpropConfig as RpropConfig
from nshtrainer.optimizer import SGDConfig as SGDConfig
from nshtrainer.optimizer import Union as Union
from nshtrainer.optimizer import optimizer_registry as optimizer_registry

__all__ = [
    "ASGDConfig",
    "AdadeltaConfig",
    "AdafactorConfig",
    "AdagradConfig",
    "AdamConfig",
    "AdamWConfig",
    "AdamaxConfig",
    "NAdamConfig",
    "OptimizerConfig",
    "OptimizerConfigBase",
    "RAdamConfig",
    "RMSpropConfig",
    "RpropConfig",
    "SGDConfig",
    "Union",
    "optimizer_registry",
]
