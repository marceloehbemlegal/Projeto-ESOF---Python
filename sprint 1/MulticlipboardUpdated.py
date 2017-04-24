#! python3

import pyperclip, shelve, sys

mcbShelf=shelve.open('mcb')

if len(sys.argv)==3 and sys.argv[1].lower()=='save':
    mcbShelf[sys.argv[2]]=pyperclip.paste()
elif len(sys.argv)==3 and sys.argv[1].lower()=='delete':
    del mcbShelf[sys.argv[2]]
elif sys.argv[1].lower()=='list':
    pyperclip.copy(str(list(mcbShelf.keys())))
elif sys.argv[1].lower()=='delete':
    mcbShelf.clear()
elif sys.argv[1] in mcbShelf:
    pyperclip.copy(mcbShelf[sys.argv[1]])

mcbShelf.close()
