"""Stem separation functionality using spleeter."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Final, Literal

from pydantic import BaseModel
from spleeter.separator import Separator as SpleeterSeparator

logger: Final[logging.Logger] = logging.getLogger(__name__)


class StemSeparationResult(BaseModel):
    """Result of stem separation process."""

    input_file: Path
    output_dir: Path
    stems: dict[str, Path]


class StemSeparator:
    """Handles stem separation using spleeter."""

    def __init__(
        self,
        model_name: Literal["2stems", "4stems", "5stems"] = "4stems",
        output_dir: Path = Path("output"),
    ) -> None:
        """Initialize the stem separator.

        Args:
            model_name: Name of the model to use for separation
            output_dir: Directory to save separated stems
        """
        self.model_name = model_name
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.separator = SpleeterSeparator(f"spleeter:{model_name}")

    def separate(self, input_file: Path) -> StemSeparationResult:
        """Separate stems from an audio file.

        Args:
            input_file: Path to the input audio file

        Returns:
            StemSeparationResult containing paths to separated stems
        """
        logger.info(f"Separating stems from {input_file}")
        
        # Perform separation
        self.separator.separate_to_file(
            str(input_file),
            str(self.output_dir),
            filename_format="{instrument}.{codec}",
            codec="wav",
        )
        
        # Get stem files
        stems = {}
        for stem in self.separator._get_stems_for_model():
            stem_file = self.output_dir / f"{stem}.wav"
            if stem_file.exists():
                stems[stem] = stem_file
        
        return StemSeparationResult(
            input_file=input_file,
            output_dir=self.output_dir,
            stems=stems,
        ) 