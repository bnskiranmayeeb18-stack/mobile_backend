# pip install pymupdf
import fitz
doc = fitz.open()
page = doc.new_page()
text = open('design.txt').read() # Task 2 text antha oka file lo pettu
page.insert_textbox((40,40,560,800), text, fontsize=10)
doc.save("Task2_Design_Document.pdf")
print("Done")