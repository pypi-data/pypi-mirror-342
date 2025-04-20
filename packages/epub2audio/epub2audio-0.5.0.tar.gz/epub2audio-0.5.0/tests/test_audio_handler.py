"""Unit tests for audio file handling module."""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from mutagen.oggopus import OggOpus
from soundfile import SoundFile

from epub2audio.audio_handler import AudioHandler
from epub2audio.config import ErrorCodes
from epub2audio.epub_processor import BookMetadata
from epub2audio.helpers import AudioHandlerError


@pytest.fixture
def sample_metadata() -> BookMetadata:
    """Create sample book metadata."""
    return BookMetadata(
        title="Test Book",
        creator="Test Author",
        date="2025",
        identifier="id123",
        language="en",
        publisher="Test Publisher",
        description="Test Description",
    )


@pytest.fixture
def audio_handler(tmp_path: Path, sample_metadata: BookMetadata) -> AudioHandler:
    """Create an AudioHandler instance."""
    epub_path = str(tmp_path / "test.epub")
    output_path = str(tmp_path / "test.ogg")
    # Create an empty epub file for testing
    with open(epub_path, "w") as f:
        f.write("dummy content")
    return AudioHandler(epub_path, output_path, sample_metadata, quiet=True)


def test_audio_handler_init(
    audio_handler: AudioHandler, sample_metadata: BookMetadata
) -> None:
    """Test AudioHandler initialization."""
    assert audio_handler is not None
    assert audio_handler.metadata == sample_metadata
    assert audio_handler.chapter_markers == []
    assert audio_handler.total_chapters == 0
    assert audio_handler.total_duration == 0.0


def test_add_chapter_marker(audio_handler: AudioHandler) -> None:
    """Test adding chapter markers."""
    audio_handler.add_chapter_marker("Chapter 1", 0.0, 10.0)
    audio_handler.add_chapter_marker("Chapter 2", 10.0, 20.0)

    assert len(audio_handler.chapter_markers) == 2

    # Check first chapter marker
    first_chapter = audio_handler.chapter_markers[0]
    assert first_chapter.title == "Chapter 1"
    assert first_chapter.start_time == 0.0
    assert first_chapter.end_time == 10.0
    assert first_chapter.start_time_str == "00:00:00.000"
    assert first_chapter.end_time_str == "00:00:10.000"

    # Check second chapter marker
    second_chapter = audio_handler.chapter_markers[1]
    assert second_chapter.title == "Chapter 2"
    assert second_chapter.start_time == 10.0
    assert second_chapter.end_time == 20.0
    assert second_chapter.start_time_str == "00:00:10.000"
    assert second_chapter.end_time_str == "00:00:20.000"


def test_write_metadata(
    audio_handler: AudioHandler, sample_metadata: BookMetadata
) -> None:
    """Test writing metadata to audio file."""
    mock_audio_file = Mock(spec=OggOpus)
    mock_audio_file.__setitem__ = Mock()

    audio_handler.add_chapter_marker("Chapter 1", 0.0, 10.0)
    with patch.object(audio_handler, "_write_vorbis_metadata") as mock_write_vorbis:
        audio_handler._write_metadata(mock_audio_file)
        mock_write_vorbis.assert_called_once_with(mock_audio_file)


def test_finalize_audio_file(audio_handler: AudioHandler, tmp_path: Path) -> None:
    """Test finalizing audio file."""
    # Create a mock audio segment
    mock_segment = Mock(spec=SoundFile)
    mock_segment.name = str(tmp_path / "test_segment.ogg")
    mock_segment.close = Mock()

    # Create mock for concatenate_segments
    with patch.object(audio_handler, "_concatenate_segments") as mock_concatenate:
        mock_concatenate.return_value = mock_segment

        with patch("epub2audio.audio_handler.SUPPORTED_AUDIO_FORMATS") as mock_formats:
            # Mock the types
            mock_type = type("MockOggOpus", (), {})
            format_info_mock = Mock()
            format_info_mock.file_class = mock_type
            mock_formats.__getitem__.return_value = format_info_mock

            # Mock the type initialization
            mock_file_instance = Mock()
            with patch.object(mock_type, "__new__", return_value=mock_file_instance):
                # Mock the file operations
                with patch.object(
                    audio_handler, "_write_metadata"
                ) as mock_write_metadata:
                    # Mock shutil.move to prevent file operation
                    with patch("epub2audio.audio_handler.move") as mock_move:
                        audio_handler.finalize_audio_file([mock_segment])

                        # Check if metadata was written
                        mock_formats.__getitem__.assert_called_with(
                            audio_handler.extension
                        )
                        mock_write_metadata.assert_called_once_with(mock_file_instance)
                        mock_file_instance.save.assert_called_once()
                        # Check file was moved
                        mock_move.assert_called_once_with(
                            mock_segment.name, audio_handler.output_path
                        )


def test_finalize_audio_file_error(audio_handler: AudioHandler, tmp_path: Path) -> None:
    """Test error handling in finalize_audio_file."""
    # Create a mock audio segment
    mock_segment = Mock(spec=SoundFile)
    mock_segment.name = str(tmp_path / "test_segment.ogg")
    mock_segment.close = Mock()

    # Create mock for concatenate_segments
    with patch.object(audio_handler, "_concatenate_segments") as mock_concatenate:
        mock_concatenate.return_value = mock_segment

        with patch("epub2audio.audio_handler.SUPPORTED_AUDIO_FORMATS") as mock_formats:
            # Set up mock to raise an exception
            file_class_mock = Mock(side_effect=Exception("Save error"))
            format_info_mock = Mock()
            format_info_mock.file_class = file_class_mock
            mock_formats.__getitem__.return_value = format_info_mock

            with pytest.raises(AudioHandlerError) as exc_info:
                audio_handler.finalize_audio_file([mock_segment])
            assert exc_info.value.error_code == ErrorCodes.FILESYSTEM_ERROR


def test_total_chapters(audio_handler: AudioHandler) -> None:
    """Test total chapters property."""
    assert audio_handler.total_chapters == 0

    audio_handler.add_chapter_marker("Chapter 1", 0.0, 10.0)
    assert audio_handler.total_chapters == 1

    audio_handler.add_chapter_marker("Chapter 2", 10.0, 20.0)
    assert audio_handler.total_chapters == 2


def test_total_duration(audio_handler: AudioHandler) -> None:
    """Test total duration property."""
    assert audio_handler.total_duration == 0.0

    audio_handler.add_chapter_marker("Chapter 1", 0.0, 10.0)
    assert audio_handler.total_duration == 10.0

    audio_handler.add_chapter_marker("Chapter 2", 10.0, 20.0)
    assert audio_handler.total_duration == 20.0
