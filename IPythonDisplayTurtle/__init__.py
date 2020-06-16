from IPython.display import HTML
from IPython.display import display
import random
import math
import os.path

# This is used to import the required js files
def ReadFile (filename):
    with open(os.path.join(os.path.dirname(__file__), 'jspart' , filename), 'r') as myfile:
        data = myfile.read()
        return data


# These two are used in 'draw level' method to easily convert the python arrays to javascript compatible strings
def _xyobjectarraytostring(arr):
    dat = "["
    for obj in arr:
        dat += '[%s, %s], ' % (obj[0], obj[1])
    dat += "],"
    return dat
    
def _xydatobjectarraytostring(arr):
    dat = "["
    for obj in arr:
        dat += '[%s, %s, %s], ' % (obj[0], obj[1], obj[2])
    dat += "],"
    return dat

class Snake():
    _gridSize = 50
    
    def __init__(self, _pendown=1, homeX = 50 + 25 + 5, homeY = 50 + 25 + 5, canvWidth = 400, canvHeigth = 200, \
                    turtleMainColor="#00A651", turtleAccentColor="#FFF600", speed = 5, rotspeed = 5, pencolor = 'red', penwidth=3):
        """Initializes the snake. Can be customized with arguments"""
        self._turtleMainColor = turtleMainColor
        self._turtleAccentColor = turtleAccentColor
        self._speed = speed
        self._rotspeed = rotspeed
        self._pendown = _pendown
        self._pencolor = pencolor
        self._penwidth = penwidth
        self._rotation = 90
        self._x = homeX
        self._y = homeY
        self._canvWidth = canvWidth
        self._canvHeigth = canvHeigth
        self._gridSize = self._gridSize
        self._actions = []
        self._appendCurrentState();
        
    def _appendCurrentState (self):
        """An Internal helper method for 'saving' the current state of the snake"""
        self._actions.append([self._rotation, self._x, self._y,
                            self._speed, self._rotspeed,
                            self._pendown, self._pencolor, self._penwidth,
                            self._turtleMainColor, self._turtleAccentColor
                           ])
        
    def _moveTo(self, x, y):
        """An Internal helper method for setting the snake's position."""
        if x < 0:
            x = 0
        elif x > self._canvWidth:
            x = self._canvWidth
        if y < 0:
            y = 0
        elif y > self._canvHeigth:
            y = self._canvHeigth
    
        self._x = round(x, 2)
        self._y = round(y, 2)
        self._appendCurrentState()
        
    def _rotateTo(self, rot):
        """An Internal helper method for setting the snake's rotation."""
        self._rotation = round(rot, 2)
        self._appendCurrentState()
        
        
    ## Helper methods, these are the expected way to interract with the turtle
    def speed(self, speed):
        """Set the snake's movement speed"""
        self._speed = speed
        
    def rotationSpeed(self, rotspeed):
        """Set the snake's rotation speed"""
        self._rotspeed = rotspeed
        
    def penDown(self):
        """Start drawing"""
        self._pendown = 1
        
    def penUp(self):
        """Stop drawing"""
        self._pendown = 0
        
    def penColor(self, color):
        """Change the pen's color to a color name or hex code: 'red' or '#ff0000'"""
        # TODO: check if color is legal and throw errors
        self._pencolor = color
        
    def penWidth(self, width):
        """Change the pen's width"""
        self._penwidth = width
        
    def turnRight(self, amount):
        """turn right by x amount of degrees"""
        self._rotateTo(self._rotation + amount)
        
    def turnLeft(self, amount):
        """turn left by x amount of degrees"""
        self._rotateTo(self._rotation - amount)
        
    def move(self, amount):
        """moves forward in the direction the snake is pointing at by x units"""
        newX = self._x + round(amount * math.sin(math.radians(self._rotation)), 2)
        newY = self._y - round(amount * math.cos(math.radians(self._rotation)), 2)
        self._moveTo(newX, newY)
    
        
    
    def drawLevel (self, xSize = 8, ySize = 4, gridSize=50, backgroundColor='white', drawGrid=1,\
                        apple = [], walls = [], doorways = [], lava = [], bridges = [], debug = False):
        '''
            Use this to draw a level with a grid + objects
            for walls and doorways and bridges, input should be an array of arrays of size 3 [x, y, data]
            for lava and apples, input should be an array of arrays of size 2 [x, y]
            Walls can have 6 orientations as data > lines >> 0 = │; 1 = ─; corners >> 2 = └; 3 = ┌; 4 = ┐; 5 = ┘;
            Doorways and bridges can have 2 orientations as data >> 0 = │; 1 = ─;
            Also you should NOT draw lava under bridge, it comes with it
            eg walls = [[1,2,0], [1,3,0], [1,4,5]]
            eg lava = [[1,2], [1,2]]
        '''
                        
        self._levelDataString = "["
        
        gridBorders = 5 # This is also set like this in the javascript side of the code, so don't change it here
        self._gridSize = gridSize
        self._canvWidth = xSize * self._gridSize + gridBorders*2
        self._canvHeight = ySize * self._gridSize + gridBorders*2
        
        self._levelDataString += "[%s, %s, %s, '%s', %s], " % (self._canvWidth, self._canvHeight, self._gridSize, backgroundColor, drawGrid)

        self._levelDataString += _xyobjectarraytostring(apple)
        self._levelDataString += _xydatobjectarraytostring(walls)
        self._levelDataString += _xydatobjectarraytostring(doorways)
        self._levelDataString += _xyobjectarraytostring(lava)
        self._levelDataString += _xydatobjectarraytostring(bridges)
        
        self._levelDataString += "]"
        
        if(debug):
            print(self._levelDataString)
    
    def display(self):
        """Displays the snake. This method is required at the end to actually show the snake"""
        # this is so that each turtle gets their own canvas. Without this they all try to draw to the first created canvas
        self._randHash = random.getrandbits(128)
        ## Canvas creation
        display(HTML('<script type="text/javascript">%s</script>'%ReadFile('paper.js')))
        display(HTML('<canvas id="canv%s" width=%spx height=%spx></canvas>'%(self._randHash, self._canvWidth, self._canvHeight)))
        
        
        # prepare data for injection
        self._arrayString = "["
        for act in self._actions:
            self._arrayString += '[%s, %s, %s, %s, %s, %s, "%s", %s, "%s", "%s"], ' \
            % (act[0], act[1], act[2], act[3], act[4], act[5], act[6], act[7], act[8], act[9])
        self._arrayString += "]"
        #print(arrayString)
        
        # inject data
        display(HTML('<script type="text/javascript">var actionData = %s; var levelData = %s</script>'% (self._arrayString, self._levelDataString)))
        
        ## Drawing the turtle
        display(HTML('<script type="text/paperscript" canvas="canv%s">%s</script>'% (self._randHash, ReadFile('AtahansTurtle.js'))))
  