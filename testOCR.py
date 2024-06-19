from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # here is the address of where you install you tesseract

# Open an image file
image = Image.open(r'C:\Users\xxx\xxx\xxx.jpg') # here is the address of the image you want it to read

# Use pytesseract to do OCR on the image
text = pytesseract.image_to_string(image)

print(text)
