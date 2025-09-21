"""Tests for the stem separator module."""

from __future__ import annotations

from pathlib import Path

import pytest
from spleeter.separator import Separator as SpleeterSeparator

from music_stem_separator.separator import StemSeparator, StemSeparationResult


@pytest.fixture
def separator() -> StemSeparator:
    """Create a stem separator instance for testing."""
    return StemSeparator(model_name="4stems", output_dir=Path("test_output"))


def test_separator_initialization(separator: StemSeparator) -> None:
    """Test that the separator initializes correctly."""
    assert separator.model_name == "4stems"
    assert separator.output_dir == Path("test_output")
    assert isinstance(separator.separator, SpleeterSeparator)


def test_separate_stems(
    separator: StemSeparator,
    tmp_path: Path,
) -> None:
    """Test stem separation functionality."""
    # Create a dummy audio file for testing
    test_file = tmp_path / "test.wav"
    test_file.write_bytes(b"dummy audio data")
    
    # Test separation
    result = separator.separate(test_file)
    
    # Verify result structure
    assert isinstance(result, StemSeparationResult)
    assert result.input_file == test_file
    assert result.output_dir == separator.output_dir
    assert isinstance(result.stems, dict) 