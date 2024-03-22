import os
import img2pdf
from fpdf import FPDF
#from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from pypdf import PdfReader, PdfWriter, PdfMerger
import copy

if not os.path.exists('./output'): os.makedirs('./output')

#Save images into PDF file
def image_to_pdf(images, output):
    # Creating PDF File Object
    pdfFile = open(output, 'wb')
    image = []
    image_type = ['.bmp', '.jpg', 'jpeg', 'png']
    for img in images:
        for ext in image_type:
            if img.endswith(ext):
                image.append(img)
                break
    # Converting Image File to PDF
    pdfFile.write(img2pdf.convert(image))
    #Closing Image File Object

#Saving plain text to PDF file
def text_to_pdf(text_file, output, font_size=10):
    # save FPDF() class into a variable pdf
    pdf = FPDF()

    # Add a page
    pdf.add_page()
    
    # set style and size of font in the pdf
    pdf.set_font("Arial", size = font_size)
    # open the text file in read mode
    file = open(text_file, "r")

    # insert the texts in pdf
    for text in file: pdf.cell(200, int(font_size/2), txt = text, ln = 1)

    # save the pdf with name .pdf
    pdf.output(output)
    file.close()

#Extracting text from PDF file
def PDF_extracting_text(pdf_file, select_page):
    # creating a pdf reader object
    reader = PdfReader(pdf_file)
    outputtxt = pdf_file.replace('.pdf', '.txt')

    # printing number of pages in pdf file
    total_page = len(reader.pages)
    print(f'total page={total_page}')

    # creating a page object 
    if select_page < total_page:
        # extracting text from page
        page = reader.pages[select_page]
        with open(outputtxt, "w") as file: file.write(page.extract_text())
        print(page.extract_text())
    else:
        # extracting text from whole pdf
        with open(outputtxt, "w") as file: file.write("")
        for select in range(total_page):
            print(select)
            page = reader.pages[select]
            with open(outputtxt, "a") as file: file.write(page.extract_text() + "\n\n\n")
            print(page.extract_text() + "\n\n")

#Rotating PDF pages
def PDF_rotate(originalFileName, newFileName, rotation):
    if rotation in [90, 180, 270]:

        # creating a pdf Reader object
        reader = PdfReader(originalFileName)
    
        # creating a pdf writer object for new pdf
        writer = PdfWriter()
    
        # rotating each page
        for page in range(len(reader.pages)):
    
            # creating rotated page object
            pageObj = reader.pages[page]
            pageObj.rotate(rotation)
    
            # adding rotated page object to pdf writer
            writer.add_page(pageObj)
    
            # new pdf file object
            newFile = open(newFileName, 'wb')
    
            # writing rotated pages to new file
            writer.write(newFile)
    
        # closing the new pdf file object
        newFile.close()

#Merging PDF files
def PDF_merge(pdfs, output):
    # creating pdf file merger object
    pdfMerger = PdfMerger()

    # appending pdfs one by one
    for pdf in pdfs:
        print(pdf)
        pdfMerger.append(pdf)

    # writing combined pdf to output pdf file
    with open(output, 'wb') as f: pdfMerger.write(f)

#Splitting PDF file
def PDF_split(pdf, splits):
    # creating pdf reader object
    reader = PdfReader(pdf)

    # starting index of first slice
    start = 0

    # starting index of last slice
    end = splits[0]

    for i in range(len(splits) + 1):
        # creating pdf writer object for (i+1)th split
        writer = PdfWriter()

        # output pdf file name
        outputpdf = pdf.split('.pdf')[0] + f'{i}.pdf'
        print(f'{outputpdf} {start+1}-{end}page')
        # adding pages to pdf writer object
        for page in range(start, end):
            writer.add_page(reader.pages[page])
            # writing split pdf pages to pdf file
            with open(outputpdf, 'wb') as f: writer.write(f)

            # interchanging page split start position for next split
            start = page + 1
            try:
                # setting split end position for next split
                end = splits[i + 1]
            except IndexError:
                # setting split end position for last split
                end = len(reader.pages)

