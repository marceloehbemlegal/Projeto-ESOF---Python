import re
import os

fileList=os.listdir()
userRegex=input("Enter the expression to be searched: ")
searchRegex=re.compile('(.*)?(%s)(.*)?' % userRegex)
stringList=[]
textInFile=""

for i in range(len(fileList)):
    if os.path.isfile(fileList[i]):
        fileOP=open(fileList[i], 'r')
        textInFile=fileOP.read()
        
        stringList=searchRegex.findall(textInFile)
        
        print("In file %s:" % fileList[i])
        if stringList==[]:
            print("  No text found.")
        else:
            for j in range(len(stringList)):
                print('  '+''.join((stringList[j])).strip())
        
        print("\n")
    
        fileOP.close()
