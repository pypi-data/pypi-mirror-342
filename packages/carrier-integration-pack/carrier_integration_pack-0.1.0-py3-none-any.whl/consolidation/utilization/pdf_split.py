

from pypdf import PdfWriter, PdfReader


def get_pdf_pages(filename):

    inputpdf = PdfReader(filename)
    for page in range(len(inputpdf.pages)):
        output = PdfWriter()
        output.add_page(inputpdf.pages[page])
        new_file = "new_file{}.pdf".format(page)
        with open(new_file, "wb") as f:
            output.write(f)
        output.close()


# if __name__ == "__main__":

#     fileName = "/home/mock/Downloads/fedex.pdf"
#     get_pdf_pages(fileName)
