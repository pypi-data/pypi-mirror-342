# PEC-DSS Documentation

PEC-DSS (Paralinguistic Event Classification from Diarized Speaker Segments) is an advanced audio analysis system that identifies paralinguistic vocal events (like laughter, sighs, etc.) and attributes them to specific speakers through sophisticated speaker diarization and neural audio processing.

## Key Features

* Advanced speaker identification using neural audio encoders
* Attribution of paralinguistic events to specific speakers
* High-accuracy SNAC (Scalable Neural Audio Codec) model integration
* Voice embedding and similarity-based speaker matching
* Comprehensive audio codebook analysis
* Modular architecture for easy customization

## Installation

Install from PyPI:

```bash
pip install pec-dss
```

Or install from source:

```bash
git clone https://github.com/hwk06023/PEC-DSS.git
cd PEC-DSS
pip install -e .
```

## Quick Start

```python
from pec_dss.models.snac_model import load_snac_model
from pec_dss.core.speaker_identification import assign_speakers_to_laughs
import librosa

# Load model
snac_model = load_snac_model(device="cpu")  # or "cuda" for GPU

# Prepare speaker reference samples
speaker_audios = {
    "speaker1": [librosa.load("speaker1_sample1.wav", sr=24000)[0],
                librosa.load("speaker1_sample2.wav", sr=24000)[0]],
    "speaker2": [librosa.load("speaker2_sample1.wav", sr=24000)[0],
                librosa.load("speaker2_sample2.wav", sr=24000)[0]]
}

# Prepare unidentified events
unidentified_events = [
    librosa.load("laugh1.wav", sr=24000)[0],
    librosa.load("laugh2.wav", sr=24000)[0]
]

# Identify speakers for each audio event
results = assign_speakers_to_laughs(speaker_audios, unidentified_events, snac_model)

# Print results
for speaker, events in results.items():
    print(f"Speaker {speaker} has {len(events)} attributed events")
```

## CLI Usage

PEC-DSS includes a command-line interface for batch processing:

```bash
pec-dss --speakers-dir ./speakers --unidentified-dir ./events --output-dir ./results
```

For more options:

```bash
pec-dss --help
```

## Contents

```{toctree}
:maxdepth: 2

installation
usage
api
examples
contributing
```

## License

This project is licensed under the GNU General Public License v3.0. 