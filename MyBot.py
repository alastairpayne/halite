from hlt import *
from networking import *

myID, gameMap = getInit()
PRODUCTION_FACTOR = 5
sendInit("MyPythonBotXXX")

def move(location, x, y, gameMap):
    site = gameMap.getSite(location)
    weakestBeatableForeignDirection = weakestBeatableForeignNeighbour(location)

    if weakestBeatableForeignDirection != 0:
        weakestBFSite = gameMap.getSite(location, weakestBeatableForeignDirection)
        if weakestBFSite.strength < site.strength and site.strength >= site.production * PRODUCTION_FACTOR:
            return Move(location, weakestBeatableForeignDirection)

    #this bit is shit
    if allFriendly(location):
        #return Move(location, randomNW())
        return Move(location, directionOfNearestUnfriendlySquare(x,y,gameMap))

    return Move(location,STILL)

def randomNW():
    if random.random() < 0.5 :
        return NORTH
    else:
        return WEST

def directionOfNearestUnfriendlySquare(x, y, gameMap):
    directionCounts = [0,0,0,0]
    localX = 0
    localY = 0
    for d in CARDINALS:
        # if d == EAST:
        #     while localX <= gameMap.width:
        #         neighbour_site = gameMap.getSite(Location((x+localX) % gameMap.width, y),d)
        #         localX +=1
        #         break
        # if d == WEST:
        #     c=1
        # if d == NORTH:
        #     c=1
        # if d == SOUTH:
        #     c=1
        #
        if d == EAST:
            while localX <= gameMap.width:
                neighbour_site = gameMap.getSite(Location((x+localX) % gameMap.width, y),d)
                if neighbour_site.owner == myID:
                    directionCounts[d-1]+=1
                    localX+=1
                else:
                    localX = 0;
                    break
                if localX > 10:
                    break;
        if d == WEST:
            while localX <= gameMap.width:
                neighbour_site = gameMap.getSite(Location((x-localX) % gameMap.width, y),d)
                if neighbour_site.owner == myID:
                    directionCounts[d-1]+=1
                    localX+=1
                else:
                    localX = 0
                    break
                if localX > 10:
                    break;
        if d == NORTH:
            while localY <= gameMap.height:
                neighbour_site = gameMap.getSite(Location(x, (y - localY) % gameMap.height),d)
                if neighbour_site.owner == myID:
                    directionCounts[d-1]+=1
                    localY+=1
                else:
                    localY = 0
                    break
                if localY > 10:
                    break;
        if d == SOUTH:
            while localY <= gameMap.height:
                neighbour_site = gameMap.getSite(Location(x, (y+localY) % gameMap.height),d)
                if neighbour_site.owner == myID:
                    directionCounts[d-1]+=1
                    localY+=1
                else:
                    localY=0
                    break
                if localY > 10:
                    break;

    return directionCounts.index(min(directionCounts)) + 1


def allFriendly(location):
    allFriend = True;
    for d in CARDINALS:
        neighbour_site = gameMap.getSite(location,d)
        if neighbour_site.owner != myID:
            allFriend = False;
    return allFriend

def weakestBeatableForeignNeighbour(location):
    strength = 255
    direction = 0
    for d in CARDINALS:
        neighbour_site = gameMap.getSite(location,d)
        if neighbour_site.strength <= strength and myID != neighbour_site.owner:
            strength = neighbour_site.strength
            direction = d;
    return direction;


while True:
    moves = []
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                moves.append(move(location,x,y,gameMap))
    sendFrame(moves)
