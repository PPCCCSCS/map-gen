"""
 MapMaker by Neil Austin
    This is not even slightly optimized. Caveat computor and all that.
 
"""
# Import libraries
import pygame, random, statistics
from datetime import datetime

# Initialize the game engine
pygame.init()

# Set the height and width of the screen
screenWidth  = 640
screenHeight = 480
margin = 0
gudnuf = 0.95
screen = pygame.display.set_mode([screenWidth, screenHeight])
writes = 0

# Define some colors
BLACK     = (   0,   0,   0)
WHITE     = ( 255, 255, 255)
OFFWHITE  = ( 254, 254, 254)
NOTWHITE  = ( 253, 253, 253)
BLUE      = (   0,   0, 255)
GREEN     = (   0, 128,   0)
BROWN     = (  92,  64,  51)

clock = pygame.time.Clock()

# Returns a list containing an X and Y coordinate.
#
# If rng (random number generator) is false, returns the exact (rounded to
# int) XY coord specified in arguments
#
# If rny is true, returns an XY coordinate within the distance of the
# exact coord specified by the chosen denominator, eg:
#
# PW(1,4,7,8,True)
#
# will return an X value within 1/4 of the width of the map from the point
# 1/4 from the left edge of the screen, and a Y value within 1/8 the height
# of the screen from the point 7/8 of the height from the top of the screen

def PW(numX=1,denX=2,numY=1,denY=2,rng=False):
    # using abs here is a hack
    tX = abs(int(numX*screenWidth/denX)-1)
    tY = abs(int(numY*screenHeight/denY)-1)
    ###print(tX,tY)
    
    if rng == False:
        return [tX,tY]
    else:
        # Don't start left of left edge
        lX = tX - int(numX*screenWidth/(2*denX))
        if lX < 0:
            lX = 0
        # Don't start right of right edge
        uX = tX + int(numX*screenWidth/(2*denX))
        if uX > screenWidth - 1:
            uX = screenWidth -1
        # Don't start above top edge
        lY = tY - int(numY*screenHeight/(2*denY))
        if lY < 0:
            lY = 0
        # Don't start below bottom edge
        uY = tY + int(numY*screenHeight/(2*denY))
        if uY > screenHeight - 1:
            uY = screenHeight - 1
            
        ###print("lx=",lX,"tX=",tX,"uX=",uX,":\nlY=",lY,"tY=",tY,"uY=",uY)
        rX = random.randint(lX,uX)
        rY = random.randint(lY,uY)

        ###print(rX,rY)

        return [rX,rY]

def main():

    global writes

    cartos  = [[BLUE,      PW(1,8,1,8,True)],
               [GREEN,      PW(7,8,7,8,True)],
               ]

    colormap = initColormap() 
    
    pygame.display.set_caption("Drawing Map")



    makeIslands(cartos, screen, colormap)
    pygame.display.flip()

    fastFill( colormap )
    pygame.display.flip()

    addBorderLayer( colormap )
    pygame.display.flip()
    
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    pygame.image.save(screen,"map"+now+".png")

    try:
        input("Press Any Key to Quit")
    except:
        pygame.quit()
        
    # Be IDLE friendly
    pygame.quit()

def initColormap():
    colormap = []

    for bork in range(screenWidth):
        column = [BLACK] * (screenHeight)
        colormap.append(column)

    screen.fill(BLACK)

    return colormap
    
def makeIslands(cartos, screen, colormap):
    global writes

    full = (screenHeight-(2*margin))*(screenWidth-(2*margin))
    done = False
    
    # Loop as long as done == False
    while writes < full*gudnuf and done == False:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop

        # Clear the screen and set the screen background
        #screen.fill(BLACK)

        for cartog in cartos:
            here = walk(screen, colormap, cartog[0], cartog[1])
            
            if colorize(colormap, here) == True:
                writes=writes+1
                h = cartog[1][1]
                w = cartog[1][0]
                colormap[w][h] = cartog[0]
                
        # Go ahead and update the screen with what we've drawn.
        # This MUST happen after all the other drawing commands.
        #if full // writes == 0:
            if writes%1000 == 0:
                pygame.display.flip()

        # This limits the while loop to a max of 60 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(6000)

def walk(screen, maparray, color=(0,0,0), location=[0,0]):

    emptySquares = getEmptySquares( maparray, location )
    validSquares = getValidSquares( maparray, location )

    if len(emptySquares) > 0:
        goTo = random.choice(emptySquares)
        pygame.draw.line(screen, color, location,[location[0]+goTo[0],location[1]+goTo[1]],1)
    else:
        goTo = random.choice(validSquares)
   
    location[0]+=goTo[0]
    location[1]+=goTo[1]

    # Border-drawing algorithm removed. Add as optional post-process?
    return [location[0],location[1]]

def colorize( maparray, location=[0,0] ):
    if maparray[location[0]][location[1]] == (0,0,0):
        return True
    else:
        return False

def isInBounds( maparray, location ):
    if location[0] >= margin \
       and location[0] < screenWidth - margin \
       and location[1] >= margin \
       and location[1] < screenHeight - margin:
        return True
    else:
        return False

def getEmptySquares( maparray, location ):
    directions = [[0,-1],[-1,0],[1,0],[0,1]]
    emptySquares = list()
    
    for square in directions:
        if isInBounds( maparray, (location[0]+square[0],location[1]+square[1])):
           if maparray[location[0]+square[0]][location[1]+square[1]] == BLACK:
                emptySquares.append(square)
    return emptySquares

def getValidSquares( maparray, location ):
    directions = [[0,-1],[-1,0],[1,0],[0,1]]
    validSquares = [[0,0]]
    COLOR = maparray[location[0]][location[1]]
    for square in directions:
        if isInBounds( maparray, (location[0]+square[0],location[1]+square[1])):
            if maparray[location[0]+square[0]][location[1]+square[1]] in [BLACK, COLOR]:
                validSquares.append(square)
    return validSquares

def getMode( maparray, location ):
    directions = [[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[-1,1],[0,1],[1,1]]
    neighbors = list()

    for square in directions:
        if isInBounds( maparray, (location[0]+square[0],location[1]+square[1])):
            if maparray[location[0]+square[0]][location[1]+square[1]] != BLACK:
                neighbors.append(maparray[location[0]+square[0]][location[1]+square[1]])

    if len(neighbors) == 0:
        return BLUE
    else:
        return statistics.mode(neighbors)

def fastFill( maparray ):
    global writes
    for x in random.sample(list(range(screenWidth-1)),screenWidth-1):
        for y in random.sample(list(range(screenHeight-1)),screenHeight-1):
            if maparray[x][y] == BLACK:
                maparray[x][y] = getMode(maparray,[x,y])
                pygame.draw.line(screen, maparray[x][y], (x,y),(x,y),1)
                writes=writes+1
            y+=1
        y=0
        x+=1
        pygame.display.flip()

def addBorderLayer( maparray ):
    for x in range(screenWidth-1):
        for y in range(screenHeight-1):
            if maparray[x][y] != BLUE:
                if maparray[x][y] != maparray[x+1][y] and maparray[x+1][y] != BLUE:
                    pygame.draw.line(screen, BROWN, (x,y),(x,y),2)
                elif maparray[x][y] != maparray[x][y+1] and maparray[x][y+1] != BLUE:
                    pygame.draw.line(screen, BROWN, (x,y),(x,y),2)
            y+=1
        y=0
        x+=1
        pygame.display.flip()

if __name__ == "__main__":
    main()
