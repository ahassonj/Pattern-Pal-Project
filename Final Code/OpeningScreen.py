# Main file for launching the opening screen of the application
# Created main app object of which there are different modes for each of the templates
# as well as the help screen, different grid options, and for returning back to the main screen

import basic_graphics
import math
import decimal
from cmu_112_graphics import *
from patternObjects import *
from PIL import ImageGrab
from allDrawFunctions import * 
from userDefinedPattern import *
from template1 import *
from template2 import *
from template3 import *
from traceImage import *  

programScreen = [None] # needed to create a global list to store the command return value from the Tkinter buttons

# different functions below for selecting the template from the first Tkinter screen
# using the button widgets
def selectMode1():
    programScreen[0] = 1

def selectMode2():
    programScreen[0] = 2

def selectMode3():
    programScreen[0] = 3

def selectMode4():
    programScreen[0] = 4

def selectMode5():
    programScreen[0] = 5

# one of the modes for the modal app that contains text showing all the different commands and keys for using the program
class helpScreen(Mode):
    def redrawAll(mode, canvas):
        font = 'Calibri 11'
        height = 27
        canvas.create_text(mode.width / 2, height, text='Commands:', font='Calibri 22', fill='grey')
        canvas.create_text(mode.width / 2, height * 2, text='Press "u" to toggle the circle templates', font=font, fill='grey')
        canvas.create_text(mode.width / 2, height * 3, text='Press "q" to turn on the square template', font=font, fill='grey')
        canvas.create_text(mode.width / 2, height * 4, text='Press "h" and/or "j" to turn on the hexagon templates', font=font, fill='grey')
        canvas.create_text(mode.width / 2, height * 5, text='Press "c" to pick your own color', font=font, fill='grey')
        canvas.create_text(mode.width / 2, height * 5.5, text='Your selected color is shown at the bottom left corner of the canvas', font=font, fill='grey')
        canvas.create_text(mode.width / 2, height * 7, text='Press "i" to save your existing pattern to your files', font=font, fill='grey')
        canvas.create_text(mode.width / 2, height * 8, text='Press "o" to open an existing pattern from your files', font=font, fill='grey')
        canvas.create_text(mode.width / 2, height * 9, text='Press "x" to delete the last drawn line with the mouse', 
                                    font=font, fill='grey')
        canvas.create_text(mode.width / 2, height * 10, text='Press "a" to add a circle', 
                                    font=font, fill='grey')  
        canvas.create_text(mode.width / 2, height * 11, text='Press "p" to add a polygon', 
                                    font=font, fill='grey')                          
        canvas.create_text(mode.width / 2, height * 12, text='Press the UP or DOWN key to change the circle/polygon size',  
                                    font=font, fill='grey')
        canvas.create_text(mode.width / 2, height * 12.5, text='Drag the mouse inside to move the shape',  
                                    font=font, fill='grey')
        canvas.create_text(mode.width / 2, height * 14, text='Press "y" and "e" to change the number of sides for the polygon', 
                                    font=font, fill='grey')
        canvas.create_text(mode.width / 2, height * 15, text='Press the LEFT and RIGHT keys to rotate the polygon', 
                                    font=font, fill='grey')
        canvas.create_text(mode.width / 2, height * 16, text='Press "f" to free draw with the mouse', 
                                    font=font, fill='grey')
        canvas.create_text(mode.width / 2, height * 17, text='Press "n" to delete the last polygon/circle/free shape added', 
                                    font=font, fill='grey')
    
    # transitioning the current help screen to the next help screen
    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.helpScreenContd)

