from multilingual_pdf2text.pdf2text import PDF2Text
from multilingual_pdf2text.models.document_model.document import Document
import logging
logging.basicConfig(level=logging.INFO)

def main():
    ## create document for extraction with configurations
    pdf_document = Document(
        document_path='NIOS_YOGA-A_Sanskrit_Ch-2.pdf',
        language='san'
        )
    pdf2text = PDF2Text(document=pdf_document)
    content = pdf2text.extract()
    
    with open('extractedtext.text','w') as f:
        for item in content:
            f.write("%s\n" % item)
if __name__ == "__main__":
    main()