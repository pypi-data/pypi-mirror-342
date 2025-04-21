from __future__ import annotations

import json
import logging
from typing import Any, cast

import nshconfig as C
from lightning.pytorch import LightningDataModule, Trainer

log = logging.getLogger(__name__)


def _dict(obj: Any):
    if isinstance(obj, C.Config):
        return obj.model_dump(mode="json")

    try:
        return dict(obj)
    except Exception:
        return json.loads(
            json.dumps(obj, default=lambda o: str(o), indent=4, sort_keys=True)
        )


def _dict_and_clean(obj: Any):
    d = _dict(obj)

    # Remove LightningCLI's internal hparam
    d = {k: v for k, v in d.items() if k != "_class_path"}
    return d


def _log_hyperparams(trainer: Trainer) -> None:
    if not trainer.loggers:
        return

    hparams_to_log: dict[str, Any] = {}

    from .trainer import Trainer

    if isinstance(trainer, Trainer):
        hparams_to_log["trainer"] = _dict_and_clean(trainer.hparams)

    if (
        pl_module := trainer.lightning_module
    ) is not None and pl_module._log_hyperparams:
        hparams_to_log["model"] = _dict_and_clean(pl_module.hparams_initial)

    if (
        datamodule := cast(
            LightningDataModule | None, getattr(trainer, "datamodule", None)
        )
    ) is not None and (datamodule._log_hyperparams):
        hparams_to_log["datamodule"] = _dict_and_clean(datamodule.hparams_initial)

    for logger in trainer.loggers:
        logger.log_hyperparams(hparams_to_log)
        logger.log_graph(pl_module)
        logger.save()


def patch_log_hparams_function():
    try:
        import lightning.pytorch.loggers.utilities
        import lightning.pytorch.trainer.trainer

        lightning.pytorch.loggers.utilities._log_hyperparams = _log_hyperparams
        lightning.pytorch.trainer.trainer._log_hyperparams = _log_hyperparams
        log.info(
            "Patched lightning.pytorch's _log_hyperparams to use nshtrainer's version"
        )
    except ImportError:
        pass

    try:
        import pytorch_lightning.loggers.utilities
        import pytorch_lightning.trainer.trainer

        pytorch_lightning.loggers.utilities._log_hyperparams = _log_hyperparams
        pytorch_lightning.trainer.trainer._log_hyperparams = _log_hyperparams
        log.info(
            "Patched pytorch_lightning's _log_hyperparams to use nshtrainer's version"
        )
    except ImportError:
        pass
