# File for third pattern template of hexagonal shapes that is an instance of the user defined mode mode object.
import basic_graphics
import math
import decimal
import json

from tkinter import *


from cmu_112_graphics import *
from patternObjects import * 
from allDrawFunctions import *
from userDefinedPattern import *
from OpeningScreen import *

class patternTemplate3(buildPattern):
    # updated base grid incorporating this specific mode's template
    def drawBaseGrid(mode, canvas):
        cx = mode.width / 2
        cy = mode.height / 2
        rad = min(mode.height, mode.width) / 2
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
        drawHexPattern(canvas, point(cx - rad, cy - rad), point(cx + rad, cy + rad), mode.userColor)  

    # all grid functions are the same as those found in the userDefinedPattern file
    # grid functions here just account for including the specific pattern template within them
    def standardGrid(mode, canvas, startPoint, endPoint, level):
        a = (endPoint.x - startPoint.x) / 2 + startPoint.x
        b = (endPoint.y - startPoint.y) / 2 + startPoint.y
        if level == 0:
            mode.tesellatePattern2(canvas, startPoint, endPoint)
            drawHexPattern(canvas, startPoint, endPoint, mode.userColor)  
        else: 
            mode.standardGrid(canvas, point(startPoint.x, startPoint.y), point(a, b), level - 1)
            mode.standardGrid(canvas, point(startPoint.x, b), point(a, endPoint.y), level - 1)
            mode.standardGrid(canvas, point(a, startPoint.y), point(endPoint.x, b), level - 1)
            mode.standardGrid(canvas, point(a, b), endPoint, level - 1)

    def drawHexGrid1(mode, canvas, startPoint, endPoint, level):
        a = (endPoint.x - startPoint.x) / 2 + startPoint.x
        b = (endPoint.y - startPoint.y) / 2 + startPoint.y
        r = (endPoint.x - startPoint.x) / 2
        hexOffsetY = (startPoint.y + b) / 2
        if level == 0:
            mode.tesellatePattern2(canvas, startPoint, endPoint)
            drawHexPattern(canvas, startPoint, endPoint, mode.userColor)
        else:
            mode.drawHexGrid1(canvas, point(startPoint.x, startPoint.y), point(a, b), level - 1)
            mode.drawHexGrid1(canvas, point(startPoint.x, b), point(a, endPoint.y), level - 1)
            mode.drawHexGrid1(canvas, point(a, hexOffsetY), point(endPoint.x, ((b + endPoint.y) / 2)), level - 1)
            mode.drawHexGrid1(canvas, point(a, hexOffsetY - r), point(endPoint.x, ((b + endPoint.y) / 2) - r), level - 1)
            mode.drawHexGrid1(canvas, point(a, hexOffsetY + r), point(endPoint.x, ((b + endPoint.y) / 2) + r), level - 1)
    
    def drawHexGrid2(mode, canvas, startPoint, endPoint, level):
        a = (endPoint.x - startPoint.x) / 2 + startPoint.x
        b = (endPoint.y - startPoint.y) / 2 + startPoint.y
        r = (endPoint.x - startPoint.x) / 2
        hexOffset = r - (r * math.sqrt(3) / 2)
        hexLength = r * math.sqrt(3) / 4
        hexHeight = r * .75
        if level == 0:
            mode.tesellatePattern2(canvas, startPoint, endPoint)
            drawHexPattern(canvas, startPoint, endPoint, mode.userColor)
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

    def subdividedGrid(mode, canvas, startPoint, endPoint, level):
        a = (endPoint.x - startPoint.x) / 2 + startPoint.x
        b = (endPoint.y - startPoint.y) / 2 + startPoint.y
        r = (endPoint.x - startPoint.x) / 2
        rprime = r * math.sqrt(2) / 2
        if level == 0:
            mode.tesellatePatternRotated(canvas, startPoint, endPoint,22.5)
            drawHexPattern(canvas, startPoint, endPoint, mode.userColor)
        else:
            mode.tesellatePattern2(canvas, startPoint, endPoint)
            drawHexPattern(canvas, startPoint, endPoint, mode.userColor)
            mode.subdividedGrid(canvas, point(a - rprime , b - rprime), point(a, b), level - 1)
            mode.subdividedGrid(canvas, point(a - rprime, b), point(a, b + rprime), level - 1)
            mode.subdividedGrid(canvas, point(a, b - rprime), point(a + rprime, b), level - 1)
            mode.subdividedGrid(canvas, point(a, b), point(a + rprime, b + rprime), level - 1)

    def drawOverlappingGrid(mode, canvas, startPoint, endPoint, level):
        a = (endPoint.x - startPoint.x) / 2 + startPoint.x
        b = (endPoint.y - startPoint.y) / 2 + startPoint.y
        if level == 0:
            mode.tesellatePattern2(canvas, startPoint, endPoint)
            drawHexPattern(canvas, startPoint, endPoint, mode.userColor)
        else:
            if level % 2 == 1:
                mode.tesellatePatternRotated(canvas, startPoint, endPoint, 22.5)
                drawHexPattern(canvas, startPoint, endPoint, mode.userColor)
            else:
                mode.tesellatePattern2(canvas, startPoint, endPoint)
                drawHexPattern(canvas, startPoint, endPoint, mode.userColor)
            mode.drawOverlappingGrid(canvas, startPoint, point(a, b), level - 1)
            mode.drawOverlappingGrid(canvas, point(startPoint.x, b), point(a, endPoint.y), level - 1)
            mode.drawOverlappingGrid(canvas, point(a, startPoint.y), point(endPoint.x, b), level - 1)
            mode.drawOverlappingGrid(canvas, point(a, b), endPoint, level - 1)

    def spiralGrid(mode, canvas, startPoint, endPoint, level, rad, rotationAngle):
        scale = mapRange(mode.starScale, 0, mode.height, 0, (endPoint.y - startPoint.y))
        cx = (endPoint.x - startPoint.x) / 2 + startPoint.x
        cy = (endPoint.y - startPoint.y) / 2 + startPoint.y
        goldenAngle = 360 / ((1 + math.sqrt(5)) / 2)**2
        if level == 0:
            mode.tesellatePatternRotated(canvas, point(cx - rad, cy - rad), point(cx + rad, cy + rad), rotationAngle)
            drawHexPattern(canvas, point(cx - rad, cy - rad), point(cx + rad, cy + rad), mode.userColor)
        else:
            drawHexPattern(canvas, point(cx - rad, cy - rad), point(cx + rad, cy + rad), mode.userColor)
            mode.tesellatePatternRotated(canvas, point(cx - rad, cy - rad), point(cx + rad, cy + rad), rotationAngle)
            mode.spiralGrid(canvas, startPoint, endPoint, level - 1, rad * .75, rotationAngle - goldenAngle)

if __name__ == '__main__':
    main()

