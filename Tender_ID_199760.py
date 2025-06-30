import pytesseract
from PIL import Image
import openpyxl

# Load your image
image = Image.open('tender_1.1.jpg')

# Perform OCR to extract text
text = pytesseract.image_to_string(image)

# Split text into lines
lines = text.strip().split('\n')

# Create new Excel workbook
wb = openpyxl.Workbook()
ws = wb.active

# Write each line to Excel row
for i, line in enumerate(lines, start=1):
    # If line has columns separated by tabs/spaces, split them:
    cols = line.split()  # adjust this if your columns have clear separators
    for j, col in enumerate(cols, start=1):
        ws.cell(row=i, column=j, value=col)

# Save workbook
wb.save('output.xlsx')

print("Excel file 'output.xlsx' created successfully!")
