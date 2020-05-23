import pygame
import random
import math
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import random
import socket
from datetime import datetime

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)          
port = 12345                
remote_host = "0.tcp.ngrok.io"

isServer = int(sys.argv[1])


FPS = 30

# Define Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (168,0,168)
YELLOW = (255,255,0)
ORANGE = (250,102,0)
LGREY = (179,179,179)
DGREY = (102,102,102)

tileColours = [RED, GREEN, PURPLE, BLUE, YELLOW, ORANGE]
colours = [0,1,2,3,4,5]
colourScores = [[0,0,0,0,0,0],
                [0,0,0,0,0,0],
                [0,0,0,0,0,0],
                [0,0,0,0,0,0]]

tiles = [(colour2, colour) for colour2 in colours for colour in colours for i in range(3)]
tiles.extend((colour, colour) for colour in colours for i in range(2))

## initialize pygame and create window
pygame.init()
pygame.mixer.init()  ## For sound
WIDTH = int(pygame.display.Info().current_w/4 *3)
HEIGHT = int(pygame.display.Info().current_h/7 * 6)

gap = 5

r = 20
n = 6

#players = 3



activeTileIndex = 0

playerTurn = 0

yStep = 75 / 50 * r
xStep = 43.3013 / 50 * r

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ingenious")
clock = pygame.time.Clock()     ## For syncing the FPS
myFont = pygame.font.Font('freesansbold.ttf', 10) 
myFont2 = pygame.font.Font('freesansbold.ttf', 30) 

Ingenious = False

activeTile = 0
activeSpot1 = (-1,-1)
activeSpot2 = (-1,-1)


def CharToInt(character):
    return ord(character) -97

def IntToCharacter(inte):
    return chr(inte+97)

def sendToAllClients(message):
    for i in range(numberOfClients):
        sendToClient(i, message)

def sendToClient(client, message):
    print(str(message) + " sent to " + str(client))
    c[client].send(str.encode(str(message)))
    time.sleep(.05)

def drawScoreBoard(surface, player):
    xOffset = 10 + 1000* (player % 2)
    yOffset = 10 + (int(player/2) *500)

    pygame.draw.rect(surface, LGREY, (xOffset+ 0, yOffset+ 0, 290,123))

    for j in range(6):
        for i in range(19):
            pygame.draw.circle(surface, BLACK, (xOffset+ 10+i*15,yOffset+ 10+j*20), 5)

        pygame.draw.circle(surface, tileColours[j], (xOffset+ 10+colourScores[player][j]*15,yOffset+ 10+j*20), 7)


class Tile:
    global activeTile
    def __init__(self, colourPair, pos1, pos2):
        self.colourPair = colourPair
        self.points1 = createPoly(pos1)
        self.points2 = createPoly(pos2)
        self.polygon1 = Polygon(self.points1)
        self.polygon2 = Polygon(self.points2)
        self.active = -1

    def checkPoint(self, pos):
        if self.polygon1.contains(Point(pos)):
            self.active = 0
            return True

        elif self.polygon2.contains(Point(pos)):
            self.active = 0
            return True

    def draw(self, surface):
        pygame.draw.polygon(surface, tileColours[self.colourPair[0]], self.points1)
        pygame.draw.polygon(surface, tileColours[self.colourPair[1]], self.points2)

    def placed(self):
        self.active = (self.active +1) % 2


class Space:
    def __init__(self, row, col, pos):
        self.row = row
        self.col = col
        self.x ,self.y = pos
        self.points = createPoly(pos)
        self.polygon = Polygon(self.points)
        self.colour = WHITE
        self.inPlay = True

    def checkPoint(self, pos):
        global activeTile
        global activeSpot1
        global playerTurn
        global Ingenious
        if self.polygon.contains(Point(pos)):

            if self.row == activeSpot1[0] and self.col == activeSpot1[1]:
                activeSpot1 = (-1,-1)
                activeTile.placed()
                self.inPlay = True
                self.colour = WHITE
                print("Reset")
            elif self.inPlay:
                if activeTile != 0:
                    if activeTile.active == 0: #first side placed
                        self.colour = tileColours[activeTile.colourPair[0]]
                        activeTile.placed()
                        activeSpot1 = (self.row, self.col)
                    else: #second side placed
                        test = False
                        direction = 0
                            #print("Direction = " + str(direction))
                            #print(activeSpot1)
                            #print(activeSpot2)
                            print(playerTurn)
                            if not Ingenious:
                                for player in range(players):
                                    playerTurn = (playerTurn+1) % players
                                    if not fullIngenious(player):
                                        break

                                print("Next player")
                            else:
                                Ingenious = not Ingenious
                                print("Another go")
                            print(playerTurn)
                            activeTile = 0

                    self.inPlay = False

    def setColour(self, colour):
        self.colour = colour
        self.inPlay = False

    def draw(self, surface):
        pygame.draw.polygon(surface, self.colour, self.points)
        #textsurface = myFont.render(str(self.row) + ',' + str(self.col), False, (0, 0, 0))
        #surface.blit(textsurface,(self.x-10,self.y-5))

