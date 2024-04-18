import pdf_function

#1 Save images into PDF file
images = ['./images/Eiffel-Tower.jpg', './images/Nature-Scenery.jpg', './images/Sky.jpeg', './images/Sky2.jpeg',
         './images/Waterfall.bmp', './images/cat1.png', './images/cat2.png', './images/Flower.gif']
output = './output/image_to_pdf_example.pdf'
pdf_function.image_to_pdf(images, output)

#2 Saving plain text to PDF file
text_file = 'pdf_master.py'
output = './output/text_to_pdf_example.pdf'
font_size = 10
pdf_function.text_to_pdf(text_file, output, font_size=font_size)

#3 Extracting text from PDF file
pdf_file = './pdfs/sample_c.pdf'
select_page = 10 # Extract text on page 10 and save into ".txt"
pdf_function.PDF_extracting_text(pdf_file, select_page)

pdf_file = './pdfs/sample_d.pdf'
select_page = 1000 # Extract text from whole pdf and save into ".txt"
pdf_function.PDF_extracting_text(pdf_file, select_page)

#4 Rotating PDF pages
originalFileName = './pdfs/sample_d.pdf'
newFileName = './output/rotate_example.pdf'
rotation = 180 # 90, 180, 270
pdf_function.PDF_rotate(originalFileName, newFileName, rotation)

#5 Merging PDF files
pdfs = ['./pdfs/sample_b.pdf', './pdfs/sample_c.pdf', './pdfs/sample_d.pdf', './pdfs/sample_e.pdf']
output = './output/merge_example.pdf'
pdf_function.PDF_merge(pdfs, output)

#6 Splitting PDF file
pdf = './pdfs/sample_a.pdf'
splits = [4, 6] # Three new pdf with split 1 (page 0-3), split 2 (page 4-5), split 3 (page 6-end)
pdf_function.PDF_split(pdf, splits)

#7 Insert PDF file
insertFileName = './pdfs/example.pdf'
insert_page = 5 # Insert "insertFileName" into page 5 of "originalFileName"
originalFileName = './pdfs/sample_a.pdf'
newFileName = './output/insert_example.pdf'
pdf_function.PDF_insert_page(insertFileName, insert_page, originalFileName, newFileName)

#8 Cropping PDF page with rectangle object
pdf = './pdfs/sample_d.pdf'
output = './output/crop_example.pdf'
crop_page = 2
crop_area = [50, 305, 500, 570]
pdf_function.PDF_crop_page(pdf, output, crop_page, crop_area)

#9 Adding watermark to PDF pages
watermark = './pdfs/watermark.pdf'
originalFileName = './pdfs/sample_b.pdf'
newFileName = './output/watermark_example.pdf'
pdf_function.PDF_add_watermark(watermark, originalFileName, newFileName)

#10 Encrypting PDF with password protection
pdf = './pdfs/sample_b.pdf'
output = './output/password_protected_example.pdf'
password = "abcd1234"
pdf_function.PDF_encrypt(pdf, output, password)

#11 Decrypting PDF to remove password protection
pdf = './output/password_protected_example.pdf'
output = './output/password_decrypt_example.pdf'
password = "abcd1234"
pdf_function.PDF_decrypt(pdf, output, password)