# second mode in the modal app class that contains additional help screen instructions
class helpScreen2(Mode):
    def redrawAll(mode, canvas):
        font = 'Calibri 11'
        height = 27
        canvas.create_text(mode.width / 2, height, text='Commands Continued:', font='Calibri 20', fill='grey')
        canvas.create_text(mode.width / 2, height * 2, text='Press "b" to activate the shape slider', 
                                    font=font, fill='grey')
        canvas.create_text(mode.width / 2, height * 3, text='Press "d" to show the lenghts of all lines', font=font, fill='grey')
        canvas.create_text(mode.width / 2, height * 4, text='Press "D" to measure the distance between two points on the screen', 
                            font=font, fill='grey')
        canvas.create_text(mode.width / 2, height * 5, text='Press "A" to measure the angle between two lines on the screen', 
                                    font=font, fill='grey')
        canvas.create_text(mode.width / 2, height * 6, text='Press ENTER to tesellate your drawn pattern', 
                                    font=font, fill='grey')
        canvas.create_text(mode.width / 2, height * 7, text='Press "l" to change the grid modes for your tesellation', 
                                    font=font, fill='grey')
        canvas.create_text(mode.width / 2, height * 8, text='Press ESCAPE to switch to another pattern template from the opening screen', 
                                    font=font, fill='grey')
        canvas.create_text(mode.width / 2, height * 9, text='Press "W" to save an image of your pattern', font=font, fill='grey')
        
    # switching from the help screen back to the drawing modes
    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.currentScreen)

# a subapp in the modal app that lists all the available options for tesellating the base pattern
class gridOptions(Mode):
    def appStarted(mode):
        mode.buttonLoc = mode.width / 8

    def redrawAll(mode, canvas):
        font = 'Calibri 14'
        canvas.create_rectangle(mode.buttonLoc, mode.buttonLoc, mode.width - mode.buttonLoc, mode.buttonLoc + 30, fill=None, outline="black")
        canvas.create_text(mode.width / 2, mode.buttonLoc + 15, text='Standard Grid', font=font, fill='red')

        canvas.create_rectangle(mode.buttonLoc, mode.buttonLoc * 2, mode.width - mode.buttonLoc, mode.buttonLoc * 2 + 30, fill=None, outline="black")
        canvas.create_text(mode.width / 2, mode.buttonLoc * 2 + 15, text='Offset Grid', font=font, fill='red')

        canvas.create_rectangle(mode.buttonLoc, mode.buttonLoc * 3, mode.width - mode.buttonLoc, mode.buttonLoc * 3 + 30, fill=None, outline="black")
        canvas.create_text(mode.width / 2, mode.buttonLoc * 3 + 15, text='Hexagonal Grid', font=font, fill='red')
        
        canvas.create_rectangle(mode.buttonLoc, mode.buttonLoc * 4, mode.width - mode.buttonLoc, mode.buttonLoc * 4 + 30, fill=None, outline="black")
        canvas.create_text(mode.width / 2, mode.buttonLoc * 4 + 15, text='Subdivided Grid', font=font, fill='red')

        canvas.create_rectangle(mode.buttonLoc, mode.buttonLoc * 5, mode.width - mode.buttonLoc, mode.buttonLoc * 5 + 30, fill=None, outline="black")
        canvas.create_text(mode.width / 2, mode.buttonLoc * 5 + 15, text='Overlapping Grid', font=font, fill='red')

        canvas.create_rectangle(mode.buttonLoc, mode.buttonLoc * 6, mode.width - mode.buttonLoc, mode.buttonLoc * 6 + 30, fill=None, outline="black")
        canvas.create_text(mode.width / 2, mode.buttonLoc * 6 + 15, text='Spiral Grid', font=font, fill='red')

    # switching back to the drawing mode
    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.currentScreen)

    # creating buttons on the screen where if the user presses the text box drawn on the canvas
    # they can change the type of grid they want to use
    def mousePressed(mode, event):
        if mode.buttonLoc < event.x < (mode.width - mode.buttonLoc):
            if (mode.buttonLoc) < event.y < (mode.buttonLoc + 30):
                mode.app.gridOption = 0
            elif (mode.buttonLoc * 2) < event.y < (mode.buttonLoc * 2 + 30):
                mode.app.gridOption = 1
            elif (mode.buttonLoc * 3) < event.y < (mode.buttonLoc * 3 + 30):
                mode.app.gridOption = 2
            elif (mode.buttonLoc * 4) < event.y < (mode.buttonLoc * 4 + 30):
                mode.app.gridOption = 3
            elif (mode.buttonLoc * 5) < event.y < (mode.buttonLoc * 5 + 30):
                mode.app.gridOption = 4
            elif (mode.buttonLoc * 6) < event.y < (mode.buttonLoc * 6 + 30):
                mode.app.gridOption = 5

