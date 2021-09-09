import os, re, requests
from tkinter import *
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup

window = Tk()
window.title("Downloader manga images by URL")
window.minsize(320, 240)
window.maxsize(640, 480)


url = StringVar()
selectedDir = StringVar()
selectedDir.set("/")
name = StringVar()
chapter = IntVar()



frameUrl = Frame(window)
frameUrl.pack(fill = "x", padx = 20, pady = 5)

labelUrl = Label(frameUrl, text = "Add Url:")
labelUrl.pack()

fieldUrl = Entry(frameUrl, textvariable = url)
fieldUrl.pack(fill = "x")



frameDir = Frame(window)
frameDir.pack(fill = "x", padx = 20, pady = 5)

labelDir = Label(frameDir, text = "Select Directory to save:")
labelDir.pack()

fieldDir = Entry(frameDir, textvariable = selectedDir , state='disabled')
fieldDir.pack(fill = "x", expand = True, padx = (0, 5), side = "left")
    
buttonDir = Button(frameDir, width = 10, text = "Choose")
buttonDir["command"] = lambda: selectedDir.set(filedialog.askdirectory(title = "Please select a directory"))
buttonDir.pack(side = "right")



frameName = Frame(window)
frameName.pack(fill = "x", padx = 20, pady = 5)

labelName = Label(frameName, text = "Manga Name (optional):")
labelName.pack(side = "left")

def withoutSpecialChars(char):
    return bool(re.match("[\w+\s'&%;.,=-]", char))
nameValidation = window.register(withoutSpecialChars)

fieldName = Entry(frameName, textvariable = name, validate="key", validatecommand=(nameValidation, '%S'))
fieldName.pack(fill = "x", expand = True, padx = (5, 0), side = "right")



frameChp = Frame(window)
frameChp.pack(fill = "x", padx = 20, pady = 5)

labelChp = Label(frameChp, text = "Chapter:")
labelChp.pack(side = "left")

def onlyNums(char):
    return char.isdigit()
numValidation = window.register(onlyNums)

fieldChp = Entry(frameChp, textvariable = chapter, validate="key", validatecommand=(numValidation, '%S'))
fieldChp.pack(fill = "x", expand = True, padx = (5, 0), side = "right")



def download():

    urlSite = url.get()
    mangaName = name.get()
    chapterNumber = chapter.get()
    if mangaName:
        filesDir = "%s/%s/%s" %(selectedDir.get(), mangaName, chapterNumber)
    else:
        filesDir = "%s/%s" %(selectedDir.get(), chapterNumber)


    response = requests.get(urlSite, headers = {"User-Agent": ""})

    links = [urlSite + img['href'] for img in BeautifulSoup(response.content, 'html5lib').findAll('a') if img['href'].endswith((".png", ".jpg", ".jpeg"))]

    if not os.path.isdir(filesDir):
        os.makedirs(filesDir)

    for index, link in enumerate(links) :

        statusLabel["text"] = "Downloading... %s of %s" %(str(index + 1), str(len(links)))
        window.update()

        fileDir = filesDir + "/" + link.split('/')[-1]

        file = requests.get(link, headers = {"User-Agent": ""})

        with open(fileDir, 'wb') as f:
            f.write(file.content)
            f.close()

    statusLabel["text"] = "Finished Chapter %s" %chapterNumber
    messagebox.showinfo("Alert", "Finished")


button = Button(window, width = 10, pady = 5, text = "Download", command = download)
button.pack()

statusLabel = Label(window, text = "Nothing...", bd = 1, relief = SUNKEN, anchor = W)
statusLabel.pack(side = "bottom", fill = "x")

window.mainloop()