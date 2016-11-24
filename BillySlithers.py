from hlt import *
from networking import *

myID, gameMap = getInit()
START_POS = [0,0]
INIT = False
PRODUCTION_FACTOR = 3
GIVE_UP_ON_THAT_LONG_FUNCTION_FACTOR = 2
PRODUCTION_FACTOR_THRESHOLD = [0,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,4,4]
#PRODUCTION_FACTOR_THRESHOLD= [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
GAME_H = 0
GAME_W = 0
MAP_SIZE = 0
MY_TERRITORY = 0
sendInit("BillySlithersssssss")

def move(location, x, y, gameMap):
    global MY_TERRITORY
    site = gameMap.getSite(location)
    weakestBeatableForeignDirection = weakestBeatableForeignNeighbour(location)

    if weakestBeatableForeignDirection != 0:
        weakestBFSite = gameMap.getSite(location, weakestBeatableForeignDirection)
        if weakestBFSite.strength < site.strength and productionCheck(site.strength, site.production):
            MY_TERRITORY+=1
            return Move(location, weakestBeatableForeignDirection)

    #this bit is shit
    if allFriendly(location):
        #return Move(location, randomNW())
        if productionCheck(site.strength, site.production):
            return Move(location, directionOfNearestUnfriendlySquare(x,y,gameMap))


    return Move(location,STILL)


def productionCheck(strength, production):
    return strength >= PRODUCTION_FACTOR * PRODUCTION_FACTOR_THRESHOLD[production]


#I'M TIMING OUT AGAINST BRONZE FFS
def directionOfNearestUnfriendlySquare(x, y, gameMap):
    global MAP_SIZE, MY_TERRITORY
    if MY_TERRITORY / MAP_SIZE >= 0.65:
        return OkayJustGoBasedOnTheStartPosition(x,y)

    directionCounts = [0,0,0,0]
    localX = 0
    localY = 0
    for d in CARDINALS:
        if d == EAST:
            while localX <= gameMap.width:
                neighbour_site = gameMap.getSite(Location((x+localX) % gameMap.width, y),d)
                if neighbour_site.owner == myID:
                    directionCounts[d-1]+=1
                    localX+=1
                else:
                    localX = 0;
                    break
                if localX > GIVE_UP_ON_THAT_LONG_FUNCTION_FACTOR:
                    localX = 0;
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
                if localX > GIVE_UP_ON_THAT_LONG_FUNCTION_FACTOR:
                    localX = 0;
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
                if localY > GIVE_UP_ON_THAT_LONG_FUNCTION_FACTOR:
                    localY = 0;
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
                if localY > GIVE_UP_ON_THAT_LONG_FUNCTION_FACTOR:
                    localY = 0;
                    break;

    if directionCounts[0] == directionCounts[1] and directionCounts[1] == directionCounts[2] and directionCounts[2] == directionCounts[3]:
        return OkayJustGoBasedOnTheStartPosition(x,y)

    return directionCounts.index(min(directionCounts)) + 1


#They run along the edges when they get there. They need to just keep going as if it wraps
def OkayJustGoBasedOnTheStartPosition(x,y):
    global GAME_H, GAME_W

    if x == GAME_W or x == 0 or y == GAME_H or y ==0:
        return random.choice(DIRECTIONS)

    startX = START_POS[0]
    startY = START_POS[1]
    diffX = abs(startX - x)
    diffY = abs(startY - y)
    if diffX > diffY:
        if x > startX:
            return EAST
        else:
            return WEST
    else:
        if y > startY:
            return SOUTH
        else:
            return NORTH


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


#should I look for a first enemy to attack?
while True:
    moves = []
    gameMap = getFrame()
    if (not INIT):
        GAME_H = gameMap.height
        GAME_W = gameMap.width
        MAP_SIZE = GAME_H * GAME_W
        MY_TERRITORY = 0
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                if (not INIT):
                    INIT = True
                    START_POS = [x,y]
                moves.append(move(location,x,y,gameMap))
    sendFrame(moves)
