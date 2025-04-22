"""
Advanced usage example for PEC-DSS.

This script demonstrates how to use the ParalinguisticEventProcessor class
for more advanced control over the paralinguistic event classification process.
"""
import os
import torch
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from pec_dss.core.processor import ParalinguisticEventProcessor


def visualize_similarities(results, output_path=None):
    """Create a visualization of similarity scores."""
    # Collect all speakers and their similarity scores
    all_speakers = set()
    event_data = []

    for speaker, assignments in results.items():
        for item in assignments:
            if "all_similarities" in item:
                all_speakers.update(item["all_similarities"].keys())
                event_data.append(item["all_similarities"])

    all_speakers = sorted(list(all_speakers))

    if not event_data:
        print("No similarity data available for visualization")
        return

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.arange(len(event_data))
    width = 0.8 / len(all_speakers)

    for i, speaker in enumerate(all_speakers):
        scores = [event.get(speaker, 0) for event in event_data]
        ax.bar(x + i * width - 0.4 + width / 2, scores, width, label=speaker)

    ax.set_xlabel("Event Index")
    ax.set_ylabel("Similarity Score")
    ax.set_title("Speaker Similarity Scores for Each Event")
    ax.set_xticks(x)
    ax.set_xticklabels([f"Event {i}" for i in range(len(event_data))])
    ax.legend()

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path)
        print(f"Visualization saved to {output_path}")
    else:
        plt.show()


def main():
    # Check if CUDA is available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # Initialize the processor
    processor = ParalinguisticEventProcessor(device=device)

    # Define directories
    # For this example, we'll use dummy data and create our own directories
    output_dir = "pec_dss_advanced_example"
    speakers_dir = os.path.join(output_dir, "speakers")
    unidentified_dir = os.path.join(output_dir, "unidentified")
    results_dir = os.path.join(output_dir, "results")

    # Create directories
    os.makedirs(speakers_dir, exist_ok=True)
    os.makedirs(unidentified_dir, exist_ok=True)

    # Create subdirectories for each speaker
    speaker1_dir = os.path.join(speakers_dir, "speaker1")
    speaker2_dir = os.path.join(speakers_dir, "speaker2")
    os.makedirs(speaker1_dir, exist_ok=True)
    os.makedirs(speaker2_dir, exist_ok=True)

    # Generate and save dummy audio files
    # In a real scenario, you would use actual audio recordings

    print("Generating dummy audio files...")

    # Generate speaker reference samples
    for i in range(2):
        # Speaker 1 - lower frequency content
        audio1 = np.sin(2 * np.pi * 200 * np.arange(24000) / 24000) * 0.5
        audio1 += np.random.randn(24000) * 0.1

        # Speaker 2 - higher frequency content
        audio2 = np.sin(2 * np.pi * 400 * np.arange(24000) / 24000) * 0.5
        audio2 += np.random.randn(24000) * 0.1

        # Save files
        np.save(os.path.join(speaker1_dir, f"sample_{i}.npy"), audio1)
        np.save(os.path.join(speaker2_dir, f"sample_{i}.npy"), audio2)

    # Generate unidentified samples (mix of both speakers)
    for i in range(3):
        # Alternate between speaker characteristics
        if i % 2 == 0:
            # More like speaker 1
            audio = np.sin(2 * np.pi * 210 * np.arange(24000) / 24000) * 0.5
        else:
            # More like speaker 2
            audio = np.sin(2 * np.pi * 390 * np.arange(24000) / 24000) * 0.5

        audio += np.random.randn(24000) * 0.15
        np.save(os.path.join(unidentified_dir, f"event_{i}.npy"), audio)

    # Load speaker reference data from numpy files
    print("Loading speaker reference data...")
    speaker_audios = {}
    for speaker_dir in os.listdir(speakers_dir):
        speaker_path = os.path.join(speakers_dir, speaker_dir)
        if os.path.isdir(speaker_path):
            samples = []
            for file in os.listdir(speaker_path):
                if file.endswith(".npy"):
                    samples.append(np.load(os.path.join(speaker_path, file)))
            if samples:
                speaker_audios[speaker_dir] = samples

    # Load unidentified events
    print("Loading unidentified events...")
    unidentified_audios = []
    unidentified_paths = []
    for file in os.listdir(unidentified_dir):
        if file.endswith(".npy"):
            file_path = os.path.join(unidentified_dir, file)
            unidentified_audios.append(np.load(file_path))
            unidentified_paths.append(file_path)

    # Process the data
    print("Processing audio data...")
    processor.load_model()
    results = processor.process_paralinguistic_events(
        speaker_audios,
        unidentified_audios,
        threshold=0.4,  # Use a slightly lower threshold for this example
    )

    # Save results
    print("Saving results...")
    processor.save_results(results, results_dir, unidentified_paths)

    # Print summary
    print("\nResults Summary:")
    for speaker, assigned in results.items():
        print(f"Speaker {speaker}: {len(assigned)} assigned events")
        for i, item in enumerate(assigned):
            print(f"  Event {i}: similarity score = {item['similarity_score']:.4f}")

    # Visualize results
    print("\nGenerating visualization...")
    os.makedirs(os.path.join(results_dir, "plots"), exist_ok=True)
    visualize_similarities(
        results, output_path=os.path.join(results_dir, "plots", "similarity_scores.png")
    )

    print("\nNote: This example uses synthetic audio data.")
    print("In a real application, you would use actual audio recordings.")
    print(f"Results saved to {results_dir}")


if __name__ == "__main__":
    main()