# subapp created to change the template mode from the initial template chosen in the opening Tkinter window
# added so that the user doesn't have to close the app everytime and rerun the program again just to access a different template
class changeTemplates(Mode):
    def appStarted(mode):
        mode.buttonLoc = mode.width / 6

    def redrawAll(mode, canvas):
        font = 'Calibri 14'
        canvas.create_rectangle(mode.buttonLoc, mode.buttonLoc, mode.width - mode.buttonLoc, mode.buttonLoc + 30, fill=None, outline="black")
        canvas.create_text(mode.width / 2, mode.buttonLoc + 15, text='Pattern 1', font=font, fill='red')

        canvas.create_rectangle(mode.buttonLoc, mode.buttonLoc * 2, mode.width - mode.buttonLoc, mode.buttonLoc * 2 + 30, fill=None, outline="black")
        canvas.create_text(mode.width / 2, mode.buttonLoc * 2 + 15, text='Pattern 2', font=font, fill='red')

        canvas.create_rectangle(mode.buttonLoc, mode.buttonLoc * 3, mode.width - mode.buttonLoc, mode.buttonLoc * 3 + 30, fill=None, outline="black")
        canvas.create_text(mode.width / 2, mode.buttonLoc * 3 + 15, text='Pattern 3', font=font, fill='red')
        
        canvas.create_rectangle(mode.buttonLoc, mode.buttonLoc * 4, mode.width - mode.buttonLoc, mode.buttonLoc * 4 + 30, fill=None, outline="black")
        canvas.create_text(mode.width / 2, mode.buttonLoc * 4 + 15, text='Build Your Own Pattern', font=font, fill='red')

        canvas.create_rectangle(mode.buttonLoc, mode.buttonLoc * 5, mode.width - mode.buttonLoc, mode.buttonLoc * 5 + 30, fill=None, outline="black")
        canvas.create_text(mode.width / 2, mode.buttonLoc * 5 + 15, text='Trace an Image', font=font, fill='red')

        
    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.currentScreen)

    # utilizes a button interface similar to the grid option subapp where the user clicks on the different template options
    # that are the same as the opening screen
    def mousePressed(mode, event):
        if mode.buttonLoc < event.x < (mode.width - mode.buttonLoc):
            if (mode.buttonLoc) < event.y < (mode.buttonLoc + 30):
                mode.app.currentScreen = mode.app.pattern1Mode
            elif (mode.buttonLoc * 2) < event.y < (mode.buttonLoc * 2 + 30):
                mode.app.currentScreen = mode.app.pattern2Mode
            elif (mode.buttonLoc * 3) < event.y < (mode.buttonLoc * 3 + 30):
                mode.app.currentScreen = mode.app.pattern3Mode
            elif (mode.buttonLoc * 4) < event.y < (mode.buttonLoc * 4 + 30):
                mode.app.currentScreen = mode.app.buildPattern
            elif (mode.buttonLoc * 5) < event.y < (mode.buttonLoc * 5 + 30):
                mode.app.currentScreen = mode.app.portraitMode

# the main modal app for running the program
class PatternPalApp(ModalApp):
    def appStarted(app):
        # assigning all the different app modes to the modal app
        app.pattern1Mode = patternTemplate1()
        app.pattern2Mode = patternTemplate2()
        app.pattern3Mode = patternTemplate3()
        app.buildPattern = buildPattern()
        app.helpScreen = helpScreen()
        app.helpScreenContd = helpScreen2()
        app.changeTemplate = changeTemplates()
        app.portraitMode = imageDrawing()
        app.currentScreen = buildPattern()
        app.gridOptions = gridOptions()
        app.gridOption = 0
        # the conditionals below set the user's interaction with the opening Tkinter window and its widgets
        # to the matching template mode within the modal app
        if programScreen[0] == 1:
            app.currentScreen = app.pattern1Mode
        elif programScreen[0] == 2:
            app.currentScreen = app.pattern2Mode
        elif programScreen[0] == 3:
            app.currentScreen = app.pattern3Mode
        elif programScreen[0] == 4:
            app.currentScreen = app.buildPattern
        elif programScreen[0] == 5:
            app.currentScreen = app.portraitMode
        app.setActiveMode(app.currentScreen)

