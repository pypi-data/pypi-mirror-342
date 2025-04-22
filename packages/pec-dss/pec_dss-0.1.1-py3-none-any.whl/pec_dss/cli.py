"""Command-line interface for PEC-DSS."""
import argparse
import logging
import sys
import os
import torch

from pec_dss import __version__
from pec_dss.core.processor import ParalinguisticEventProcessor


def configure_logging(verbose=False):
    """Configure logging for the CLI."""
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def create_parser():
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="PEC-DSS: Paralinguistic Event Classification from Diarized Speaker Segments",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("--version", action="version", version=f"PEC-DSS {__version__}")

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    parser.add_argument(
        "--speakers-dir",
        required=True,
        help="Directory containing speaker reference audio samples",
    )

    parser.add_argument(
        "--unidentified-dir",
        required=True,
        help="Directory containing unidentified audio samples",
    )

    parser.add_argument(
        "--output-dir", default="pec_dss_results", help="Directory to save results"
    )

    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="Similarity threshold for speaker assignment (0.0-1.0)",
    )

    parser.add_argument(
        "--sample-rate",
        type=int,
        default=24000,
        help="Sample rate to use for audio processing",
    )

    parser.add_argument(
        "--use-gpu", action="store_true", help="Use GPU for processing if available"
    )

    return parser


def main():
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()

    configure_logging(args.verbose)
    logger = logging.getLogger("pec_dss")

    logger.info(f"PEC-DSS version {__version__}")

    # Check if speakers directory exists
    if not os.path.isdir(args.speakers_dir):
        logger.error(f"Speakers directory not found: {args.speakers_dir}")
        return 1

    # Check if unidentified directory exists
    if not os.path.isdir(args.unidentified_dir):
        logger.error(f"Unidentified audio directory not found: {args.unidentified_dir}")
        return 1

    # Determine device
    device = "cpu"
    if args.use_gpu and torch.cuda.is_available():
        device = "cuda"
        logger.info("Using GPU for processing")
    else:
        if args.use_gpu:
            logger.warning("GPU requested but not available, falling back to CPU")
        else:
            logger.info("Using CPU for processing")

    # Process the audio files
    try:
        processor = ParalinguisticEventProcessor(device=device)

        logger.info(f"Processing audio files...")
        logger.info(f"Speaker references: {args.speakers_dir}")
        logger.info(f"Unidentified audio: {args.unidentified_dir}")
        logger.info(f"Output directory: {args.output_dir}")
        logger.info(f"Similarity threshold: {args.threshold}")

        results = processor.run_pipeline(
            speakers_dir=args.speakers_dir,
            unidentified_dir=args.unidentified_dir,
            output_dir=args.output_dir,
            threshold=args.threshold,
            sr=args.sample_rate,
        )

        # Print summary
        logger.info("Processing complete!")
        logger.info("Speaker assignment summary:")
        for speaker, assigned in results.items():
            logger.info(f"  {speaker}: {len(assigned)} audio samples")

        return 0

    except Exception as e:
        logger.error(f"Error during processing: {e}", exc_info=args.verbose)
        return 1


if __name__ == "__main__":
    sys.exit(main())
