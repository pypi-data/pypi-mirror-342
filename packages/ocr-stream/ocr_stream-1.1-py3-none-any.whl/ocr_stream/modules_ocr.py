#!/usr/bin/env python3
from __future__ import annotations
from types import ModuleType
from typing import List, Dict
from pathlib import Path
import re
import os

from ocr_stream.models import ( 
    ABCModuleOcr,
    ABCTextRecognized,
    LibraryOCR,
)
from pandas import DataFrame
from ocr_stream.utils import (
    PageDocumentPdf, DocumentPdf, LibraryImage, ImageObject, ArrayString, DataString,
    File, Directory
)

from pytesseract import pytesseract, Output

def get_temp_dir(prefix=Path().home()) -> str:
    prefix = Path().home()
    sys_temp_dir = os.environ.get('TMP', os.path.join(prefix, 'var', 'temp'))
    if not sys_temp_dir:
        sys_temp_dir = os.path.join(prefix, 'var', 'temp')
    if not os.path.exists(sys_temp_dir):
        try:
            os.makedirs(sys_temp_dir)
        except Exception as e:
            print(e)
    os.environ["TEMP"] = sys_temp_dir
    print('-' * 30)
    print(f'Diretório temporário: {sys_temp_dir}')
    print('-' * 30)
    return sys_temp_dir

  
class TextRecognizedToi(object):
    """
        Extração/Filtro de texto em documentos do tipo carta TOI.
    """
    def __init__(self, value:str=None, *, separator:str='\n', column_text='TEXT', file:File):
        # Todas as linhas que foram reconhecidas em uma imagem/página PDF.
        if not isinstance(value, str):
            raise ValueError(f'{__class__.__name__}Use: str, não {type(value)}')
        self.text_document:str = DataString(value).to_upper().value if value is not None else None
        self.separator:str = separator
        self.file:File = file
        self.column_text:str = column_text
        
        self.pattern_line_uc_toi = r'UC:\s*\d+\s*TOI:\s*\d+'
        self.pattern_uc = r'\b(?:UC:?|UC):?\s*(\d+)'
        self.pattern_toi = r'\b(?:TOI?|TO):?\s*(\d+)'
        self.pattern_localidade = r'LOCALIDADE:\s*(.*)'
        
        self.words_toi = (
            'TO]!', 'TO]', 'TOl', 'TOI', 'TOI:'
        )
        
        self.words_uc = (
            'UE', 'UE:' 'UC', 'UC:', 'JC;'
        )
        
    def __replace_chars(self, text, char, new_char) -> str:
        return re.sub(r'{}'.format(char), new_char, text)
    
    def __get_match_groups(self, pattern, text:str) -> object | None:
        i = re.search(pattern, text)
        if i is None:
            return None
        return i.groups()
        
    def __get_match_group(self, pattern, text:str) -> object | None:
        i = re.search(pattern, text)
        if i is None:
            return None
        return i.group()
    
    def is_null(self) -> bool:
        if self.text_document is None:
            return True
        if self.text_document == '':
            return True
        return False
        
    def to_string(self) -> str | None:
        return DataString(self.text_document).to_upper().value if not self.is_null() else None
    
    def to_list(self) -> List[str]:
        return self.text_document.split(self.separator)
    
    def to_array_string(self) -> ArrayString:
        values:List[str] = self.to_list()
    
    def to_upper(self) -> TextRecognizedToi:
        self.text_document = self.text_document.upper()
        return self
    
    def to_dataframe(self) -> DataFrame:
        uc = self.uc()
        toi = self.toi()
        if uc is None:
            uc = 'nan'
        else:
            uc = DataString(uc).replace_bad_chars().replace_all('- ', ' ').replace_all('_', ' ').value.strip()
        #
        if toi is None:
            toi = 'nan'
        else:
            toi = DataString(toi).replace_bad_chars()
            toi = toi.replace_all('- ', '-').replace_all('_', ' ').replace_all('-', ' ').replace_all('TOI', '').value.strip()
        
        df = DataFrame()
        df[self.column_text] = self.to_list()
        num = len(df)
        df['UC'] = [uc] * num
        df['TOI'] = [toi] * num
        df['LOCALIDADE'] = [self.localidade()] * num
        df['ARQUIVO'] = [self.file.absolute()] * num
        df['MD5'] = [self.file.md5()] * num
        return df
    
    def remove_bad_chars(self) -> TextRecognizedToi:
        values = []
        for item in self.to_list():
            values.append(
                DataString(item).replace_bad_chars(new_char='_').replace_all('/', '-').value
            )
        self.listText = values
        return self
    
    def uc(self) -> str:
        """
            Extrair o número da UC em forma de string, se a operação falhar, será retornado (nan)
        """
        line_uc_toi = self.line_uc_and_toi()
        uc_value:str = None
        if line_uc_toi is not None:
            uc_value = self.__get_match_group(self.pattern_uc, line_uc_toi)
        if uc_value is not None:
            return uc_value.replace('UC', '')
        
        arr = ArrayString(self.text_document.split(' '))
        for w in self.words_uc:
            out = arr.get_next(w).value
            try:
                int(out)
            except:
                pass
            else:
                return out
        return None
    
    def toi(self) -> str:
        line_uc_toi = self.line_uc_and_toi()
        toi_value:str = None
        if line_uc_toi is not None:
            toi_value = self.__get_match_group(self.pattern_toi, line_uc_toi)
        if toi_value is not None:
            return toi_value.replace('TOI', '')
        arr = ArrayString(self.text_document.split(' '))
        
        for w in self.words_toi:
            out = arr.get_next(w).value
            try:
                int(out)
            except:
                pass
            else:
                return out
        return None
        
    def roteiro(self) -> str:
        self.remove_bad_chars()
        pass

    def localidade(self) -> str:
        lines = self.to_list()
        loc = 'nan'
        for line in lines:
            out = re.search(self.pattern_localidade, line)
            if out:
                loc = out.group(1)
                break
        loc = DataString(loc).replace_all(' ').value
        # Remover "_" do final
        return re.sub(r"_$", "", loc)
    
    def line_postagem(self) -> str:
        pass
        
    def line_uc_and_toi(self) -> DataString | None:
        line_toi = None
        lines = self.to_list()
        for item in lines:
            out = self.__get_match_group(self.pattern_line_uc_toi, item)
            if out is None:
                continue
            line_toi = out
            break
        return line_toi
    
    def line_roteiro(self) -> DataString:
        return DataString(None) 

