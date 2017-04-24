import pyperclip
import re

phoneNumRegex=re.compile(r'\(?\d\d\)? \d{3,}-?\d{3,}')
emailRegex=re.compile(r'(\w+@\w+\.\w+)(\.\w+)?')



moTel=phoneNumRegex.findall(pyperclip.paste())
moEmail=emailRegex.findall(pyperclip.paste())


listaTel=""
listaEmail=""

for phoneNumber in moTel:
    listaTel+= phoneNumber+ '\n'
    
for email in moEmail:
    listaEmail+= email[0] + email[1]+ "\n"

if listaEmail=="":
    print("Nenhum endereço de email encontrado. \n")
else:
    print(">Lista de endereços de emails encontrados:")
    print (listaEmail)

if listaTel == "":
    print("Nenhum número encontrado.\n")
else:
    print (">Lista de números de telefone encontrados: \n" + listaTel)