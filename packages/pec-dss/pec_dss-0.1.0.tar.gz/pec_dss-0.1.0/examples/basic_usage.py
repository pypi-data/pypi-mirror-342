"""
Basic usage example for PEC-DSS.

This script demonstrates how to use the PEC-DSS library to identify
paralinguistic events and assign them to speakers.
"""
import os
import librosa
import numpy as np
import soundfile as sf

from pec_dss.models.snac_model import load_snac_model
from pec_dss.core.speaker_identification import assign_speakers_to_laughs


def main():
    # Use CPU for processing
    device = "cpu"

    # Load the SNAC model
    print("Loading SNAC model...")
    snac_model = load_snac_model(device)

    # Create some example data (you would normally load real audio files)
    # For demonstration, we'll just use noise as dummy data
    print("Preparing example data...")

    # Create dummy speaker reference samples
    speaker_audios = {
        "speaker1": [np.random.randn(24000) * 0.1 for _ in range(2)],
        "speaker2": [np.random.randn(24000) * 0.1 for _ in range(2)],
    }

    # Create dummy unidentified audio samples
    unidentified_audios = [np.random.randn(24000) * 0.1, np.random.randn(24000) * 0.1]

    # In a real scenario, you would load actual audio files:
    # speaker_audios = {
    #     "speaker1": [librosa.load("speaker1_sample1.wav", sr=24000)[0],
    #                 librosa.load("speaker1_sample2.wav", sr=24000)[0]],
    #     "speaker2": [librosa.load("speaker2_sample1.wav", sr=24000)[0],
    #                 librosa.load("speaker2_sample2.wav", sr=24000)[0]]
    # }
    # unidentified_audios = [
    #     librosa.load("laugh1.wav", sr=24000)[0],
    #     librosa.load("laugh2.wav", sr=24000)[0]
    # ]

    # Process the audio
    print("Processing audio samples...")
    results = assign_speakers_to_laughs(
        speaker_audios, unidentified_audios, snac_model, device, threshold=0.5
    )

    # Print results
    print("\nResults:")
    for speaker, assigned_audios in results.items():
        print(f"Speaker {speaker} has {len(assigned_audios)} assigned events")
        for i, item in enumerate(assigned_audios):
            print(f"  Event {i}: similarity score = {item['similarity_score']:.4f}")

    print("\nNote: This example uses random noise as audio data.")
    print("In a real application, you would use actual audio recordings.")


if __name__ == "__main__":
    main()
