import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pymupdf

Tk().withdraw()
filename = askopenfilename()
print("!!! search in '" + filename + "'")

# opening the pdf file  
my_pdf = pymupdf.open(filename)

words = ["00,00", " 000,00", "0 000,00", "00 000,00"]
for word in words:
    # iterating through pages for highlighting the input phrase
    for n_page in my_pdf:
        matchWords = n_page.search_for(word)
        # print(matchWords)
        for findedWord in matchWords:
            my_highlight = n_page.add_highlight_annot(findedWord)
            my_highlight.update()

    # saving the pdf file as highlighted.pdf
    
    my_pdf.save( os.path.join(os.path.dirname(filename),  "highlighted_" + os.path.basename(filename)))