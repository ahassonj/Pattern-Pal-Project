# contains all the associated helper drawing functions of the pattern shapes for the app modes.
import basic_graphics
import math
import decimal
from cmu_112_graphics import *
from patternObjects import *

# draws a circle divided into 12 sections
def drawCircle12parts(canvas, cx, cy, r, color, visible):
    if visible:
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline=color)
        canvas.create_line(cx, cy - r, cx, cy + r, fill=color)
        canvas.create_line(cx - r, cy, cx + r, cy, fill=color)
        circPoints = []
    for a in range(1, 12):
        point1 = math.pi/2 - (math.pi / 6) * a
        px1 = cx + r * math.cos(point1)
        py1 = cy - r * math.sin(point1)
        circPoints.append(point(px1, py1))
        if visible:
            canvas.create_line(cx, cy, px1, py1, fill=color)

# draws a hexagon inscribed within a circle
def drawHexagon(canvas, cx, cy, r, color):
    px1 = cx + r * math.cos(math.pi / 2)
    py1 = cy - r * math.sin(math.pi / 2)
    p1 = point(px1, py1)
    for a in range(1, 13):
        angle1 = math.pi/2 - (math.pi / 6) * a
        px2 = cx + r * math.cos(angle1)
        py2 = cy - r * math.sin(angle1)
        p2 = point(px2, py2)
        if a % 2 == 0:
            canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill=color)
            l = LineSegment(p1, p2)
            p1.x, p1.y = p2.x, p2.y

# draws a smaller hexagon inscribed within a circle
def drawHexagon2(canvas, cx, cy, r, color):
    px1 = cx + r * math.cos(math.pi / 2)
    py1 = cy - r * math.sin(math.pi / 2)
    p1 = point(px1, py1)
    midPoints = []
    for a in range(1, 13):
        angle1 = math.pi/2 - (math.pi / 6) * a
        px2 = cx + r * math.cos(angle1)
        py2 = cy - r * math.sin(angle1)
        p2 = point(px2, py2)
        if a % 2 == 0:
            line1 = LineSegment(p1, p2)
            midPoints.append(line1.getMidpoint())
            p1.x, p1.y = p2.x, p2.y
    for i in range(-1, len(midPoints) - 1):
        p3 = midPoints[i]
        p4 = midPoints[i + 1]
        canvas.create_line(p3.x, p3.y, p4.x, p4.y, fill=color)

# draws triangles created from the hexagon above, not used in my project, but was used in earlier studies
def drawTriangles(canvas, cx, cy, r, color):
    px1 = cx + r * math.cos(math.pi / 2)
    py1 = cy - r * math.sin(math.pi / 2)
    p1 = point(px1, py1)
    midPoints = []
    for a in range(1, 13):
        angle1 = math.pi/2 - (math.pi / 6) * a
        px2 = cx + r * math.cos(angle1)
        py2 = cy - r * math.sin(angle1)
        p2 = point(px2, py2)
        if a % 2 == 0:
            line1 = LineSegment(p1, p2)
            midPoints.append(line1.getMidpoint())
            p1.x, p1.y = p2.x, p2.y
    mid1 = []
    mid2 = []
    for i in range(-1, len(midPoints) - 1):
        p3 = midPoints[i]
        p4 = midPoints[i + 1]
        lineSeg = LineSegment(p3, p4)
        if i == -1 or i % 2 == 1:
            mid1.append(lineSeg.getMidpoint())
        else:
            mid2.append(lineSeg.getMidpoint())
    for j in range(-1, len(mid2) - 1):
        p5, p6 = mid1[j], mid1[j + 1]
        p7, p8 = mid2[j], mid2[j + 1]
        canvas.create_line(p5.x, p5.y, p6.x, p6.y, fill=color)
        canvas.create_line(p7.x, p7.y, p8.x, p8.y, fill=color)

# creates the pattern from the above hexagons by connecting the point intersections
def drawHexPattern(canvas, bound1, bound2, color):
    r = (bound2.x - bound1.x) / 2
    cx = bound2.x - r
    cy = bound2.y - r
    drawHexagon(canvas, cx, cy, r, color)
    px1 = cx + r * math.cos(math.pi / 2)
    py1 = cy - r * math.sin(math.pi / 2)
    p1 = point(px1, py1)
    midPoints = []
    for a in range(1, 13):
        angle1 = math.pi/2 - (math.pi / 6) * a
        px2 = cx + r * math.cos(angle1)
        py2 = cy - r * math.sin(angle1)
        p2 = point(px2, py2)
        if a % 2 == 0:
            line1 = LineSegment(p1, p2)
            midPoints.append(line1.getMidpoint())
            p1.x, p1.y = p2.x, p2.y
    trianglePoints = []
    intersections = []
    for i in range(-1, len(midPoints) - 1):
        p3 = midPoints[i]
        p4 = midPoints[i + 1]
        lineSeg = LineSegment(p3, p4)
        trianglePoints.append(lineSeg.getMidpoint())
        line2 = LineSegment(p4, point(cx, cy))
        intersections.append(line2.getMidpoint())
    result = []
    for a in range(len(trianglePoints)):
        result.extend([trianglePoints[a], intersections[a]])
    for i in range(-1, len(result) - 1):
        p3 = result[i]
        p4 = result[i + 1]
        canvas.create_line(p3.x, p3.y, p4.x, p4.y, fill=color)