def start():
    window1 = Tk() # creating the Tk window object that sets up the opening page of the program
    canvas1 = Canvas(window1, width=600, height=300) # canvas for containing all the text
    canvas1.create_text(300, 25, text="Welcome to Pattern Pal", fill='grey', font='Calibri 26')
    descriptionText = 'Pattern Pal is an introductory guide into the beautiful art of geometric tesellations,'
    canvas1.create_text(300, 70, text=descriptionText, fill='grey', font='Calibri 12')
    canvas1.create_text(300, 90, text='inspired by geometric patterns commonly associated with Islamic art and culture.', fill='grey', font='Calibri 12')
    canvas1.create_text(300, 150, text="Select the pattern you'd like to start with", fill='grey', font='Calibri 18')
    canvas1.create_text(300, 175, text="When drawing, note that at anytime you can press 'g' to open up a help window", fill='grey', font='Calibri 12')
    canvas1.pack()
    # frames created for adding the different template modes and accompanying images onto the screen
    frame1 = Frame(window1)
    frame1.pack()
    canvasPattern1 = Canvas(frame1, width=200, height=200)
    canvasPattern1.grid(row=0, column=0, sticky=W)
    canvasPattern1.create_rectangle(10, 10, 190, 190, fill='white', outline='white')
    drawSquarePattern(canvasPattern1, point(10, 10), point(190, 190), .765, 'red')
    button1 = Button(frame1, text='Pattern 1', command=selectMode1)
    button1.grid(row=1, column=0, sticky=W)
    # frames created for adding the different template modes and accompanying images onto the screen
    canvasPattern2 = Canvas(frame1, width=200, height=200)
    canvasPattern2.grid(row=0, column=1, sticky=W)
    canvasPattern2.create_rectangle(10, 10, 190, 190, fill='white', outline='white')
    drawStar1(canvasPattern2, point(10, 10), point(190, 190), 0, 'red') 
    drawStar2(canvasPattern2, point(10, 10), point(190, 190), 'red') 
    button2 = Button(frame1, text='Pattern 2', command=selectMode2)
    button2.grid(row=1, column=1, sticky=W)
    # frames created for adding the different template modes and accompanying images onto the screen
    canvasPattern3 = Canvas(frame1, width=200, height=200)
    canvasPattern3.grid(row=0, column=2, sticky=W)
    canvasPattern3.create_rectangle(10, 10, 190, 190, fill='white', outline='white')
    drawHexPattern(canvasPattern3, point(10, 10), point(190, 190), 'red')
    button3 = Button(frame1, text='Pattern 3', command=selectMode3)
    button3.grid(row=1, column=2, sticky=W)
    # frames created for adding the different template modes and accompanying images onto the screen
    canvasPattern4 = Canvas(frame1, width=200, height=200)
    canvasPattern4.grid(row=0, column=3, sticky=W)
    canvasPattern4.create_rectangle(10, 10, 190, 190, fill='white', outline='white')
    drawCircle8parts(canvasPattern4, point(10, 10), point(190, 190), 'light grey', True)
    button4 = Button(frame1, text='Build Your Own', command=selectMode4)
    button4.grid(row=1, column=3, sticky=W)
    # frames created for adding the different template modes and accompanying images onto the screen
    canvasPattern5 = Canvas(frame1, width=200, height=200)
    canvasPattern5.grid(row=0, column=4, sticky=W)
    img = PhotoImage(file='faces6.png')
    canvasPattern5.create_image(10, 10, anchor='nw', image=img)
    button5 = Button(frame1, text='Trace an Image', command=selectMode5)
    button5.grid(row=1, column=4, sticky=W)
    
    window1.mainloop() 

    myApp = PatternPalApp(width=600, height=600) # this begins running the modal app after the user closes the Tkinter window

def main():
    start()

if __name__ == '__main__':
    main()



