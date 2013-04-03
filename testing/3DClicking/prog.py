import random

from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import CollisionHandlerEvent, CollisionNode, CollisionSphere, CollisionTraverser, BitMask32, CollisionRay
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText

import direct.directbase.DirectStart

from panda3d.core import Geom, GeomNode, GeomTriangles, GeomVertexData, GeomVertexFormat, GeomVertexWriter, NodePath, Texture, TextureStage

camYMove = 0
camXMove = 0
camMovingX = False
camMovingY = False
camSpeed = 1

base.disableMouse()

base.cTrav = CollisionTraverser()
cHandler = CollisionHandlerEvent()

pickerNode = CollisionNode("mouseRayNode")
pickerNPos = base.camera.attachNewNode(pickerNode)
pickerRay = CollisionRay()
pickerNode.addSolid(pickerRay)

pickerNode.setTag("rays","ray1")
base.cTrav.addCollider(pickerNPos, cHandler)

countBuilding = 0
buildingName = []
buildingX = []
buildingY = []



def createBuilding(num,name,x,y):
    oBuilding = loader.loadModel("frowney")
    oBuilding.setName(name)
    oBuilding.reparentTo(render)
    oBuilding.setPos((x,y,1))
    oBuildingCol = oBuilding.attachNewNode(CollisionNode("BuildingCNode%d"%num))
    oBuildingCol.node().addSolid(CollisionSphere(0,0,0,1))
    oBuildingCol.setTag("building","buildPlayer1")

createBuilding(1, "House", 50, 60)

def collideInBuilding(entry):
    np_into=entry.getIntoNodePath()
    np_into.getParent().setColor(.6,.5,1.0,1)

def collideOutBuilding(entry):
    global pickingEnabledObject

    np_into=entry.getIntoNodePath()
    np_into.getParent().setColor(1.0,1.0,1.0,1)

    pickingEnabledObject = None
    txtBox.setText("<No building selected>")


txtBox = OnscreenText("Building Selected: ")

def collideAgainstBuilds(entry):
    global pickingEnabledObject

    if entry.getIntoNodePath().getParent() <> pickingEnabledOject:
        np_from=entry.getFromNodePath()
        np_into=entry.getIntoNodePath()

        pickingEnabledObject = np_into.getParent()

        txtBox.setText(pickingEnabledObject.getName())

def mouseClick(status):
    global pickingEnabledObject

    if pickingEnabledObject:
        if status == "down":
            pickingEnabledObject.setScale(0.95)

        if status == "up":
            pickingEnabledObject.setScale(1.0)

def rayUpdate(task):
    if base.mouseWatcherNode.hasMouse():
        mpos = base.mouseWatcherNode.getMouse()

        pickerRay.setFromLens(base.camNode, mpos.getX(),mpos.getY())
    return task.cont

def moveCam(status):
    global camMovingX
    global camMovingY
    global camXMove
    global camYMove
    global camSpeed

    if status == "up":
        camMovingY = True
        camYMove = camSpeed
    if status == "down":
        camMovingY = True
        camYMove = -camSpeed
    if status == "left":
        camMovingX = True
        camXMove = -camSpeed
    if status == "right":
        camMovingX = True
        camXMove = camSpeed
    if status == "stopX":
        camXMove = 0
        camMovingX = False
    if status == "stopY":
        camYMove = 0
        camMovingY = False

    if status == "rise":
        base.camera.setZ(base.camera.getZ()+1)
    if status == "fall":
        base.camera.setZ(base.camera.getZ()-1)


def updateCam(task):
    global camMovingX
    global camMovingY
    global camXMove
    global camYMove

    if camMovingX:
        base.camera.setX(base.camera.getX()+camXMove)
    if camMovingY:
        base.camera.setY(base.camera.getY()+camYMove)


    #base.camera.setY(base.camera.getY()+0.2)

    return task.cont


from array import array
import os
    #loadLevel("level.txt")

