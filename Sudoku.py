import pygame, sys
import time

pygame.init()

width = 270
height = width + 230
cells = {}

FPS = 20
FPSCLOCK = pygame.time.Clock()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Sudoko')
screen.fill(pygame.Color("white"))

BASICFONTSIZE = 25
BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

pygame.display.flip()

def main():

    defCells()


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    clicked(pos)
            if event.type == pygame.KEYDOWN:
                numbers = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
                if event.key in numbers:
                    x = numbers.index(event.key)
                    changeNum(x)

        drawCells()
        drawGrid()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    pygame.quit()
    sys.exit()


WINDOWHEIGHT = width
WINDOWWIDTH = width
SQUARESIZE = int(width/3)
CELLSIZE = int(width/9)
NUMBERSIZE = int(CELLSIZE/3)
WINDOWSIZE = 81


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):
        pygame.draw.line(screen, pygame.Color("gray"), (x,0), (x,WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):
        pygame.draw.line(screen, pygame.Color("gray"), (0,y), (WINDOWWIDTH,y))
    
    
    for x in range(0, WINDOWWIDTH + SQUARESIZE, SQUARESIZE):
        pygame.draw.line(screen, pygame.Color("black"), (x,0), (x,WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT + SQUARESIZE, SQUARESIZE):
        pygame.draw.line(screen, pygame.Color("black"), (0,y), (WINDOWWIDTH,y))


def defCells():
    for x in range(0, WINDOWWIDTH, CELLSIZE):
        for y in range(0, WINDOWWIDTH, CELLSIZE):
            cells[x,y] = CellBlock(x, y, CELLSIZE,'', False)
            
            


class CellBlock:
    def __init__(self,x, y, CELLSIZE, number='', fluid=False):
        self.number = number
        self.fluid = fluid
        self.rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        self.x = x
        self.y = y
        self.highlighted = False

    def drawCell(self, screen):
        if self.highlighted:
            pygame.draw.rect(screen, pygame.Color('gray'), self.rect)
        else:
            pygame.draw.rect(screen, pygame.Color('white'), self.rect)

    def drawNum(self, number = -1):
        if number > 0 & self.fluid:
            self.number = number
        cellSurf = BASICFONT.render(str(self.number), False, (0, 0, 0))
        screen.blit(cellSurf, (self.x+10,self.y+5))

    def setHighlighted(self, highlighted):
        self.highlighted = highlighted
        

        

def drawCells():
    for x in range(0, WINDOWWIDTH, CELLSIZE):
        for y in range(0, WINDOWWIDTH, CELLSIZE):
            cells[x,y].drawCell(screen)
            cells[x,y].drawNum()
            


def clicked(pos):
    for x in range(0, WINDOWWIDTH, CELLSIZE):
        for y in range(0, WINDOWWIDTH, CELLSIZE):
            cells[x,y].setHighlighted(cells[x,y].rect.collidepoint(pos))


def changeNum(n):
    for x in range(0, WINDOWWIDTH, CELLSIZE):
        for y in range(0, WINDOWWIDTH, CELLSIZE):
            if cells[x,y].highlighted:
                cells[x,y].drawNum(n)
                
    


main()
