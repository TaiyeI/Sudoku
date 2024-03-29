import pygame, sys
import time

pygame.init()

#Defining Window Dimensions
width = 9*30
height = width + 230
#Creating Arrays to hold instances of classes
cells = {}
buttons = {}
#Setting global variables for refresh, screen,display and font
FPS = 20
FPSCLOCK = pygame.time.Clock()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Sudoko')
screen.fill(pygame.Color("white"))

BASICFONTSIZE = int(width/14.4)
BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

pygame.display.flip()


def main():

    #Define Cells and Buttons
    defCells(exampleBoard)
    defButtons()


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                #Quit Game if exit button clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Checking for mouseclicks
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    clicked(pos)
            if event.type == pygame.KEYDOWN:
                #Checking for number input
                numbers = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
                if event.key in numbers:
                    x = numbers.index(event.key)
                    changeNum(x)
                    if pos:
                        clicked(pos)
        #Drawing game features
        drawCells()
        drawButtons()
        drawGrid()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    pygame.quit()
    sys.exit()

#Defining static dependable variables to allow for window size scalability
WINDOWHEIGHT = height
GRIDHEIGHT = width
GRIDWIDTH = width
SQUARESIZE = int(width/3)
CELLSIZE = int(width/9)
NUMBERSIZE = int(CELLSIZE/3)
WINDOWSIZE = 81
BUTTONHEIGHT = GRIDWIDTH*(50/270)
BUTTONWIDTH = GRIDWIDTH*(70/270)
NUMOFCELLS = int(GRIDWIDTH/CELLSIZE)

def drawGrid():
    for x in range(0, GRIDWIDTH, CELLSIZE):
        pygame.draw.line(screen, pygame.Color("gray"), (x,0), (x,GRIDHEIGHT))
    for y in range(0, GRIDHEIGHT, CELLSIZE):
        pygame.draw.line(screen, pygame.Color("gray"), (0,y), (GRIDWIDTH,y))
    
    
    for x in range(0, GRIDWIDTH + SQUARESIZE, SQUARESIZE):
        pygame.draw.line(screen, pygame.Color("black"), (x,0), (x,GRIDHEIGHT))
    for y in range(0, GRIDHEIGHT + SQUARESIZE, SQUARESIZE):
        pygame.draw.line(screen, pygame.Color("black"), (0,y), (GRIDWIDTH,y))

    
    

exampleBoard = [[3, 0, 6, 5, 0, 8, 4, 0, 0], 
                [5, 2, 0, 0, 0, 0, 0, 0, 0], 
                [0, 8, 7, 0, 0, 0, 0, 3, 1], 
                [0, 0, 3, 0, 1, 0, 0, 8, 0], 
                [9, 0, 0, 8, 6, 3, 0, 0, 5], 
                [0, 5, 0, 0, 9, 0, 6, 0, 0], 
                [1, 3, 0, 0, 0, 0, 2, 5, 0], 
                [0, 0, 0, 0, 0, 0, 0, 7, 4], 
                [0, 0, 5, 2, 0, 6, 3, 0, 0]]

correctBoard = [[3, 1, 6, 5, 7, 8, 4, 9, 2],
                [5, 2, 9, 1, 3, 4, 7, 6, 8],
                [4, 8, 7, 6, 2, 9, 5, 3, 1],
                [2, 6, 3, 4, 1, 5, 9, 8, 7],
                [9, 7, 4, 8, 6, 3, 1, 2, 5],
                [8, 5, 1, 7, 9, 2, 6, 4, 3],
                [1, 3, 8, 9, 4, 7, 2, 5, 6],
                [6, 9, 2, 3, 5, 1, 8, 7, 4],
                [7, 4, 5, 2, 8, 6, 3, 1, 9]]


#Creates intances of class CellBlock
def defCells(board):
    for x in range(NUMOFCELLS):
        for y in range(NUMOFCELLS):
            boardNum = board[round(y)][round(x)]
            if  boardNum == 0:
                cells[x,y] = CellBlock(x, y, CELLSIZE,True, '')
            else:
                cells[x,y] = CellBlock(x, y, CELLSIZE,False, str(boardNum))    

#Creates intances of class Buttons     
def defButtons():
    y = 0
    for x in range(int((GRIDWIDTH/3 - BUTTONWIDTH)/2), GRIDWIDTH, int(GRIDWIDTH/3)):
        buttons[x,y] = Buttons(x, y)


