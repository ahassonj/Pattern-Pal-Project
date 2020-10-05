# File creating the basic user interface app mode of the project that lets users draw and tesellate a base pattern.
import basic_graphics
import math
import decimal
import json
from tkinter import *

from cmu_112_graphics import *
from patternObjects import * 
from allDrawFunctions import *
from PIL import ImageGrab

# subapp mode that creates a base grid where the user can draw and then a tesellating grid that repeats
# the same pattern in different ways
class buildPattern(Mode):
    def appStarted(mode):
        # all app attributes added below for the different modes and lists needed
        mode.changeSlider = False
        mode.appStarterMessage = True
        mode.squareScale, mode.starScale = .765, 0
        mode.sliderLocation = point(mode.width - 20, mode.width / 2)
        mode.level = 1
        mode.dotsize = mode.height / 600
        mode.drawUserPattern = False
        mode.drawSquares = False
        mode.drawHex = False
        mode.drawHex2 = False
        mode.showDistances = False
        mode.distanceMode = False
        mode.angleMode = False
        mode.angleLines = []
        mode.anglePoints = []
        mode.pointsForDistance = []
        mode.distanceLine = None
        mode.userColor = 'red'
        mode.colorMode = False
        mode.colorPalette = 0
        mode.colorBoard = mode.getColorGrid()
        mode.margin = mode.width * .1
        mode.cellSize = (mode.width - mode.margin) / 52
        mode.circleMode = 1
        mode.createCircle = False
        mode.currentCirc = None
        mode.circList = []
        mode.createPolygon = False
        mode.currentPol = None
        mode.polygonList = []
        mode.angleText = None
        mode.outlinePoints = []
        mode.freeDraw = False
        mode.shapeList = []
        mode.currentShape = None
        mode.outlinePoints = []
        mode.pic = None

    # function for saving drawn shapes, circles, polygons and their colors to the user's hard drive
    def savePatternToFile(mode):
        shapes = []
        shapeColors = []
        circles = []
        circColors = []
        polygons = []
        polygonColors = []
        # creating lists for storing all the integer values of each shape, circle, etc. in order to convert to JSON
        for shape in mode.shapeList:
            resultPoints = []
            for p in shape.points:
                resultPoints.append((p.x, p.y))
            shapes.append(resultPoints)
            shapeColors.append(shape.color)
        for circ in mode.circList:
            circCenter = (circ.center.x, circ.center.y)
            circles.append([circCenter, circ.rad])
            circColors.append(circ.color)
        for pol in mode.polygonList:
            polCenter = (pol.center.x, pol.center.y)
            polygons.append([polCenter, pol.size, pol.rangle, pol.numSides])
            polygonColors.append(pol.color)
        
        # creates a dictionary storing all the resulting the shape, circle, etc. lists that can be converted to one string
        filePath = mode.getUserInput("What name would you like to save your file as? ---> ")
        canvasObjects = {'shapes': shapes, 'shapeColors': shapeColors, 'circles': circles,
                            'circColors': circColors, 'polygons': polygons, 'polygonColors': polygonColors}
        if filePath == None:
            mode.app.showMessage("You didn't enter a name to save the file")
        else:
            # creates a JSON string from the dictionary that is then written into user's hard drive
            objectsToWrite = json.dumps(canvasObjects)
            writeFile(filePath + '.txt', objectsToWrite)

    # opens an existing pattern drawn by the user by taking a file saved on their computer
    def openPatternFromFile(mode):
        filePath = mode.getUserInput("Enter the saved pattern on your computer that you would like to open ---> ")
        if filePath == None:
            mode.app.showMessage("You didn't enter a valid file name")
            return None
        else:
            # takes the string from the text file and converts it back into a dictionary
            objectString = readFile(filePath + '.txt')
            objects = json.loads(objectString)
            resultShapes, resultCircs, resultPols = [], [], []
            # loops through the different shape lists in the dictionary to create resulting shapes, circles, etc. that are
            # then added back into the app attribute shapes
            for i in range(len(objects['shapes'])):
                newFreeShape = freeShape2(objects['shapeColors'][i])
                for coordinates in objects['shapes'][i]:
                    x, y = coordinates
                    newFreeShape.points.append(point(x, y))
                resultShapes.append(newFreeShape)
            for i in range(len(objects['circles'])):
                cx, cy = objects['circles'][i][0]
                tempCircle = patternCircle(point(cx, cy), objects['circColors'][i])
                tempCircle.rad = objects['circles'][i][1]
                resultCircs.append(tempCircle)
            for i in range(len(objects['polygons'])):
                cx, cy = objects['polygons'][i][0]
                tempPol = patternPolygon(point(cx, cy), objects['polygons'][i][3], objects['polygonColors'][i])
                tempPol.size = objects['polygons'][i][1]
                tempPol.rangle = objects['polygons'][i][2]
                resultPols.append(tempPol)
            return (resultShapes, resultCircs, resultPols)

    def keyPressed(mode, event):
        # different key commands for operating the app interface and drawing the pattern
        mode.appStarterMessage = False
        if event.key == 'g':
            mode.app.setActiveMode(mode.app.helpScreen)
        elif event.key == 'v':
            mode.dotsize += .1
        elif event.key == 'Escape':
            mode.app.setActiveMode(mode.app.changeTemplate)
        elif event.key == 'k':
            mode.dotsize -= .1
        elif event.key == 'b':
            mode.changeSlider = not mode.changeSlider
            mode.createCircle = False
            mode.createPolygon = False
            mode.freeDraw = False
        elif event.key == 'w':
            # code below copied from 15112 course notes page on Image Methods from App Class Part 2
            snapshotImage = mode.app.getSnapshot()
            mode.app.saveSnapshot()
        elif event.key == 'Enter':
            mode.drawUserPattern = not mode.drawUserPattern
        elif event.key == 'l':
            mode.app.setActiveMode(mode.app.gridOptions)
        elif event.key == 'u':
            mode.circleMode = (mode.circleMode + 1) % 3
        # the drawUserPattern boolean is true whenever the pattern is being tesellated using one of the grid functions
        elif mode.drawUserPattern:
            # when in the grid mode, pressing up and down changes the levels of the fractal recursion methods to continue to divide the grid
            if event.key == 'Up':
                mode.level += 1
            elif event.key == 'Down':
                if mode.level > 1:
                    mode.level -= 1
        # the conditionals below refer to when the app is in the base grid mode, where the user can actually draw
        if not mode.drawUserPattern:
            if event.key == 'q':
                mode.drawSquares = not mode.drawSquares
            elif event.key == 'h':
                mode.drawHex = not mode.drawHex
            elif event.key == 'j':
                mode.drawHex2 = not mode.drawHex2
            elif event.key == 'c':
                mode.colorMode = not mode.colorMode
                mode.createCircle = False
                mode.createPolygon = False
                mode.freeDraw = False
            elif event.key == 'i':
                mode.savePatternToFile()
            elif event.key == 'o':
                result = mode.openPatternFromFile()
                if result != None:
                    tempShapeList, tempcircList, temppolygonList = result
                    mode.shapeList.extend(tempShapeList)
                    mode.circList.extend(tempcircList)
                    mode.polygonList.extend(temppolygonList)
            elif event.key == 'd':
                mode.showDistances = not mode.showDistances
            elif event.key == 'D':
                mode.distanceMode = True
            elif event.key == 'A':
                mode.angleMode = True
            elif event.key == 'p':
                mode.createPolygon = not mode.createPolygon
                mode.createCircle = False
                mode.freeDraw = False
                if mode.createPolygon:
                    # similar framework to the circle function below
                    newPol = patternPolygon(point(mode.width / 2, mode.height / 2), 3, color=mode.userColor)
                    mode.polygonList.append(newPol)
                    mode.currentPol = mode.polygonList[len(mode.polygonList) - 1]
            elif event.key == 'a':
                mode.createCircle = not mode.createCircle
                mode.createPolygon = False
                mode.freeDraw = False
                if mode.createCircle:
                    # everytime the add circle button is pressed, a new circle object is added to circle list
                    # the most recently created circle is set to the current circle variable which means the user can adjust that circle
                    newCircle = patternCircle(point(mode.width / 2, mode.height / 2), mode.userColor)
                    mode.circList.append(newCircle)
                    mode.currentCirc = mode.circList[len(mode.circList) - 1]
            elif event.key == 'f':
                mode.freeDraw = not mode.freeDraw
                mode.createCircle = False
                mode.createPolygon = False
                if mode.freeDraw:
                    # similar framework to the circle function above
                    newShape = freeShape2(mode.userColor)
                    mode.shapeList.append(newShape)
                    mode.currentShape = mode.shapeList[len(mode.shapeList) - 1]
            if mode.colorMode:
                if event.key == 'Up':
                    mode.colorPalette = (mode.colorPalette + 1) % 3
                    mode.colorBoard = mode.getColorGrid()
            if mode.freeDraw:
                if event.key == 'n':
                    # deletes the most recent object from the shapes lists
                    if len(mode.shapeList) != 0:
                        mode.shapeList.pop()
                        if len(mode.shapeList) > 0:
                            mode.currentShape = mode.shapeList[len(mode.shapeList) - 1]
                        else:
                            mode.currentShape = None
                            mode.freeDraw = False
                elif event.key == 'x':
                    # deletes the last point drawn for the free shape objects
                    if len(mode.currentShape.points) > 0:
                        mode.currentShape.points.pop()
            if mode.createCircle:
                if event.key == 'Up':
                    mode.currentCirc.rad += 5
                elif event.key == 'Down':
                    mode.currentCirc.rad -= 5
                elif event.key == 'n':
                    if len(mode.circList) != 0:
                        mode.circList.pop()
                        if len(mode.circList) != 0:
                            mode.currentCirc = mode.circList[len(mode.circList) - 1]
                        else:
                            mode.currentCirc = None
                            mode.createCircle = False
            if mode.createPolygon:
                if event.key == 'Up':
                    mode.currentPol.size += 5
                elif event.key == 'Down':
                    mode.currentPol.size -= 5
                # pressing right or left rotates the current polygon
                elif event.key == "Right":
                    mode.currentPol.rangle -= 2
                elif event.key == "Left":
                    mode.currentPol.rangle += 2
                elif event.key == "y":
                    mode.currentPol.changeNumberOfSides(1)
                elif event.key == 'e':
                    if mode.currentPol.numSides > 3:
                        mode.currentPol.changeNumberOfSides(-1)
                elif event.key == 'n':
                    if len(mode.polygonList) > 0:
                        mode.polygonList.pop()
                        if len(mode.polygonList) > 0:
                            mode.currentPol = mode.polygonList[len(mode.polygonList) - 1]
                        else: 
                            mode.currentPol = None
                            mode.createPolygon = False
            
    def mousePressed(mode, event):
        mode.appStarterMessage = False
        if not mode.drawUserPattern:
            if mode.colorMode:
                # changing the current app color to the what the user selects on the color grid using the mouse
                if mode.pointInGrid(event.x, event.y):
                    col, row = mode.getCell(event.x, event.y)
                    mode.userColor = mode.colorBoard[row][col]
                    if mode.currentShape != None:
                        mode.currentShape.color = mode.userColor
                    if mode.currentCirc != None:
                        mode.currentCirc.color = mode.userColor
                    if mode.currentShape != None:
                        mode.currentShape.color = mode.userColor
            if mode.distanceMode:
                # this activates the distance mode where the user selects two points on the canvas to get the distance between them
                mode.pointsForDistance.append(point(event.x, event.y))
                if len(mode.pointsForDistance) == 2:
                    mode.distanceLine = LineSegment(mode.pointsForDistance[0], mode.pointsForDistance[1])
                elif len(mode.pointsForDistance) > 2:
                    mode.pointsForDistance = []
                    mode.distanceMode = False
                    mode.distanceLine = None
            elif mode.angleMode:
                # this activates the angle mode where the user selects three points
                # the angle between the resulting line segments created from connecting these three points is then displayed
                mode.anglePoints.append(point(event.x, event.y))
                if len(mode.anglePoints) > 3:
                    mode.angleLines, mode.anglePoints = [], []
                    mode.angleMode = False
                    mode.angleText = None
                elif len(mode.anglePoints) == 2:
                    mode.angleLines.append(LineSegment(mode.anglePoints[0], mode.anglePoints[1]))
                elif len(mode.anglePoints) == 3:
                    mode.angleLines.append(LineSegment(mode.anglePoints[1], mode.anglePoints[2]))
                    mode.angleText = mode.angleLines[0].findAngle(mode.angleLines[1])
            elif mode.freeDraw: # adding points to the free drawed shape by clicking the mouse
                mode.currentShape.points.append(point(event.x, event.y))

    def mouseDragged(mode, event):
        mode.appStarterMessage = False
        if not mode.drawUserPattern:
            # by dragging the mouse inside the current circle or polygon, the user can move these shapes across the canvas
            if mode.createCircle:
                centerPoint = mode.currentCirc.center
                result = LineSegment(centerPoint, point(event.x, event.y))
                if result.getDistance() < mode.currentCirc.rad:
                    mode.currentCirc.center = point(event.x, event.y)
            elif mode.createPolygon:
                centerPoint = mode.currentPol.center
                result = LineSegment(centerPoint, point(event.x, event.y))
                if result.getDistance() < mode.currentPol.size * 2:
                    mode.currentPol.center = point(event.x, event.y)
            elif mode.freeDraw: # drawing a free shape by dragging the mouse across the canvas
                mode.currentShape.points.append(point(event.x, event.y))

    # creates a grid of colors with different palettes based on varying the rgb values
    def getColorGrid(mode):
        rows, cols = 52, 52
        board = []
        for row in range(rows):
            result = []
            for col in range(cols):
                if mode.colorPalette == 0: # different palette options
                    cellColor = rgbString(col * 5, ((col + row) // 2) * 5, row * 5)
                elif mode.colorPalette == 1:
                    cellColor = rgbString(col * 5, row * 5, ((col + row) // 2) * 5)
                elif mode.colorPalette == 2:
                    cellColor = rgbString(((col + row) // 2) * 5, row * 5, col * 5)
                result.append(cellColor)
            board.append(result) # color strings are stored in a 2d list
        return board

    # function takes the color strings 2d list from the getColorGrid method and draws rectangles with the corresponding color
    # to create a color palette
    def drawColorGrid(mode, canvas):
        for row in range(len(mode.colorBoard)):
            for col in range(len(mode.colorBoard[0])):
                mode.drawSquare(canvas, row, col, mode.colorBoard[row][col])

    # helper function for drawing an individual cell in the color grid
    def drawSquare(mode, canvas, row, col, cellColor):
        canvas.create_rectangle(mode.margin + mode.cellSize * col, mode.margin + mode.cellSize * row,
                            mode.cellSize * (col + 1), mode.cellSize * (row + 1), outline=cellColor, fill=cellColor)

    # Cited from 15-112 course notes from Animations Part 1 
    def pointInGrid(mode, x, y):
        # return True if (x, y) is inside the grid defined by mode.
        return ((mode.margin <= x <= mode.width-mode.margin) and
                (mode.margin <= y <= mode.height-mode.margin))

    # Cited partially from 15-112 course notes from Animations Part 1
    # used for view to model conversion by taking the user's selected color input and getting the matching color string
    # from the 2d list
    def getCell(mode, x, y):
        if (not mode.pointInGrid(x, y)):
            return (-1, -1)
        gridWidth  = mode.width - mode.margin
        gridHeight = mode.height - mode.margin
        row = roundHalfUp(mapRange(x, mode.margin, gridWidth, 0, 51))
        col = roundHalfUp(mapRange(y, mode.margin, gridHeight, 0, 51))
        row = 51 if (row > 51) else row
        row = 0 if (row < 0) else row
        col = 51 if (col > 51) else col
        col = 0 if (col < 0) else col
        return (row, col)

    # draws all the annotative features on the base grid screen such as the distances and angles
    def drawAnnotations(mode, canvas, cx, cy, r):
        if mode.showDistances:
            for shape in mode.shapeList:
                for i in range(len(shape.points) - 1):
                    newLine = LineSegment(shape.points[i], shape.points[i + 1])
                    canvas.create_text(newLine.getMidpoint().x, newLine.getMidpoint().y,
                                    text=f'{newLine.getDistance()}', anchor='s', fill='light grey')
        if mode.distanceMode:
            if mode.distanceLine != None:
                canvas.create_text(mode.distanceLine.getMidpoint().x, mode.distanceLine.getMidpoint().y,
                                        text=f'{mode.distanceLine.getDistance()}', anchor='s')
                dlinep1 = mode.distanceLine.p1
                dlinep2 = mode.distanceLine.p2
                canvas.create_oval(dlinep1.x - 2, dlinep1.y - 2, dlinep1.x + 2, dlinep1.y + 2,
                                        fill = 'light grey')
                canvas.create_oval(dlinep2.x - 2, dlinep2.y - 2, dlinep2.x + 2, dlinep2.y + 2,
                                        fill = 'light grey')
                mode.distanceLine.drawLineSegment(canvas, 'yellow')
        if mode.angleMode:
            for lin in mode.angleLines:
                lin.drawLineSegment(canvas, 'yellow')
            if mode.angleText != None:
                intersect = mode.angleLines[0].findIntersection(mode.angleLines[1])
                canvas.create_text(intersect.x, intersect.y, text=f'{mode.angleText}°', anchor='s',
                                            fill='light grey')
        margin = 10
        endPoint = point(0, cy + r) #this is for displaying the current color at the bottom of the screen as an indicator to the user
        canvas.create_rectangle(endPoint.x + margin, endPoint.y - margin - 20, endPoint.x + margin + 20,
                                    endPoint.y - margin, fill=mode.userColor, outline='grey')

    # draws the base grid for the screen that the user can continue to draw on and modify, add shapes, etc.
    def drawBaseGrid(mode, canvas):
        cx = mode.width / 2
        cy = mode.height / 2
        rad = min(mode.height, mode.width) / 2
        # below are conditionals for turning on different helper templates when drawing to aid the user in creating shapes
        if mode.circleMode == 1: 
            drawCircle8parts(canvas, point(cx - rad, cy - rad), point(cx + rad, cy + rad), 'light grey', True)
        elif mode.circleMode == 2:
            drawCircle12parts(canvas, cx, cy, rad, 'light grey', True)
        if mode.drawSquares:
            drawSquares(canvas, point(cx - rad, cy - rad), point(cx + rad, cy + rad), 'light blue')
        if mode.drawHex:
            drawHexagon(canvas, cx, cy, rad, 'light green')
        if mode.drawHex2:
            drawHexagon2(canvas, cx, cy, rad, 'orange')
        for circ in mode.circList:
            circ.drawCircle(canvas)
        for pol in mode.polygonList:
            pol.drawPolygon(canvas)
        for shape in mode.shapeList:
            shape.drawShapePoints(canvas)
            shape.drawShape(canvas)
        mode.drawAnnotations(canvas, cx, cy, rad)        

    # this function maps the drawn shapes from the base grid into smaller canvases that are part of the tesellation
    def tesellatePattern2(mode, canvas, bound1, bound2):
        r = (bound2.x - bound1.x) / 2
        cx = bound2.x - r
        cy = bound2.y - r
        # for every list of shapes, the values are all mapped accordingly based on the canvas bounding box
        for shape in mode.shapeList:
            newShapePoints = []
            for p in shape.points:
                newx = mapRange(p.x, 0, mode.height, cx - r, cx + r)
                newy = mapRange(p.y, 0, mode.width, cy - r, cy + r)
                newShapePoints.append(point(newx, newy))
            # new shapes, circles, polygons are created and then directly drawn on the screen
            newFreeShape = freeShape2(shape.color)
            newFreeShape.points = newShapePoints
            newFreeShape.drawShape(canvas)
        for circ in mode.circList:
            newCenterX = mapRange(circ.center.x, 0, mode.width, cx - r, cx + r)
            newCenterY = mapRange(circ.center.y, 0, mode.height, cy - r, cy + r)
            newRad = mapRange(circ.rad, 0, (min(mode.width, mode.height) / 2), 0, r)
            newCircle = patternCircle(point(newCenterX, newCenterY), circ.color)
            newCircle.rad = newRad
            newCircle.drawCircle(canvas)
        for pol in mode.polygonList:
            newCenterX = mapRange(pol.center.x, 0, mode.width, cx - r, cx + r)
            newCenterY = mapRange(pol.center.y, 0, mode.height, cy - r, cy + r)
            newSize = mapRange(pol.size, 0, (min(mode.width, mode.height) / 2), 0, r)
            cellPol = patternPolygon(point(newCenterX, newCenterY), pol.numSides, pol.color)
            cellPol.size, cellPol.rangle = newSize, pol.rangle
            cellPol.drawPolygon(canvas)

    # same exact function as above, only it rotates the entire base pattern by a certain angle
    def tesellatePatternRotated(mode, canvas, bound1, bound2, rangle):
        r = (bound2.x - bound1.x) / 2
        cx = bound2.x - r
        cy = bound2.y - r
        centerP = point(cx, cy)
        for shape in mode.shapeList:
            newShapePoints = []
            for p in shape.points:
                newx = mapRange(p.x, 0, mode.height, cx - r, cx + r)
                newy = mapRange(p.y, 0, mode.width, cy - r, cy + r)
                newShapePoints.append(point(newx, newy))
            newFreeShape = freeShape2(shape.color)
            newFreeShape.points = newShapePoints
            newFreeShape.rotateShape(rangle, centerP)
            newFreeShape.drawShape(canvas)
        for circ in mode.circList:
            newCenterX = mapRange(circ.center.x, 0, mode.width, cx - r, cx + r)
            newCenterY = mapRange(circ.center.y, 0, mode.height, cy - r, cy + r)
            rotatedCenter = point(newCenterX, newCenterY)
            rotatedCenter.rotatePoint(rangle, centerP)
            newRad = mapRange(circ.rad, 0, (min(mode.width, mode.height) / 2), 0, r)
            newCircle = patternCircle(rotatedCenter, circ.color)
            newCircle.rad = newRad
            newCircle.drawCircle(canvas)
        for pol in mode.polygonList:
            newCenterX = mapRange(pol.center.x, 0, mode.width, cx - r, cx + r)
            newCenterY = mapRange(pol.center.y, 0, mode.height, cy - r, cy + r)
            rotatedCenter = point(newCenterX, newCenterY)
            rotatedCenter.rotatePoint(rangle, centerP)
            newSize = mapRange(pol.size, 0, (min(mode.width, mode.height) / 2), 0, r)
            cellPol = patternPolygon(rotatedCenter, pol.numSides, pol.color)
            cellPol.size, cellPol.rangle = newSize, (pol.rangle + 22.5)
            cellPol.drawPolygon(canvas)
    
    def redrawAll(mode, canvas):
        if mode.drawUserPattern: # when in the tesellation mode, the grid is divided based on the whatever grid mode is selected 
            if mode.app.gridOption == 0:
                mode.standardGrid(canvas, point(0, 0), point(mode.width, mode.height), mode.level)
            elif mode.app.gridOption == 1:
                mode.drawHexGrid1(canvas, point(0,0), point(mode.width, mode.height), mode.level)
            elif mode.app.gridOption == 2:
                mode.drawHexGrid2(canvas, point(0,0), point(mode.width, mode.height), mode.level)
            elif mode.app.gridOption == 3:
                mode.subdividedGrid(canvas, point(0,0), point(mode.width, mode.height), mode.level)
            elif mode.app.gridOption == 4:
                mode.drawOverlappingGrid(canvas, point(0,0), point(mode.width, mode.height), mode.level)
            elif mode.app.gridOption == 5:
                rad = mode.width / 2
                mode.spiralGrid(canvas, point(0,0), point(mode.width, mode.height), mode.level, rad, 180)
        else:
            if mode.colorMode:
                mode.drawColorGrid(canvas)
            else:
                if mode.appStarterMessage:
                    canvas.create_text(mode.width / 2, 10, text='Press f to begin creating a new shape!', fill='grey')
                # draws the base grid
                mode.drawBaseGrid(canvas)

    # first recursive grid function that creates a simple matrix of the pattern
    def standardGrid(mode, canvas, startPoint, endPoint, level):
        a = (endPoint.x - startPoint.x) / 2 + startPoint.x
        b = (endPoint.y - startPoint.y) / 2 + startPoint.y
        if level == 0:
            mode.tesellatePattern2(canvas, startPoint, endPoint)
        else:
            mode.standardGrid(canvas, point(startPoint.x, startPoint.y), point(a, b), level - 1)
            mode.standardGrid(canvas, point(startPoint.x, b), point(a, endPoint.y), level - 1)
            mode.standardGrid(canvas, point(a, startPoint.y), point(endPoint.x, b), level - 1)
            mode.standardGrid(canvas, point(a, b), endPoint, level - 1)

    # second recursive grid function that creates a matrix that is offset by a little bit
    def drawHexGrid1(mode, canvas, startPoint, endPoint, level):
        a = (endPoint.x - startPoint.x) / 2 + startPoint.x
        b = (endPoint.y - startPoint.y) / 2 + startPoint.y
        r = (endPoint.x - startPoint.x) / 2
        hexOffsetY = (startPoint.y + b) / 2
        if level == 0:
            mode.tesellatePattern2(canvas, startPoint, endPoint)
        else:
            mode.drawHexGrid1(canvas, point(startPoint.x, startPoint.y), point(a, b), level - 1)
            mode.drawHexGrid1(canvas, point(startPoint.x, b), point(a, endPoint.y), level - 1)
            mode.drawHexGrid1(canvas, point(a, hexOffsetY), point(endPoint.x, ((b + endPoint.y) / 2)), level - 1)
            mode.drawHexGrid1(canvas, point(a, hexOffsetY - r), point(endPoint.x, ((b + endPoint.y) / 2) - r), level - 1)
            mode.drawHexGrid1(canvas, point(a, hexOffsetY + r), point(endPoint.x, ((b + endPoint.y) / 2) + r), level - 1)
    
    # third recursive grid that tesellates the base drawing in a hexagonal pattern
    # the first hexagonal background template in the base grid becomes the new bounding area for the base tile in this recursive grid
    def drawHexGrid2(mode, canvas, startPoint, endPoint, level):
        a = (endPoint.x - startPoint.x) / 2 + startPoint.x
        b = (endPoint.y - startPoint.y) / 2 + startPoint.y
        r = (endPoint.x - startPoint.x) / 2
        hexOffset = r - (r * math.sqrt(3) / 2)
        hexLength = r * math.sqrt(3) / 4
        hexHeight = r * .75
        if level == 0:
            mode.tesellatePattern2(canvas, startPoint, endPoint)
        else:
            mode.drawHexGrid2(canvas, point(startPoint.x, startPoint.y), point(a, b), level - 1)
            mode.drawHexGrid2(canvas, point(a - hexOffset, startPoint.y), point(endPoint.x - hexOffset, b), level - 1)
            mode.drawHexGrid2(canvas, point(endPoint.x - hexOffset * 2, startPoint.y), point((endPoint.x - hexOffset * 2 + r), b), level - 1)
            mode.drawHexGrid2(canvas, point(startPoint.x - hexLength, startPoint.y + hexHeight), 
                            point(a - hexLength, b + hexHeight), level - 1)
            mode.drawHexGrid2(canvas, point(startPoint.x + hexLength, startPoint.y + hexHeight), 
                            point(a + hexLength, b + hexHeight), level - 1)
            mode.drawHexGrid2(canvas, point(a - hexOffset + hexLength, startPoint.y + hexHeight), 
                            point(endPoint.x - hexOffset + hexLength, b + hexHeight), level - 1)
            mode.drawHexGrid2(canvas, point(startPoint.x, startPoint.y + hexHeight * 2), 
                            point(a, b + hexHeight * 2), level - 1)
            mode.drawHexGrid2(canvas, point(a - hexOffset, startPoint.y + hexHeight * 2), 
                            point(endPoint.x - hexOffset, b + hexHeight * 2), level - 1)
            mode.drawHexGrid2(canvas, point(endPoint.x - hexOffset * 2, startPoint.y + hexHeight * 2), 
                        point((endPoint.x - hexOffset * 2 + r), b + hexHeight * 2), level - 1)

    # fourth recursive function that continues to subdivide the base grid into smaller cells and overlaps the pattern
    def subdividedGrid(mode, canvas, startPoint, endPoint, level):
        a = (endPoint.x - startPoint.x) / 2 + startPoint.x
        b = (endPoint.y - startPoint.y) / 2 + startPoint.y
        r = (endPoint.x - startPoint.x) / 2
        rprime = r * math.sqrt(2) / 2
        if level == 0:
            mode.tesellatePatternRotated(canvas, startPoint, endPoint, 22.5)
        else:
            mode.tesellatePattern2(canvas, startPoint, endPoint)
            mode.subdividedGrid(canvas, point(a - rprime , b - rprime), point(a, b), level - 1)
            mode.subdividedGrid(canvas, point(a - rprime, b), point(a, b + rprime), level - 1)
            mode.subdividedGrid(canvas, point(a, b - rprime), point(a + rprime, b), level - 1)
            mode.subdividedGrid(canvas, point(a, b), point(a + rprime, b + rprime), level - 1)

    # fifth recursive grid that creates the matrix but overlaps it with the same pattern rotated, creating an interesting overlapping effect
    def drawOverlappingGrid(mode, canvas, startPoint, endPoint, level):
        a = (endPoint.x - startPoint.x) / 2 + startPoint.x
        b = (endPoint.y - startPoint.y) / 2 + startPoint.y
        if level == 0:
            mode.tesellatePattern2(canvas, startPoint, endPoint)
        else:
            mode.tesellatePatternRotated(canvas, startPoint, endPoint, 22.5)
            mode.drawOverlappingGrid(canvas, startPoint, point(a, b), level - 1)
            mode.drawOverlappingGrid(canvas, point(startPoint.x, b), point(a, endPoint.y), level - 1)
            mode.drawOverlappingGrid(canvas, point(a, startPoint.y), point(endPoint.x, b), level - 1)
            mode.drawOverlappingGrid(canvas, point(a, b), endPoint, level - 1)

    # sixth recursive function that spirals the base pattern smaller and smaller towards the center of the app window
    def spiralGrid(mode, canvas, startPoint, endPoint, level, rad, rotationAngle):
        cx = (endPoint.x - startPoint.x) / 2 + startPoint.x
        cy = (endPoint.y - startPoint.y) / 2 + startPoint.y
        goldenAngle = 360 / ((1 + math.sqrt(5)) / 2)**2
        if level == 0:
            mode.tesellatePatternRotated(canvas, point(cx - rad, cy - rad), point(cx + rad, cy + rad), rotationAngle)
        else:
            mode.tesellatePatternRotated(canvas, point(cx - rad, cy - rad), point(cx + rad, cy + rad), rotationAngle)
            mode.spiralGrid(canvas, startPoint, endPoint, level - 1, rad * .75, rotationAngle - goldenAngle)

def createPattern():
    global userWidth, userHeight
    runApp(width=500, height=500)                

def main():
    createPattern()

if __name__ == '__main__':
    main()

