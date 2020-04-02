import pygame, sys, random
import math
import py2exe

pygame.init()

size = 544, 608
running = True
purple = (255, 255, 255)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

class SpriteSheet:
    def __init__(self, image):
        self.image = image

    def get_rect(self, rect):
        return self.image.subsurface(rect)


def scaleByFactor(image, factor):
    size = image.get_size()
    return pygame.transform.scale(image, (int(size[0]*factor), int(size[1]*factor)))

# Icon
icon = pygame.image.load("data/icon.png")
pygame.display.set_icon(icon)
# Sprite Sheets
buttonSpriteSheet = pygame.image.load("data/Button-Sheet.png")
buttonSpriteSheet = buttonSpriteSheet.convert_alpha()
colorTileSprites = pygame.image.load('data/ColorTileSheet.png')
winTextSpriteSheet = pygame.image.load('data/WinTextSheet.png')
winTextSprites = SpriteSheet(winTextSpriteSheet)
tileSprites = SpriteSheet(colorTileSprites)
buttonSprites = SpriteSheet(buttonSpriteSheet)
# Background Images
pygame.display.set_caption("Flood-It")
menu = pygame.image.load("data/MenuScreen1.png")
optionMenuBackgroundIm = pygame.image.load('data/OptionMenu.png')
lose = pygame.image.load("data/LoseScreen.png")
boardBackground = pygame.image.load("data/BoardBackground.png")
# Menu Button Sprites
menu_released = buttonSprites.get_rect(pygame.rect.Rect(0, 0, 100, 33))
menu_pressed = buttonSprites.get_rect(pygame.rect.Rect(101, 0, 100, 33))
# Retry Button Sprites
retry_released = buttonSprites.get_rect(pygame.rect.Rect(0, 99, 100, 33))
retry_pressed = buttonSprites.get_rect(pygame.rect.Rect(101, 99, 100, 33))
# Start Button Sprites
start_released = buttonSprites.get_rect(pygame.rect.Rect(0, 66, 100, 33))
start_released = scaleByFactor(start_released, 1.5)
start_pressed = buttonSprites.get_rect(pygame.rect.Rect(101, 66, 100, 33))
start_pressed = scaleByFactor(start_pressed, 1.5)
# Option Button Sprites
option_released = buttonSprites.get_rect(pygame.rect.Rect(0, 33, 100, 33))
option_released = scaleByFactor(option_released, 1.5)
option_pressed =  buttonSprites.get_rect(pygame.rect.Rect(101, 33, 100, 33))
option_pressed = scaleByFactor(option_pressed, 1.5)
colorselectionim = pygame.image.load('data/ColorSelection.png')
# SplashScreens / WinScreen
grayOver = pygame.image.load('data/GrayOver.png')
grayOver = grayOver.convert()
grayOver.set_alpha(200)
winText = pygame.image.load('data/WinText.png')
winText = winText.convert_alpha()
winText = scaleByFactor(winText, 1.5)
winTextImages = []
winTextIndex = 0
for i in range(6):
    winTextImages.append(scaleByFactor(winTextSprites.get_rect(pygame.Rect(0, i*60, 300, 60)), 1.5))

# ---------------------
currentScreenIndex = 0
tileRow = 0
won = False
# Prepare game objects
allSprites = pygame.sprite.Group()
menuSprites = pygame.sprite.Group()
loseSprites = pygame.sprite.Group()
optionsSprites = pygame.sprite.Group()
winSprites = pygame.sprite.Group()
spriteCollections = [menuSprites, allSprites, loseSprites, winSprites, optionsSprites]
tileColorPallets = []
for i in range(3):
    tileColorPallets.append((tileSprites.get_rect(pygame.Rect(0, i*32, 32*6, 32)), (tileSprites.get_rect(pygame.Rect(32*6, i*32, 32*6, 32)))))


