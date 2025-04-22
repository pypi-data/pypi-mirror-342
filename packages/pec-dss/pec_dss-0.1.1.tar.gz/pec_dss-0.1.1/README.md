# PEC-DSS 🎵🔊

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

[English](README.md) | [한국어](i18n/README_ko.md) | [中文](i18n/README_zh.md) | [日本語](i18n/README_jp.md)

**Paralinguistic Event Classification from Diarized Speaker Segments**

PEC-DSS is an advanced audio analysis system that identifies paralinguistic vocal events (like laughter, sighs, etc.) and attributes them to specific speakers through sophisticated speaker diarization and neural audio processing.

## ✨ Features

* 🎙️ Advanced speaker identification using neural audio encoders
* 😀 Attribution of paralinguistic events to specific speakers
* 🔍 High-accuracy SNAC (Scalable Neural Audio Codec) model integration
* 🔊 Voice embedding and similarity-based speaker matching
* 📊 Comprehensive audio codebook analysis
* 🔄 Modular architecture for easy customization

## 🚀 Installation

### From PyPI

```bash
pip install pec-dss
```

### From Source with pip

```bash
git clone https://github.com/hwk06023/PEC-DSS.git
cd PEC-DSS
pip install -e .
```

### From Source with requirements.txt

```bash
git clone https://github.com/hwk06023/PEC-DSS.git
cd PEC-DSS
pip install -r requirements.txt
```

For development:

```bash
pip install -r requirements-dev.txt
```

## 📖 Quick Start

### Basic Usage

```python
from snac_model import load_snac_model
from audio_encoder import get_codebook_vectors
from speaker_identification import assign_speakers_to_laughs
import librosa

# Load SNAC model
snac_model = load_snac_model(device="cpu")  # or "cuda" for GPU

# Prepare speaker reference samples
speaker_samples = {
    "speaker1": [audio1, audio2],  # Audio waveforms as numpy arrays
    "speaker2": [audio3, audio4]
}

# Process unidentified audio events
unidentified_events = [event1, event2]  # Audio waveforms as numpy arrays

# Identify speakers for each audio event
results = assign_speakers_to_laughs(speaker_samples, unidentified_events, snac_model)

# Print results
for speaker, events in results.items():
    print(f"Speaker {speaker} has {len(events)} attributed events")
```

### CLI Usage

```bash
pec-dss --speakers-dir ./speakers --unidentified-dir ./events --output-dir ./results
```

## 📁 Directory Structure

PEC-DSS expects a specific directory structure for processing audio files:

### Speaker Reference Structure

```
speakers_directory/
   ├── speaker_A/       # Each speaker's name becomes their ID
   │   ├── audio1.wav   # Reference voice samples for this speaker
   │   ├── audio2.wav
   │   └── ...
   ├── speaker_B/
   │   ├── audio1.wav
   │   └── ...
   └── speaker_C/
       ├── audio1.wav
       └── ...
```

### Unidentified Audio Structure

```
unidentified_directory/
   ├── laugh1.wav      # Non-linguistic vocal events to be classified
   ├── giggle1.wav
   └── ...
```

### Output Structure (After Processing)

```
output_directory/
   ├── results.json           # JSON file with all results
   ├── speaker_A/             # Files assigned to each speaker
   │   ├── 0_laugh1.wav
   │   └── ...
   ├── speaker_B/
   │   ├── 0_giggle1.wav
   │   └── ...
   └── unknown/               # Files below similarity threshold (if any)
       └── ...
```

## 🧩 System Architecture

PEC-DSS consists of the following components:

* **snac_model.py**: SNAC model initialization and management
* **audio_encoder.py**: Audio encoding and vectorization
* **codebook_analysis.py**: Statistical analysis of audio codebooks
* **speaker_identification.py**: Speaker identification algorithms
* **main.py**: Integration and execution framework

## 🔊 Audio Event Types

The system can identify various paralinguistic events including:

* Laughter
* Sighs
* Crying
* Coughing
* Other non-verbal vocal expressions

**Note:** PEC-DSS does not automatically classify these event types. It only determines which speaker produced the audio event.

## 🚀 Future Developments

* 🧠 Integration with more audio encoder models
* 😢 Expanded paralinguistic event recognition
* 🎵 Emotional tone classification
* ⚡ Performance optimization for real-time processing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the GNU General Public License v3.0.

## 🙏 Acknowledgements

* [SNAC](https://github.com/hubertsiuzdak/snac) - Scalable Neural Audio Codec
* [HuggingFace Transformers](https://huggingface.co/docs/transformers/index) - Machine learning tools
* [Llama](https://ai.meta.com/llama/) - Language models for text processing