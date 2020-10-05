# File for creating all the associated helper functions and helper objects used in the draw functions.
from cmu_112_graphics import *
from tkinter import *
import cmath, math
import decimal

# Cited from the 15-112 Course Website Notes in graphics section
def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

# Cited from the 15-112 Course Website Notes
def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

# Cited from the 15-112 Course Website Notes
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

# used in the annotations to reduce decimals
def keepDecimals(n, d):
    n = int(n * (10**d))
    return (n / (10**d))

# Cited from the 15112 course notes section on Strings
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

# Cited from the 15112 course notes section on Strings
def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

# function that takes a value and remaps it into a new range, used for tesellating the patterns into a grid
def mapRange(val, start1, stop1, start2, stop2):
    valRange = val / (stop1 - start1)
    val2 = (stop2 - start2) * valRange
    return start2 + val2

# point class that creates a point from an x and y coordinate
class point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def getHashables(self):
        return (self.x, self.y)

    def __hash__(self):
        return hash(self.getHashables())

    def inRangeOf(self, other):
        return abs(self.x - other.x) < 5 and abs(self.y - other.y) < 5

    def rotatePoint(self, angle, center):
        rangle = math.radians(angle)
        # rotating point algorithm was written by looking at example problems from stackOverflow
        # https://stackoverflow.com/questions/45508202/how-to-rotate-a-polygon
        # code was written by myself for the context of this project, but logic belongs to martineau from stackoverflow
        x1 = self.x - center.x           
        y1 = self.y - center.y
        rotatedX = (x1 * math.cos(rangle) + y1 * math.sin(rangle)) + center.x
        rotatedY = (x1 * math.sin(rangle) -  y1 * math.cos(rangle)) + center.y
        self.x, self.y = rotatedX, rotatedY

# line segment class created from two points, used for drawing lines, and also finding intersections between other lines using algebra
class LineSegment(object):
    def __init__(self, point1, point2, color='black'):
        self.p1 = point1
        self.p2 = point2
        if (self.p2.x - self.p1.x != 0):
            self.slope = (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)
            self.intercept = self.p1.y - (self.slope * self.p1.x)
        else:
            self.slope = None
            self.intercept = None
        self.color = color

    def getSlope(self):
        return self.slope

    def findIntersection(self, other):
        if self.slope == other.slope and self.intercept != other.intercept:
            return None
        if other.slope != None:
            xint = (self.intercept - other.intercept) / (other.slope - self.slope)
        else:
            xint = other.p1.x
        yint = self.slope * xint + self.intercept
        return point(xint, yint)

    def getMidpoint(self):
        mx = (self.p1.x + self.p2.x) / 2
        my = (self.p1.y + self.p2.y) / 2
        return point(mx, my)

    def getDistance(self):
        result = (self.p2.x - self.p1.x)**2 + (self.p2.y - self.p1.y)**2
        return keepDecimals(math.sqrt(result), 3)

    def drawLineSegment(self, canvas, color):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=color)

    def findAngle(self, other):
        tangentVal = (self.slope - other.slope) / (1 + self.slope * other.slope)
        return abs(keepDecimals(math.degrees(math.atan(tangentVal)), 2))

# takes two lines and finds if the point is within it, used as part of earlier explorations within my project
def pointInLine(line1, point1):
    if line1.slope == None:
        return point1.x == line1.p1.x
    else:
        if point1.x < min(line1.p1.x, line1.p2.x) or point1.x > max(line1.p1.x, line1.p2.x):
            return False
        if point1.y < min(line1.p1.y, line1.p2.y) or point1.y > max(line1.p1.y, line1.p2.y):
            return False
        testLine = LineSegment(point1, line1.p2)
        if testLine.slope == None:
            return False
        return abs(testLine.slope - line1.slope) < 1

# a circle object created for adding shapes to the tile drawing
class patternCircle(object):
    def __init__(self, center, color='black'):
        # circle object has a center point and given radius and color, and draws the circle using that information
        self.center = center
        self.rad = 50
        self.color = color

    def drawCircle(self, canvas):
        canvas.create_oval(self.center.x - self.rad, self.center.y - self.rad,
                                self.center.x + self.rad, self.center.y + self.rad, outline=self.color)

# polygon class similar to the circle class above for adding polygons to the base pattern drawing
class patternPolygon(object):
    def __init__(self, center, sides, color):
        # polygon is created using a center, color, and number of sides which in the app is set to 3 by default
        self.center = center
        self.size = 50
        self.color = color
        self.rangle = 0
        self.numSides = sides
        self.points = [0] * self.numSides

    # points around the center are calculated using geometry
    def getPoints(self):
        for i in range(self.numSides):
            angle1 = math.pi / 2 - math.pi / self.numSides * 2 * i
            p1 = point(self.center.x + self.size * math.cos(angle1), self.center.y - self.size * math.sin(angle1))
            self.points[i] = p1

    # changes the polygon's number of sides and adjusts its list of points accordingly
    def changeNumberOfSides(self, factor):
        self.numSides += factor
        self.points = [0] * self.numSides

    def rotatePolygon(self):
        # rotating polygon algorithm was written by looking at example problems from stackOverflow
        # https://stackoverflow.com/questions/45508202/how-to-rotate-a-polygon
        # code was written by myself for the context of this project, but logic belongs to martineau from stackoverflow
        rangle = math.radians(self.rangle)
        result = []
        for p in self.points:
            x1 = p.x - self.center.x
            y1 = p.y - self.center.y
            rotatedX = (x1 * math.cos(rangle) + y1 * math.sin(rangle)) + self.center.x
            rotatedY = (x1 * math.sin(rangle) -  y1 * math.cos(rangle)) + self.center.y
            result.append(point(rotatedX, rotatedY))
        self.points = result

    def drawPolygon(self, canvas):
        self.getPoints()
        self.rotatePolygon()
        for i in range(-1, len(self.points) - 1):
            p1, p2 = self.points[i], self.points[i + 1]
            line1 = LineSegment(p1, p2)
            line1.drawLineSegment(canvas, self.color)

# freeshape objects are meant to be anything the user draws with their mouse and are just a list of points
# created to allow for the user to create multiple drawings across the canvas with their mouse
class freeShape2(object):
    def __init__(self, color):
        self.points = [] # collects a list of points that are then used for drawing lines connecting the shape
        self.color = color

    def drawShape(self, canvas):
        for i in range(len(self.points) - 1):
            p1, p2 = self.points[i], self.points[i+1]
            newLine = LineSegment(p1, p2)
            newLine.drawLineSegment(canvas, self.color)

    def rotateShape(self, angle, centerP):
        result = []
        for p in self.points:
            rotatedP = p
            rotatedP.rotatePoint(angle, centerP)
            result.append(rotatedP)
        self.points = result
                
    def drawShapePoints(self, canvas):
        dotSize = 1
        for p in self.points:
            canvas.create_oval(p.x - dotSize, p.y - dotSize, p.x + dotSize, p.y + dotSize,
                                fill='black')