class Board:
    def __init__(self, w, h):
        self.size = w, h
        self.w = w
        self.h = h
        self.brickList = []
        self.loseList = []
        self.winList = []
        self.scorefont = pygame.font.Font('freesansbold.ttf', 18)
        self.scoreText = self.scorefont.render("test", True, (0, 0, 0))
        self.reset()

    def get_Neighbors(self, r, c):
        neighborlist = []
        if c > 0:  # Check for left brick
            neighborlist.append(self.brickList[(r * self.w) + c - 1])
        else:
            neighborlist.append(None)
        if c < self.w - 1:  # Check for right brick
            neighborlist.append(self.brickList[(r * self.w) + c + 1])
        else:
            neighborlist.append(None)
        if r > 0:  # Check for up brick
            neighborlist.append(self.brickList[((r - 1) * self.w) + c])
        else:
            neighborlist.append(None)
        if r < self.h - 1:  # Check for down brick
            neighborlist.append(self.brickList[((r + 1) * self.w) + c])
        else:
            neighborlist.append(None)
        return neighborlist

    def showScore(self):
        self.scoreText = self.scorefont.render("Tries Remaining: " + str(self.tries), True, (0, 0, 0))
        score_rect = self.scoreText.get_rect()
        score_rect.topleft = (32, (myBoard.h + 1) * 32 +10)
        screen.blit(self.scoreText, score_rect)

    def reset(self):
        global allSprites
        for s in allSprites:
            if isinstance(s, ColorTile):
                s.kill()
        self.tries = 30
        self.brickList = []
        simageList = []
        print("Tile row: " + str(tileRow))
        for i in range(6):
            simageList.append(tileSprites.get_rect(pygame.Rect(i*32, tileRow*32, 32, 32)))
        for i in range(self.w):
            for j in range(self.h):
                randomcolor = simageList[random.randrange(0, len(simageList))]
                self.brickList.append(ColorTile(randomcolor, i, j))
        for brick in self.brickList:
            allSprites.add(brick)

    def checkForWin(self):
        brickwincount = 0
        for brick in myBoard.brickList:
            if brick.image is myBoard.brickList[0].image:
                brickwincount += 1
                if brickwincount == len(myBoard.brickList):
                    return True
        return False

