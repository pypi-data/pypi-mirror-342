from __future__ import annotations

import functools
import logging
from collections.abc import Iterator, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, Generic, Literal, cast, overload

import torch
from lightning.fabric.utilities.apply_func import move_data_to_device
from lightning.pytorch.callbacks import BasePredictionWriter
from typing_extensions import TypeVar, final, override

from .base import CallbackConfigBase, CallbackMetadataConfig, callback_registry

if TYPE_CHECKING:
    from ..model.base import IndividualSample


log = logging.getLogger(__name__)


@final
@callback_registry.register
class DistributedPredictionWriterConfig(CallbackConfigBase):
    metadata: ClassVar[CallbackMetadataConfig] = CallbackMetadataConfig(
        enabled_for_barebones=True
    )
    """Metadata for the callback."""

    name: Literal["distributed_prediction_writer"] = "distributed_prediction_writer"

    dirpath: Path | None = None
    """Directory to save the predictions to. If None, will use the default directory."""

    move_to_cpu_on_save: bool = True
    """Whether to move the predictions to CPU before saving. Default is True."""

    save_raw: bool = True
    """Whether to save the raw predictions."""

    save_processed: bool = True
    """Whether to process and save the predictions.

    "Processing" means that the model's batched predictions are split into individual predictions
    and saved as a list of tensors.
    """

    @override
    def create_callbacks(self, trainer_config):
        if (dirpath := self.dirpath) is None:
            dirpath = trainer_config.directory.resolve_subdirectory(
                trainer_config.id, "predictions"
            )

        yield DistributedPredictionWriter(self, dirpath)


def _move_and_save(data, path: Path, move_to_cpu: bool):
    if move_to_cpu:
        data = move_data_to_device(data, "cpu")

    # Save the data to the specified path
    torch.save(data, path)


class DistributedPredictionWriter(BasePredictionWriter):
    def __init__(
        self,
        config: DistributedPredictionWriterConfig,
        output_dir: Path,
    ):
        self.config = config

        super().__init__(write_interval="batch")

        self.output_dir = output_dir

    @override
    def write_on_batch_end(
        self,
        trainer,
        pl_module,
        prediction,
        batch_indices,
        batch,
        batch_idx,
        dataloader_idx,
    ):
        save = functools.partial(
            _move_and_save,
            move_to_cpu=self.config.move_to_cpu_on_save,
        )

        # Regular, unstructured writing.
        if self.config.save_raw:
            output_dir = (
                self.output_dir
                / "raw"
                / f"dataloader_{dataloader_idx}"
                / f"rank_{trainer.global_rank}"
                / f"batch_{batch_idx}"
            )
            output_dir.mkdir(parents=True, exist_ok=True)
            save(prediction, output_dir / "predictions.pt")
            save(batch, output_dir / "batch.pt")
            save(batch_indices, output_dir / "batch_indices.pt")

        if self.config.save_processed:
            # Processed writing.
            from ..model.base import LightningModuleBase

            if not isinstance(pl_module, LightningModuleBase):
                raise ValueError(
                    "The model must be a subclass of LightningModuleBase to use the distributed prediction writer."
                )

            output_dir = self.output_dir / "processed" / f"dataloader_{dataloader_idx}"
            output_dir.mkdir(parents=True, exist_ok=True)

            # Split into individual predictions
            assert batch_indices is not None, (
                "Batch indices must be provided for processed writing."
            )
            for sample in pl_module.split_batched_predictions(
                batch, prediction, batch_indices
            ):
                sample = {
                    **sample,
                    "global_rank": trainer.global_rank,
                    "world_size": trainer.world_size,
                    "is_global_zero": trainer.is_global_zero,
                }
                save(sample, output_dir / f"{sample['index']}.pt")


SampleT = TypeVar(
    "SampleT",
    bound="IndividualSample",
    default="IndividualSample",
    infer_variance=True,
)


class DistributedPredictionReader(Sequence[SampleT], Generic[SampleT]):
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir

    @override
    def __len__(self) -> int:
        return len(list(self.output_dir.glob("*.pt")))

    @overload
    def __getitem__(self, index: int) -> SampleT: ...

    @overload
    def __getitem__(self, index: slice) -> list[SampleT]: ...

    @override
    def __getitem__(self, index: int | slice) -> SampleT | list[SampleT]:
        if isinstance(index, slice):
            # Handle slice indexing
            indices = range(*index.indices(len(self)))
            return [self.__getitem__(i) for i in indices]

        # Handle integer indexing
        path = self.output_dir / f"{index}.pt"
        if not path.exists():
            raise FileNotFoundError(f"File {path} does not exist.")

        sample = cast(SampleT, torch.load(path))
        return sample

    @override
    def __iter__(self) -> Iterator[SampleT]:
        for i in range(len(self)):
            yield self[i]