class CellBlock:
    def __init__(self,x, y, CELLSIZE, fluid=True, number=''):
        self.number = number
        self.fluid = fluid
        self.x = x*CELLSIZE
        self.y = y*CELLSIZE
        self.rect = pygame.Rect(self.x, self.y, CELLSIZE, CELLSIZE)
        self.highlighted = 0
        self.correct = False

    #Colours the cell block depending on options
    def drawCell(self, screen):
        options = {0:'white', 1:'gray68', 2:'gray79'}
        pygame.draw.rect(screen, pygame.Color(options.get(self.highlighted, 'white')), self.rect)
    
    #Changes the displayed number and value of the number in a Cell
    #Changes Colour of Cell
    def drawNum(self, number=-1):
        if number > 0:
            self.number = str(number)
        if self.correct:
                cellSurf = BASICFONT.render(str(self.number), True, (153,50,204))
                self.fluid = False
        elif self.fluid:
            cellSurf = BASICFONT.render(str(self.number), True, (255, 0, 0))
        else:
            cellSurf = BASICFONT.render(str(self.number), True, (0,0,0))
        screen.blit(cellSurf, (self.x+(CELLSIZE/3),self.y+(CELLSIZE/4)))

    def setHighlighted(self, highlighted):
        self.highlighted = highlighted

class Buttons:
    def __init__(self, x, y):
        self.name = "button"
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, int(WINDOWHEIGHT*0.70), BUTTONWIDTH, BUTTONHEIGHT)
   
    #Draw the visual button
    def drawbutton(self, screen):
        pygame.draw.rect(screen, pygame.Color('green'), self.rect)

#Drwa all cells and numbers
def drawCells():
    for x in range(NUMOFCELLS):
        for y in range(NUMOFCELLS):
            cells[x,y].drawCell(screen)
            cells[x,y].drawNum()

#Draws 3 spaced button            
def drawButtons():
    y = 0
    for x in range(int((GRIDWIDTH/3 - BUTTONWIDTH)/2), GRIDWIDTH, int(GRIDWIDTH/3)):
        buttons[x,y].drawbutton(screen)

#Occurs when a position on window is clicked
def clicked(pos):
    #Things that occur if gid is clicked
    if pos[1]>0 and pos[1]<GRIDHEIGHT:
        for x in range(NUMOFCELLS):
            for y in range(NUMOFCELLS):
                if cells[x,y].rect.collidepoint(pos):
                    cells[x,y].setHighlighted(1)
                    num = cells[x,y].number
                else:
                    cells[x,y].setHighlighted(0)
        
        for x in range(NUMOFCELLS):
            for y in range(NUMOFCELLS):
                if cells[x,y].number == num and not cells[x,y].highlighted and num != '':
                    cells[x,y].setHighlighted(2)

    #Things that occur if s button is clicked
    for x in range(int((GRIDWIDTH/3 - BUTTONWIDTH)/2), GRIDWIDTH, int(GRIDWIDTH/3)):
        y = 0
        if buttons[x,y].rect.collidepoint(pos):
            print("clicked")
            if x == 10:
                solveBoard(exampleBoard)
                if solveBoard:
                    for x in range(NUMOFCELLS):
                        for y in range(NUMOFCELLS):
                            inputCheck(x, y, int(cells[x,y].number))




#Checks if a number can be changed and cheanges it
def changeNum(n):
    for x in range(NUMOFCELLS):
        for y in range(NUMOFCELLS):
            if cells[x,y].highlighted == 1 and cells[x,y].fluid:
                cells[x,y].drawNum(n)
                inputCheck(x, y, n)

#Checks if a number input is correct and highlights accordingly
def inputCheck(x, y, n):
    if correctBoard[int(y)][int(x)] == n:
        cells[x,y].correct = True
        print('correct')
    else:
        print('incorrect')

#Recursive backtracking algorithm
def solveBoard(board):
    find = findSpaces(board)
    if not find:
        return True
    else:
        x,y = find

    for i in range(1,10):
        if valid(board, i, x, y):
            cells[x,y].drawNum(i)

            if solveBoard(board):
                return True
            
            #This may need to be else:
            cells[x,y].number = ''
            cells[x,y].drawNum()
    
        
    
    return False


#Find enpty fluid spaces
def findSpaces(board):
    for x in range(NUMOFCELLS):
        for y in range(NUMOFCELLS):
            if cells[x,y].number == '':
                return (x,y)
    return None

#Checks if a number input is valid
def valid(board, num, x, y):
    #Checks rows and columns
    for i in range(9):
        if cells[x,i].number == str(num) and y != i:
            print("invalid")
            return False

    for i in range(9):
        if cells[i,y].number == str(num) and x != i:
            print("invalid")
            return False

    #Checks 3x3 boxes
    box_x = x // 3
    box_y = y // 3

    for i in range(box_x*3, box_x*3 + 3):
        for j in range(box_y*3, box_y*3 + 3):
            if cells[i,j].number == str(num) and (i,j) != (x,y):
                return False


    return True



main()
