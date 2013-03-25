from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TransparencyAttrib
from panda3d.core import TextNode
from direct.task import Task
from direct.gui.DirectGui import DirectFrame

class MyApp(ShowBase):
    gameMode = "Intro"

    def __init__(self):
        ShowBase.__init__(self)

        #self.cameraSetup()

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
        self.textToType = "Hello this is Silvio Berluspony\nThis is a good conversation box"
        self.textVisible = ""

        #self.txtConvo = OnscreenText(self.textVisible, align = TextNode.ALeft)
        self.txtConvo = TextNode("Texty Bastard")
        self.txtConvo.setText(self.textToType)

        #self.txtConvo.setFrameColor(0, 0, 1, 1)
        #self.txtConvo.setFrameAsMargin(0.2, 0.2, 0.1, 0.1)


        myFrame = DirectFrame(frameColor=(0.8, 0.8, 0.8, 0.4),
                      frameSize=(-1, 0, -1, 0))
        textNodePath = aspect2d.attachNewNode(self.txtConvo)
        textNodePath.setScale(0.07)
        textNodePath.setPos(-1, 0, -0.1)
        self.i = 0

        taskMgr.add(self.gameConvoUpdate, "GameConvoUpdate")


    def gameConvoUpdate(self, task):
        task.delayTime = 0.05
        while (self.i < len(self.textToType)):

            self.textVisible += self.textToType[self.i]
            self.txtConvo.setText(self.textVisible)
            self.i += 1

            return Task.again



app = MyApp()
app.run()