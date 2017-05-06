import PyPDF2

pdfFileOutput = open('encrypted.pdf', 'wb')
pdfFileRead = open('meetingminutes.pdf', 'rb')
pdfFileReader = PyPDF2.PdfFileReader(pdfFileRead)

pdfFileWriter = PyPDF2.PdfFileWriter()
pdfFileWriter.addPage(pdfFileReader.getPage(0))

pdfFileWriter.encrypt('zurich')
pdfFileWriter.write(pdfFileOutput)


pdfFileOutput.close()
pdfFileRead.close()