# helper function for drawing the star pattern by connecting intersecting points across a circle
def drawVShapes(canvas, bound1, bound2, color, visible):
    r = (bound2.x - bound1.x) / 2
    cx = bound2.x - r
    cy = bound2.y - r
    circPoints = drawCircle8parts(canvas, bound1, bound2, 'white', False)
    lines = []
    for i in range(0, len(circPoints), 2):
        j = (i + 3) % len(circPoints)
        k = (j + 2) % len(circPoints)
        v1 = LineSegment(circPoints[i], circPoints[k])
        v2 = LineSegment(circPoints[i], circPoints[j])
        if visible:
            v1.drawLineSegment(canvas, color)
            v2.drawLineSegment(canvas, color)
        lines.extend([v1, v2])
    return lines

# draws one of the stars in the star pattern using the resulting points from the vshapes above
def drawStar1(canvas, bound1, bound2, scale, color):
    r = (bound2.x - bound1.x) / 2
    cx = bound2.x - r
    cy = bound2.y - r
    boxp = [[point(cx - r, cy - r), point(cx, cy - r), point(cx + r, cy - r)], 
                [point(cx - r, cy), point(cx + r, cy)],
                [point(cx - r, cy + r), point(cx, cy + r), point(cx + r, cy + r)]]
    canvas.create_rectangle(boxp[0][0].x, boxp[0][0].y, boxp[2][2].x, boxp[2][2].y, outline=color)
    TOPLINE = LineSegment(boxp[0][1], boxp[2][1])
    HORIZONTALLINE = LineSegment(boxp[1][0], boxp[1][1])
    BOXLINE1 = LineSegment(boxp[0][0], boxp[0][2])
    BOXLINE2 = LineSegment(boxp[0][2], boxp[2][2])
    BOXLINE3 = LineSegment(boxp[2][2], boxp[2][0])
    BOXLINE4 = LineSegment(boxp[0][0], boxp[2][0])

    # had to manually create intersecting points between diagonal lines drawn on the canvas and the resulting v shape lines
    # from the helper function above, just to create the overall star shape
    lines = drawVShapes(canvas, bound1, bound2, 'white', False)
    l2, l7 = lines[2], lines[7]
    p1 = l2.findIntersection(TOPLINE)
    p1.y -= scale
    int2 = l2.findIntersection(BOXLINE4)
    int7 = l7.findIntersection(BOXLINE2)
    canvas.create_line(int2.x, int2.y, p1.x, p1.y, fill=color)
    canvas.create_line(int7.x, int7.y, p1.x, p1.y, fill=color)

    l3, l6 = lines[3], lines[6]
    p2 = l3.findIntersection(TOPLINE)
    p2.y += scale
    int3 = l3.findIntersection(BOXLINE4)
    int6 = l6.findIntersection(BOXLINE2)
    canvas.create_line(int3.x, int3.y, p2.x, p2.y, fill=color)
    canvas.create_line(int6.x, int6.y, p2.x, p2.y, fill=color)

    l0, l5 = lines[0], lines[5]
    p3 = l0.findIntersection(HORIZONTALLINE)
    p3.x -= scale
    int0 = l0.findIntersection(BOXLINE3)
    int5 = l5.findIntersection(BOXLINE1)
    canvas.create_line(int0.x, int0.y, p3.x, p3.y, fill=color)
    canvas.create_line(int5.x, int5.y, p3.x, p3.y, fill=color)

    l1, l4 = lines[1], lines[4]
    p4 = l1.findIntersection(HORIZONTALLINE)
    p4.x += scale
    int1 = l1.findIntersection(BOXLINE3)
    int4 = l4.findIntersection(BOXLINE1)
    canvas.create_line(int1.x, int1.y, p4.x, p4.y, fill=color)
    canvas.create_line(int4.x, int4.y, p4.x, p4.y, fill=color)

