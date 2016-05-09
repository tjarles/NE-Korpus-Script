from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

#Global variable that buttons can change before printing to file
NE = ""
isSaveMode = False

class Windows:
    def __init__(self, firstWord, secondWord, thirdWord):
        self.Master=Tk()

        #Set default closing action to call on save-mode.
        self.Master.protocol("WM_DELETE_WINDOW", self.ExitAndSave)

        #Creates labelbox containing three cooccuring words
        self.labelbox = LabelFrame(self.Master, text="Möjlig entitet:").grid_anchor(CENTER)
        self.w = Label(self.labelbox, text=firstWord, font = "Helvetica 12").grid(row = 0, column = 0)
        self.w2 = Label(self.labelbox, text=secondWord, font = "Helvetica 12").grid(row = 0, column = 1)
        self.w3 = Label(self.labelbox, text=thirdWord, font = "Helvetica 12 bold").grid(row = 0, column = 2)

        #Current NE
        self.currentNE = Label(self.labelbox, text="Current NE: ", font = "Helvetica 12").grid(row = 1, column = 0)
        self.ne = Label(self.labelbox, text=NE, font = "Helvetica 12 bold").grid(row = 1, column = 1)

        #Keybindings
        self.Master.bind('1', lambda x: self.Set("sjukdom"))
        self.Master.bind('2', lambda x: self.Set("medicin"))
        self.Master.bind('3', lambda x: self.Set("åtgärd"))
        self.Master.bind('4', lambda x: self.Set("kroppsdel"))
        self.Master.bind('7', lambda x: self.Set("verktyg"))
        self.Master.bind('8', lambda x: self.Set("mottagning"))
        self.Master.bind('9', lambda x: self.Set("person"))
        self.Master.bind('0', lambda x: self.Set("organisation"))
        self.Master.bind('+', lambda x: self.Set("REPLACEWITH_"))

        #Buttons
        self.Button=Button(self.Master,text="Sjukdom (1)",command=lambda: self.Set("sjukdom")).grid(row = 2, column = 0)
        self.Button=Button(self.Master,text="Medicin (2)",command=lambda: self.Set("medicin")).grid(row = 2, column = 1)
        self.Button=Button(self.Master,text="Åtgärd (3)",command=lambda:self.Set("åtgärd")).grid(row = 3, column = 0)
        self.Button=Button(self.Master,text="Kroppsdel (4)",command=lambda:self.Set("kroppsdel")).grid(row = 3, column = 1)

        #Creates space between buttons
        self.Label=Label(self.Master,text="             ").grid(row = 2, column = 3)

        self.Button=Button(self.Master,text="Verktyg (7)",command=lambda: self.Set("verktyg")).grid(row = 2, column = 4)
        self.Button=Button(self.Master,text="Mottagning (8)",command=lambda: self.Set("mottagning")).grid(row = 2, column = 5)
        self.Button=Button(self.Master,text="Person (9)",command=lambda:self.Set("person")).grid(row = 3, column = 4)
        self.Button=Button(self.Master,text="Organisation (0)",command=lambda:self.Set("organisation")).grid(row = 3, column = 5)

        self.Button=Button(self.Master,text="Leave unchanged (+)",command=lambda:self.Set("REPLACEWITH_")).grid(row = 4, column = 5)
        self.Button=Button(self.Master,text="Exit and save",command=lambda:self.ExitAndSave()).grid(row = 6, column = 5)
        self.Master.mainloop()

    #Function setting the NE and destroying window
    def Set(self, entityLabel = ""):
        global NE
        NE = entityLabel
        self.Master.destroy()

    def ExitAndSave(self):
        result = messagebox.askokcancel("Exit and save confirmation", "Are you sure you want to save and quit? You can pickup where you left by opening this file again.")
        #If answer "ok" enter savemode and close screen
        if result:
            global isSaveMode
            isSaveMode = True
            self.Master.destroy()

#File to save to
f2 = open("NE-tagged_blogg_corpus9.conll", "w")

#For letting user chose file in the future
# with open(filedialog.askopenfilename(), "r",  encoding='utf-8') as f:

#File to read from
with open('NE-tagged_blogg_corpus8.conll', "r",  encoding='utf-8') as f:
    threeCurrentWords = ["",""]
    for line in f:
        if isSaveMode:
            f2.write(line)
            continue;
        if line == "\n":
            f2.write("\n")
        if line != "\n":
            lineList = line.split('\t')

            # if lineList[0] == "1":
            #     f2.write("\n")

            NE = lineList[-2]

            #Saves three latest words
            if len(threeCurrentWords) == 3:
                del threeCurrentWords[0]
            threeCurrentWords.append(lineList[1])

            #Windows() takes input from the user and assigns that as NE
            try:
                if (lineList[3] == "PM" or lineList[3] == "NN") and NE == "_":
                    Windows(firstWord = threeCurrentWords[0], secondWord = threeCurrentWords[1], thirdWord = threeCurrentWords[2])
                    lineList[-2] = NE
            except IndexError:
                print(line)

            newLine = ""
            for column in lineList:
                newLine += column + "\t"
            newLine = newLine[:-2]
            newLine += "\n"

            f2.write(newLine)

            #sentences with ne are saved to file
#            if ne_count > 0:
#                str_sentence = ""
#                for entry in sentence:
#                    str_sentence += entry
#                str_sentence += "\n"
#                f1.write(str_sentence)



#f.close()