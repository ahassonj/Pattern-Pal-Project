# File for the fifth template option that lets users upload an image and trace it as part of the pattern base drawing
import basic_graphics
import math
import decimal
import json

from tkinter import *
from PIL import ImageGrab

from cmu_112_graphics import *
from patternObjects import * 
from allDrawFunctions import *
from userDefinedPattern import *
from OpeningScreen import *

class imageDrawing(buildPattern):
    def keyPressed(mode, event):
        mode.appStarterMessage = False
        if event.key == 'g':
            mode.app.setActiveMode(mode.app.helpScreen)
        elif event.key == 'J': # allows the user to enter the picture they want to trace
            mode.getPicture()
        elif event.key == 'Escape':
            mode.app.setActiveMode(mode.app.changeTemplate)
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
        elif mode.drawUserPattern:
            if event.key == 'Up':
                if mode.level < 6:
                    mode.level += 1
            elif event.key == 'Down':
                if mode.level > 1:
                    mode.level -= 1
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
                    mode.shapeList, mode.circList, mode.polygonList = result
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
                    newPol = patternPolygon(point(mode.width / 2, mode.height / 2), 3, color=mode.userColor)
                    mode.polygonList.append(newPol)
                    mode.currentPol = mode.polygonList[len(mode.polygonList) - 1]
            elif event.key == 'a':
                mode.createCircle = not mode.createCircle
                mode.createPolygon = False
                mode.freeDraw = False
                if mode.createCircle:
                    newCircle = patternCircle(point(mode.width / 2, mode.height / 2), mode.userColor)
                    mode.circList.append(newCircle)
                    mode.currentCirc = mode.circList[len(mode.circList) - 1]
            elif event.key == 'f':
                mode.freeDraw = not mode.freeDraw
                mode.createCircle = False
                mode.createPolygon = False
                if mode.freeDraw:
                    newShape = freeShape2(mode.userColor)
                    mode.shapeList.append(newShape)
                    mode.currentShape = mode.shapeList[len(mode.shapeList) - 1]
            if mode.colorMode:
                if event.key == 'Up':
                    mode.colorPalette = (mode.colorPalette + 1) % 3
                    mode.colorBoard = mode.getColorGrid()
            if mode.freeDraw:
                if event.key == 'n':
                    if len(mode.shapeList) != 0:
                        mode.shapeList.pop()
                        if len(mode.shapeList) > 0:
                            mode.currentShape = mode.shapeList[len(mode.shapeList) - 1]
                        else:
                            mode.currentShape = None
                            mode.freeDraw = False
                elif event.key == 'x':
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

    # function that takes in user input for an image name that uploads that image to be traced 
    def getPicture(mode):
        imageName = mode.getUserInput("Type the name of the file you'd like to trace (put filetype at the end)" + '\n' +
                                            'NOTE: Image has to be against a white or light background to be traced properly and ideally less than 200x200pixels')
        if imageName != None:
            mode.pic = mode.app.loadImage(imageName)
            scaleFactor = 600 / mode.pic.width
            mode.pic = mode.scaleImage(mode.pic, scaleFactor)
            # image is traced by looping through pixels and comparing color values to determine where an outline is
            for x in range(1, mode.pic.width - 1, 1):
                for y in range(1, mode.pic.height - 1, 1):                     
                    currentPixel = mode.pic.getpixel((x,y))
                    pixColor1 = getColorAverage(currentPixel)
                    nextPixel = mode.pic.getpixel((x + 1, y + 1))
                    pixColor2 = getColorAverage(nextPixel)
                    if abs(pixColor1 - pixColor2) >= 110:
                        # the outline points are then added into a list of points that is later used for drawing on the canvas
                        mode.outlinePoints.append(point(x, y))

    def drawBaseGrid(mode, canvas):
        cx = mode.width / 2
        cy = mode.height / 2
        rad = min(mode.height, mode.width) / 2
        if mode.circleMode == 1: 
            drawCircle8parts(canvas, point(cx - rad, cy - rad), point(cx + rad, cy + rad), 'light grey', True)
        elif mode.circleMode == 2:
            drawCircle12parts(canvas, cx, cy, rad, 'light grey', True)

        # base grid is the same except the outline points are then drawn on the canvas as dots to create an outline effect
        if mode.pic == None:
            canvas.create_rectangle(mode.width / 2 - 200, mode.height / 2 - 40, mode.width / 2 + 200,
                                        mode.height / 2 + 40, outline='red', fill=None)
            canvas.create_text(mode.width / 2, mode.height / 2, text='Press "J" to enter an image you want to trace', fill='red')
        else:
            for p in mode.outlinePoints:
                canvas.create_oval(p.x - mode.dotsize, p.y - mode.dotsize, p.x + mode.dotsize, 
                                        p.y + mode.dotsize, fill=mode.userColor, outline=mode.userColor)
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

    # tesellate functions the same but also include the outline points list so that they are included in the recursive grids
    def tesellatePattern2(mode, canvas, bound1, bound2):
        r = (bound2.x - bound1.x) / 2
        cx = bound2.x - r
        cy = bound2.y - r
        newDotSize = 0.1
        for po in mode.outlinePoints:
            px = mapRange(po.x, 0, mode.height, (cx - r), (cx + r))
            py = mapRange(po.y, 0, mode.height, (cy - r), (cy + r))
            canvas.create_oval(px - newDotSize, py - newDotSize, px + newDotSize, 
                                    py + newDotSize, fill=mode.userColor, outline=mode.userColor)
        for shape in mode.shapeList:
            newShapePoints = []
            for p in shape.points:
                newx = mapRange(p.x, 0, mode.height, cx - r, cx + r)
                newy = mapRange(p.y, 0, mode.width, cy - r, cy + r)
                newShapePoints.append(point(newx, newy))
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

    def tesellatePatternRotated(mode, canvas, bound1, bound2, rangle):
        r = (bound2.x - bound1.x) / 2
        cx = bound2.x - r
        cy = bound2.y - r
        centerP = point(cx, cy)
        newDotSize = 0.1
        for po in mode.outlinePoints:
            px = mapRange(po.x, 0, mode.height, (cx - r), (cx + r))
            py = mapRange(po.y, 0, mode.height, (cy - r), (cy + r))
            rp = point(px, py)
            rp.rotatePoint(rangle, centerP)
            canvas.create_oval(rp.x - newDotSize, rp.y - newDotSize, rp.x + newDotSize, 
                                    rp.y + newDotSize, fill=mode.userColor, outline=mode.userColor)
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

# function that takes a tuple of rgb values from a pixel and averages them to give a color brightness value
def getColorAverage(rgbval):
    if len(rgbval) == 4:
        r, g, b, a = rgbval
    elif len(rgbval) == 3:
        r, g, b = rgbval
    return ((r + g + b) / 3)



if __name__ == '__main__':
    main()

