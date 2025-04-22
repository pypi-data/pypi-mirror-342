# Installation Guide

This guide explains how to install PEC-DSS on your system.

## Requirements

PEC-DSS requires Python 3.8 or newer. The following dependencies will be automatically installed:

* torch >= 1.10.0
* torchaudio >= 0.10.0
* librosa >= 0.9.1
* soundfile >= 0.10.0
* numpy >= 1.20.0
* transformers >= 4.15.0
* huggingface_hub >= 0.4.0
* matplotlib >= 3.4.0

### SNAC Dependency

PEC-DSS uses the Scalable Neural Audio Codec (SNAC) for audio processing. This is a temporary solution and may be replaced in future versions. You need to install it separately:

```bash
pip install snac
```

## Installation Methods

### From PyPI (Recommended)

The simplest way to install PEC-DSS is from PyPI:

```bash
pip install pec-dss
```

This will install the latest stable version along with all dependencies except SNAC, which you need to install separately as mentioned above.

### From Source

To install the latest development version, you can install directly from the GitHub repository:

```bash
git clone https://github.com/hwk06023/PEC-DSS.git
cd PEC-DSS
pip install -e .
```

This creates an editable installation, where changes to the source code will be immediately available without reinstalling.

## GPU Support

PEC-DSS can use GPU acceleration through PyTorch. To enable GPU support, make sure you have:

1. A CUDA-compatible NVIDIA GPU
2. CUDA toolkit installed
3. PyTorch with CUDA support

You can install PyTorch with CUDA support following the instructions on the [PyTorch website](https://pytorch.org/get-started/locally/).

## Verifying Installation

To verify that PEC-DSS is installed correctly, you can run:

```bash
pec-dss --version
```

This should display the currently installed version.

## Development Installation

If you're planning to contribute to PEC-DSS, you can install the development dependencies:

```bash
pip install -e ".[dev]"
```

This installs additional packages like pytest for testing, black for code formatting, and other development tools.

## Troubleshooting

### Common Issues

**ImportError: No module named 'snac'**

Solution: Install the SNAC package:
```bash
pip install snac
```

**RuntimeError related to CUDA**

Solution: This usually means PyTorch was not installed with CUDA support or your CUDA version is incompatible. Try:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
(Replace `cu118` with your CUDA version)

**ImportError: cannot import name 'XXXX' from 'torchaudio'**

Solution: Your torchaudio version might be incompatible. Try:
```bash
pip install --upgrade torchaudio
```

**Issues with librosa**

Solution: Some librosa dependencies might be missing. Install:
```bash
pip install numba soxr
```

For any other issues, please check the [GitHub issues page](https://github.com/hwk06023/PEC-DSS/issues) or submit a new issue. 