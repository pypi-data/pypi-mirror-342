# API Reference

This section provides detailed documentation for the PEC-DSS API.

## Core Module

The core module contains the main functionality for speaker identification and paralinguistic event processing.

### ParalinguisticEventProcessor

```python
from pec_dss.core.processor import ParalinguisticEventProcessor
```

The `ParalinguisticEventProcessor` class provides the main interface for the PEC-DSS system.

**Methods:**

- `__init__(device="cpu")`: Initialize the processor.
- `load_model()`: Load the SNAC model.
- `load_audio(audio_path, sr=24000)`: Load an audio file.
- `load_audio_directory(directory_path, sr=24000)`: Load all audio files from a directory.
- `load_speaker_references(base_directory, sr=24000)`: Load speaker reference samples.
- `process_paralinguistic_events(speaker_audios, unidentified_audios, threshold=0.5)`: Process events.
- `save_results(results, output_dir, unidentified_paths=None)`: Save processing results.
- `run_pipeline(speakers_dir, unidentified_dir, output_dir, threshold=0.5, sr=24000)`: Run the full pipeline.

### Speaker Identification

```python
from pec_dss.core.speaker_identification import (
    calculate_speaker_average_vectors,
    identify_speaker_for_audio,
    assign_speakers_to_laughs
)
```

Functions for speaker identification:

- `calculate_speaker_average_vectors(speaker_audios, snac_model, device="cpu")`: Calculate speaker voice profiles.
- `identify_speaker_for_audio(unidentified_audios, speaker_avg_vectors, snac_model, device="cpu")`: Identify speakers.
- `assign_speakers_to_laughs(speaker_audios, unidentified_audios, snac_model, device="cpu", threshold=0.0)`: Assign events to speakers.

## Models Module

The models module contains functionality related to the underlying neural models.

### SNAC Model

```python
from pec_dss.models.snac_model import load_snac_model, load_tokenizer
```

Functions for loading models:

- `load_snac_model(device="cpu")`: Load the SNAC model.
- `load_tokenizer(tokeniser_name="meta-llama/Llama-3.2-3B-Instruct")`: Load a tokenizer.

## Utils Module

The utils module contains utility functions for audio processing and analysis.

### Audio Encoder

```python
from pec_dss.utils.audio_encoder import tokenise_audio, get_codebook_vectors
```

Functions for audio encoding:

- `tokenise_audio(waveform, snac_model, device="cpu")`: Tokenize audio waveform.
- `get_codebook_vectors(waveform, snac_model, device="cpu")`: Extract codebook vectors.

### Analysis

```python
from pec_dss.utils.analysis import calculate_codebook_averages, calculate_full_codebook_statistics
```

Functions for audio analysis:

- `calculate_codebook_averages(waveform, snac_model, device="cpu")`: Calculate codebook averages.
- `calculate_full_codebook_statistics(snac_model)`: Calculate codebook statistics.

## Command-Line Interface

The command-line interface is provided by the `pec_dss.cli` module:

```python
from pec_dss.cli import main, create_parser
```

Functions:

- `main()`: Main entry point for the CLI.
- `create_parser()`: Create the argument parser. 