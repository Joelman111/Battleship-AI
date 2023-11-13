import random
import math


class Ship(object):
    def __init__(self):
        pass
    def __repr__(self):
        return self.boat
    def placeBoat(self,boat):
        def isLegal(self,boat):
            if boat.set==False:
                if boat.orientation==True:
                    for (row,col) in boat.location:
                        if row>=self.rows or self.board[row][col]>0:
                            return False
                else:
                    for (row,col) in boat.location:
                        if (col>=self.cols or self.board[row][col]>0):
                            return False
                boat.set=True
                return True
            return False
        if isLegal(self,boat):
            for (row,col) in boat.location:
                self.board[row][col]=1
            return True
        return False
    def placeAIBoat(self,boat,row,col,orientation):
        def isLegal(self,boat,row,col,orientation):
            if boat.set==False:
                if orientation=='vert':
                    for y in range(boat.length):
                        if row+y>=self.rows or self.board[row+y][col]>0:
                            return False
                else:
                    for x in range(boat.length):
                        if (col+x>=self.cols or self.board[row][col+x]>0):
                            return False
                boat.set=True
                return True
            return False
        if isLegal(self,boat,row,col,orientation):
            if orientation=='vert':
                for y in range(boat.length):
                    self.board[row+y][col]=1
                    boat.location.append((row+y,col))
            else:
                for x in range(boat.length):
                    self.board[row][col+x]=1
                    boat.location.append((row,col+x))
            return True
        return False
    def isSunk(self,other):
        for (row,col) in other.location:
            if self.board[row][col]==1: return False
        return True
    def isHit(self,row,col):
        if row<0 or row>=10 or col<0 or col>=10:
            return False,False
        if self.board[row][col]==1:
            self.board[row][col] += 1
            for boat in self.boats:
                if (row,col) in boat.location:
                    if self.isSunk(boat):
                        for (row,col) in boat.location:
                            self.board[row][col]=3
                            boat.sunk=True
                        return (True,True) #SUNK
                    return (True,False) #HIT
        return (False,False)

class Battleship(Ship):
    def __init__(self):
        self.boat='battleship'
        self.length=4
        self.location=[]
        self.orientation=None
        self.set=False
        self.sunk=False
        self.imageVert=None
        self.imageHoriz=None
        self.rect=[]

class Cruiser(Ship):
    def __init__(self):
        self.boat='cruiser'
        self.length=3
        self.location=[]
        self.orientation=None
        self.set=False
        self.sunk=False
        self.imageVert=None
        self.imageHoriz=None
        self.rect=[]

class Sub(Ship):
    def __init__(self):
        self.boat='sub'
        self.length=3
        self.location=[]
        self.orientation=None
        self.set=False
        self.sunk=False
        self.imageVert=None
        self.imageHoriz=None
        self.rect=[]

class Carrier(Ship):
    def __init__(self):
        self.boat='carrier'
        self.length=5
        self.location=[]
        self.orientation=None
        self.set=False
        self.sunk=False
        self.imageVert=None
        self.imageHoriz=None
        self.rect=[]

class Patrol(Ship):
    def __init__(self):
        self.boat='patrol'
        self.length=2
        self.location=[]
        self.orientation=None
        self.set=False
        self.sunk=False
        self.imageVert=None
        self.imageHoriz=None
        self.rect=[]

class Board(Ship):
    def __init__(self,rows,cols):
        def createBoard(rows,cols):
            A=[[0 for x in range(cols)] for y in range(rows)]
            return A
        self.board=createBoard(rows,cols)
        self.rows=rows
        self.cols=cols
        self.cruiser=Cruiser()
        self.battleship=Battleship()
        self.carrier=Carrier()
        self.sub=Sub()
        self.patrol=Patrol()
        self.boats=[]
    def __repr__(self):
        return str(self.board)

def autoPlaceBoats(board):
    def placeBoat(board,boat):
        orientations=['vert','horiz']
        headRow=random.randint(0,9)
        headCol=random.randint(0,9)
        randOrient=orientations[random.randint(0,1)]
        if board.placeAIBoat(boat,headRow,headCol,randOrient) == False:
            placeBoat(board,boat)
        else:
            board.placeAIBoat(boat,headRow,headCol,randOrient)
    for boat in board.boats:
        placeBoat(board,boat)


class GuessBoard(object):
    def __init__(self,rows,cols):
        self.guessBoard=[[0 for x in range(rows)]for y in range(cols)]
        self.sunkShips=[]
        self.gameOver=False
        self.hitList=[]
    def makeGuess(self,other,row,col):
        if self.guessBoard[row][col]>0: return
        (hit,sunk)=other.isHit(row,col)
        if sunk:
            for boat in other.boats:
                if (row,col) in boat.location:
                    self.sunkShips.append(boat.length)
                    for (row,col) in boat.location:
                        if (row,col) in boat.location:
                            self.guessBoard[row][col]=3
        elif hit:
            self.guessBoard[row][col]=2
        else:
            self.guessBoard[row][col]=1
        if sorted(self.sunkShips)==[2,3,3,4,5]:
            self.gameOver=True

