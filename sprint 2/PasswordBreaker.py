import time
import PyPDF2

dictionaryFile = open('dictionary.txt', 'r')
dictionaryList = dictionaryFile.readlines()
dictionaryFile.close()

pdfFileRead = open('encrypted.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileRead)

startTime = time.time()
for word in dictionaryList:
    print('Testing "%s"...' % word.rstrip().lower())
    if pdfReader.decrypt(word.rstrip().lower()):
        print('Password is %s' % word.rstrip().lower())
        break
endTime = time.time()

print('%d seconds elapsed.' % round(endTime - startTime))

pdfFileRead.close()