#======================================================================#
# Texto reconhecido de uma imagem.
#======================================================================#
class TextRecognized(ABCTextRecognized):
    """
        Recebe os bytes de uma página PDF reconhecida de imagem
    e exporta para vários tipos de dados.
    -> DataFrame()
    -> str
    -> PageDocumentPdf()
    """
    def __init__(self, bytes_recognized):
        super().__init__(bytes_recognized)
        
        self.list_bad_char:List[str] = [
                            ':', ',', ';', '$', '=', 
                            '!', '}', '{', '(', ')', 
                            '|', '\\', '‘', '*'
                            '¢', '“', '\'', '¢', '"', 
                            '#', '.', '<', '?', '>', 
                            '»', '@', '+', '[', ']',
                            '%', '~', '¥', '♀',
        ]
    
    def to_string(self) -> str | None:
        return self.to_page_pdf().to_string()
    
    def to_page_pdf(self) -> PageDocumentPdf:
        return PageDocumentPdf.create_from_page_bytes(self.bytes_recognized)
    
    def to_document(self) -> DocumentPdf:
        doc: DocumentPdf = DocumentPdf()
        doc.add_page(self.to_page_pdf())
        return doc
    
    def to_dict(self, separator:str='\n') -> Dict[str, List[str]]:
        image_dict:Dict[str, List[str]] = {
            'TEXT': [],
            'NUM_LINHA': [],
        }
        image_text:str = self.to_string()
        if (image_text is None) or (image_text == ''):
            return {
                    'TEXT': ['nan'],
                    'NUM_LINHA': ['nan'],
                }
        
        image_lines:List[str] = image_text.split(separator)
        for num, line in enumerate(image_lines):
            image_dict['TEXT'].append(line)
            image_dict['NUM_LINHA'].append(num+1)
        return image_dict    
    
    def to_dataframe(self, column = 'TEXT', separator:str='\n') -> DataFrame:
        return DataFrame(self.to_dict(separator))
    
#======================================================================#
# Modulo OCR pytesseract
#======================================================================#

