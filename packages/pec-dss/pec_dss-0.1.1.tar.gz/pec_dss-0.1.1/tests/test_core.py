"""Basic tests for the core functionality of PEC-DSS."""
import pytest
import numpy as np

from pec_dss.core.speaker_identification import (
    calculate_speaker_average_vectors,
    identify_speaker_for_audio,
    assign_speakers_to_laughs,
)


class MockSNACModel:
    """Mock SNAC model for testing."""

    def __init__(self):
        self.quantizer = MockQuantizer()

    def encode(self, waveform):
        """Mock encode function."""
        batch_size = waveform.shape[0]
        # Return dummy codes for 3 codebooks
        return [
            np.zeros((batch_size, 10), dtype=np.int64),
            np.zeros((batch_size, 20), dtype=np.int64),
            np.zeros((batch_size, 40), dtype=np.int64),
        ]


class MockQuantizer:
    """Mock quantizer for testing."""

    def __init__(self):
        self.quantizers = [MockQuantizerLayer() for _ in range(3)]


class MockQuantizerLayer:
    """Mock quantizer layer for testing."""

    def __init__(self):
        self.codebook = MockCodebook()

    def embed_code(self, code):
        """Mock embed_code function."""
        batch_size = code.shape[0]
        code_len = code.shape[1]
        # Return a dummy embedding tensor
        return np.zeros((batch_size, code_len, 8), dtype=np.float32)


class MockCodebook:
    """Mock codebook for testing."""

    @property
    def weight(self):
        """Mock weight property."""
        return np.zeros((256, 8), dtype=np.float32)


@pytest.fixture
def mock_snac_model():
    """Create a mock SNAC model for testing."""
    return MockSNACModel()


@pytest.fixture
def speaker_audios():
    """Create test speaker audio samples."""
    return {
        "speaker1": [np.random.randn(24000) for _ in range(2)],
        "speaker2": [np.random.randn(24000) for _ in range(2)],
    }


@pytest.fixture
def unidentified_audios():
    """Create test unidentified audio samples."""
    return [np.random.randn(24000) for _ in range(3)]


def test_calculate_speaker_average_vectors(mock_snac_model, speaker_audios):
    """Test calculate_speaker_average_vectors function."""
    vectors = calculate_speaker_average_vectors(speaker_audios, mock_snac_model)
    assert "speaker1" in vectors
    assert "speaker2" in vectors
    assert len(vectors["speaker1"]) == 3  # Number of codebooks
    assert len(vectors["speaker2"]) == 3


def test_identify_speaker_for_audio(
    mock_snac_model, speaker_audios, unidentified_audios
):
    """Test identify_speaker_for_audio function."""
    speaker_vectors = calculate_speaker_average_vectors(speaker_audios, mock_snac_model)
    results = identify_speaker_for_audio(
        unidentified_audios, speaker_vectors, mock_snac_model
    )

    assert len(results) == len(unidentified_audios)

    for result in results:
        assert "identified_speaker" in result
        assert "similarity_score" in result
        assert "all_similarities" in result
        assert result["identified_speaker"] in ["speaker1", "speaker2"]


def test_assign_speakers_to_laughs(
    mock_snac_model, speaker_audios, unidentified_audios
):
    """Test assign_speakers_to_laughs function."""
    assignments = assign_speakers_to_laughs(
        speaker_audios, unidentified_audios, mock_snac_model
    )

    assert isinstance(assignments, dict)
    assert "speaker1" in assignments or "speaker2" in assignments

    total_assigned = sum(len(items) for items in assignments.values())
    assert total_assigned == len(unidentified_audios)
