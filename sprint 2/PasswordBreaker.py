#! python3
# PasswordBreaker.py - Tests password for PDF file against provided dictionary of english words.

import time
import PyPDF2

dictionaryFile = open('dictionary.txt', 'r')
dictionaryList = dictionaryFile.readlines() # creates list with all the words
dictionaryFile.close()

pdfFileRead = open('encrypted.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileRead)

for word in dictionaryList:
    print('Testing "%s"...' % word.rstrip().lower()) # tests password for each word on the dictionary (lower case)
    if pdfReader.decrypt(word.rstrip().lower()): # .decrypt() method returns 1 when successful
        print('Password is %s' % word.rstrip().lower()) # when password found, prints it
        break

pdfFileRead.close()

