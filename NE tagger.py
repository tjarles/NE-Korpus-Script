from tkinter import *

#Global variable that buttons can change before printing to file
NE = ""

class Windows:
    def __init__(self, firstWord, secondWord, thirdWord):
        self.Master=Tk()

        #Creates labelbox containing three cooccuring words
        self.labelbox = LabelFrame(self.Master, text="Möjlig entitet:").grid_anchor(CENTER)
        self.w = Label(self.labelbox, text=firstWord, font = "Helvetica 12").grid(row = 0, column = 0)
        self.w2 = Label(self.labelbox, text=secondWord, font = "Helvetica 12").grid(row = 0, column = 1)
        self.w3 = Label(self.labelbox, text=thirdWord, font = "Helvetica 12 bold").grid(row = 0, column = 2)

        #Current NE
        self.currentNE = Label(self.labelbox, text="Current NE: ", font = "Helvetica 12").grid(row = 1, column = 0)
        self.ne = Label(self.labelbox, text=NE, font = "Helvetica 12 bold").grid(row = 1, column = 1)

        #Keybindings
        self.Master.bind('m', lambda x: self.Set("MEDICIN"))
        self.Master.bind('s', lambda x: self.Set("SJUKDOM"))
        self.Master.bind('b', lambda x: self.Set("BEHANDLING"))
        self.Master.bind('k', lambda x: self.Set("KEEP"))

        #Buttons
        self.Button=Button(self.Master,text="Medicin",command=lambda: self.Set("MEDICIN")).grid(row = 2, column = 0)
        self.Button=Button(self.Master,text="Sjukdom",command=lambda: self.Set("SJUKDOM")).grid(row = 2, column = 1)
        self.Button=Button(self.Master,text="Behandling",command=lambda:self.Set("BEHANDLING")).grid(row = 2, column = 2)
        self.Button=Button(self.Master,text="Keep Current",command=lambda:self.Set("KEEP")).grid(row = 2, column = 3)
        self.Master.mainloop()

    #Function setting the NE and destroying window
    def Set(self, entityLabel = ""):
        global NE
        NE = entityLabel
        self.Master.destroy()


f2 = open("NE-tagged_blogg_corpus.conll", "w")

with open('blogg_corpus.conll', "r",  encoding='utf-8') as f:
    threeCurrentWords = ["",""]
    for line in f:
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
            if lineList[3] == "PM":
                Windows(firstWord = threeCurrentWords[0], secondWord = threeCurrentWords[1], thirdWord = threeCurrentWords[2])
                lineList[-2] = NE

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