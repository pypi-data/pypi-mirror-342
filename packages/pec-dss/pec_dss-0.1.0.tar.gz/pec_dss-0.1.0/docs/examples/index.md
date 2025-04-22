# Examples

This section provides examples demonstrating how to use PEC-DSS for various tasks and scenarios.

## Basic Examples

* [Basic Processor Example](basic_processor.md) - Learn how to use the `ParalinguisticEventProcessor` class to process audio files and identify speakers for paralinguistic events.

## Advanced Examples

* [Working with Different Audio Formats](../examples/audio_formats.md) - How to process different audio formats and handle various sampling rates.
* [Custom Processing Pipeline](../examples/custom_pipeline.md) - Build your own processing pipeline using the lower-level API.
* [Visualization](../examples/visualization.md) - Create visualizations of similarity scores and speaker assignments.

## CLI Examples

```bash
# Basic usage
pec-dss --speakers-dir ./speakers --unidentified-dir ./events --output-dir ./results

# Use GPU for processing
pec-dss --speakers-dir ./speakers --unidentified-dir ./events --use-gpu

# Set a higher threshold for more confident assignments
pec-dss --speakers-dir ./speakers --unidentified-dir ./events --threshold 0.7

# Process high-resolution audio
pec-dss --speakers-dir ./speakers --unidentified-dir ./events --sample-rate 44100

# Verbose mode for debugging
pec-dss --speakers-dir ./speakers --unidentified-dir ./events --verbose
```

## Example Projects

* **Podcast Analysis**: Attribute laughs and other reactions to specific podcast hosts and guests.
* **Meeting Transcription Enhancement**: Add speaker-attributed paralinguistic events to meeting transcripts.
* **Interview Processing**: Identify and analyze non-verbal responses in interviews.
 