class ButtonSprite(pygame.sprite.Sprite):
    def __init__(self, image, pressedim, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.releasedim = image
        self.pressedim = pressedim
        self.currentim = self.image
        self.rect = self.currentim.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.isPressed = False

    def action(self):
        print("Default action is to say Hello World")

    def press(self):
        self.image = self.pressedim
        self.isPressed = True


    def release(self):
        self.image = self.releasedim
        self.isPressed = False

    def setLocation(self, absx, absy):
        self.x = absx
        self.y = absy
        self.rect.y = self.y
        self.rect.x = self.x


class ColorTile(ButtonSprite):

    def __init__(self, color, r, c):
        ButtonSprite.__init__(self, color, color, r, c)
        self.image = color
        self.lastimage = color
        self.rect = color.get_rect()
        self.r = r
        self.c = c
        self.rect.x = (r + 1) * 32
        self.rect.y = (c + 1) * 32
        self.leftNeighbor = None
        self.rightNeighbor = None
        self.upNeighbor = None
        self.downNeighbor = None

    def change_color(self, color, board):
        self.image = color
        self.get_neighbors(board)

    def action(self, color, board):
        self.change_color(color, board)

    def fill_color(self, color):
        self.image = color

    def get_neighbors(self, board):
        neighbors = board.get_Neighbors(self.r, self.c)
        self.upNeighbor = neighbors[0]
        self.downNeighbor = neighbors[1]
        self.leftNeighbor = neighbors[2]
        self.rightNeighbor = neighbors[3]
        if self.image == self.lastimage:
            return
        if self.rightNeighbor is not None:
            if self.rightNeighbor.image is self.lastimage:
                self.rightNeighbor.change_color(self.image, myBoard)
        if self.leftNeighbor is not None:
            if self.leftNeighbor.image is self.lastimage:
                self.leftNeighbor.change_color(self.image, myBoard)
        if self.upNeighbor is not None:
            if self.upNeighbor.image is self.lastimage:
                self.upNeighbor.change_color(self.image, myBoard)
        if self.downNeighbor is not None:
            if self.downNeighbor.image is self.lastimage:
                self.downNeighbor.change_color(self.image, myBoard)
        self.lastimage = self.image

    def press(self):
        pass

    def release(self):
        pass


class ChangeSceneButton(ButtonSprite):
    def __init__(self, image, pressedim, x, y, scenenum):
        ButtonSprite.__init__(self, image, pressedim, x, y)
        self.scenenum = scenenum

    def action(self):
        pygame.mixer_music.load("data/Audio/ButtonSound.mp3")
        pygame.mixer_music.play(0)
        global currentScreenIndex
        global won
        global currentSC
        won = False
        currentScreenIndex = self.scenenum
        currentSC = spriteCollections[currentScreenIndex]
        currentSC.draw(screen)
        myBoard.reset()


class BackgroundSprite(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0

    def setLocation(self, absx, absy):
        self.x = absx
        self.y = absy
        self.rect.y = self.y
        self.rect.x = self.x


class ColorSelectionButton(ButtonSprite):

    def __init__(self, image, pressedim, x, y, index):
        ButtonSprite.__init__(self, image, pressedim, x, y)
        self.index = index

    def action(self):
        global tileRow
        tileRow = self.index


class ButtonGroup:
    def __init__(self, buttonlist):
        self.buttonlist = []
        self.selected = 0
        for button in buttonlist:
            self.buttonlist.append(button)

    def append(self, button):
        self.buttonlist.append(button)

    def appendList(self, buttonList):
        for button in buttonList:
            self.buttonlist.append(button)

    def activate(self, button):
        self.selected = self.buttonlist.index(button)


myBoard = Board(15, 15)
# Main Menu
menuBackground = BackgroundSprite(menu)
startButton = ChangeSceneButton(start_released, start_pressed, 12*32, (1*32), 1)
optionButton = ChangeSceneButton(option_released, option_pressed, 12*32, 3*32, 4)
menuSprites.add(menuBackground)
menuSprites.add(startButton)
menuSprites.add(optionButton)
# lose Screen Sprites
loseBackground = BackgroundSprite(lose)
retryButton = ChangeSceneButton(retry_released, retry_pressed, 13*32, 1*32, 1)
mainMenuButton = ChangeSceneButton(menu_released, menu_pressed, 13*32, 2*32, 0)
loseSprites.add(loseBackground)
loseSprites.add(retryButton)
loseSprites.add(mainMenuButton)
# Options Menu
i = 1
optionBackground = BackgroundSprite(optionMenuBackgroundIm)
optionColorSelection = BackgroundSprite(colorselectionim)
optionColorSelection.setLocation(13, 48)
optionsSprites.add(optionBackground)
optionsSprites.add(mainMenuButton)
for i, val in enumerate(tileColorPallets):
    option_space = 50 + (i * 5)
    optionsSprites.add(ColorSelectionButton(val[0], val[1], 15, option_space + i*32, i))
optionsSprites.add(optionColorSelection)
# Game Screen Sprites
allSprites.add(BackgroundSprite(boardBackground))
allSprites.add(ChangeSceneButton(retry_released, retry_pressed, 1*32, 17*32, 1))
allSprites.add(ChangeSceneButton(menu_released, menu_pressed, 13*32, 17*32, 0))
# Win Screen Sprites
grayBackground = BackgroundSprite(grayOver)
grayBackground.setLocation(32, 32)
winSprites.add(grayBackground)
winTextSprite = BackgroundSprite(winText)
winTextSprite.setLocation(screen.get_size()[0]/2 - winTextSprite.rect.w/2, 64)
winSprites.add(winTextSprite)
winMenu = ChangeSceneButton(scaleByFactor(menu_released, 1.5), scaleByFactor(menu_pressed, 1.5), 0, 14*32, 0)
winMenu.setLocation((screen.get_size()[0]/2) - 68, winMenu.y)
print("Your X: ", str(winMenu.rect[0]/2))


def indexTextAnimation():
    global winTextIndex
    winTextIndex +=1
    if winTextIndex > 5:
        winTextIndex = 0
    winTextSprite.image = winTextImages[winTextIndex]

winSprites.add(winMenu)
while running:
    clock.tick(12)
    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        currentSC = spriteCollections[currentScreenIndex]
        screen.fill(purple)
        currentSC.draw(screen)
        pos = pygame.mouse.get_pos()
        # Check if the mouse is over the sprite
        for s in currentSC:
            if s.rect.collidepoint(pos):
                if isinstance(s, ButtonSprite):
                    if not s.isPressed:
                        s.press()
            else:
                if isinstance(s, ButtonSprite):
                    s.release()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for s in currentSC:
                if s.rect.collidepoint(pos):
                    if isinstance(s, ColorTile):
                        if s.image is not myBoard.brickList[0].image:
                            myBoard.brickList[0].action(s.image, myBoard)
                            myBoard.tries -= 1
                            if myBoard.checkForWin():
                                won = True
                                pygame.mixer_music.load('data/Audio/YouWin.mp3')
                                pygame.mixer_music.play(0)
                            if myBoard.tries <= 0:
                                currentScreenIndex = 2
                                pygame.mixer_music.load('data/Audio/YouLose.xm')
                                pygame.mixer_music.play(0)
                    elif isinstance(s, ColorSelectionButton):
                        print("color selection")
                        s.action()
                        optionColorSelection.setLocation(13, 48 + (tileRow * 5) + tileRow * 32)
                    elif isinstance(s, ButtonSprite):
                        s.action()
        if won:
            currentSC = winSprites
            currentScreenIndex = 3
            winSprites.draw(screen)

    if won:
        indexTextAnimation()
    currentSC.draw(screen)
    if currentScreenIndex == 1:
        myBoard.showScore()
    pygame.display.update()