def fullIngenious(player):
    fullIngenious = True
    for colour in colourScores[player]:
        if colour != 18:
            fullIngenious = False

def incrementScore(colour):
    global Ingenious
    if colourScores[playerTurn][tileColours.index(colour)] < 18:
        colourScores[playerTurn][tileColours.index(colour)] += 1
        if colourScores[playerTurn][tileColours.index(colour)] == 18:
            if not fullIngenious(playerTurn):
                Ingenious = True   

def calculateScore(pos1, pos2):
    if (self.row == activeSpot1[0]  and self.col - activeSpot1[1] == 1):
        test = True
        direction = 1

    elif (self.row == activeSpot1[0]  and self.col - activeSpot1[1] == -1):
        test = True
        direction = 2

    elif (activeSpot1[0] - self.row == 1 and activeSpot1[0] <= 7 and (0 == (activeSpot1[1] - self.col)) ):
        test = True
        direction = 3

    elif (activeSpot1[0] - self.row == 1 and activeSpot1[0] <= 7 and ( (activeSpot1[1] - self.col) == 1) ):
        test = True
        direction = 4

    elif (activeSpot1[0] - self.row == -1 and activeSpot1[0] <= 6 and (-1 == (activeSpot1[1] - self.col))):
        test = True
        direction = 5

    elif (activeSpot1[0] - self.row == -1 and activeSpot1[0] <= 6 and (activeSpot1[1] - self.col== 0)):
        test = True
        direction = 6

    elif (activeSpot1[0] - self.row == 1 and activeSpot1[0] >= 7 and (-1 == (activeSpot1[1] - self.col))):
        test = True
        direction = 3

    elif (activeSpot1[0] - self.row == 1 and activeSpot1[0] >= 7 and ( (activeSpot1[1] - self.col) == 0)):
        test = True
        direction = 4

    elif (activeSpot1[0] - self.row == -1 and activeSpot1[0] >= 6 and (0== (activeSpot1[1] - self.col))):
        test = True
        direction = 5

    elif (activeSpot1[0] - self.row == -1 and activeSpot1[0] >= 6 and  (activeSpot1[1] - self.col == 1)):
        test = True
        direction = 6

    if test:
        self.colour = tileColours[activeTile.colourPair[1]] # set the space to the tile colour
        tilesInHand[playerTurn][activeTileIndex] = getTile(playerTurn, activeTileIndex)
        activeSpot2 = (self.row, self.col)
        if direction != 2:
            checkEast(places[self.row][self.col], self.colour)
        if direction != 1:
            checkWest(places[self.row][self.col], self.colour)
        if direction != 5:
            checkNorthWest(places[self.row][self.col], self.colour)
        if direction != 6:
            checkNorthEast(places[self.row][self.col], self.colour)
        if direction != 4:                            
            checkSouthEast(places[self.row][self.col], self.colour)
        if direction != 3:
            checkSouthWest(places[self.row][self.col], self.colour)

        if direction != 1:
            checkEast(places[activeSpot1[0]][activeSpot1[1]], places[activeSpot1[0]][activeSpot1[1]].colour)
        if direction != 2:
            checkWest(places[activeSpot1[0]][activeSpot1[1]], places[activeSpot1[0]][activeSpot1[1]].colour)
        if direction != 4:                            
            checkNorthWest(places[activeSpot1[0]][activeSpot1[1]], places[activeSpot1[0]][activeSpot1[1]].colour)
        if direction != 3:                            
            checkNorthEast(places[activeSpot1[0]][activeSpot1[1]],  places[activeSpot1[0]][activeSpot1[1]].colour)
        if direction != 5:
            checkSouthEast(places[activeSpot1[0]][activeSpot1[1]],  places[activeSpot1[0]][activeSpot1[1]].colour)
        if direction != 6:
            checkSouthWest(places[activeSpot1[0]][activeSpot1[1]],  places[activeSpot1[0]][activeSpot1[1]].colour)



