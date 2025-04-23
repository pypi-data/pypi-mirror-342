# ocrlib

# Uso simples

from ocrlib.utils import File, DocumentPdf
from ocrlib import RecognizeImage

# passo 1 instânciar o objeto para reconhecer texto, ultilzaremos o caminho do tesseract
# Substitua pelo tesseract do seu sistema

tess = File('/usr/bin/tesseract')
ocr = RecognizeImage.create(path_tesseract=tess)

# passo 2 instânciar um arquivo de imagem para extrair o texto.
image = File('path/to/file.png')

# passo 3 extrair o texto
text = ocr.image_to_string(image)
print(text)

# passo 4 opcional - você pode salvar um arquivo PDF com o texto extraido
output_file = File('path/to/save.pdf')
recognized = ocr.image_recognize(image)
recognized.to_document().to_file_pdf(output_file)

# passo 5 opcional - você pode salvar uma planilha com o texto da imagem
output_excel = File('path/to/file.xlsx')
recognized = ocr.image_recognize(image)
recognized.to_document().to_excel(output_excel)