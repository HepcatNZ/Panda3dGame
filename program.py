from math import pi, sin, cos
from array import *


from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from direct.showbase import DirectObject
from panda3d.core import Point3
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
import math


# for cam control
from pandac.PandaModules import *

class MyApp(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)



		self.txtConvo = OnscreenText("Jim Bob:",style=1, align = TextNode.ALeft, fg=(1,1,1,1), pos = (-1.1,-0.6,0), scale = 0.1)
		self.txtConvoOp1 = OnscreenText("  - ",style=1, align = TextNode.ALeft, fg=(1,1,1,1), pos = (-1.1,-0.65,0), scale = 0.1)
		self.txtConvoOp2 = OnscreenText("  - ",style=1, align = TextNode.ALeft, fg=(1,1,1,1), pos = (-1.1,-0.7,0), scale = 0.1)
		self.txtConvoOp3 = OnscreenText("  - ",style=1, align = TextNode.ALeft,fg=(1,1,1,1), pos = (-1.1,-0.75,0), scale = 0.1)
		self.convoLineSelected = 0

		self.keyboardSetup()

		#self.cTrav=CollisionTraverser()
		#self.collisionHandler = CollisionHandlerQueue()

		self.cameraDistance = -50
		self.camAngle = -15



		self.createPlayer()

		self.terrainSize = 50
		self.drawTerrain()
		self.placeModels()
		self.placeNPC()

		self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
		self.taskMgr.add(self.step, "GameStep")

		#base.cTrav=CollisionTraverser()
		#collisionHandler = CollisionHandlerQueue()



		self.drawUI()

	def createPlayer(self):
		self.player = self.loader.loadModel("models/man.x") #,{"walk": "models/panda-walk4"}
		self.playerNode = render.attachNewNode("PlayerNode")
		self.playerNode.setScale(1, 1, 1)
		#self.playerCollider = self.player.attachNewNode(CollisionNode('smileycnode'))
		#self.playerCollider.node().addSolid(CollisionSphere(0, 0, 0, 1))
		self.player.reparentTo(self.playerNode)

		#self.cTrav.addCollider(self.playerCollider, self.collisionHandler)

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
		self.playerNode.setH(self.playerDir+90)

	def step(self, task):
		#self.txtStats
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
		if (self.playerMove == 0):
			self.playerAngle = self.playerNode.getH( ) * math.pi / 180.0
			self.corrAngle = math.pi / 2
			self.camX = self.playerX+self.cameraDistance*math.cos( self.corrAngle - self.playerAngle )
			self.camY = self.playerY+self.cameraDistance*-math.sin( self.corrAngle - self.playerAngle )

			self.corrAngle = math.pi / 2
			self.camX = self.playerX+self.cameraDistance*math.cos( self.corrAngle - self.playerAngle )
			self.camY = self.playerY+self.cameraDistance*-math.sin( self.corrAngle - self.playerAngle )
			self.camZ = self.getObjectZ(self.playerX,self.playerY)+25

			self.camera.setPos(self.camX, self.camY, self.camZ)
			self.camera.setHpr(self.playerDir+270, self.camAngle, 0)

		return Task.cont

	#def updateStats(self):
		#self.txtStats.setText("playerX: "+str(self.playerX)+" playerY: "+str(self.playerY)+" playerZ: "+str(self.playerZ))

	def drawUI(self):
		self.imgInv1 = OnscreenImage(image = "textures/inventoryBox.png", pos = (-1, 0, -0.9), scale = (0.1,0.1,0.1))
		self.imgInv1.setTransparency(TransparencyAttrib.MAlpha)
		self.imgInv2 = OnscreenImage(image = "textures/inventoryBox.png", pos = (-0.78, 0, -0.9), scale = (0.1,0.1,0.1))
		self.imgInv2.setTransparency(TransparencyAttrib.MAlpha)
		self.imgInv3 = OnscreenImage(image = "textures/inventoryBox.png", pos = (-0.56, 0, -0.9), scale = (0.1,0.1,0.1))
		self.imgInv3.setTransparency(TransparencyAttrib.MAlpha)
		self.imgInv4 = OnscreenImage(image = "textures/inventoryBox.png", pos = (-0.34, 0, -0.9), scale = (0.1,0.1,0.1))
		self.imgInv4.setTransparency(TransparencyAttrib.MAlpha)
		self.imgInv5 = OnscreenImage(image = "textures/inventoryBox.png", pos = (-0.12, 0, -0.9), scale = (0.1,0.1,0.1))
		self.imgInv5.setTransparency(TransparencyAttrib.MAlpha)

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


	def placeNPC(self):
		npcX = -50
		npcY = -50
		npcScale = 1

		self.npc = self.loader.loadModel("models/man.x")
		self.npcNode = render.attachNewNode("PlayerNode")
		self.npc.reparentTo(self.npcNode)
		self.npcNode.setScale(1, 1, 1)
		self.npcNode.setPos(npcX,npcY,0)

		#self.conversationWithNPC()

		#self.npcCollider = frowneyModel.attachNewNode(CollisionNode('npcColNode'))
		#self.npcCollider.node().addSolid(CollisionSphere(0, 0, 0, 1))

	def conversationWithNPC(self):
		self.txtConvo.setText("Jim Bob:")
		self.txtConvoOp1.setText("  - ")
		self.txtConvoOp2.setText("  - ")
		self.txtConvoOp3.setText("  - ")


	def drawTerrain(self):
		self.terrain = GeoMipTerrain("terrain")
		self.terrain.setHeightfield(Filename("textures/heights.png"))
		self.terrain.setColorMap("textures/texRock2.png")

		self.terrain.setBlockSize(64)
		self.terrain.setFactor(1)
		self.terrain.setNear(40)
		self.terrain.setFar(120)
		self.terrain.setMinLevel(0)
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
		self.corrAngle = math.pi / 2

		self.dx = self.playerMove * math.cos( self.corrAngle - self.playerAngle )
		self.dy = self.playerMove * -math.sin( self.corrAngle - self.playerAngle )

		self.playerAngle = self.playerNode.getH( ) * math.pi / 180.0
		self.corrAngle = math.pi / 2
		self.camX = self.playerX+self.cameraDistance*math.cos( self.corrAngle - self.playerAngle )
		self.camY = self.playerY+self.cameraDistance*-math.sin( self.corrAngle - self.playerAngle )

		self.playerX += self.dx / 10
		self.playerY += self.dy / 10
		self.playerZ = self.getObjectZ(self.playerX,self.playerY)
		self.camZ = self.getObjectZ(self.playerX,self.playerY)+25
		self.playerNode.setPos(self.playerX, self.playerY, self.playerZ+self.playerJumpDist)
		self.camera.setPos(self.camX, self.camY, self.camZ)
		self.camera.setHpr(self.playerDir+270, self.camAngle, 0)

		self.terrain.setFocalPoint(Point3(self.playerX,self.playerY,self.playerZ))
		self.terrain.update()

	def drawPlayer(self):
		self.playerNode.setPos(self.playerX, self.playerY, self.playerZ+self.playerJumpDist)

	def turnPlayer(self, task):
		self.playerDir += self.playerTurn
		self.playerNode.setH(self.playerDir+90)

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


