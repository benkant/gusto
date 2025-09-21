"""Tests for the audio analyzer module."""

from __future__ import annotations

from pathlib import Path

import pytest

from music_stem_separator.analyzer import AudioAnalyzer, AudioAnalysisResult


@pytest.fixture
def analyzer() -> AudioAnalyzer:
    """Create an audio analyzer instance for testing."""
    return AudioAnalyzer(bpm_method="madmom", key_method="librosa")


def test_analyzer_initialization(analyzer: AudioAnalyzer) -> None:
    """Test that the analyzer initializes correctly."""
    assert analyzer.bpm_method == "madmom"
    assert analyzer.key_method == "librosa"


def test_analyze_audio(
    analyzer: AudioAnalyzer,
    tmp_path: Path,
) -> None:
    """Test audio analysis functionality."""
    # Create a dummy audio file for testing
    test_file = tmp_path / "test.wav"
    test_file.write_bytes(b"dummy audio data")
    
    # Test analysis
    result = analyzer.analyze(test_file)
    
    # Verify result structure
    assert isinstance(result, AudioAnalysisResult)
    assert isinstance(result.bpm, float)
    assert isinstance(result.key, str)
    assert isinstance(result.confidence, float) 