###############################################################################
#AI BELOW
###############################################################################

def battleshipAI(aiBoard, sunkShips, d):
    rows,cols=len(aiBoard),len(aiBoard[0])
    shipsLeft=[2,3,3,4,5]
    for sunkShip in sunkShips:
        shipsLeft.remove(sunkShip)
    for row in range(rows):
        for col in range(cols):
            if aiBoard[row][col]==2:
                return doHitThings(row,col,aiBoard,shipsLeft,d)
    return doBlankThings(aiBoard, shipsLeft,d)

def doHitThings(row,col,aiBoard,shipsLeft,d):
    mostHits,rows,cols=None,len(aiBoard),len(aiBoard[0])
    for direction in [(0,1),(1,0)]:
        hits=searchShipInDirection(row,col,direction,aiBoard)
        if mostHits==None or hits>mostHits:
            mostHits=hits
            bestDirection=direction
    drow,dcol=bestDirection
    if(isLegal(row+mostHits*drow,col+mostHits*dcol,aiBoard) and 
        aiBoard[row+mostHits*drow][col+mostHits*dcol]==0):
        return row+mostHits*drow,col+mostHits*dcol
    elif(isLegal(row-drow,col-dcol,aiBoard) and
        aiBoard[row-drow][col-dcol]==0):
        return row-drow,col-dcol
    elif(isLegal(row+int(not drow),col+int(not dcol),aiBoard) and 
        aiBoard[row+int(not drow)][col+int(not dcol)]==0):
        return row+int(not drow),col+int(not dcol)
    elif(isLegal(row-int(not drow),col-int(not dcol),aiBoard) and 
        aiBoard[row-int(not drow)][col-int(not dcol)]==0):
        return row-int(not drow),col-int(not dcol)
    else:
        return doBlankThings(aiBoard, shipsLeft,d)

def isLegal(row,col,aiBoard):
    rows,cols=len(aiBoard),len(aiBoard[0])
    if row<rows and col<cols and row>=0 and col>=0:
        return True
    else:
        return False

def searchShipInDirection(row,col,direction, aiBoard,hits=1):
    rows,cols=len(aiBoard),len(aiBoard[0])
    drow,dcol=direction
    newRow,newCol=row+drow,col+dcol
    if(newRow<0 or newCol<0 or newRow>=rows or newCol>=cols or 
        aiBoard[newRow][newCol]!=2):
        return hits
    else:
        return searchShipInDirection(newRow,newCol,direction,aiBoard,hits+1)

def addNearbyCells(row,col,aiBoard,shipsLeft, d):
    result,rows,cols=0,len(aiBoard),len(aiBoard[0])
    for (drow,dcol) in [(-1,0),(1,0),(0,-1),(0,1)]:
        for i in range(1,max(shipsLeft)):
            newRow=row+i*drow
            newCol=col+i*dcol
            if(newRow>=rows or newCol>=cols or newRow<0 or newCol<0):
                result+=i-1
                break
            elif aiBoard[newRow][newCol]!=0:
                result+=i-1
                break
            elif i==max(shipsLeft)-1:
                result+=i
                break
    return result+learnedConstant(row,col,d)

def doBlankThings(aiBoard,shipsLeft,d):
    rows,cols=len(aiBoard),len(aiBoard[0])
    maxResult=None
    for row in range(rows):
        for col in range(cols):
            if aiBoard[row][col]==0:
                result=addNearbyCells(row,col,aiBoard,shipsLeft,d)
                if maxResult==None or result>maxResult:
                    maxResult=result
                    maxRow,maxCol=row,col
    return maxRow,maxCol

def dictionaryOfValues():
    try:
        x=readFile('battleship.txt')
        d=dict()
        for location in x.splitlines():
            if location[0]=='n':
                d['n']=determineNumber(location)
            if location[0].isdigit():
                d['%s,%s'%(location[0],location[2])]=determineNumber(location[4:])
        return d
    except:
        return {'n':0}

def determineNumber(location):
    result=''
    for c in location:
        if c.isdigit():
            result+=c
    return int(result)

def learnedConstant(row,col,d):
    n=d['n']
    val = d.get('%d,%d'%(row,col),0)/d['n'] if d['n'] > 0 else 0
    k=val**2*8*(1-math.e**(-n*.02))
    return k

def readFile(path):
    with open(path, 'rt') as f:
        return f.read()

def writeFile(path, contents):
    with open(path, 'wt') as f:
        f.write(contents)

def changeFile(boatLocations, d):
    result=''
    d['n']+=1
    for (row,col) in boatLocations:
        d['%d,%d'%(row,col)] = d.get('%d,%d'%(row,col), 0) + 1
    for key in sorted(d.keys()):
        result+=key
        result+=': '
        result+=str(d[key])
        result+='\n'
    writeFile("battleship.txt",result)


##############################################################################