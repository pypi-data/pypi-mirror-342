# Usage Guide

This guide provides detailed instructions on how to use the PEC-DSS package for paralinguistic event classification and speaker attribution.

## Basic Concepts

PEC-DSS works with two main types of audio inputs:

1. **Speaker reference samples**: Audio samples of known speakers that are used to build speaker profiles.
2. **Unidentified audio events**: Audio samples containing paralinguistic events (like laughter, sighs, etc.) that you want to attribute to specific speakers.

The system uses the SNAC model to extract audio features and performs similarity-based matching to identify which speaker most likely produced each paralinguistic event.

## Directory Structure

For best results, organize your audio files as follows:

```
speakers/
├── speaker1/
│   ├── sample1.wav
│   ├── sample2.wav
│   └── ...
├── speaker2/
│   ├── sample1.wav
│   ├── sample2.wav
│   └── ...
└── ...

events/
├── event1.wav
├── event2.wav
└── ...
```

Where:
- Each speaker has their own directory with reference audio samples
- Events directory contains the unidentified audio events to be classified

## Using the Command-Line Interface

The simplest way to use PEC-DSS is through its command-line interface:

```bash
pec-dss --speakers-dir ./speakers --unidentified-dir ./events --output-dir ./results
```

### CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--speakers-dir` | Directory containing speaker reference samples | (Required) |
| `--unidentified-dir` | Directory containing unidentified audio events | (Required) |
| `--output-dir` | Directory to save results | `pec_dss_results` |
| `--threshold` | Similarity threshold for speaker assignment | `0.5` |
| `--sample-rate` | Sample rate for audio processing | `24000` |
| `--use-gpu` | Use GPU for processing if available | (Disabled) |
| `--verbose` | Enable verbose logging | (Disabled) |

## Using the Python API

For more advanced usage, you can use the Python API directly:

### Using the ParalinguisticEventProcessor

```python
import os
from pec_dss.core.processor import ParalinguisticEventProcessor

# Initialize the processor
processor = ParalinguisticEventProcessor(device="cuda" if use_gpu else "cpu")

# Run the full pipeline
results = processor.run_pipeline(
    speakers_dir="./speakers",
    unidentified_dir="./events",
    output_dir="./results",
    threshold=0.6,
    sr=24000
)

# Process the results
for speaker, assignments in results.items():
    print(f"Speaker {speaker} has {len(assignments)} assigned events")
    for item in assignments:
        print(f"  Similarity score: {item['similarity_score']:.4f}")
```

### Using the Lower-Level API

For more control over the process:

```python
import librosa
import numpy as np
from pec_dss.models.snac_model import load_snac_model
from pec_dss.core.speaker_identification import assign_speakers_to_laughs

# Load the model
snac_model = load_snac_model(device="cpu")

# Prepare speaker reference samples (manually loading audio files)
speaker_audios = {}
for speaker_dir in os.listdir("./speakers"):
    speaker_path = os.path.join("./speakers", speaker_dir)
    if os.path.isdir(speaker_path):
        samples = []
        for file in os.listdir(speaker_path):
            if file.endswith((".wav", ".mp3", ".flac")):
                audio, _ = librosa.load(os.path.join(speaker_path, file), sr=24000)
                samples.append(audio)
        if samples:
            speaker_audios[speaker_dir] = samples

# Load unidentified events
unidentified_audios = []
for file in os.listdir("./events"):
    if file.endswith((".wav", ".mp3", ".flac")):
        audio, _ = librosa.load(os.path.join("./events", file), sr=24000)
        unidentified_audios.append(audio)

# Process the audio
results = assign_speakers_to_laughs(
    speaker_audios, 
    unidentified_audios, 
    snac_model, 
    device="cpu",
    threshold=0.5
)

# Handle the results
for speaker, assignments in results.items():
    print(f"Speaker {speaker} has {len(assignments)} assigned events")
```

## Understanding the Results

The results of the processing are saved in the output directory with the following structure:

```
results/
├── results.json                # Main results file
├── speaker1/                   # Directory for each speaker
│   ├── 0_event2.wav            # Assigned audio files
│   └── ...
├── speaker2/
│   ├── 0_event1.wav
│   └── ...
└── unknown/                    # Events below threshold (if any)
    └── ...
```

The `results.json` file contains detailed information about the assignments, including similarity scores and other metadata.

## Tips for Better Results

1. **Use high-quality reference samples**: Make sure reference samples clearly represent each speaker's voice.
2. **Provide multiple samples per speaker**: More samples help build a better speaker profile.
3. **Adjust the threshold**: If too many events are assigned to the wrong speaker, try increasing the threshold.
4. **Use GPU for faster processing**: For large datasets, enable GPU processing with the `--use-gpu` flag.
5. **Preprocess audio**: Try to minimize background noise in your audio samples.

## Handling Errors

If you encounter errors, try the following:

1. Check that your audio files are valid and can be read by librosa.
2. Ensure you have installed all dependencies correctly.
3. Run with the `--verbose` flag to get more detailed error information.
4. Make sure your speaker directories contain at least one valid audio file each. 