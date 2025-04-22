# Basic ParalinguisticEventProcessor Example

This example demonstrates how to use the main `ParalinguisticEventProcessor` class to process audio files and identify speakers for paralinguistic events.

## Setup

First, let's import the necessary modules and set up the processor:

```python
import os
import torch
from pec_dss.core.processor import ParalinguisticEventProcessor

# Check if GPU is available and initialize processor
device = "cuda" if torch.cuda.is_available() else "cpu"
processor = ParalinguisticEventProcessor(device=device)
```

## Directory Structure

For this example, we'll assume you have a directory structure like this:

```
my_project/
├── speakers/
│   ├── speaker1/
│   │   ├── reference1.wav
│   │   └── reference2.wav
│   └── speaker2/
│       ├── reference1.wav
│       └── reference2.wav
├── events/
│   ├── laugh1.wav
│   ├── laugh2.wav
│   └── sigh1.wav
└── results/
```

## Running the Pipeline

The simplest way to process your audio files is to use the `run_pipeline` method, which handles all the steps for you:

```python
results = processor.run_pipeline(
    speakers_dir="speakers",
    unidentified_dir="events",
    output_dir="results",
    threshold=0.6  # Set a threshold for similarity matching
)
```

## Understanding the Results

After running the pipeline, the `results` variable will contain a dictionary mapping speaker IDs to lists of assigned audio events:

```python
# Print summary of results
print("Results Summary:")
for speaker, events in results.items():
    print(f"Speaker '{speaker}' has {len(events)} assigned events with similarity scores:")
    for i, event in enumerate(events):
        print(f"  Event {i}: {event['similarity_score']:.4f}")
```

The results are also saved to the `results` directory with this structure:

```
results/
├── results.json           # Detailed results in JSON format
├── speaker1/              # Directory for each speaker
│   └── 0_laugh1.wav       # Assigned audio files
└── speaker2/
    ├── 0_laugh2.wav
    └── 1_sigh1.wav
```

## Manual Processing Steps

If you want more control over the processing steps, you can use the individual methods:

```python
# Load the model
processor.load_model()

# Load speaker references
speaker_audios = processor.load_speaker_references("speakers")

# Load unidentified events
events = processor.load_audio_directory("events")
unidentified_audios = list(events.values())
unidentified_paths = list(events.keys())

# Process events
results = processor.process_paralinguistic_events(
    speaker_audios, 
    unidentified_audios,
    threshold=0.6
)

# Save results
processor.save_results(results, "results", unidentified_paths)
```

## Full Example

Here's a complete example script:

```python
import os
import torch
from pec_dss.core.processor import ParalinguisticEventProcessor

def process_audio_files():
    # Initialize processor
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    processor = ParalinguisticEventProcessor(device=device)
    
    # Define directories
    speakers_dir = "speakers"
    events_dir = "events"
    results_dir = "results"
    
    # Ensure directories exist
    os.makedirs(results_dir, exist_ok=True)
    
    # Run the pipeline
    print("Processing audio files...")
    results = processor.run_pipeline(
        speakers_dir=speakers_dir,
        unidentified_dir=events_dir,
        output_dir=results_dir,
        threshold=0.6
    )
    
    # Print results
    print("\nResults Summary:")
    for speaker, events in results.items():
        print(f"Speaker '{speaker}' has {len(events)} assigned events:")
        for i, event in enumerate(events):
            print(f"  Event {i}: similarity score = {event['similarity_score']:.4f}")
    
    print(f"\nResults saved to: {results_dir}")

if __name__ == "__main__":
    process_audio_files() 