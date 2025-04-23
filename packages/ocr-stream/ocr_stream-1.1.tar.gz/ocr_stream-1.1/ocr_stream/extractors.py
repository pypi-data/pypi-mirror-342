#!/usr/bin/env python3
from __future__ import annotations

from ocr_stream.utils import (
    File, 
    Directory, 
    ImageObject, 
    DataFrame, 
    PageDocumentPdf, 
    DocumentPdf, 
    PdfStream, 
    LibraryPDF,    
)

from ocr_stream.models import ( 
    ABCRecognizeImage,
    LibraryOCR,
)

from ocr_stream.modules_ocr import ModuleOcr, TextRecognized

class RecognizeImage(ABCRecognizeImage):
    def __init__(self, module_ocr):
        super().__init__(module_ocr)

    def image_content_data(self, img: ImageObject | File) -> DataFrame:
        if isinstance(img, File):
            return self.module_ocr.image_content_data(ImageObject.create_from_file(img))
        elif isinstance(img, ImageObject):
            return self.module_ocr.image_content_data(img)
        else:
            raise ValueError(f'{__class__.__name__}\nUse: ImageObject() ou File(), não {type(img)}')
    
    def image_recognize(self, img: ImageObject | File) -> TextRecognized:
        if isinstance(img, File):
            return self.module_ocr.image_recognize(ImageObject.create_from_file(img))
        elif isinstance(img, ImageObject):
            return self.module_ocr.image_recognize(img)
        else:
            raise ValueError(f'{__class__.__name__}\nUse: ImageObject() ou File(), não {type(img)}')
    
    def image_to_string(self, img: ImageObject | File) -> str:
        if isinstance(img, File):
            return self.module_ocr.imag_to_string(ImageObject.create_from_file(img))
        elif isinstance(img, ImageObject):
            return self.module_ocr.imag_to_string(img)
        else:
            raise ValueError(f'{__class__.__name__}\nUse: ImageObject() ou File(), não {type(img)}')
    
    @classmethod
    def create(cls, library_ocr=LibraryOCR.PYTESSERACT, *, path_tesseract, lang=None, tess_data_dir=None) -> RecognizeImage:
        module_ocr:ModuleOcr = ModuleOcr.create(
            library_ocr,
            path_tesseract=path_tesseract,
            lang=lang,
            tess_data_dir=tess_data_dir
        )
        return cls(module_ocr)
  
  
class RecognizePdf(object):
    def __init__(self, recognize_image:RecognizeImage):
        self.recognize_image:RecognizeImage = recognize_image

    def recognize_page_pdf(self, page:PageDocumentPdf) -> PageDocumentPdf:
        """
            Converte a página em Imagem, reconhece o texto com OCR e
        retorna uma nova página com o texto reconhecido.
        """
        pdf_stream = PdfStream(library_pdf=LibraryPDF.FITZ)
        pdf_stream.add_page(page)
        img:ImageObject = pdf_stream.to_images()[0]
        text_recognized:TextRecognized = self.recognize_image.image_recognize(img)
        return text_recognized.to_page_pdf()
    
    def recognize_document(self, doc:DocumentPdf) -> DocumentPdf:
        new:DocumentPdf = DocumentPdf()
        for page in doc.pages:
            recognized_page:PageDocumentPdf = self.recognize_page_pdf(page)
            new.add_page(recognized_page)
        return new

    @classmethod
    def create(
                cls, 
                library_ocr=LibraryOCR.PYTESSERACT, 
                *,
                path_tesseract:File, 
                lang:str=None,
                tess_data_dir:Directory=None,
            ) -> RecognizePdf:
        ##
        recognize_image = RecognizeImage.create(
                    library_ocr, 
                    path_tesseract=path_tesseract, 
                    lang=lang, 
                    tess_data_dir=tess_data_dir
                )
        return cls(recognize_image)
   

            
        
        
        
        
        

