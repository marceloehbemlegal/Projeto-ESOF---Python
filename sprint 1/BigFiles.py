import os

folder=os.path.abspath('.')
os.chdir(folder)
bigFiles=[]
bigFolders=[]

for foldername, subfolders, filenames in os.walk(folder):
    for subfolder in subfolders:
        if os.path.getsize(os.path.abspath(foldername)+'\\'+subfolder)>=(100*1024**2):
            bigFolders.append(subfolder)
    for filename in filenames:
        if os.path.getsize(os.path.abspath(foldername)+'\\'+filename)>=(100*1024**2):
            bigFiles.append(filename)


if bigFolders==[]:
    print("No folders bigger than 100MB found.")
else:
    print("Folders bigger than 100MB: ")
    for foldername in bigFolders:
        print(foldername)

if bigFiles==[]:
    print("\nNo files bigger than 100MB found.")
else:
    print("Files bigger than 100MB: ")
    for filename in bigFiles:
        print(filename)