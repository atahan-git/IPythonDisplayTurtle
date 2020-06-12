from IPython.display import HTML
from IPython.display import display
import random
import math
import os.path

def ReadFile (filename):
    with open(os.path.join(os.path.dirname(__file__), 'jspart' , filename), 'r') as myfile:
        data = myfile.read()
        return data

class Snake():
    _homeX = 100
    _homeY = 75
    
    def __init__(self, _pendown=1):
        self._turtleMainColor = "green"
        self._turtleAccentColor = "yellow"
        self._backgroundColor = "white"
        self._speed = 5
        self._rotspeed = 5
        self._pendown = _pendown
        self._pencolor = "red"
        self._penwidth = 3
        self._rotation = 90
        self._x = self._homeX
        self._y = self._homeY
        self._actions = []
        self._appendCurrentState();
        
    def _appendCurrentState (self):
        self._actions.append([self._rotation, self._x, self._y,
                            self._speed, self._rotspeed,
                            self._pendown, self._pencolor, self._penwidth,
                            self._turtleMainColor, self._turtleAccentColor, self._backgroundColor
                           ])
        
    def _moveTo(self, x, y):
        self._x = int(x)
        self._y = int(y)
        self._appendCurrentState()
        
    def _rotateTo(self, rot):
        self._rotation = rot
        self._appendCurrentState()
        
        
    ## Helper methods, these are the expected way to interract with the turtle
    def speed(self, speed):
        self._speed = speed
        
    def rotationSpeed(self, rotspeed):
        self._rotspeed = rotspeed
        
    def penDown(self):
        self._pendown = 1
        
    def penUp(self):
        self._pendown = 0
        
    def penColor(self, color):
        # TODO: check if color is legal and throw errors
        self._pencolor = color
        
    def penWidth(self, width):
        self._penwidth = width
        
    def turnRight(self, amount):
        self._rotateTo(self._rotation + amount)
        
    def turnLeft(self, amount):
        self._rotateTo(self._rotation - amount)
        
    def goForward(self, amount):
        newX = self._x + round(amount * math.sin(math.radians(self._rotation)), 1)
        newY = self._y - round(amount * math.cos(math.radians(self._rotation)), 1)
        self._moveTo(newX, newY)
    
    def display(self, canvWidth = 400, canvHeight = 200, draw = True):
        # for some reason it is not doing the last 2 actions... sooooo
        self.goforward(1)
        self.turnright(1)
        # this is so that each turtle gets their own canvas
        self._randHash = random.getrandbits(128)
        #self._randHash = "asForTurtle";
        ## Canvas creation
        display(HTML('<script type="text/javascript">%s</script>'%ReadFile('paper.js')))
        display(HTML('<canvas id="canv%s" width=%spx height=%spx></canvas>'%(self._randHash, canvWidth, canvHeight)))
        
        
        ## Data injection
        arrayString = "["
        for act in self._actions:
            arrayString += '[%s, %s, %s, %s, %s, %s, "%s", %s, "%s", "%s", "%s"], ' \
            % (act[0], act[1], act[2], act[3], act[4], act[5], act[6], act[7], act[8], act[9], act[10])
        arrayString += "]"
        #print(arrayString)
        
        display(HTML('<script type="text/javascript">var actionData = %s;</script>'% (arrayString)))
        
        ## Drawing the turtle/executing on the injected data
        if(draw):
            display(HTML('<script type="text/paperscript" canvas="canv%s">%s</script>'% (self._randHash, ReadFile('AtahansTurtle.js'))))
  