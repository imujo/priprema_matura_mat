from tkinter import *
import tkinter.font as font
from PIL import Image, ImageTk
from editFile import *


class HoverButton(Button):
    def __init__(self, master, **kw):
        Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground


def setup():
    rjesenjeIndex.set(0)


def displayImage(imageLink, widget):
    # open image
    img = Image.open(imageLink)

    # resize image
    w, h = img.size
    if w > 1280 or h > 900:
        img.thumbnail((1200, 850))

    # display image
    img = ImageTk.PhotoImage(img)
    widget.configure(image=img)
    widget.image = img


def rjesenjeButtonsValidation():
    currentRjIndex = rjesenjeIndex.get()
    rjArrayLen = len(getRjesenjeLinksArray())

    nextRjesenjeBtn.configure(state=NORMAL)
    prevRjesenjeBtn.configure(state=NORMAL)
    if currentRjIndex == rjArrayLen-1:
        nextRjesenjeBtn.configure(state=DISABLED)
    if currentRjIndex == 0:
        prevRjesenjeBtn.configure(state=DISABLED)


def getRjesenjeLinksArray():
    return rjesenjeLinks.get().split(',')


def nextZadatak():
    setup()

    # get random zadatak
    zad, rjesenja, cjelina, lekcija, podlekcija = getRandomZad().values()
    rjesenjeLinks.set(','.join(rjesenja))
    zadatakLink.set(zad)

    rjesenjeButtonsValidation()
    hideRjesenje()

    displayImage(zadatakLink.get(), zadatak)

    # set breadcrumbs
    breadcrumbVar.set(
        '{} - {} - {}'.format(cjelina, lekcija, podlekcija))


def correctAnswer():
    removeZadatak(zadatakLink.get())
    nextZadatak()


# Rjesenja functions

def showRjesenje(external=False):
    rjesenjeLinksArray = getRjesenjeLinksArray()

    # if image or text is already displayed
    # external - prev or next
    if (rjesenje.image or rjesenje['text']) and not external:
        hideRjesenje()
        return

    # show rjesenje frame
    rjesenjeFrame.lift()

    # if rjesenje = null
    if not rjesenjeLinksArray[0]:
        rjesenje.configure(text='Nema rjesenja', fg='white')
        rjesenjeButtonText.set('Hide rjesenje')
        return

    # get image link by index
    link = rjesenjeLinksArray[rjesenjeIndex.get()]

    displayImage(link, rjesenje)

    rjesenjeButtonText.set('Hide rjesenje')


def hideRjesenje():
    rjesenjeFrame.lower()
    rjesenje.configure(image='', text='')
    rjesenje.image = ''
    rjesenjeButtonText.set('Show rjesenje')


def nextRjesenje():
    currentRjIndex = rjesenjeIndex.get()
    rjesenjeIndex.set(currentRjIndex+1)
    showRjesenje(True)

    rjesenjeButtonsValidation()


def prevRjesenje():
    currentRjIndex = rjesenjeIndex.get()
    rjesenjeIndex.set(currentRjIndex-1)
    showRjesenje(True)

    rjesenjeButtonsValidation()


# tocno function -> calls next image after storing to tocno
# krivo function -> calls next image after storing to krivo


root = Tk()

# default vars
primaryColor = 'white'
width = 1200
heigth = 900
buttonFont = font.Font(family='Helvetica', weight='bold')
root.configure(bg=primaryColor)


# global variables
rjesenjeIndex = IntVar()
rjesenjeIndex.set(0)

rjesenjeButtonText = StringVar()
rjesenjeButtonText.set('Show Rjesenje')

rjesenjeLinks = StringVar()
breadcrumbVar = StringVar()
zadatakLink = StringVar()


# BREADCRUMB SECTION
breadcrumb = Label(root, textvariable=breadcrumbVar, bg=primaryColor)
breadcrumb.pack(side='top', anchor=NW, pady=10, padx=20)


# ZADATAK SECTION
zadatak = Label(root, bg=primaryColor)
zadatak.pack(side='top', fill='y', expand=True)


# BUTTONS SECTION
buttonsFr = Frame(root, bg='black', height=120)
buttonsFr.pack(side='bottom', fill='x')
buttonsFr.pack_propagate(0)
buttonsFr.columnconfigure(0, weight=1)
buttonsFr.columnconfigure(1, weight=1)
buttonsFr.columnconfigure(2, weight=1)


wrongAnswer = Button(buttonsFr, text='Netocno', command=nextZadatak,
                     bg='red',  highlightthickness=0, bd=0, fg='white', height=3, font=buttonFont)
wrongAnswer.grid(column=0, row=0, sticky='nesw')


showRjesenjeBtn = Button(
    buttonsFr, textvariable=rjesenjeButtonText, command=showRjesenje,  highlightthickness=0, bd=0, bg='black', fg='white', height=3, font=buttonFont)
showRjesenjeBtn.grid(column=1, row=0, sticky='nesw')


correctAnswerBtn = Button(buttonsFr, text='Tocno',
                          command=correctAnswer, bg='green',  highlightthickness=0, bd=0, fg='white', height=3, font=buttonFont)
correctAnswerBtn.grid(column=2, row=0, sticky='nesw')

# RJESENJE SECTION

rjesenjeFrame = Frame(root, bg=primaryColor)
rjesenjeFrame.place(relx=0.5, rely=0.5, anchor=CENTER)
rjesenjeFrame.lower()

# prev btn
prevRjesenjeBtn = HoverButton(
    rjesenjeFrame, text='Prev Rjesenje', command=prevRjesenje,
    highlightthickness=0, bd=0, bg='white', activebackground='gray', width=30)
prevRjesenjeBtn.pack(side=LEFT, fill='both')

# image
rjesenje = Label(rjesenjeFrame, bg='#333333')
rjesenje.image = ''
rjesenje.pack(side=LEFT)

# next btn
nextRjesenjeBtn = HoverButton(
    rjesenjeFrame, text='Next Rjesenje', command=nextRjesenje,
    highlightthickness=0, bd=0, bg='white', activebackground='gray', width=30)
nextRjesenjeBtn.pack(side=LEFT, fill='both', padx=30)


nextZadatak()


# page config
root.title('Vjezba za maturu')
root.geometry("%dx%d" % (width, heigth))
root.resizable(True, True)
root.mainloop()