def checkEast(space, colour):
    try:
        newSpace = places[space.row][space.col+1]
    except:
        print("Something went wrong")
    else:
        if newSpace.colour == colour:
            print("EAST")
            #incrementScore(colour)
            return checkEast(deep, newSpace, colour) +1
        else:
            return 0

def checkWest(space, colour):
    try:
        newSpace = places[space.row][space.col-1]
    except:
        print("Something went wrong")
    else:        
        if newSpace.colour == colour:
            print("WEST")
            #incrementScore(colour)
            return checkWest(deep, newSpace, colour) + 1
        else:
            return 0

def checkNorthEast(space, colour):
    if space.row < 8:
        newSpace = places[space.row-1][space.col]
    else:
        newSpace = places[space.row-1][space.col+1]

    if colour == newSpace.colour:
        print("NortEast")
        #incrementScore(colour)
        return checkNorthEast(1, newSpace, colour) + 1
    else:
        return 0

def checkNorthWest(space, colour):
    if space.row < 8:
        newSpace = places[space.row-1][space.col-1]
    else:
        newSpace = places[space.row-1][space.col]

    if colour == newSpace.colour:
        print("NortWest")
        #incrementScore(colour)
        return checkNorthWest(1, newSpace, colour) + 1
    else:
        return 0

def checkSouthEast(space, colour):
    if space.row < 7:
        newSpace = places[space.row+1][space.col+1]
    else:
        newSpace = places[space.row+1][space.col]

    if colour == newSpace.colour:
        print("SouthEast")
        #incrementScore(colour)
        return checkSouthEast(1, newSpace, colour) + 1
    else:
        return 0

def checkSouthWest(space, colour):
    if space.row < 7:
        newSpace = places[space.row+1][space.col]
    else:
        newSpace = places[space.row+1][space.col-1]

    if colour == newSpace.colour:
        print("SouthWest")
        #incrementScore(colour)
        return checkSouthWest(1, newSpace, colour) + 1
    else:
        return 0

def createPoly(pos):
    x, y = pos
    return [ (int(x + r * math.sin(2 * math.pi * i / n)), int(y + r * math.cos(2 * math.pi * i / n)))
        for i in range(n)]

def setUp(places):
    starters = [ (2,2),
                 (2,8),
                 (7,2),
                 (7,13),
                 (12,2),
                 (12,8)                                                   
                ]
    for index, spot in enumerate(starters):
        places[spot[0]][spot[1]].setColour(tileColours[index])

    if players <4:
        for index in range(9):
            places[0][index].setColour(DGREY)
            places[14][index].setColour(DGREY)
        for index in range(1,14):
            places[index][0].setColour(DGREY)

        for index in range(1,8):
            places[index][index+8].setColour(DGREY)
        for index in range(1,7):
            places[index+7][15-index].setColour(DGREY)

        if players < 3:
            for index in range(8):
                places[1][1+index].setColour(LGREY)
                places[13][1+index].setColour(LGREY)
            for index in range(2,13):
                places[index][1].setColour(LGREY)

            for index in range(2,8):
                places[index][index+7].setColour(LGREY)
            for index in range(1,7):
                 places[index+7][14-index].setColour(LGREY)           


def getTile(player, i):
    random.seed(datetime.now())
    number = random.randint(0,len(tiles)-1)
    tilePair = tiles[number]
    tiles.pop(number)

    pos1 = (40 +(1000* (player%2)) ,  200 + i*50 + (500 * int(player/2)) )
    pos2 = (80 +(1000* ( player%2) ),  200 + i*50 + (500 * int(player/2)))

    return Tile(tilePair, pos1, pos2)    


tilesInHand = [[],[],[],[]]
for player in range(players):
    for i in range(6):
        tilesInHand[player].append(getTile(player, i))
        

places = []

cols = 8
jStep = 0

for row in range(15):
    if row < 8:
        cols = cols +1
        jStep = jStep + xStep + (gap/2)
    else:
        cols = cols -1
        jStep = jStep - xStep - (gap/2)
    places.append([])
    for col in range(cols):
        xPos = 500 - (jStep) + (col*(xStep*2+gap))
        yPos = 150 + row*(yStep + gap)
        places[row].append(Space(row, col, (xPos,yPos)))

playerText = myFont2.render("Player ", False, WHITE)