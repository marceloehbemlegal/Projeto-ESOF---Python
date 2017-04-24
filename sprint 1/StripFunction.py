import re

def RegexStrip(text, stripChar=""):
    
    if stripChar=="":
        stripReg=re.compile(r'^ *(.*?) *$')
        moStrip=stripReg.search(text)
        return moStrip.group(1)
    else:
        stripReg=re.compile(r'[^{}]'.format(stripChar))
        moStrip=stripReg.findall(text)
        strippedText=""
        for item in moStrip:
            strippedText+=item
        return(strippedText)
    
    

userInput=input("Enter the text to be stripped: ")
# Assuming user input is different from ""
stripCharacters=input("Enter characters to be stripped(if none, press Enter): ")

strippedText=RegexStrip(userInput, stripCharacters)
print(strippedText)