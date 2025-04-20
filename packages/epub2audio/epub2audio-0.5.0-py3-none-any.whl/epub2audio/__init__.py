"""EPUB to Audiobook converter package."""

from ._version import __version__, version
from .audio_converter import AudioConverter
from .audio_handler import AudioHandler
from .config import ErrorCodes, WarningTypes
from .epub2audio import main, process_epub
from .epub_processor import BookMetadata, Chapter, EpubProcessor
from .helpers import ConversionError, ConversionWarning
from .voices import Voice, VoiceInfo, available_voices

__author__ = "Clay Rosenthal"
__email__ = "epub2audio@mail.clayrosenthal.me"

__all__ = [
    "main",
    "process_epub",
    "ErrorCodes",
    "WarningTypes",
    "EpubProcessor",
    "Chapter",
    "BookMetadata",
    "AudioConverter",
    "AudioHandler",
    "ConversionError",
    "ConversionWarning",
    "__version__",
    "version",
    "available_voices",
    "Voice",
    "VoiceInfo",
]
