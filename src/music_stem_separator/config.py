"""Configuration settings for audio analysis, metadata extraction, and stem separation."""

from __future__ import annotations

from pathlib import Path
from typing import Final, Literal

from pydantic import BaseModel, Field


class AudioAnalysisConfig(BaseModel):
    """Configuration for audio analysis."""

    bpm_analysis_methods: list[Literal["librosa", "essentia", "aubio", "madmom"]] = Field(
        default=["librosa", "essentia", "aubio"],
        description="Methods to use for BPM analysis",
    )

    key_analysis_methods: list[Literal["librosa", "essentia", "aubio", "madmom"]] = Field(
        default=["librosa", "essentia", "aubio"],
        description="Methods to use for key analysis",
    )

    qualitative_analysis_methods: list[Literal["essentia", "librosa"]] = Field(
        default=["essentia", "librosa"],
        description="Methods to use for qualitative feature extraction",
    )

    sample_rate: int = Field(
        default=48000,
        description="Sample rate for audio processing",
    )

    bit_depth: int = Field(
        default=16,
        description="Bit depth for audio processing",
    )

    output_dir: Path = Field(
        default=Path("analyzed"),
        description="Directory to save analyzed files",
    )


class MusicBrainzConfig(BaseModel):
    """Configuration for MusicBrainz fingerprinting."""

    enabled: bool = Field(
        default=True,
        description="Whether to perform MusicBrainz fingerprinting",
    )

    user_agent: str = Field(
        default="MusicStemSeparator/0.1.0 ( https://github.com/benkant/music-stem-separator )",
        description="User agent to use for MusicBrainz API",
    )

    fpcalc_path: Path | None = Field(
        default=None,
        description="Path to the fpcalc executable (if None, will search in PATH)",
    )


class StemSeparationConfig(BaseModel):
    """Configuration for stem separation using DEMUCS."""

    model_name: str = Field(
        default="htdemucs",
        description="DEMUCS model to use for stem separation "
        "(e.g., htdemucs, htdemucs_ft, mdx_extra)",
    )

    output_dir: Path = Field(
        default=Path("stems"),
        description="Directory to save separated stems",
    )

    sample_rate: int = Field(
        default=48000,
        description="Sample rate for audio processing",
    )

    bit_depth: int = Field(
        default=16,
        description="Bit depth for audio processing",
    )

    device: Literal["cuda", "cpu"] = Field(
        default="cpu",
        description="Device to use for DEMUCS inference",
    )

    shifts: int = Field(
        default=1,
        description="Number of random shifts for DEMUCS separation",
    )


class Config(BaseModel):
    """Main configuration for the application."""

    audio_analysis: AudioAnalysisConfig = Field(
        default_factory=AudioAnalysisConfig,
    )

    musicbrainz: MusicBrainzConfig = Field(
        default_factory=MusicBrainzConfig,
    )

    stem_separation: StemSeparationConfig = Field(
        default_factory=StemSeparationConfig,
    )


# Default configuration instance
DEFAULT_CONFIG: Final[Config] = Config()
