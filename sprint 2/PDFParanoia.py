import os
import PyPDF2


def encrypt(password):
    for foldername, subfolders, filenames in os.walk('.'):
        pdfFiles = []
        for filename in filenames:
            if filename.endswith('.pdf'):
                pdfFiles.append(filename)
        for pdfFile in pdfFiles:
            print('Encrypting %s...' % pdfFile)
            pdfFileRead = open(pdfFile, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileRead)


            if pdfReader.isEncrypted:
                print('File already encrypted.')
                pdfFileRead.close()
                continue

            pdfWriter = PyPDF2.PdfFileWriter()
            for pageNum in range(pdfReader.numPages):
                pdfWriter.addPage(pdfReader.getPage(pageNum))
            pdfOutputFile = open(pdfFile[:-4]+'_encrypted.pdf', 'wb')
            pdfWriter.encrypt(password)
            pdfWriter.write(pdfOutputFile)
            pdfOutputFile.close()
            pdfFileRead.close()

            pdfFileRead = open(pdfFile[:-4]+'_encrypted.pdf', 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileRead)
            if pdfReader.decrypt(password):
                print('File encrypted with success.')
                os.remove(pdfFile)
            else:
                print('Failed to encrypt %s.' % pdfFile)
                os.remove(pdfFile[:-4]+'_encrypted.pdf')
            pdfFileRead.close()

def decrypt(password):
    for foldername, subfolders, filenames in os.walk('.'):
        pdfFiles = []
        for filename in filenames:
            if filename.endswith('.pdf'):
                pdfFiles.append(filename)
        for pdfFile in pdfFiles:
            print('Decrypting %s...' % pdfFile)
            pdfFileRead = open(pdfFile, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileRead)

            if not pdfReader.isEncrypted:
                print('File not encrypted.')
                pdfFileRead.close()
                continue

            if not pdfReader.decrypt(password):
                print('Failed to decrypt file.')
                continue

            pdfWriter = PyPDF2.PdfFileWriter()
            for pageNum in range(pdfReader.numPages):
                pdfWriter.addPage(pdfReader.getPage(pageNum))

            pdfFileWrite = open(pdfFile[:-4]+'_decrypted.pdf', 'wb')
            pdfWriter.write(pdfFileWrite)
            pdfFileWrite.close()
            pdfFileRead.close()
            os.remove(pdfFile)

            print('File decrypted with success.')


encrypt('ilikebananas')
decrypt('ilikebananas')
