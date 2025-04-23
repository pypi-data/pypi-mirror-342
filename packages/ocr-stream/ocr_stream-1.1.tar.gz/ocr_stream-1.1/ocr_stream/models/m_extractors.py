#!/usr/bin/env python3
#
from __future__ import annotations
from abc import ABC, abstractmethod

from pandas import DataFrame
from soup_files import File, Directory
from convert_stream import ImageObject
from ocr_stream.models.m_modules_ocr import ABCModuleOcr, ABCTextRecognized, LibraryOCR

class ABCRecognizeImage(ABC):
    def __init__(self, module_ocr:ABCModuleOcr):
        super().__init__()
        self.module_ocr:ABCModuleOcr = module_ocr
        
    @abstractmethod
    def image_to_string(self, img:ImageObject | File) -> str:
        pass
    
    @abstractmethod
    def image_recognize(self, img:ImageObject | File) -> ABCTextRecognized:
        pass
        
    @abstractmethod
    def image_content_data(self, img:ImageObject | File) -> DataFrame:
        pass
        
    @classmethod
    def create(
                cls, 
                library_ocr:LibraryOCR = LibraryOCR.PYTESSERACT,
                *,
                path_tesseract:File, 
                lang:str=None, 
                tess_data_dir:Directory=None
            ) -> ABCRecognizeImage:
        pass

    
