from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TransparencyAttrib
from panda3d.core import TextNode
from direct.task import Task
from direct.gui.DirectGui import DirectFrame
import os
import sys

class MyApp(ShowBase):
    gameMode = "Intro"

    def __init__(self):
        ShowBase.__init__(self)

        #self.cameraSetup()
        self.setupKeyboard()

        self.initIntro()

    def gameChangeMode(self):
        if base.gameMode == "Intro":
            self.initIntro()
        elif base.gameMode == "Convo":
            self.initConvo()

    def initIntro(self):
        self.fadeAlpha = 0.0
        self.fadeTime = 30.0
        self.fadeInc = 1.0/self.fadeTime
        self.fadeDir = "up"

        self.sceneImage = OnscreenImage(image = "images/scene.png", scale = (1920.0/1080.0,1,1))
        self.sceneImage.setTransparency(TransparencyAttrib.MAlpha)
        self.sceneImage.setAlphaScale(self.fadeAlpha)

        self.imageNumber = 0
        self.sceneImageList = ["images/scene.png","images/image1.jpg"]

        #self.texty = OnscreenText(str(self.fadeAlpha))

        taskMgr.add(self.gameIntroUpdate, "GameIntroUpdate")

    def gameIntroUpdate(self, task):
        self.slideManager()
        if (base.gameMode != "Intro"):
            self.gameChangeMode()
            return Task.done

        return Task.cont

    def cameraSetup(self):
        base.camLens.setAspectRatio(1920.0/1080.0)

    def slideManager(self):
        if self.fadeDir == "up" and self.fadeAlpha<1:
            self.fadeAlpha += self.fadeInc
            self.sceneImage.setAlphaScale(self.fadeAlpha)
            #self.texty.setText(str(self.fadeAlpha))

        if self.fadeDir == "down" and self.fadeAlpha > 0:
            self.fadeAlpha -= self.fadeInc
            self.sceneImage.setAlphaScale(self.fadeAlpha)

        if self.fadeDir == "up" and self.fadeAlpha >= 1:
            self.fadeDir = "down"

        if self.fadeDir == "down" and self.fadeAlpha <= 0:
            if self.imageNumber < 1:
                self.fadeDir = "up"
                self.sceneImage.setImage(self.nextImage())
                self.sceneImage.setTransparency(TransparencyAttrib.MAlpha)
                self.sceneImage.setAlphaScale(self.fadeAlpha)
            else:
                self.fadeDir = "up"
                base.gameMode = "Convo"
                self.sceneImage.setImage(self.sceneImageList[self.imageNumber])
                self.sceneImage.setTransparency(TransparencyAttrib.MAlpha)
                self.sceneImage.setAlphaScale(self.fadeAlpha)

    def nextImage(self):
            self.imageNumber += 1
            return self.sceneImageList[self.imageNumber]

    def initConvo(self):
        self.textToType = "This will be used for talking\nThis is a good conversation box"
        self.textVisible = ""

        self.strOptionA = "Yes"
        self.strOptionB = "No"
        self.strOptionC = "Maybe"

        self.convoResponseSelected = False
        self.convoDepth = "1"

        self.intOptionCount = 3

        #self.txtConvo = OnscreenText(self.textVisible, align = TextNode.ALeft)
        self.txtConvo = TextNode("Texty Bastard")
        self.txtConvo.setText(self.textToType)
        self.txtReply = TextNode("reply")
        self.txtReply.setText("")
        self.intHover = 0

        #self.txtConvo.setFrameColor(0, 0, 1, 1)
        #self.txtConvo.setFrameAsMargin(0.2, 0.2, 0.1, 0.1)



        myFrame = DirectFrame(frameColor=(0.8, 0.8, 0.8, 0.4),
                      frameSize=(-1, 0, -1, 0))
        nodePathConvo = aspect2d.attachNewNode(self.txtConvo)
        nodePathConvo.setScale(0.07)
        nodePathConvo.setPos(-1, 0, -0.1)
        self.i = 0
        self.indent = 0.0
        self.selectedResponse = 0
        self.txtOptionA = OnscreenText(text = "", pos = (-1,-0.6), align = TextNode.ALeft)
        self.txtOptionB = OnscreenText(text = "", pos = (-1,-0.7), align = TextNode.ALeft)
        self.txtOptionC = OnscreenText(text = "", pos = (-1,-0.8), align = TextNode.ALeft)

        taskMgr.add(self.gameConvoUpdate, "GameConvoUpdate")

    def gameConvoUpdate(self, task):

        if (len(self.textVisible) != len(self.textToType)):
			task.delayTime = 0.001
			while (self.i < len(self.textToType)):

				self.textVisible += self.textToType[self.i]
				self.txtConvo.setText(self.textVisible)
				self.i += 1

				return Task.again

        else:
            taskMgr.add(self.gameConvoOptions, "ConvoOptions")
            return Task.done

    def gameConvoOptions(self, task):
        self.txtOptionA.setText(self.strOptionA)
        self.txtOptionB.setText(self.strOptionB)
        self.txtOptionC.setText(self.strOptionC)

        if self.convoResponseSelected == True:
            if self.convoCheckBranch("01", self.convoDepth):
                #self.txtConvo.setText(self.convoGetStrings("01", self.convoDepth))
                self.convoNextDialogue("01", self.convoDepth)
            else:
                #self.txtConvo.setText("It DIDn't worked")
                self.convoDepth = "1"
                self.convoNextDialogue("01", self.convoDepth)
            return Task.done

        elif self.selectedResponse == 0:
            if self.intOptionCount > 0:
                self.txtOptionA.setX(-1+self.indent)
                self.txtOptionA.setFg(fg = (1,0,0,1))
            if self.intOptionCount > 1:
                self.txtOptionB.setX(-1)
                self.txtOptionB.setFg(fg = (0,0,0,1))
            if self.intOptionCount > 2:
                self.txtOptionC.setX(-1)
                self.txtOptionC.setFg(fg = (0,0,0,1))
            self.indent = self.getIndent(self.indent,0.01,0.1)
            return Task.again

        elif self.selectedResponse == 1:
            if self.intOptionCount > 0:
                self.txtOptionA.setX(-1)
                self.txtOptionA.setFg(fg = (0,0,0,1))
            if self.intOptionCount > 1:
                self.txtOptionB.setX(-1+self.indent)
                self.txtOptionB.setFg(fg = (1,0,0,1))
            if self.intOptionCount > 2:
                self.txtOptionC.setX(-1)
                self.txtOptionC.setFg(fg = (0,0,0,1))
            self.indent = self.getIndent(self.indent,0.01,0.1)
            return Task.again

        elif self.selectedResponse == 2:
            if self.intOptionCount > 0:
                self.txtOptionA.setX(-1)
                self.txtOptionA.setFg(fg = (0,0,0,1))
            if self.intOptionCount > 1:
                self.txtOptionB.setX(-1)
                self.txtOptionB.setFg(fg = (0,0,0,1))
            if self.intOptionCount > 2:
                self.txtOptionC.setX(-1+self.indent)
                self.txtOptionC.setFg(fg = (1,0,0,1))
            self.indent = self.getIndent(self.indent,0.01,0.1)
            return Task.again

    def convoGetStrings(self,npcId,depth):
        if self.convoCheckBranch(npcId,depth) != True:
            return "#Error# String Not Found\nLooking for: "+"("+str(npcId)+")."+depth+":"
        char = ""
        line = ""
        feed = ""



        path = os.path.abspath(os.getcwd())
        f = open(path+"\\text\\stringsConvo.txt","r")
        while line != "("+str(npcId)+")."+depth+":":
            while char != ":":
                char = f.readline(1)
                line += char
            feed += "\n"+line
            if line != "("+str(npcId)+")."+depth+":":
                char = ""
                line = ""
                f.readline()
        print(feed + " Selected")
        f.readline(1)
        line = f.readline()
        line = line.replace("##", "\n")
        f.close()
        return line

    def convoCheckBranch(self,npcId,depth):
        path = os.path.abspath(os.getcwd())
        f = open(path+"\\text\\stringsConvo.txt","r")
        char = ""
        line = ""
        branchFound = False

        while line != "<END>:":
            char = ""
            line = ""
            while char != ":":
                char = f.readline(1)
                line += char
            if line == "<END>:":
                f.close()
                return False
            elif line == "("+str(npcId)+")."+str(depth)+":":
                f.close()
                return True
            else:
                f.readline()

    def convoNextDialogue(self,npcId,depth):
        self.textToType = self.convoGetStrings(npcId, depth)
        self.intOptionCount = self.convoGetOptionCount(npcId, depth)

        if self.intOptionCount == 1:
            self.strOptionA = self.convoGetStrings(npcId, depth+".A")
            self.strOptionB = ""
            self.strOptionC = ""
        elif self.intOptionCount == 2:
            self.strOptionA = self.convoGetStrings(npcId, depth+".A")
            self.strOptionB = self.convoGetStrings(npcId, depth+".B")
            self.strOptionC = ""
        elif self.intOptionCount == 3:
            self.strOptionA = self.convoGetStrings(npcId, depth+".A")
            self.strOptionB = self.convoGetStrings(npcId, depth+".B")
            self.strOptionC = self.convoGetStrings(npcId, depth+".C")
        else:
            self.strOptionA = ""
            self.strOptionB = ""
            self.strOptionC = ""

        self.textVisible = ""
        self.txtOptionA.setText("")
        self.txtOptionB.setText("")
        self.txtOptionC.setText("")
        self.txtConvo.setText(self.textVisible)
        #self.intOptionCount = 2
        self.selectedResponse = 0
        self.i = 0
        self.convoResponseSelected = False
        taskMgr.add(self.gameConvoUpdate, "GameConvoUpdate")

    def convoGetOptionCount(self,npcId,depth):
        if self.convoCheckBranch(npcId,depth+".A") and self.convoCheckBranch(npcId,depth+".B") and self.convoCheckBranch(npcId,depth+".C"):
            return 3
        elif self.convoCheckBranch(npcId,depth+".A") and self.convoCheckBranch(npcId,depth+".B"):
            return 2
        elif self.convoCheckBranch(npcId,depth+".A"):
            return 1
        else:
            return 0

    def getIndent(self, value, increment, limit):
        if (value + increment >= limit):
            return limit
        else:
            return value+increment

    def setupKeyboard(self):
        self.accept("arrow_down", self.convoOptionDown)
        self.accept("arrow_up", self.convoOptionUp)
        self.accept("enter",self.convoOptionSelect)

    def convoOptionUp(self):
        self.indent = 0.0
        if self.selectedResponse == 0:
            self.selectedResponse = self.intOptionCount-1
        elif self.selectedResponse > 0:
            self.selectedResponse -= 1

    def convoOptionDown(self):
        self.indent = 0.0
        if self.selectedResponse < self.intOptionCount-1:
            self.selectedResponse += 1
        elif self.selectedResponse == self.intOptionCount-1:
            self.selectedResponse = 0

    def convoOptionSelect(self):
        if self.selectedResponse == 0:
            self.convoDepth += ".A.1"
        elif self.selectedResponse == 1:
            self.convoDepth += ".B.1"
        elif self.selectedResponse == 2:
            self.convoDepth += ".C.1"

        self.convoResponseSelected = True



app = MyApp()
app.run()