class IModulePytesseract(ABCModuleOcr):
    def __init__(self, *, cmd_executable, lang = None, tess_data_dir = None):
        super().__init__(cmd_executable=cmd_executable, lang=lang, tess_data_dir=tess_data_dir)
        self.current_library:LibraryOCR = LibraryOCR.PYTESSERACT
        self._pyTesseract:pytesseract = pytesseract
        self._pyTesseract.tesseract_cmd = self.cmd_executable.absolute()
        
    def __get_tess_dir_config(self) -> str | None:
        """
        https://github.com/h/pytesseract
        
        Example config: r'--tessdata-dir "C:\Program Files (x86)\Tesseract-OCR\tessdata"'
        tessdata_dir_config = r'--tessdata-dir <replace_with_your_tessdata_dir_path>'
        It's important to add double quotes around the dir path.
        """
        #
        # Caminho para os dados de idioma, por, eng etc...
        # os.environ["TESSDATA_PREFIX"] = self.tess_data_dir.absolute()
        if self.tess_data_dir is None:
            return ''
        if not self.tess_data_dir.path.exists():
            return ''
        return r'--tessdata-dir "{}"'.format(self.tess_data_dir.absolute())
        
    def imag_to_string(self, img) -> str:
        if img.current_library == LibraryImage.OPENCV:
            text_img:str = self._pyTesseract.image_to_string(
                img.to_image_opencv(),
                lang=self.lang,
                config=self.__get_tess_dir_config()
            )
        else:
            text_img:str = self._pyTesseract.image_to_string(
                    img.to_image_pil(),
                    lang=self.lang,
                    config=self.__get_tess_dir_config()
                )
        return text_img
        
    def image_recognize(self, img) -> TextRecognized:
        if img.current_library == LibraryImage.OPENCV:
            pdf_bytes:bytes = self._pyTesseract.image_to_pdf_or_hocr(
                img.to_image_opencv(),
                lang=self.lang,
                config=self.__get_tess_dir_config()
            )
        else:
            pdf_bytes:bytes = self._pyTesseract.image_to_pdf_or_hocr(
                    img.to_image_pil(),
                    lang=self.lang,
                    config=self.__get_tess_dir_config()
                )
        return TextRecognized(pdf_bytes)
        
    def image_content_data(self, img) -> DataFrame:
        if img.current_library == LibraryImage.OPENCV:
            text_data:DataFrame = self._pyTesseract.image_to_data(
                img.to_image_opencv(),
                lang=self.lang,
                config=self.__get_tess_dir_config(),
                output_type=Output.DATAFRAME,
            )
        else:
            text_data:DataFrame = self._pyTesseract.image_to_data(
                img.to_image_pil(),
                lang=self.lang,
                config=self.__get_tess_dir_config(),
                output_type=Output.DATAFRAME,
            )
        return text_data
    
   
#======================================================================#
# Modulo OCR pyocr
#======================================================================#

class IModulePyOcr(ABCModuleOcr):
    def __init__(self, *, cmd_executable, lang = None, tess_data_dir = None):
        super().__init__(cmd_executable=cmd_executable, lang=lang, tess_data_dir=tess_data_dir)
        self.current_library:LibraryOCR = LibraryOCR.PYOCR
        self.cmd_executable:File = cmd_executable
        self.tess_data_dir:Directory = tess_data_dir
        try:
            import pyocr
            import pyocr.tesseract
        except Exception as e:
            raise (e)
        
        pyocr_modules:List[ModuleType] = pyocr.get_available_tools()
        if len(pyocr_modules) == 0:
            raise ValueError(f"{__class__.__name__} No OCR tool found")
        # The tools are returned in the recommended order of usage
        self._pyOcr:pyocr.tesseract = pyocr_modules[0]
        langs:List[str] = self._pyOcr.get_available_languages()
        if lang in lang:
            self.lang = lang
        else:
            self.lang = langs[0]
        
        # Ex: Will use tool 'libtesseract'
        print(f"Will use tool {self._pyOcr.get_name()}")
        
    def imag_to_string(self, img) -> str:
        return self._pyOcr.image_to_string(
            img.to_image_pil(),
            lang=self.lang,
            builder=pyocr.builders.TextBuilder()
        )
        
    def image_recognize(self, img) -> TextRecognized:
        raise NotImplementedError(f'{__class__.__name__} método não implementado')
        
    def image_content_data(self, img) -> DataFrame:
        raise NotImplementedError(f'{__class__.__name__} método não implementado')
    

class ModuleOcr(ABCModuleOcr):
    def __init__(self, module_ocr:ABCModuleOcr):
        super().__init__(
                cmd_executable=module_ocr.cmd_executable, 
                lang=module_ocr.lang, 
                tess_data_dir=module_ocr.tess_data_dir
            )
        self.module_ocr:ABCModuleOcr = module_ocr
        
    def image_content_data(self, img:ImageObject) -> DataFrame:
        return self.module_ocr.image_content_data(img)
    
    def image_recognize(self, img:ImageObject) -> TextRecognized:
        return self.module_ocr.image_recognize(img)
    
    def imag_to_string(self, img) -> str:
        return self.module_ocr.imag_to_string(img)
    
    @classmethod
    def create(
                cls, 
                library_ocr = LibraryOCR.PYTESSERACT, 
                *, 
                path_tesseract, 
                lang = None, 
                tess_data_dir = None
            ) -> ModuleOcr:
        #
        if library_ocr == LibraryOCR.PYTESSERACT:
            _module_ocr = IModulePytesseract(cmd_executable=path_tesseract, lang=lang, tess_data_dir=tess_data_dir)
        elif library_ocr == LibraryOCR.PYOCR:
            _module_ocr = IModulePyOcr(cmd_executable=path_tesseract, lang=lang, tess_data_dir=tess_data_dir)
        else:
            raise NotImplementedError(f'{__class__.__name__}\nLibraryOcr não implementada: {library_ocr}')
        return cls(_module_ocr)
        
        
      
   

            
        
        
        
        
        

