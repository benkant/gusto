# TODO: Audio File Analysis, Metadata Extraction, and Stem Separation

## High-Level Description

Build a system with two separate CLI tools:

1. **analyse** - For audio analysis and metadata extraction:
   - Take a directory of WAV files as input
   - Each WAV file is a recording of a single song
   - The filename is unhelpful, so we need to analyse the audio to extract metadata
   - Use audio fingerprinting (MusicBrainz) to identify artist, song name, etc.
   - Use multiple libraries to analyse for key and BPM
   - Rename each file to `artist_songname_bpm_key.wav` (key: major by default, `s` for sharp, `b` for flat, `m` for minor)
   - Create a JSON file with the same basename containing all metadata

2. **split** - For stem separation:
   - Take a directory of properly named WAV files as input
   - Run DEMUCS stem separator on each file
   - Output: for each track, a set of stem WAVs named as `artist_songname_bpm_key_stemname.wav`
   - All output files should be 16-bit, 48kHz WAV format

---

## Tasks

### 1. Audio Analysis Tool (`analyse`)

#### Input Handling
- [ ] Read WAV files from input directory
- [ ] Verify they are 16-bit, 48kHz WAV files
- [ ] If not, convert them to proper format

#### Audio Fingerprinting & Metadata
- [ ] Implement audio fingerprinting using pyacoustid
- [ ] Query MusicBrainz API with musicbrainzngs to extract:
  - [ ] Artist, song name, album, year, genre
  - [ ] Credits (composers, producers, engineers)
  - [ ] Other available metadata
- [ ] Handle cases where fingerprinting fails (≈20% of files)

#### Audio Feature Analysis
- [ ] Implement BPM analysis using multiple libraries:
  - [ ] librosa
  - [ ] essentia
  - [ ] aubio
  - [ ] madmom (optional)
- [ ] Implement key detection using multiple libraries:
  - [ ] librosa
  - [ ] essentia
  - [ ] aubio
  - [ ] madmom (optional)
- [ ] Extract qualitative features:
  - [ ] essentia (danceability, mood, etc.)
  - [ ] librosa (energy, spectral features)

#### Output Generation
- [ ] Rename each file to `artist_songname_bpm_key.wav` format
- [ ] Create JSON file with same basename containing all metadata:
  - [ ] Structured by source (musicbrainz, librosa, essentia, etc.)
  - [ ] Lists stored as arrays of strings
  - [ ] All available metadata included

### 2. Stem Separation Tool (`split`)

#### Input Handling
- [ ] Read properly named WAV files from input directory
- [ ] Parse existing filenames to extract metadata

#### Stem Separation
- [ ] Implement DEMUCS for stem separation
- [ ] For each WAV, run stem separation
- [ ] Output one WAV per stem (16-bit, 48kHz)
- [ ] Name each stem file as `artist_songname_bpm_key_stemname.wav`

### 3. File Management
- [ ] Ensure all output files are in correct format (WAV, 16-bit, 48kHz)
- [ ] Handle temp/intermediate files, clean up as needed

### 4. Configurability & Extensibility
- [ ] Allow config for output dir, stem separator, audio analysis backends
- [ ] Make BPM/key extraction modular (for different libraries)
- [ ] Document requirements and setup in README.md

### 5. Error Handling & Logging
- [ ] Robust error handling for all steps (fingerprinting, analysis, separation)
- [ ] Log progress and errors to file/console
- [ ] Command line verbosity options

---

## Optional/Advanced
- [ ] Add support for tagging WAVs with metadata
- [ ] Parallelise analysis and stem separation for speed
- [ ] Add a GUI frontend for the CLI tools
- [ ] Add database storage for processed files and metadata 