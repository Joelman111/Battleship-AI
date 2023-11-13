################################################################################
# colors
################################################################################
'''
pygamegame.py
created by Lukas Peraza
 for 15-112 F15 Pygame Optional Lecture, 11/11/15
'''
import pygame
from objects import *

################################################################################
# colors
################################################################################

WHITE = (255, 255, 255)
GOLD = (255,215,0)
BLACK = (0,0,0)
RED = (139,0,0)
ORANGE = (255, 165, 0)
DARK_BLUE = (0, 0 ,139)

################################################################################
# Main init
################################################################################

class PygameGame(object):

    def init(self):
        self.hit_sound = pygame.mixer.Sound('assets\\sounds\\Hit.wav')
        self.fire_sound = pygame.mixer.Sound('assets\\sounds\\Boom.wav')
        self.fire_sound.set_volume(.2)
        # pygame.mixer.Sound.play(self.fire_sound)
        # pygame.mixer.Sound.play(self.hit_sound)

        self.mode = "Menu"
        self.callersMode = self.mode
        self.buttonHeight = 450
        (self.playx0, self.playy0) = (40, self.buttonHeight)
        (self.playx1, self.playy1) = (150, self.buttonHeight+75)
        (self.instx0, self.insty0) = (550, self.buttonHeight)
        (self.instx1, self.insty1) = (875, self.buttonHeight+75)
        self.rows = 10
        self.cols = 10
        self.cellSize = 40
        self.gridSize = self.rows*self.cellSize
        self.gridMargin = self.cellSize*1.5
        self.marginx1 = (self.width-(2*self.gridSize+self.gridMargin))/2
        self.marginx2 = self.gridMargin+self.gridSize+self.marginx1
        self.marginy = (self.height-self.gridSize)/2
        self.highlightedRow = 0
        self.highlightedCol = 0
        self.marginBetweenBoats = 30
        self.boatWidth = self.cellSize
        self.boat1Height = self.cellSize*5
        self.boat2Height = self.cellSize*4
        self.boat3Height = self.cellSize*3
        self.boat4Height = self.cellSize*3
        self.boat5Height = self.cellSize*2
        self.boat1X = self.marginBetweenBoats
        self.boat1Y = 2*self.marginBetweenBoats
        self.boat2X = self.marginBetweenBoats
        self.boat2Y = self.boat1Y+self.boat1Height+self.marginBetweenBoats
        self.boat3X = self.marginBetweenBoats*4
        self.boat3Y = self.boat1Y
        self.boat4X = self.marginBetweenBoats*4
        self.boat4Y = self.boat3Y+self.boat3Height+self.marginBetweenBoats
        self.boat5X = self.marginBetweenBoats*4
        self.boat5Y = self.boat4Y+self.boat4Height+self.marginBetweenBoats
        self.carrier = Carrier()
        self.battleship = Battleship()
        self.cruiser = Cruiser()
        self.sub = Sub()
        self.patrol = Patrol()
        self.carrier.rect = [self.boat1X, self.boat1Y, self.boat1X+\
                             self.boatWidth,self.boat1Y+self.boat1Height]
        self.battleship.rect = [self.boat2X, self.boat2Y, self.boat2X+\
                                self.boatWidth,self.boat2Y+self.boat2Height]
        self.cruiser.rect = [self.boat3X, self.boat3Y, self.boat3X+\
                             self.boatWidth, self.boat3Y+self.boat3Height]
        self.sub.rect = [self.boat4X, self.boat4Y, self.boat4X+self.boatWidth,
                         self.boat4Y+self.boat4Height]
        self.patrol.rect = [self.boat5X, self.boat5Y, self.boat5X+\
                            self.boatWidth,self.boat5Y+self.boat5Height]
        self.carrier.imageHoriz = pygame.image.load("assets\\images\\Carrier.png")
        self.battleship.imageHoriz = pygame.image.load("assets\\images\\BattleShip.png")
        self.cruiser.imageHoriz = pygame.image.load("assets\\images\\Cruiser.png")
        self.sub.imageHoriz = pygame.image.load("assets\\images\\Sub.png")
        self.patrol.imageHoriz = pygame.image.load("assets\\images\\Patrol.png")
        self.carrier.imageVert = pygame.image.load("assets\\images\\CarrierHorizontal.png")
        self.battleship.imageVert = pygame.image.load("assets\\images\\BattleShipHorizontal.png")
        self.cruiser.imageVert = pygame.image.load("assets\\images\\CruiserHorizontal.png")
        self.sub.imageVert = pygame.image.load("assets\\images\\SubHorizontal.png")
        self.patrol.imageVert = pygame.image.load("assets\\images\\PatrolHorizontal.png")
        self.carrier.orientation = True
        self.battleship.orientation = True
        self.cruiser.orientation = True
        self.sub.orientation = True
        self.patrol.orientation = True
        self.selectedBoat = None
        self.buildHighlightedCells = []
        self.buildOrientation = False
        self.board = Board(self.rows, self.cols)
        self.board.boats = [self.carrier, self.battleship, self.cruiser, self.sub, self.patrol]
        self.AIBoard = Board(self.rows, self.cols)
        self.AIBoard.boats = [Carrier(), Battleship(), Cruiser(), Sub(), Patrol()]
        autoPlaceBoats(self.AIBoard)
        self.dictionary = dictionaryOfValues()
        self.guessBoard = GuessBoard(self.rows, self.cols)
        self.AIGuessBoard = GuessBoard(self.rows, self.cols)
        self.AITurn = False
        self.AITime=15
        self.AIText = "Thinking..."
        self.xImage = pygame.image.load("assets\\images\\redX.png")
        self.textSpacing = 50
        self.instr1 = 'The objective of Battlship is to sink all of your opponents boats'
        self.instr2 = 'Click on a ship, then use arrow keys to move, space to rotate, and enter to place'
        self.instr3 = 'Once you have placed your boats, press "p" to play'
        self.instr4 = 'While playing, use arrow keys to move and space to shoot'
        self.instr5 = 'Return to the menu using "m" at any time to restart game'
        self.instr6 = "Press 'i' at any time to view the instructions, press any key to return to game"

    def __init__(self, width=900, height=579, fps=50, title="Battleship"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()

################################################################################
# run 
################################################################################

    def run(self):

        clock = pygame.time.Clock()
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.load("assets\\sounds\\Epic_TV_Theme.mp3")
        pygame.mixer.music.play(-1)
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()

################################################################################
# Mode Dispatcher
################################################################################

    def mousePressed(self, x, y):
        if(self.mode == 'Menu'): self.menuMousePressed(x, y)
        elif(self.mode == 'Instructions'): self.instMousePressed(x, y)
        elif(self.mode == 'Build'): self.buildMousePressed(x, y)
        elif(self.mode == 'Game'): self.gameMousePressed(x, y)

    def mouseReleased(self, x, y):
        if(self.mode == 'Menu'): self.menuMouseReleased(x, y)
        elif(self.mode == 'Instructions'): self.instMouseReleased(x, y)
        elif(self.mode == 'Build'): self.buildMouseReleased(x, y)
        elif(self.mode == 'Game'): self.gameMouseReleased(x, y)

    def mouseMotion(self, x, y):
        if(self.mode == 'Menu'): self.menuMouseMotion(x, y)
        elif(self.mode == 'Instructions'): self.instMouseMotion(x, y)
        elif(self.mode == 'Build'): self.buildMouseMotion(x, y)
        elif(self.mode == 'Game'): self.gameMouseMotion(x, y)

    def mouseDrag(self, x, y):
        if(self.mode == 'Menu'): self.menuMouseDrag(x, y)
        elif(self.mode == 'Instructions'): self.instMouseDrag(x, y)
        elif(self.mode == 'Build'): self.buildMouseDrag(x, y)
        elif(self.mode == 'Game'): self.gameMouseDrag(x, y)

    def keyPressed(self, keyCode, modifier):
        if(self.mode == 'Menu'): self.menuKeyPressed(keyCode, modifier)
        elif(self.mode == 'Instructions'): 
            self.instKeyPressed(keyCode, modifier)
        elif(self.mode == 'Build'): self.buildKeyPressed(keyCode, modifier)
        elif(self.mode == 'Game'): self.gameKeyPressed(keyCode, modifier)

    def keyReleased(self, keyCode, modifier):
        if(self.mode == 'Menu'): self.menuKeyReleased(keyCode, modifier)
        elif(self.mode == 'Instructions'): 
            self.instKeyReleased(keyCode, modifier)
        elif(self.mode == 'Build'): self.buildKeyReleased(keyCode, modifier)
        elif(self.mode == 'Game'): self.gameKeyReleased(keyCode, modifier)

    def timerFired(self, dt):
        if(self.mode == 'Menu'): self.menuTimerFired(dt)
        elif(self.mode == 'Instructions'): self.instTimerFired(dt)
        elif(self.mode == 'Build'): self.buildTimerFired(dt)
        elif(self.mode == 'Game'): self.gameTimerFired(dt)

    def redrawAll(self, screen):
        if(self.mode == 'Menu'): self.menuRedrawAll(screen)
        elif(self.mode == 'Instructions'): self.instRedrawAll(screen)
        elif(self.mode == 'Build'): self.buildRedrawAll(screen)
        elif(self.mode == 'Game'): self.gameRedrawAll(screen)

    def isKeyPressed(self, key):
        if(self.mode == 'Menu'): self.menuIsKeyPressed(key)
        elif(self.mode == 'Instructions'): self.instIsKeyPressed(key)
        elif(self.mode == 'Build'): self.buildIsKeyPressed(key)
        elif(self.mode == 'Game'): self.gameIsKeyPressed(key)

################################################################################
# Menu
################################################################################

    def menuMousePressed(self, x, y):
        if(x >= self.playx0 and x <= self.playx1 and \
           y >= self.playy0 and y <= self.playy1):
            pygame.mixer.Sound.play(self.fire_sound)
            self.mode = "Build"
        elif(x >= self.instx0 and x <= self.instx1 and \
             y >= self.insty0 and y <= self.insty1):
            self.mode = "Instructions"

    def menuMouseReleased(self, x, y):
        pass

    def menuMouseMotion(self, x, y):
        pass

    def menuMouseDrag(self, x, y):
        pass

    def menuKeyPressed(self, keyCode, modifier):
        pass

    def menuKeyReleased(self, keyCode, modifier):
        pass

    def menuTimerFired(self, dt):
        pass

    def menuRedrawAll(self, screen):
        image = pygame.image.load("assets\\images\\Menu.png")
        screen.blit(image, (0, 0))
        width = 120
        xLocation, yLocation = self.playx0, self.buttonHeight
        x0,y0 = xLocation - 15,yLocation - 15
        x1,y1 = xLocation + width + 5, yLocation + 65
        pygame.draw.rect(screen, ORANGE, (x0, y0, x1-x0, y1-y0), 0)
        x0,y0 = xLocation - 10, yLocation - 10
        x1,y1 = xLocation + width, yLocation + 60
        pygame.draw.rect(screen, DARK_BLUE, (x0, y0, x1-x0, y1-y0), 0)

        width = 320
        xLocation, yLocation = 550, self.buttonHeight
        x0,y0 = xLocation - 15,yLocation - 15
        x1,y1 = xLocation + width + 5, yLocation + 65
        pygame.draw.rect(screen, ORANGE, (x0, y0, x1-x0, y1-y0), 0)
        x0,y0 = xLocation - 10, yLocation - 10
        x1,y1 = xLocation + width, yLocation + 60
        pygame.draw.rect(screen, DARK_BLUE, (x0, y0, x1-x0, y1-y0), 0)
        buttonFont = pygame.font.SysFont(None, 75)
        playButton = buttonFont.render("Play", 1, WHITE)
        screen.blit(playButton, (self.playx0, self.buttonHeight))
        instructionsButton = buttonFont.render("Instructions", 1, WHITE)
        screen.blit(instructionsButton, (550, self.buttonHeight))

    def menuIsKeyPressed(self, key):
        return self._keys.get(key, False)

################################################################################
# Instructions
################################################################################

    def instMousePressed(self, x, y):
        if(x >= self.instx0 and x <= self.instx1-160 and \
            y >= self.insty0 and y <= self.insty1):
            self.init()

    def instMouseReleased(self, x, y):
        pass

    def instMouseMotion(self, x, y):
        pass

    def instMouseDrag(self, x, y):
        pass

    def instKeyPressed(self, keyCode, modifier):
        if(keyCode == pygame.K_m): 
            self.init()
        self.mode = self.callersMode

    def instKeyReleased(self, keyCode, modifier):
        pass

    def instTimerFired(self, dt):
        pass

    def instRedrawAll(self, screen):
        image = pygame.image.load("assets\\images\\ocean.jpg")
        screen.blit(image, (0, 0))
        textFont = pygame.font.SysFont(None, 70)
        instructionsSign = textFont.render("Instructions", 1, WHITE)
        screen.blit(instructionsSign, (self.width//2 - 150, 20))

        textFont = pygame.font.SysFont(None, 30)

        text1 = textFont.render(self.instr1, 1, WHITE)
        screen.blit(text1, (self.textSpacing, self.textSpacing*3))

        text2 = textFont.render(self.instr2, 1, WHITE)
        screen.blit(text2, (self.textSpacing, self.textSpacing*4))

        text3 = textFont.render(self.instr3, 1, WHITE)
        screen.blit(text3, (self.textSpacing, self.textSpacing*5))

        text4 = textFont.render(self.instr4, 1, WHITE)
        screen.blit(text4, (self.textSpacing, self.textSpacing*6))

        text5 = textFont.render(self.instr5, 1, WHITE)
        screen.blit(text5, (self.textSpacing, self.textSpacing*7))

        text6 = textFont.render(self.instr6, 1, WHITE)
        screen.blit(text6, (self.textSpacing, self.textSpacing*8))

        width = 160
        xLocation, yLocation = 550, self.buttonHeight
        x0,y0 = xLocation - 15,yLocation - 15
        x1,y1 = xLocation + width + 5, yLocation + 65
        pygame.draw.rect(screen, ORANGE, (x0, y0, x1-x0, y1-y0), 0)
        x0,y0 = xLocation - 10, yLocation - 10
        x1,y1 = xLocation + width, yLocation + 60
        pygame.draw.rect(screen, DARK_BLUE, (x0, y0, x1-x0, y1-y0), 0)

        buttonFont = pygame.font.SysFont(None, 75)
        menuButton = buttonFont.render("Menu", 1, WHITE)
        screen.blit(menuButton, (550, self.buttonHeight))

    def instIsKeyPressed(self, key):
        pass

################################################################################
# Game
################################################################################

    def gameMousePressed(self, x, y):
        pass

    def gameMouseReleased(self, x, y):
        pass

    def gameMouseMotion(self, x, y):
        pass

    def gameMouseDrag(self, x, y):
        pass

    def gameKeyPressed(self, keyCode, modifier):
        if self.AITurn==False:
            if(keyCode == pygame.K_m): 
                self.init()
            if(self.guessBoard.gameOver or self.AIGuessBoard.gameOver):
                pass
            elif(keyCode == pygame.K_i): 
                self.callersMode = self.mode
                self.mode = "Instructions"
            elif(keyCode == pygame.K_LEFT):
                self.highlightedCol -= 1
                if(self.highlightedCol < 0): 
                    self.highlightedCol = self.cols-1
            elif(keyCode == pygame.K_UP):
                self.highlightedRow -= 1
                if(self.highlightedRow < 0): 
                    self.highlightedRow = self.rows-1
            elif(keyCode == pygame.K_DOWN):
                self.highlightedRow += 1
                if(self.highlightedRow >= self.rows): 
                    self.highlightedRow = 0
            elif(keyCode == pygame.K_RIGHT):
                self.highlightedCol += 1
                if(self.highlightedCol >= self.cols): 
                    self.highlightedCol = 0
            elif(keyCode == pygame.K_SPACE):
                if(self.guessBoard.guessBoard[self.highlightedRow][self.highlightedCol] == 0):
                    pygame.mixer.Sound.play(self.hit_sound)
                    self.guessBoard.makeGuess(self.AIBoard, self.highlightedRow, self.highlightedCol)
                    if(self.guessBoard.gameOver):
                        l = []
                        for boat in self.board.boats:
                            l += boat.location
                        changeFile(l, self.dictionary)
                        pygame.mixer.Sound.play(self.fire_sound)
                        self.gameOverText = "YOU WIN!"
                    else: 
                        self.AITime=15
                        self.AITurn = not self.AITurn

    def gameKeyReleased(self, keyCode, modifier):
        pass

    def gameTimerFired(self, dt):
        if(self.AITurn and self.AITime<=0):
            (row, col) = battleshipAI(self.AIGuessBoard.guessBoard, self.AIGuessBoard.sunkShips, self.dictionary)
            self.AIGuessBoard.makeGuess(self.board, row, col)
            self.AITurn = not self.AITurn
            pygame.mixer.Sound.play(self.hit_sound)
            if(self.AIGuessBoard.gameOver):
                l = []
                for boat in self.board.boats:
                    l += boat.location
                changeFile(l, self.dictionary)
                pygame.mixer.Sound.play(self.fire_sound)
                self.gameOverText = "YOU LOSE!"
        else:
            self.AITime-=1

    def gameRedrawAll(self, screen):
        image = pygame.image.load("assets\\images\\ocean.jpg")
        screen.blit(image, (0, 0))
        drawGrid(self, screen, self.marginx1, self.marginy,
                 [(self.highlightedRow, self.highlightedCol)], self.guessBoard.guessBoard)
        drawGrid(self, screen, self.marginx2, self.marginy, [], self.AIGuessBoard.guessBoard)
        font = pygame.font.SysFont(None, 67)
        text1 = font.render("Opponent's Board", 1, WHITE)
        screen.blit(text1, (10, 10))
        text2 = font.render("Your Board", 1, WHITE)
        screen.blit(text2, (self.marginx2+75, 10))
        if(self.carrier.orientation):
            screen.blit(self.carrier.imageHoriz, (self.carrier.rect[0], 
                        self.carrier.rect[1]))
        else:
            screen.blit(self.carrier.imageVert, (self.carrier.rect[0], 
                        self.carrier.rect[1]))
        if(self.battleship.orientation):
            screen.blit(self.battleship.imageHoriz, (self.battleship.rect[0], 
                        self.battleship.rect[1]))
        else:
            screen.blit(self.battleship.imageVert, (self.battleship.rect[0], 
                        self.battleship.rect[1]))
        if(self.cruiser.orientation):
            screen.blit(self.cruiser.imageHoriz, (self.cruiser.rect[0], 
                        self.cruiser.rect[1]))
        else:
            screen.blit(self.cruiser.imageVert, (self.cruiser.rect[0], 
                        self.cruiser.rect[1]))
        if(self.sub.orientation):
            screen.blit(self.sub.imageHoriz, (self.sub.rect[0], 
                        self.sub.rect[1]))
        else:
            screen.blit(self.sub.imageVert, (self.sub.rect[0], 
                        self.sub.rect[1]))
        if(self.patrol.orientation):
            screen.blit(self.patrol.imageHoriz, (self.patrol.rect[0], 
                        self.patrol.rect[1]))
        else:
            screen.blit(self.patrol.imageVert, (self.patrol.rect[0], 
                        self.patrol.rect[1]))
        drawSymbols(self, screen, self.marginx1, self.marginy, self.guessBoard.guessBoard)
        drawSymbols(self, screen, self.marginx2, self.marginy, self.AIGuessBoard.guessBoard)
        if(self.AITurn):
            font = pygame.font.SysFont(None, 30)
            text3 = font.render(self.AIText,1, WHITE)
            screen.blit(text3, (400, 550))
        if(self.AIGuessBoard.gameOver or self.guessBoard.gameOver):
            font = pygame.font.SysFont(None, 80)
            text4 = font.render(self.gameOverText,1, WHITE)
            pygame.draw.rect(screen, RED, (100, 239, 700, 100), 0)
            screen.blit(text4, (300, 259))

    def gameIsKeyPressed(self, key):
        return self._keys.get(key, False)

################################################################################
# Build
################################################################################
    
    def buildMousePressed(self, x, y):
        if(x >= self.carrier.rect[0] and x <= self.carrier.rect[2] and \
           y >= self.carrier.rect[1] and y <= self.carrier.rect[3]):
            self.buildHighlightedCells = [(0,0),(0,1),(0,2),(0,3),(0,4)]
            self.selectedBoat = self.carrier
        elif(x >= self.battleship.rect[0] and x <= self.battleship.rect[2] and \
             y >= self.battleship.rect[1] and y <= self.battleship.rect[3]):
            self.buildHighlightedCells = [(0,0),(0,1),(0,2),(0,3)]
            self.selectedBoat = self.battleship
        elif(x >= self.cruiser.rect[0] and x <= self.cruiser.rect[2] and \
             y >= self.cruiser.rect[1] and y <= self.cruiser.rect[3]):
            self.buildHighlightedCells = [(0,0),(0,1),(0,2)]
            self.selectedBoat = self.cruiser
        elif(x >= self.sub.rect[0] and x <= self.sub.rect[2] and \
             y >= self.sub.rect[1] and y <= self.sub.rect[3]):
            self.buildHighlightedCells = [(0,0),(0,1),(0,2)]
            self.selectedBoat = self.sub
        elif(x >= self.patrol.rect[0] and x <= self.patrol.rect[2] and \
             y >= self.patrol.rect[1] and y <= self.patrol.rect[3]):
            self.buildHighlightedCells = [(0,0),(0,1)]
            self.selectedBoat = self.patrol

    def buildMouseReleased(self, x, y):
        pass

    def buildMouseMotion(self, x, y):
        pass

    def buildMouseDrag(self, x, y):
        pass

    def buildKeyPressed(self, keyCode, modifier):
        if(keyCode == pygame.K_m): 
            self.init()
        if(keyCode == pygame.K_i):
            self.callersMode = self.mode
            self.mode = "Instructions"
        elif(keyCode == pygame.K_p): 
            if(self.carrier.rect[0] != self.boat1X and self.battleship.rect[0] \
               != self.boat2X and self.cruiser.rect[0] != self.boat3X and \
               self.sub.rect[0] != self.boat4X and self.patrol.rect[0]\
               != self.boat5X):
                self.mode = "Game"
        l = []
        if(keyCode == pygame.K_LEFT):
            for (row, col) in self.buildHighlightedCells:
                if(col-1<0):
                    break
                l.append((row, col-1))
            self.moveHighlightedCells(l,False)
        elif(keyCode == pygame.K_UP):
            for (row, col) in self.buildHighlightedCells:
                if(row-1<0):
                    break
                l.append((row-1, col))
            self.moveHighlightedCells(l,False)
        elif(keyCode == pygame.K_DOWN):
            for (row, col) in self.buildHighlightedCells:
                if(row+1>=self.rows):
                    break
                l.append((row+1, col))
            self.moveHighlightedCells(l,False)
        elif(keyCode == pygame.K_RIGHT):
            for (row, col) in self.buildHighlightedCells:
                if(col+1>=self.cols):
                    break
                l.append((row, col+1))
            self.moveHighlightedCells(l,False)
        elif(keyCode == pygame.K_SPACE):
            self.buildOrientation = not self.buildOrientation
            if(self.buildOrientation):
                for (i, (row, col)) in enumerate(self.buildHighlightedCells):
                    l.append((row+i, col-i))
            else:
                for (i, (row, col)) in enumerate(self.buildHighlightedCells):
                    l.append((row-i, col+i))
            for (row, col) in l:
                if(min(row, col) < 0 or max(row, col) >= self.rows): l=[]
            self.moveHighlightedCells(l,True)
        elif(self.selectedBoat != None and keyCode == pygame.K_RETURN):
            self.selectedBoat.location = self.buildHighlightedCells
            if(self.board.placeBoat(self.selectedBoat)):
                (row, col) = self.selectedBoat.location[0]
                (x0, y0, x1, y1) = getCellBounds(self, row, col, self.marginx2, 
                                                 self.marginy)
                if(self.selectedBoat.orientation != self.buildOrientation):
                    self.selectedBoat.orientation =\
                    not self.selectedBoat.orientation
                self.selectedBoat.rect[0], self.selectedBoat.rect[1] = x0, y0
                self.buildHighlightedCells = []
                self.selectedBoat = None
                self.buildOrientation = False
            else:
                self.selectedBoat.location = []

    def moveHighlightedCells(self,l,space):
        if len(l)==len(self.buildHighlightedCells):
            self.buildHighlightedCells=l
        elif len(l)!=len(self.buildHighlightedCells) and space:
            self.buildOrientation=not self.buildOrientation

    def buildKeyReleased(self, keyCode, modifier):
        pass

    def buildTimerFired(self, dt):
        pass

    def buildRedrawAll(self, screen):
        image = pygame.image.load("assets\\images\\ocean.jpg")
        screen.blit(image, (0, 0))
        font = pygame.font.SysFont(None, 67)
        text = font.render("Place your ships", 1, WHITE) 
        screen.blit(text, (275,10))
        drawGrid(self, screen, self.marginx2, self.marginy, 
                 self.buildHighlightedCells, Board(10,10).board)
        if(self.carrier.orientation):
            screen.blit(self.carrier.imageHoriz, (self.carrier.rect[0], 
                        self.carrier.rect[1]))
        else:
            screen.blit(self.carrier.imageVert, (self.carrier.rect[0], 
                        self.carrier.rect[1]))
        if(self.battleship.orientation):
            screen.blit(self.battleship.imageHoriz, (self.battleship.rect[0], 
                        self.battleship.rect[1]))
        else:
            screen.blit(self.battleship.imageVert, (self.battleship.rect[0], 
                        self.battleship.rect[1]))
        if(self.cruiser.orientation):
            screen.blit(self.cruiser.imageHoriz, (self.cruiser.rect[0], 
                        self.cruiser.rect[1]))
        else:
            screen.blit(self.cruiser.imageVert, (self.cruiser.rect[0], 
                        self.cruiser.rect[1]))
        if(self.sub.orientation):
            screen.blit(self.sub.imageHoriz, (self.sub.rect[0], 
                        self.sub.rect[1]))
        else:
            screen.blit(self.sub.imageVert, (self.sub.rect[0], 
                        self.sub.rect[1]))
        if(self.patrol.orientation):
            screen.blit(self.patrol.imageHoriz, (self.patrol.rect[0], 
                        self.patrol.rect[1]))
        else:
            screen.blit(self.patrol.imageVert, (self.patrol.rect[0], 
                        self.patrol.rect[1]))

    def buildIsKeyPressed(self, key):
        return self._keys.get(key, False)

################################################################################
# Grid Making
################################################################################

#http://www.cs.cmu.edu/~112/ referenced

def pointInGrid(self, x, y, marginx, marginy):
    # return True if (x, y) is inside the grid defined by data.
    return ((marginx <= x <= self.width-marginx) and
            (marginy <= y <= self.height-marginy))

def getCell(self, x, y, marginx, marginy):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid(self, x, y)):
        return (-1, -1)
    gridSize  = self.rows*self.cellSize
    row = (y - marginy) // self.cellSize
    col = (x - marginx) // self.cellSize
    # triple-check that we are in bounds
    row = min(self.rows-1, max(0, row))
    col = min(self.cols-1, max(0, col))
    return (row, col)

def getCellBounds(self, row, col, marginx, marginy):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridSize  = self.rows*self.cellSize
    x0 = marginx + col * self.cellSize
    x1 = marginx + (col+1) * self.cellSize
    y0 = marginy + row * self.cellSize
    y1 = marginy + (row+1) * self.cellSize
    return (x0, y0, x1, y1)

def drawGrid(self, screen, marginx, marginy, highlightedCells, board):
    for row in range(self.rows):
        for col in range(self.cols):
            fill = 3
            if((row, col) in highlightedCells): fill = 0
            (x0, y0, x1, y1) = getCellBounds(self, row, col, marginx, marginy)
            pygame.draw.rect(screen, WHITE, (x0, y0, x1-x0, y1-y0), fill)
            if(board[row][col] == 1):
                pygame.draw.circle(screen, WHITE, (int((x1+x0)//2), int((y1+y0)//2)), fill)
            if(board[row][col] == 2):
                screen.blit(self.xImage, (x0, y0))
            if(board[row][col] == 3):
                pygame.draw.rect(screen, WHITE, (x0, y0, x1-x0, y1-y0), 0)
                screen.blit(self.xImage, (x0, y0))

def drawSymbols(self, screen, marginx, marginy, board):
    for row in range(self.rows):
        for col in range(self.cols):
            (x0, y0, x1, y1) = getCellBounds(self, row, col, marginx, marginy)
            if(board[row][col] == 1):
                pygame.draw.circle(screen, WHITE, (int((x1+x0)//2), int((y1+y0)//2)), 15)
            if(board[row][col] == 2):
                screen.blit(self.xImage, (x0, y0))
            if(board[row][col] == 3):
                pygame.draw.rect(screen, WHITE, (x0, y0, x1-x0, y1-y0), 0)
                screen.blit(self.xImage, (x0, y0))

################################################################################
# Main
################################################################################

def main():
    try:
        game = PygameGame()
        game.run()
    finally:
        pygame.quit()

if __name__ == '__main__':
    main()