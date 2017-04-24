import re

fileOP=open('madlibs.txt', 'r')

madLibsRegex=re.compile("(ADJECTIVE|NOUN|ADVERB|VERB)")
rawText=fileOP.read()

fileOP.close()

moMadLibs=madLibsRegex.findall(rawText)

wordList = []
inputWord = ""

for i in range (len(moMadLibs)):
    if(moMadLibs[i].lower()=='adjective'):
        inputWord = input("Enter an adjective: ")
    else:
        inputWord = input("Enter a %s: " % moMadLibs[i].lower())
    
    wordList.append(inputWord)

finalText=rawText

for i in range(len(wordList)):
    finalText=re.sub("(ADJECTIVE|NOUN|ADVERB|VERB)", wordList[i], finalText, 1)

print("New text: \n\n" + finalText + "\n")
    
fileOP=open('madlibsfinal.txt', 'w')

fileOP.write(finalText)

print("File created.")

fileOP.close()