#Inserting another PDF file into PDF file
def PDF_insert_page(insertFileName, insert_page, originalFileName, newFileName):
    # creating pdf reader object
    original = PdfReader(originalFileName)
    total_page_original = len(original.pages)
    insert = PdfReader(insertFileName)
    total_page_insert = len(insert.pages)
    
    if insert_page == 0: PDF_merge([insertFileName, originalFileName], newFileName)
    elif insert_page >= total_page_original: PDF_merge([originalFileName, insertFileName], newFileName)
    else:
        writer = PdfWriter()
        page_index = 0
        for page in range(insert_page):
            writer.add_page(original.pages[page])
            newFile = open(newFileName, 'wb')
            writer.write(newFile)
            page_index = page + 1
        for page in range(total_page_insert): 
            writer.add_page(insert.pages[page])
            newFile = open(newFileName, 'wb')
            writer.write(newFile)
        for page in range(page_index, total_page_original):
            writer.add_page(original.pages[page])
            newFile = open(newFileName, 'wb')
            writer.write(newFile)
        newFile.close()

#Cropping PDF page with rectangle object
def PDF_crop_page(pdf, output, crop_page, crop_area):
    reader = PdfReader(pdf)
    total_page = len(reader.pages)
    if crop_page < total_page:
        writer = PdfWriter()
        pdf_reader = reader.pages[crop_page]
        crop_reader = copy.deepcopy(pdf_reader)

        # Rectangular area, x and y coordinates of the lower-left, width and height of the rectangular region
        x, y, w, h = crop_reader.mediabox
        print(x, y, w, h)
        if crop_area[0] < w and crop_area[1] < h:
            if crop_area[2] > w: crop_area[2] = w
            if crop_area[3] > h: crop_area[3] = h
            crop_reader.mediabox.upper_left = [crop_area[0], h-crop_area[1]]
            crop_reader.mediabox.lower_right = [crop_area[2], h-crop_area[3]]
            writer.add_page(crop_reader)
            writer.write(output)
# pdf = './watermark_example.pdf'
# output = '0crop_example.pdf'
# crop_page = 0
# crop_area = [0, 230, 590, 380]
# PDF_crop_page(pdf, output, crop_page, crop_area)


#Adding watermark to PDF pages
def add_watermark(wmFileObj, pageObj):
    # creating pdf reader object of watermark pdf file
    reader = PdfReader(wmFileObj)

    # merging watermark pdf's first page with passed page object.
    pageObj.merge_page(reader.pages[0])

    # returning watermarked page object
    return pageObj

def PDF_add_watermark(watermark, originalFileName, newFileName):
    # creating pdf File object of original pdf
    pdfFileObj = open(originalFileName, 'rb')

    # creating a pdf Reader object
    reader = PdfReader(pdfFileObj)

    # creating a pdf writer object for new pdf
    writer = PdfWriter()

    # adding watermark to each page
    for page in range(len(reader.pages)):
        # creating watermarked page object
        wmpageObj = add_watermark(watermark, reader.pages[page])

        # adding watermarked page object to pdf writer
        writer.add_page(wmpageObj)

        # new pdf file object
        newFile = open(newFileName, 'wb')

        # writing watermarked pages to new file
        writer.write(newFile)

    # closing the new pdf file object
    newFile.close()

#Encrypting PDF with password protection
def PDF_encrypt(pdf, output, password):
    reader = PdfReader(pdf)
    writer = PdfWriter()
    writer.append_pages_from_reader(reader)
    writer.encrypt(user_password=password, owner_password="12345678")
    writer.write(output)

#Decrypting PDF to remove password protection
def PDF_decrypt(pdf, output, password):
    try:
        reader = PdfReader(pdf)
        reader.metadata
    except:
        try:
            reader.decrypt(password=password)
            total_page = len(reader.pages)
            print("Decrypt success")
            writer = PdfWriter()
            for page in range(total_page):
                writer.add_page(reader.pages[page])
                newFile = open(output, 'wb')
                writer.write(newFile)
        except:
            print("Decrypt unsuccess")
