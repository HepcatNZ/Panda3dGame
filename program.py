from math import pi, sin, cos
from array import *

from pandac.PandaModules import CollisionHandlerQueue, CollisionNode, CollisionSphere, CollisionTraverser, CollisionTube


from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from direct.showbase import DirectObject
from panda3d.core import Point3
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
import math

from direct.showbase.DirectObject import DirectObject


# for cam control
from pandac.PandaModules import *



class MyApp(ShowBase):


	def __init__(self):
		ShowBase.__init__(self)

		self.cTrav = CollisionTraverser()
		self.cHandler = CollisionHandlerEvent()

		self.gameMode = "Exploring"

		self.countNpc = 0
		self.npcName = []
		self.npcX = []
		self.npcY = []

		self.talkies = False

		self.txtConvo = OnscreenText("",style=1, align = TextNode.ALeft, fg=(1,1,1,1), pos = (-1.1,-0.6,0), scale = 0.1)
		self.txtConvoOp1 = OnscreenText("",style=1, align = TextNode.ALeft, fg=(1,1,1,1), pos = (-1.1,-0.65,0), scale = 0.1)
		self.txtConvoOp2 = OnscreenText("",style=1, align = TextNode.ALeft, fg=(1,1,1,1), pos = (-1.1,-0.7,0), scale = 0.1)
		self.txtConvoOp3 = OnscreenText("",style=1, align = TextNode.ALeft,fg=(1,1,1,1), pos = (-1.1,-0.75,0), scale = 0.1)
		self.convoLineSelected = 0

		self.keyboardSetup()

		self.cameraDistance = -50
		self.camHeight = 25
		
		self.camXAngle = 180
		self.camYAngle = -15
		self.camZAngle = 0
		
		self.corrAngle = math.pi / 2


		self.createPlayer()
		self.terrainSize = 20
		self.drawTerrain()
		self.placeModels()


		self.collides()

		#cTrav.showCollisions(render)

		self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
		self.taskMgr.add(self.step, "GameStep")




		self.drawUI()

	def createPlayer(self):
		self.player = self.loader.loadModel("models/man.x") #,{"walk": "models/panda-walk4"}
		self.playerNode = render.attachNewNode("PlayerNode")
		self.playerNode.setScale(1, 1, 1)

		self.playerCollider = self.playerNode.attachNewNode(CollisionNode("playerCollider"))
		self.playerCollider.node().addSolid(CollisionSphere(0,0,0,5))
		self.player.reparentTo(self.playerNode)



		self.cTrav.addCollider(self.playerCollider, self.cHandler)
		#self.playerCollider.show()

		self.playerY = 50
		self.playerX = 50
		self.playerZ = 0
		
		self.playerDir = 0.0
		self.playerMove = 0.0
		self.playerTurn = 0.0
		self.playerJumpHeight = 2
		self.playerJumpDist = 0
		self.playerJumpGrav = 0.2
		self.playerJump = 0

		self.playerSpeed = 6
		self.playerTurnSpeed = 1
		self.playerNode.setH(self.playerDir)

	def step(self, task):
		#self.txtStats
		if self.gameMode == "Exploring":
			if (self.playerMove != 0):
				self.movePlayer(task)
			if (self.playerTurn != 0):
				self.turnPlayer(task)
			if (self.playerJumpDist > 0):
				self.playerJumpDist += self.playerJump
				self.playerJump -= self.playerJumpGrav
			if (self.playerJumpDist <= 1):
				self.playerJumpDist = 0

		self.drawPlayer()
		#self.updateStats()

		return Task.cont

	def spinCameraTask(self, task):
		if (self.playerMove == 0 and self.gameMode == "Exploring"):
			self.playerAngle = self.playerNode.getH() * math.pi / 180
			self.camX = self.playerX + self.cameraDistance * math.cos( self.corrAngle - self.playerAngle )
			self.camY = self.playerY + self.cameraDistance * -math.sin( self.corrAngle - self.playerAngle )
			self.camZ = self.getObjectZ(self.playerX, self.playerY) + self.camHeight

			self.camera.setPos(self.camX, self.camY, self.camZ)
			self.camera.setHpr(self.playerDir + self.camXAngle, self.camYAngle, self.camZAngle)
			
		if (self.gameMode == "Conversation"):
			self.playerAngle = self.playerNode.getH() * math.pi / 180
			self.camX = self.playerX + self.cameraDistance * math.cos( self.corrAngle - self.playerAngle )
			self.camY = self.playerY + self.cameraDistance * -math.sin( self.corrAngle - self.playerAngle )
			self.camZ = self.getObjectZ(self.playerX, self.playerY) + self.camHeight

			self.camera.setPos(self.playerX, self.playerY, self.playerZ + 10)
			self.camera.lookAt(self.talkiesNpc.getX(), self.talkiesNpc.getY(), self.talkiesNpc.getZ() + 10)


		return Task.cont

	def drawUI(self):
		self.imgInv = dict()
		for box in range (0, 5):
			self.imgInv[box] = OnscreenImage(image = "textures/inventoryBox.png", pos = ((box * 0.22) -1, 0, -0.9), scale = (0.1, 0.1, 0.1))
			self.imgInv[box].setTransparency(TransparencyAttrib.MAlpha)

	def getObjectZ(self, x, y):
		if ((x > 0) and (x < 257) and (y > 0) and (y < 257)):
			return(self.terrain.getElevation(x,y)*self.terrainSize)
		else:
			return 0

	def placeModels(self):
		cubeCount = 12
		cubeXInc = 24

		cubeGen = 0
		cubeGenX = 0
		cubeGenY = -50

		cubeGenScale = 10
		cubeGenRot = 90

		while (cubeGen < cubeCount):
			cube = self.loader.loadModel("models/house2.x")
			cube.reparentTo(self.render)
			cube.setScale(cubeGenScale, cubeGenScale*2, cubeGenScale)
			cube.setPos(0+cubeXInc*cubeGen, cubeGenY, 0)

			cubeGen += 1

		cubeGen = 0
		while (cubeGen < cubeCount):
			cubeGen += 1

		self.placeNPC("Sally Susan",-50,-50)
		self.placeNPC("Gerald Fanturbett",-80,-40)
		self.placeNPC("Pillynostrum MacSternum",-20,-100)


	def placeNPC(self,name,x,y):
		npcScale = 1
		npcTexture = loader.loadTexture("textures/texRock2.png")

		self.npc = self.loader.loadModel("models/man.x")
		self.npcNode = render.attachNewNode("NpcNode")
		self.npc.reparentTo(self.npcNode)
		self.npcName+=[name]
		self.npc.setName(name)
		self.npc.setScale(1, 1, 1)
		self.npc.setPos(x,y,0)
		self.npcX += [x]
		self.npcY += [y]

		self.npc.setTexture(npcTexture)

		self.npcCollider = self.npc.attachNewNode(CollisionNode("npcCollider"))
		self.npcCollider.node().addSolid(CollisionSphere(0, 0, 0, 5))

		self.countNpc += 1
		#self.npcCollider.show()

	def conversationWithNPC(self):
		if self.talkies == True and self.gameMode != "Conversation":
			self.txtConvo.setText("HEY! LETS TALK!")
			self.txtConvoOp1.setText("")
			self.txtConvoOp2.setText("")
			self.txtConvoOp3.setText("")
			self.gameMode = "Conversation"
		elif self.gameMode == "Conversation":
			self.gameMode = "Exploring"


	def drawTerrain(self):
		self.terrain = GeoMipTerrain("terrain")
		self.terrain.setHeightfield(Filename("textures/heights.png"))
		#self.terrain.setColorMap("textures/texRock2.png")
		self.terrain.setColorMap("textures/heightColour.png")

		self.terrain.setBlockSize(8)
		self.terrain.setFactor(0)
		self.terrain.setNear(40)
		self.terrain.setFar(120)
		self.terrain.setMinLevel(1)
		self.terrain.setBruteforce(True)
		self.terrain.generate()
		self.terrain.setAutoFlatten(self.terrain.AFMLight)
		self.terrain.setFocalPoint(Point3(self.playerX,self.playerY,self.playerZ))

		self.root = self.terrain.getRoot()
		self.root.reparentTo(render)
		self.root.setSz(self.terrainSize)

	def jumpPlayer(self):
		if (self.playerJumpDist == 0):
			self.playerJump = self.playerJumpHeight
			self.playerJumpDist += self.playerJump

	def movePlayer(self, task):
		self.playerAngle = self.playerNode.getH( ) * math.pi / 180.0
		
		self.dx = self.playerMove * math.cos( self.corrAngle - self.playerAngle )
		self.dy = self.playerMove * -math.sin( self.corrAngle - self.playerAngle )

		self.playerAngle = self.playerNode.getH( ) * math.pi / 180.0
		self.camX = self.playerX+self.cameraDistance*math.cos( self.corrAngle - self.playerAngle )
		self.camY = self.playerY+self.cameraDistance*-math.sin( self.corrAngle - self.playerAngle )

		move = True
		#if self.distance(self.playerX + self.dx/10,self.npcNode.getX(),self.)

		for i in range(self.countNpc):
			xi = self.playerX+ self.dx / 10
			xii = self.npcX[i]
			yi = self.playerY+ self.dy / 10
			yii = self.npcY[i]
			sq1 = (xi-xii)*(xi-xii)
			sq2 = (yi-yii)*(yi-yii)
			distance = math.sqrt(sq1 + sq2)
			if distance < 5:
				move = False
		#self.txtConvoOp1.setText(str(math.sqrt(sq1 + sq2)))

		if move == True:
			self.playerX += self.dx / 10
			self.playerY += self.dy / 10
		self.playerZ = self.getObjectZ(self.playerX, self.playerY)
		self.camZ = self.getObjectZ(self.playerX, self.playerY) + self.camHeight
		self.playerNode.setPos(self.playerX, self.playerY, self.playerZ + self.playerJumpDist)
		self.camera.setPos(self.camX, self.camY, self.camZ)
		self.camera.setHpr(self.playerDir + self.camXAngle, self.camYAngle, self.camZAngle)
		
		self.terrain.setFocalPoint(Point3(self.playerX, self.playerY, self.playerZ))
		self.terrain.update()

	def drawPlayer(self):
		self.playerNode.setPos(self.playerX, self.playerY, self.playerZ + self.playerJumpDist)

	def turnPlayer(self, task):
		self.playerDir += self.playerTurn
		self.playerNode.setH(self.playerDir)

	def keyboardSetup( self ):
		self.accept("w", self.keyW)
		self.accept("w-up", self.resetMove)
		self.accept("s", self.keyS)
		self.accept("s-up", self.resetMove)
		self.accept("a", self.keyA)
		self.accept("enter", self.conversationWithNPC)
		self.accept("a-up", self.resetDir)
		self.accept("d", self.keyD)
		self.accept("d-up", self.resetDir)
		self.accept("space", self.jumpPlayer)

	def collideEventIn(self, entry):
		np_into=entry.getIntoNodePath()
		self.txtConvo.setText("<Press Enter to talk to %s>"%np_into.getParent().getName())
		np_into.getParent().setHpr(self.playerDir + 270, 0, 0)
		self.talkies = True
		self.talkiesNpc = np_into.getParent()

	def collideEventOut(self, entry):
		self.txtConvo.setText("")
		self.talkies = False
		self.gameMode = "Exploring"

	def collides(self):

		self.cHandler.addInPattern('%fn-into-%in')
		self.cHandler.addOutPattern('%fn-out-%in')

		DO=DirectObject()

		DO.accept("playerCollider-into-npcCollider", self.collideEventIn)
		DO.accept("playerCollider-out-npcCollider", self.collideEventOut)
		#DO.accept("tCol1-into-tCol2", self.collideEventIn)

	def keyW( self ):
		self.playerMove = self.playerSpeed

	def resetMove( self ):
		self.playerMove = 0

	def resetDir( self ):
		self.playerTurn = 0

	def keyS( self ):
		self.playerMove = -self.playerSpeed

	def keyA( self ):
		self.playerTurn = self.playerTurnSpeed

	def keyD( self ):
		self.playerTurn = -self.playerTurnSpeed

app = MyApp()
app.run()


