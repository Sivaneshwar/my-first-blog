# import PyPDF2

# pdfName = open('Biological Neuron.pdf','rb')
# read_pdf = PyPDF2.PdfFileReader(pdfName)
# page = read_pdf.getPage(0)
# page_content = page.extractText()
# print(page_content)

from PyPDF2 import PdfFileReader
 
 
def text_extractor(path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
 
        # get the first page
        page = pdf.getPage(0)
        print(page)
        print('Page type: {}'.format(str(type(page))))
 
        text = page.extractText()
        print(text.encode("utf-8"))
 
 
if __name__ == '__main__':
    # path = 'Biological Neuron.pdf'
    path = 'ABSTRACT_FINAL.pdf'
    text_extractor(path)