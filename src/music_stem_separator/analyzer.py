"""Audio analysis module for detecting key, BPM, and other metadata."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Final

import librosa
import numpy as np
from pydantic import BaseModel
from rich.console import Console

# Configure logging
logger: Final[logging.Logger] = logging.getLogger("music_stem_separator")
console: Final[Console] = Console()


class AudioFeatures(BaseModel):
    """Features extracted from audio analysis."""

    path: Path
    bpm: float
    key: str
    # Additional features can be added here as needed


class AudioAnalyzer:
    """Audio analyzer using librosa for BPM, key detection, etc."""

    def __init__(self, sample_rate: int = 48000, bit_depth: int = 16) -> None:
        """Initialize the audio analyzer with desired sample rate and bit depth."""
        self.sample_rate = sample_rate
        self.bit_depth = bit_depth

    def analyze_file(self, file_path: Path) -> AudioFeatures:
        """Analyze an audio file for BPM, key, and other features."""
        logger.info(f"Analyzing audio file: {file_path}")

        # Load audio file
        try:
            y, sr = librosa.load(file_path, sr=self.sample_rate, mono=True)
        except Exception as e:
            logger.error(f"Error loading audio file: {e}")
            raise

        # Extract features
        features = self._extract_features(y, sr)
        features.path = file_path

        return features

    def _extract_features(self, y: np.ndarray, sr: int) -> AudioFeatures:
        """Extract features from audio data."""
        # Estimate BPM
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        # Estimate key
        # TODO: Implement key detection logic
        key_str = "C"  # Placeholder

        # Create features object
        features = AudioFeatures(
            path=Path(""),  # Placeholder, will be set in analyze_file
            bpm=float(tempo),
            key=key_str,
        )

        return features
