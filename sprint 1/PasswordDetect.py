import re

def StrongPassword (password):
    
    if len(password)<8:
        return False
    
    passwordRegexLower=re.compile(r'[a-z]')
    passwordRegexUpper=re.compile(r'[A-Z]')
    passwordRegexDigit=re.compile(r'[0-9]')
    
    moForPassword=passwordRegexLower.search(password)
    if moForPassword==None:
        return False
    
    moForPassword=passwordRegexDigit.search(password)
    if moForPassword==None:
        return False
    
    moForPassword=passwordRegexUpper.search(password)
    if moForPassword==None:
        return False
    
    return True
            
userPass=input("Type the password: ")

if StrongPassword(userPass):
    print("Valid password.\n")
else:
    print("Password not strong enough.\n")      