def loadLevel():
    line = ""
    count_buildings = 0
    char = ""
    feed = ""

    path = os.path.abspath(os.getcwd())
    f = open(path+"\\level.txt","r")
    f.readline()
# Get number of buildings
    while char!=";":
        char = f.readline(1)
        if char != ";":
            line += char
        feed += char
        count_buildings = int(line)
    for i in range(count_buildings):
        line = ""
        char = ""
        f.readline()
        while char!=",":
            char = f.readline(1)
            if char != ",":
                line += char
            feed += char

        building = i
        b_name = line

        char = ""
        line = ""
    # Assign X
        while char!=",":
            char = f.readline(1)
            if char != ",":
                line += char
            feed += char
        b_x = int(line)
        char = ""
        line = ""
        while char!=";":
            char = f.readline(1)
            if char != ";":
                line += char
            feed += char
        b_y = int(line)
        text = ("\nBuilding"+str(building)+"\nName: "+str(b_name)+"\nX: "+str(b_x)+"\nY: "+str(b_y))
        createBuilding(building, b_name, b_x, b_y)
        print(text)

    f.close()

loadLevel()

def createPlane(width,height):

    format=GeomVertexFormat.getV3()
    vdata=GeomVertexData("vertices", format, Geom.UHStatic)

    vertexWriter=GeomVertexWriter(vdata, "vertex")
    vertexWriter.addData3f(0,0,0)
    vertexWriter.addData3f(width,0,0)
    vertexWriter.addData3f(width,height,0)
    vertexWriter.addData3f(0,height,0)

    #step 2) make primitives and assign vertices to them
    tris=GeomTriangles(Geom.UHStatic)

    #have to add vertices one by one since they are not in order
    tris.addVertex(0)
    tris.addVertex(1)
    tris.addVertex(3)

    #indicates that we have finished adding vertices for the first triangle.
    tris.closePrimitive()

    #since the coordinates are in order we can use this convenience function.
    tris.addConsecutiveVertices(1,3) #add vertex 1, 2 and 3
    tris.closePrimitive()

    #step 3) make a Geom object to hold the primitives
    squareGeom=Geom(vdata)
    squareGeom.addPrimitive(tris)

    #now put squareGeom in a GeomNode. You can now position your geometry in the scene graph.
    squareGN=GeomNode("square")
    squareGN.addGeom(squareGeom)

    terrainNode = NodePath("terrNode")
    terrainNode.reparentTo(render)
    terrainNode.attachNewNode(squareGN)
    terrainNode.setX(-width/2)
    texGrass = loader.loadTexture("textures/envir-ground.jpg")
    terrainNode.setTexture(texGrass)

cHandler.addInPattern("%(rays)ft-into-%(building)it")
cHandler.addOutPattern("%(rays)ft-out-%(building)it")

cHandler.addAgainPattern("ray_again_all%(""rays"")fh%(""building"")ih")

DO=DirectObject()

DO.accept('ray1-into-buildPlayer1', collideInBuilding)
DO.accept('ray1-out-buildPlayer1', collideOutBuilding)

DO.accept('ray_again_all', collideAgainstBuilds)

pickingEnabledOject=None

DO.accept('mouse1', mouseClick, ["down"])
DO.accept('mouse1-up', mouseClick, ["up"])

DO.accept("w",moveCam, ["up"])
DO.accept("s",moveCam, ["down"])
DO.accept("w-up",moveCam, ["stopY"])
DO.accept("s-up",moveCam, ["stopY"])
DO.accept("a",moveCam, ["left"])
DO.accept("d",moveCam, ["right"])
DO.accept("a-up",moveCam, ["stopX"])
DO.accept("d-up",moveCam, ["stopX"])
DO.accept("space",moveCam, ["rise"])
DO.accept("shift",moveCam, ["fall"])

#** And at the end of all, we start the task that continuously update the ray collider position and orientation while we move the mouse pointer
taskMgr.add(rayUpdate, "updatePicker")
taskMgr.add(updateCam, "updateCam")
createPlane(100, 100)

run()