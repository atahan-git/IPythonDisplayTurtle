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

    MAXACTIONCOUNT = 100000

    # If you  are using gridmode=True, the movement will be based on the grid not units (ie forward(1) >>> forward(1*gridSize)) and rotation will rounded to 90 degrees
    def __init__(self, _pendown=1, gridmode=False, gridsize=50, homeX = 50 + 25 + 5, homeY = 50 + 25 + 5, canvWidth = 400, canvHeight = 200, \
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
        self._gridsize = gridsize
        self._gridmode = gridmode
        
        if(gridmode and homeX == 80):
            homeX = 0
            homeY = 0
 
        self._x = homeX
        self._y = homeY
        self._homeX = homeX
        self._homeY = homeY
        
        self._canvWidth = canvWidth
        self._canvHeight = canvHeight
        self._actions = []
        self._levelDataString = [] 
        
        self._walls = []
        self._lava = []
        
        self._appendCurrentState();
        
    def drawLevel (self, xSize = 8, ySize = 4, gridSize=50, backgroundColor='white', drawGrid=1,\
                        apple = [], walls = [], doors = [], lava = [], bridges = [], debug = False):
        '''
            Use this to draw a level with a grid + objects
            for walls and doors and bridges, input should be an array of arrays of size 3 [x, y, data]
            for lava and apples, input should be an array of arrays of size 2 [x, y]
            Walls can have 6 orientations as data > lines >> 0 = │; 1 = ─; corners >> 2 = └; 3 = ┌; 4 = ┐; 5 = ┘;
            doors and bridges can have 2 orientations as data >> 0 = │; 1 = ─;
            Also you should NOT draw lava under bridge, it comes with it
            eg walls = [[1,2,0], [1,3,0], [1,4,5]]
            eg lava = [[1,2], [1,2]]
        '''
        self._walls = walls
        self._lava = lava
                        
        self._levelDataString = "["
        
        gridBorders = 5 # This is also set like this in the javascript side of the code, so don't change it here
        self._gridsize = gridSize
        self._canvWidth = xSize * self._gridsize + gridBorders*2
        self._canvHeight = ySize * self._gridsize + gridBorders*2
        
        self._levelDataString += "[%s, %s, %s, '%s', %s], " % (self._canvWidth, self._canvHeight, self._gridsize, backgroundColor, drawGrid)

        self._levelDataString += _xyobjectarraytostring(apple)
        self._levelDataString += _xydatobjectarraytostring(walls)
        self._levelDataString += _xydatobjectarraytostring(doors)
        self._levelDataString += _xyobjectarraytostring(lava)
        self._levelDataString += _xydatobjectarraytostring(bridges)
        
        self._levelDataString += "]"
        
        self._actions = []
        self._appendCurrentState();
        
        if(debug):
            print(self._levelDataString)
        
    _curActionCount = 0
    def _appendCurrentState (self):
        """An Internal helper method for 'saving' the current state of the snake"""
        x = self._x
        y = self._y
        
        if(self._gridmode):
            x = 5 + round(x)*self._gridsize + self._gridsize/2
            y = 5 + round(y)*self._gridsize + self._gridsize/2
        
        self._actions.append([self._rotation, x, y,
                            self._speed, self._rotspeed,
                            self._pendown, self._pencolor, self._penwidth,
                            self._turtleMainColor, self._turtleAccentColor
                           ])
        self._curActionCount += 1
        if(self._curActionCount > self.MAXACTIONCOUNT):
            repCount = 0
            for i in range(self.MAXACTIONCOUNT):
                if(self._actions[i] == self._actions[i]):
                    repCount += 1
                else:
                    repCount = 0
                if(repCount >= 10):
                    self._actions = self._actions[:i]
                    break;
            self.display()
            raise Exception("Your snake tried to do too many things! Do you have a while loop that never ends?")
        
        
    def goto(self, x, y):
        """An Internal helper method for setting the snake's position."""
        # note that the snake can get outside of the canvas!
        if(self._gridmode):
            self._x = round(x)
            self._y = round(y)
        else:
            self._x = round(x, 2)
            self._y = round(y, 2)
            
        self._appendCurrentState()
        
    def setheading(self, rot):
        """An Internal helper method for setting the snake's rotation."""
        if(self._gridmode):
            rot = round(rot/90)*90
        
        self._rotation = round(rot, 2)
        self._appendCurrentState()
        
        
    ## Helper methods, these are the expected way to interract with the turtle
    def speed(self, speed):
        """Set the snake's general speed"""
        self._speed = speed
        self._rotspeed = speed
        
    def movespeed(self, speed):
        """Set the snake's movement speed"""
        self._speed = speed
        
    def turnspeed(self, rotspeed):
        """Set the snake's rotation speed"""
        self._rotspeed = rotspeed
        
    def pendown(self):
        """Start drawing"""
        self._pendown = 1
        
    def penup(self):
        """Stop drawing"""
        self._pendown = 0
        
    def color(self, color):
        """Change the pen's color to a color name or hex code: 'red' or '#ff0000'"""
        # TODO: check if color is legal and throw errors
        self._pencolor = color
        
    def pencolor(self, color):
        """Change the pen's color to a color name or hex code: 'red' or '#ff0000'"""
        # TODO: check if color is legal and throw errors
        self.color(color)
        
    def pensize(self, width):
        """Change the pen's width"""
        self._penwidth = width
        
    def right(self, amount):
        """turn right by x amount of degrees"""
        self.setheading(self._rotation + amount)
        
    def left(self, amount):
        """turn left by x amount of degrees"""
        self.setheading(self._rotation - amount)
        
    def forward(self, amount):
        """moves forward in the direction the snake is pointing at by x units"""
        newX = self._x + round(amount * math.sin(math.radians(self._rotation)), 2)
        newY = self._y - round(amount * math.cos(math.radians(self._rotation)), 2)
        self.goto(newX, newY)
    
    def backward(self, amount):
        """moves backwards in the direction the snake is pointing at by x units"""
        newX = self._x - round(amount * math.sin(math.radians(self._rotation)), 2)
        newY = self._y + round(amount * math.cos(math.radians(self._rotation)), 2)
        self.goto(newX, newY)
    
    def home(self):
        self.goto(self._homeX, self.homeY)
        self.setheading(0)
        
    def pos(self):
        return self._x, self._y
    
    def islocationclear(self,x,y):
        for wall in self._walls:
            if(wall[0] == x and wall[1] == y):
                return False
                
        for lava in self._lava:
            if(lava[0] == x and lava[1] == y):
                return False
                
        return True
                
        
    
    def isfrontclear(self):
        x = self._x
        y = self._y
        rot = round((self._rotation%360)/90)
        if(rot == 0):
            y+=1
        elif(rot==1):
            x+=1
        elif(rot==2):
            y-=1
        else:
            x-=1
        return self.islocationclear(x,y)
    
    def isleftclear(self):
        x = self._x
        y = self._y
        rot = round((self._rotation%360)/90)
        if(rot == 0):
            x-=1
        elif(rot==1):
            y+=1
        elif(rot==2):
            x+=1
        else:
            y-=1
        return self.islocationclear(x,y)
    
    def isrightclear(self):
        x = self._x
        y = self._y
        rot = round((self._rotation%360)/90)
        if(rot == 0):
            x+=1
        elif(rot==1):
            y-=1
        elif(rot==2):
            x-=1
        else:
            y+=1
        return self.islocationclear(x,y)
        
    
    def display(self):
        """Displays the snake. This method is required at the end to actually show the snake"""
        # this is so that each turtle gets their own canvas. Without this they all try to draw to the first created canvas
        self._randHash = random.getrandbits(128)
        
        # The actual forum seems to be able to display only one of the html texts, so merge them and send them all in one go
        htmlString = "";
        ## Canvas creation
        htmlString += ('<script type="text/javascript">%s</script>'%ReadFile('paper.js')) + "\n"
        htmlString += ('<canvas id="canv%s" width=%spx height=%spx></canvas>'%(self._randHash, self._canvWidth, self._canvHeight)) + "\n"
        
        
        # prepare data for injection
        self._arrayString = "["
        for act in self._actions:
            self._arrayString += '[%s, %s, %s, %s, %s, %s, "%s", %s, "%s", "%s"], ' \
            % (act[0], act[1], act[2], act[3], act[4], act[5], act[6], act[7], act[8], act[9])
        self._arrayString += "]"
        #print(arrayString)
        
        # inject data
        htmlString += ('<script type="text/javascript">var actionData = %s; var levelData = %s</script>'% (self._arrayString, self._levelDataString)) + "\n"
        
        ## Drawing the turtle
        htmlString += ('<script type="text/paperscript" canvas="canv%s">%s</script>'% (self._randHash, ReadFile('AtahansTurtle.js')))
        htmlString = htmlString.replace("actionData", "actionData" + str(self._randHash));
        htmlString = htmlString.replace("levelData", "levelData" + str(self._randHash));
        display(HTML(htmlString))
  