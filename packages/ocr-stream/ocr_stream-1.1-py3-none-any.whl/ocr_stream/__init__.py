#!/usr/bin/env python3

from .models.m_modules_ocr import (
    LibraryOCR,
)

from .modules_ocr import TextRecognized
from .extractors import RecognizeImage, RecognizePdf
from ._version import __version__, __modify_data__

