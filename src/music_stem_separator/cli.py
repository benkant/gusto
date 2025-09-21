"""Command-line interface for audio analysis, metadata extraction, and stem separation."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Final

import click
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, TextColumn

from music_stem_separator.config import DEFAULT_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger: Final[logging.Logger] = logging.getLogger("music_stem_separator")
console: Final[Console] = Console()


@click.group()
@click.version_option()
def cli() -> None:
    """Audio analysis, metadata extraction, and stem separation tools."""
    pass


@cli.command()
@click.argument(
    "input_dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
)
@click.option(
    "--output-dir",
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    default=None,
    help="Directory to save analyzed files (defaults to input_dir if not specified)",
)
@click.option(
    "--skip-fingerprinting",
    is_flag=True,
    help="Skip MusicBrainz fingerprinting for metadata",
)
@click.option(
    "--skip-bpm",
    is_flag=True,
    help="Skip BPM analysis",
)
@click.option(
    "--skip-key",
    is_flag=True,
    help="Skip key detection",
)
@click.option(
    "--skip-qualitative",
    is_flag=True,
    help="Skip qualitative feature extraction (mood, energy, etc.)",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose output",
)
def analyse(
    input_dir: Path,
    output_dir: Path | None = None,
    skip_fingerprinting: bool = False,
    skip_bpm: bool = False,
    skip_key: bool = False,
    skip_qualitative: bool = False,
    verbose: bool = False,
) -> None:
    """Analyze audio files for metadata, BPM, key, and qualitative features.

    This command takes WAV files from INPUT_DIR, analyzes them using audio
    fingerprinting and various audio analysis libraries, and renames them
    according to the format: artist_songname_bpm_key.wav.

    It also creates a JSON file with the same basename containing all extracted metadata.
    """
    if verbose:
        logger.setLevel(logging.DEBUG)

    output_dir = output_dir or input_dir
    output_dir.mkdir(exist_ok=True, parents=True)

    logger.info(f"Analyzing audio files in: {input_dir}")
    logger.info(f"Output directory: {output_dir}")
    logger.info(
        "Analysis features: "
        + f"{'MusicBrainz' if not skip_fingerprinting else ''} "
        + f"{'BPM' if not skip_bpm else ''} "
        + f"{'Key' if not skip_key else ''} "
        + f"{'Qualitative' if not skip_qualitative else ''}"
    )

    # TODO: Implement analyzer and output generation
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Scanning input directory...", total=None)
        # Actual implementation will be handled by the analyzer module


@cli.command()
@click.argument(
    "input_dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
)
@click.option(
    "--output-dir",
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    default=None,
    help="Directory to save stem files (defaults to input_dir if not specified)",
)
@click.option(
    "--model",
    type=str,
    default=DEFAULT_CONFIG.stem_separation.model_name,
    help="DEMUCS model to use for stem separation",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose output",
)
def split(
    input_dir: Path,
    output_dir: Path | None = None,
    model: str = DEFAULT_CONFIG.stem_separation.model_name,
    verbose: bool = False,
) -> None:
    """Split audio files into stems using DEMUCS.

    This command takes properly named WAV files from INPUT_DIR (in the format
    artist_songname_bpm_key.wav), splits them into stems using DEMUCS, and outputs
    stem files in the format: artist_songname_bpm_key_stemname.wav.
    """
    if verbose:
        logger.setLevel(logging.DEBUG)

    output_dir = output_dir or input_dir
    output_dir.mkdir(exist_ok=True, parents=True)

    logger.info(f"Splitting audio files in: {input_dir}")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Using DEMUCS model: {model}")

    # TODO: Implement stem separation
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Scanning input directory...", total=None)
        # Actual implementation will be handled by the separator module


if __name__ == "__main__":
    cli()
