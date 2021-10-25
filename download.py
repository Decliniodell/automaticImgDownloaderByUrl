import os, re, requests
from tkinter import *
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup

window = Tk()
window.title("Automatic Img Downloader by Url")
window.iconbitmap("imgs/icon.ico")
window.minsize(320, 240)
window.maxsize(640, 480)


url = StringVar()
selectedDir = StringVar()
selectedDir.set("/")
name = StringVar()
chapter = StringVar()


def withoutSpecialChars(char):
    return bool(re.match("[\w+\s'&%;.,=-]", char))
nameValidation = window.register(withoutSpecialChars)


def onlyNums(char):
    return bool(re.match("[0-9]", char))
numValidation = window.register(onlyNums)


def fieldsVerification():
    error = False

    if not url.get():
        error = True
        labelUrl.config(fg="red")
        labelUrl.config(text="Add URL * (required)")
        fieldUrl.config(bg="#ffa6a6")

    elif not bool(re.match('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url.get())):
        error = True
        labelUrl.config(fg="red")
        labelUrl.config(text="Add URL * (invalid)")
        fieldUrl.config(bg="#ffa6a6")

    else:
        labelUrl.config(fg="black")
        labelUrl.config(text="Add URL *")
        fieldUrl.config(bg="white")


    if not selectedDir.get() or selectedDir.get() == "/":
        error = True
        labelDir.config(fg="red")
        labelDir.config(text="Select directory to save * (required)")
        fieldDir.config(disabledbackground="#ffa6a6")

    elif not os.path.isdir(selectedDir.get()):
        error = True
        labelDir.config(fg="red")
        labelDir.config(text="Select directory to save * (invalid)")
        fieldDir.config(disabledbackground="#ffa6a6")

    else:
        labelDir.config(fg="black")
        labelDir.config(text="Select directory to save *")
        fieldDir.config(disabledbackground="white")


    if not fieldChp.get():
        error = True
        labelChp.config(fg="red")
        labelChp.config(text="Chapter * (required)")
        fieldChp.config(bg="#ffa6a6")

    else:
        labelChp.config(fg="black")
        labelChp.config(text="Chapter *")
        fieldChp.config(bg="white")


    return False if error else download()


def download():

    urlSite = url.get()
    mangaName = name.get()
    chapterNumber = chapter.get()
    imageExt = ""
    imageNums = ""

    # Add 'mangaName' to the files path, C:/SelectedDir/MangaName/00
    if mangaName:
        filesDir = "%s/%s/%s" %(selectedDir.get(), mangaName, chapterNumber)
    else:
        filesDir = "%s/%s" %(selectedDir.get(), chapterNumber)

    # Check for an image in the url
    if urlSite.split('.')[-1] in ("png", "jpg", "jpeg"):
        imageNums = urlSite.split('/')[-1].split('.')[0]
        imageExt = urlSite.split('/')[-1].split('.')[1]
        urlSite = urlSite[0 : urlSite.rindex('/') + 1]

    # (Disabled) Check if the url ends with '/'
    # elif urlSite[-1] != "/":
    #     urlSite += "/"

    # Create the path if it doesn't exist
    if not os.path.isdir(filesDir):
        os.makedirs(filesDir)

    # If there is an image in the url, download and check how many there are
    if imageNums and imageExt:
        quantityImages = 0

        while True:

            # Increments the numbers according to the size of the image name (00 or 000) 01, 02, 03 ....
            if len(imageNums) == 2:
                urlTemp = urlSite + "%s%s.%s" %(("0" if quantityImages < 10 else ""), quantityImages, imageExt)

            elif len(imageNums) == 3:

                urlTemp = urlSite + "%s%s.%s" %(("00" if quantityImages < 10 else "0" if quantityImages < 100 else ""), quantityImages, imageExt)
            
            file = requests.get(urlTemp, headers = {"User-Agent": ""})

            if file.status_code == 200 :
                statusLabel["text"] = "Downloading... page %s" %(quantityImages)
                window.update()

                fileDir = filesDir + "/" + urlTemp.split('/')[-1]

                with open(fileDir, 'wb') as f:
                    f.write(file.content)
                    f.close()
                quantityImages += 1
            else :
                break
    # If there is no image in the url, check the url response for image links
    else :
        response = requests.get(urlSite, headers = {"User-Agent": ""})

        links = [urlSite + img['href'] for img in BeautifulSoup(response.content, 'html5lib').findAll('a') if img['href'].endswith((".png", ".jpg", ".jpeg"))]

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


# menuBar = Menu(window)
# optionsDrop = Menu(menuBar)
# optionsDrop.add_checkbutton(label = "Change Lang EN/PT-br", variable = lang, onvalue = 1, offvalue = 0)
# menuBar.add_cascade(label = "Options", menu = optionsDrop)


frameUrl = Frame(window)
frameUrl.pack(fill = "x", padx = 20, pady = 5)

labelUrl = Label(frameUrl, text = "Add URL *")
labelUrl.pack()

fieldUrl = Entry(frameUrl, textvariable = url)
fieldUrl.pack(fill = "x")



frameDir = Frame(window)
frameDir.pack(fill = "x", padx = 20, pady = 5)

labelDir = Label(frameDir, text = "Select directory to save *")
labelDir.pack()

fieldDir = Entry(frameDir, textvariable = selectedDir , state='disabled')
fieldDir.pack(fill = "x", expand = True, padx = (0, 5), side = "left")
    
buttonDir = Button(frameDir, width = 10, text = "Choose")
buttonDir["command"] = lambda: selectedDir.set(filedialog.askdirectory(title = "Please select a directory"))
buttonDir.pack(side = "right")



frameName = Frame(window)
frameName.pack(fill = "x", padx = 20, pady = 5)

labelName = Label(frameName, text = "Manga name")
labelName.pack(side = "left")

fieldName = Entry(frameName, textvariable = name, validate="key", validatecommand=(nameValidation, '%S'))
fieldName.pack(fill = "x", expand = True, padx = (5, 0), side = "right")



frameChp = Frame(window)
frameChp.pack(fill = "x", padx = 20, pady = 5)

labelChp = Label(frameChp, text = "Chapter *")
labelChp.pack(side = "left")

fieldChp = Entry(frameChp, textvariable = chapter, validate="key", validatecommand=(numValidation, '%S'))
fieldChp.pack(fill = "x", expand = True, padx = (5, 0), side = "right")



button = Button(window, width = 10, pady = 5, text = "Download", command = fieldsVerification)
button.pack()



statusLabel = Label(window, text = "Downloading... page 1", bd = 1, relief = SUNKEN, anchor = W)
statusLabel.pack(side = "bottom", fill = "x")

# window.config(menu = menuBar)
window.mainloop()