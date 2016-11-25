from hlt import *
from networking import *

def getValueMap(valueMap, gameMap):
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            valueMap[y][x] = gameMap.getSite(Location(x,y)).production
    return valueMap


myID, gameMap = getInit()
valueMap = [ [0 for x in range(gameMap.width)] for y in range(gameMap.height)]
valueMap = getValueMap(valueMap, gameMap)
sendInit("NadjaBot")

def move(location, gameMap, x, y):
    this_square = gameMap.getSite(location)
    #gameMap.getSite(location
    #
    #return Move(location,STILL)
    return Move(location, worthMovingCheck(sexiestNeighbour(location, gameMap, this_square.owner, this_square.strength, x, y, gameMap.width, gameMap.height), this_square.strength, this_square.production))


#our sexiest neighbour will be the highest production one we can beat
def sexiestNeighbour(location, gameMap, ownerID, myStrength, x, y,w,h):
    global valueMap
    dirs = [256,256,256,256]
    dirsIOwn = []
    #Find neighbours we can beat
    for d in CARDINALS:
        neighbour_site = gameMap.getSite(location, d)
        if ownerID == neighbour_site.owner:
            dirsIOwn.append((d,neighbour_site.strength))
        if (strongerThanYou(myStrength, neighbour_site.strength) and ownerID != neighbour_site.owner):
            dirs[d-1] = neighbour_site.strength

    if min(dirs) == 256:
        if len(dirsIOwn) == 4:
            #all the squares in the map are friends!
            friendlyChoices = []
            for i in dirsIOwn:
                friendlyChoices.append(i[0]) #we could go here
            viablePals = []
            for d in friendlyChoices:
                #it's the actual direction by now :lenny-face:
                palStrength = gameMap.getSite(location, d).strength
                if myStrength + palStrength <= 255:
                    viablePals.append(d)
            if len(viablePals)== 0:
                return travelOnMyWaywordSon(location, gameMap, ownerID, myStrength, x, y, w, h)
            return getMostValuable(viablePals,x,y,w,h)
        else:
            return STILL

    beatableDirections = []
    index = 0
    for d in dirs:
        if d != 256:
            beatableDirections.append(index+1)
        index+=1

    if len(beatableDirections) == 1:
        return beatableDirections[0]

    #There's a more complex trade-off to consider here.....
    return getMostValuable(beatableDirections, x, y,w,h)

#this function tries to determine which way a block surrounded by friendlies should move
def travelOnMyWaywordSon(location, gameMap, ownerID, myStrength, x, y, w, h):
    for y1 in range(gameMap.height):
        for x1 in range(gameMap.width):
            location1 = Location(x1, y1)
            site1 = gameMap.getSite(location1)
            if site1.owner != ownerID:
                return directionTowardsCoords(x1,y1,x,y,w,h)
    return STILL

def directionTowardsCoords(targetX,targetY,x,y,w,h):
    diffX = abs(targetX - x)
    diffY = abs(targetY - y)
    halfwayW = w/2
    halfwayH = h/2
    if x > halfwayW:
        if targetX > halfwayW:
            return EAST
        else:
            return WEST
    else:
        if targetX < halfwayW:
            return WEST
        else:
            return EAST

    if y > halfwayH:
        if targetY > halfwayH:
            return SOUTH
        else:
            return NORTH
    else:
        if targetY < halfwayH:
            return NORTH
        else:
            return SOUTH

    return STILL


def getMostValuable(directionList, x, y,w,h):
    global valueMap
    mostValuable = 0
    chosenValuableDirection = STILL
    for d in directionList:
        if d == EAST:
            val = valueMap[y][(x+1)%w]
            if val > mostValuable:
                mostValuable = val
                chosenValuableDirection = d
        if d == WEST:
            val = valueMap[y][x-1%w]
            if val > mostValuable:
                mostValuable = val
                chosenValuableDirection = d
        if d == NORTH:
            val = valueMap[(y-1)%h][x]
            if val > mostValuable:
                mostValuable = val
                chosenValuableDirection = d
        if d == SOUTH:
            val = valueMap[(y+1)%h][x]
            if val > mostValuable:
                mostValuable = val
                chosenValuableDirection = d
    return chosenValuableDirection

def worthMovingCheck(direction, siteStrength, siteProduction):
    if siteStrength >= siteProduction * 3:
        return direction
    else:
        return STILL

def strongerThanYou(a,b):
    return a > b

while True:
    moves = []
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            moves.append(move(location, gameMap, x, y))
    sendFrame(moves)
