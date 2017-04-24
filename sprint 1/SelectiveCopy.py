import os, shutil

fileExtension=input("Extension to be copied(\".ext\"): ")
copyToDirectory=input("Destination: ")

if not os.path.exists(copyToDirectory):
    os.makedirs(copyToDirectory)

copyToDirectory=os.path.abspath(copyToDirectory)

folder='.'
folder=os.path.abspath(folder)

for foldername, subfolders, filenames in os.walk(folder):
    if os.path.abspath(foldername)==copyToDirectory:
        continue
    for filename in filenames:
        if filename.endswith(fileExtension):
            print("Moving %s to %s..." % (os.path.abspath(foldername)+"\\"+filename, copyToDirectory))
            shutil.move(os.path.abspath(foldername)+"\\"+filename, copyToDirectory)
            
print("Files moved.")