# draws the other star in the star pattern using the resulting points from the vshapes above
def drawStar2(canvas, bound1, bound2, color):
    r = (bound2.x - bound1.x) / 2
    cx = bound2.x - r
    cy = bound2.y - r
    lines = drawVShapes(canvas, bound1, bound2, 'white', False)
    l0, l7 = lines[0], lines[7]
    dp1 = point(cx + r * math.cos(math.pi / 4), cy - r * math.sin(math.pi / 4))
    dp2 = point(cx - r * math.cos(math.pi / 4), cy + r * math.sin(math.pi / 4))
    dp3 = point(cx + r * math.cos(math.pi / 4), cy + r * math.sin(math.pi / 4))
    dp4 = point(cx - r * math.cos(math.pi / 4), cy - r * math.sin(math.pi / 4))
    diagonal1 = LineSegment(dp1, dp2)
    diagonal2 = LineSegment(dp3, dp4)

    for i in range(len(lines) - 1, 0, -2):
        l1, l2 = lines[(i + 1) % len(lines)], lines[i]
        if i == 5 or i == 1:
            p1 = l1.findIntersection(diagonal1)
        else:
            p1 = l1.findIntersection(diagonal2)
        canvas.create_line(l1.p1.x, l1.p1.y, p1.x, p1.y, fill=color)
        canvas.create_line(l2.p1.x, l2.p1.y, p1.x, p1.y, fill=color)

# creates a circle split into 8 parts
def drawCircle8parts(canvas, bound1, bound2, color, visible):
    r = (bound2.x - bound1.x) / 2
    cx = bound2.x - r
    cy = bound2.y - r
    if visible:
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline=color)
        canvas.create_rectangle(cx-r, cy-r, cx+r, cy+r, outline=color)
        canvas.create_line(cx, cy - r, cx, cy + r, fill=color)
        canvas.create_line(cx - r, cy, cx + r, cy, fill=color)
    circPoints = []
    for a in range(8):
        point1 = math.pi/2 - (math.pi * .25) * a
        px1 = cx + r * math.cos(point1)
        py1 = cy - r * math.sin(point1)
        circPoints.append(point(px1, py1))
        if visible: 
            canvas.create_line(cx, cy, px1, py1, fill=color)
    return circPoints

# draws two squares inscribed within a circle to be used as a base template
def drawSquares(canvas, bound1, bound2, color):
    r = (bound2.x - bound1.x) / 2
    cx = bound2.x - r
    cy = bound2.y - r
    point1 = math.pi/2
    px1 = cx + r * math.cos(point1)
    py1 = cy - r * math.sin(point1)
    for a in range(4, -1, -1):
        point1 = math.pi/2 - (math.pi/2) * a
        px2 = cx + r * math.cos(point1)
        py2 = cy - r * math.sin(point1)
        canvas.create_line(px1, py1, px2, py2, fill=color)
        px1, py1 = px2, py2

    point2 = math.pi/2 - (math.pi * .25)
    px3 = cx + r * math.cos(point2)
    py3 = cy - r * math.sin(point2)
    for a in range(3, 10, 2):
        point2 = math.pi/2 - (math.pi * .25) * a
        px4 = cx + r * math.cos(point2)
        py4 = cy - r * math.sin(point2)
        canvas.create_line(px3, py3, px4, py4, fill=color)
        px3, py3 = px4, py4
        
# draws the square pattern (the pattern 1 template) used by connecting the points found in the above helper function
def drawSquarePattern(canvas, bound1, bound2, scale, color):
    r = (bound2.x - bound1.x) / 2
    cx = bound2.x - r
    cy = bound2.y - r
    angle1 = math.pi/8
    px1 = cx + (r * math.cos(angle1) * scale)
    py1 = cy - (r * math.sin(angle1) * scale)

    for a in range(1, 17):
        angle1 = math.pi/8 - (math.pi/8) * a
        if a % 2 == 0:
            px2 = cx + r * math.cos(angle1) * scale
            py2 = cy - r * math.sin(angle1) * scale
        else:
            px2 = cx + r * math.cos(angle1)
            py2 = cy - r * math.sin(angle1)
        canvas.create_line(px1, py1, px2, py2, fill=color)
        px1, py1 = px2, py2

# same as the function above but rotates the entire square pattern by a given angle
def drawSquarePatternRotated(canvas, bound1, bound2, scale, color, rangle):
        r = (bound2.x - bound1.x) / 2
        cx = bound2.x - r
        cy = bound2.y - r
        angle1 = math.pi/8
        centr = point(cx, cy)
        px1 = cx + (r * math.cos(angle1) * scale)
        py1 = cy - (r * math.sin(angle1) * scale)

        for a in range(1, 17):
            tempPoint = point(px1, py1)
            tempPoint.rotatePoint(rangle, centr)
            angle1 = math.pi/8 - (math.pi/8) * a
            if a % 2 == 0:
                px2 = cx + r * math.cos(angle1) * scale
                py2 = cy - r * math.sin(angle1) * scale
            else:
                px2 = cx + r * math.cos(angle1)
                py2 = cy - r * math.sin(angle1)
            tempPoint2 = point(px2, py2)
            tempPoint2.rotatePoint(rangle, centr)
            canvas.create_line(tempPoint.x, tempPoint.y, tempPoint2.x, tempPoint2.y, fill=color)
            px1, py1 = px2, py2
        