from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

log = logging.getLogger(__name__)


@dataclass
class DistributedPredictionResult:
    """Represents the results of a distributed prediction run.

    This dataclass provides easy access to both raw and processed prediction data.
    """

    root_dir: Path
    """Root directory where predictions are stored."""

    @property
    def raw_dir(self) -> Path:
        """Directory containing raw prediction data."""
        return self.root_dir / "raw"

    @property
    def processed_dir(self) -> Path:
        """Directory containing processed prediction data."""
        return self.root_dir / "processed"

    def get_raw_predictions(self, dataloader_idx: int = 0) -> Path:
        """Get the directory containing raw predictions for a specific dataloader.

        Args:
            dataloader_idx: Index of the dataloader

        Returns:
            Path to the raw predictions directory for the specified dataloader
        """
        raw_loader_dir = self.raw_dir / f"dataloader_{dataloader_idx}"
        if not raw_loader_dir.exists():
            log.warning(f"Raw predictions directory {raw_loader_dir} does not exist.")
        return raw_loader_dir

    def get_processed_reader(self, dataloader_idx: int = 0):
        """Get a reader for processed predictions from a specific dataloader.

        Args:
            dataloader_idx: Index of the dataloader

        Returns:
            A DistributedPredictionReader for the processed predictions, or None if no data exists
        """
        from ..callbacks.distributed_prediction_writer import (
            DistributedPredictionReader,
        )

        processed_loader_dir = self.processed_dir / f"dataloader_{dataloader_idx}"
        if not processed_loader_dir.exists():
            log.warning(
                f"Processed predictions directory {processed_loader_dir} does not exist."
            )
            return None

        return DistributedPredictionReader(processed_loader_dir)

    @classmethod
    def load(cls, path: Path | str):
        """Load prediction results from a directory.

        Args:
            path: Path to the predictions directory

        Returns:
            A DistributedPredictionResult instance
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Predictions directory {path} does not exist.")

        return cls(root_dir=path)
