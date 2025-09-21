# Music Stem Separator

A tool for audio analysis, metadata extraction, and stem separation.

## Features

- **Audio Analysis**: Extract BPM, key, and qualitative features using multiple libraries:
  - librosa
  - essentia
  - aubio
  - madmom (optional)

- **Metadata Extraction**: Automatically identify songs using audio fingerprinting:
  - MusicBrainz/AcoustID for artist, title, album, year, genre, etc.
  - Extract qualitative features (mood, danceability, energy)
  - Store all metadata in structured JSON files

- **Stem Separation**: Split songs into individual instrument stems:
  - Use DEMUCS for high-quality stem separation
  - Create properly named stem files

## Requirements

- macOS (tested on M2 Max MacBook Pro)
- Python 3.12
- Homebrew (for installing chromaprint)

## Installation

### Quick Install

```bash
# Clone the repository
git clone https://github.com/benkant/music-stem-separator.git
cd music-stem-separator

# Run the setup script (installs UV, creates venv, installs dependencies)
chmod +x setup.sh
./setup.sh
```

### Manual Installation

```bash
# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a virtual environment
uv venv
source .venv/bin/activate

# Install the package and dependencies
uv pip install -e ".[dev]"

# Install chromaprint for audio fingerprinting
brew install chromaprint
```

## Usage

### Analyze Audio Files

```bash
# Analyze all WAV files in a directory
analyse path/to/wav/files

# Specify output directory
analyse path/to/wav/files --output-dir path/to/output

# Skip certain analysis steps
analyse path/to/wav/files --skip-fingerprinting --skip-qualitative
```

### Split Audio Files into Stems

```bash
# Split all properly named WAV files in a directory
split path/to/analyzed/files

# Specify output directory
split path/to/analyzed/files --output-dir path/to/stems

# Specify DEMUCS model
split path/to/analyzed/files --model htdemucs_ft
```

## File Formats

### Input WAV Files
- Any WAV file, 16-bit 48kHz preferred (will be converted if necessary)
- Filenames can be anything

### Output Files
- **Analyzed Audio**: `artist_songname_bpm_key.wav`
- **Metadata JSON**: `artist_songname_bpm_key.json`
- **Stem Files**: `artist_songname_bpm_key_stemname.wav`

## Development

### Setup

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=music_stem_separator
```

### Code Quality

```bash
# Run formatters and linters
ruff check .
ruff format .
pyright
```

## License

PROPRIETARY