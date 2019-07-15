import pygame
import random
from enum import Enum

from pinaps.piNapsController import PiNapsController
from pinaps.blinoParser import BlinoParser

class MindWrestle:
    def __init__(self, cbkPlayerOneValues, cbkPlayerTwoValues):
        self.state = GameState.Unconnected
        self.globalTick = 0
        self.clock = pygame.time.Clock()
        self.tugSpeed = 5
        self.cbkPlayerOneValues = cbkPlayerOneValues
        self.cbkPlayerTwoValues = cbkPlayerTwoValues
        self.isRunning = True
        self.connectionCounter = 0
        self.countdown = 0
        self.isExplosion = False
        self.idxBackground = random.randint(0,5)
        self.tmrExplosion = 0
        self.winner = 0

        #load and set the logo#
        self.logo = pygame.image.load("resources/Blino_Logo.png")
        pygame.display.set_icon(self.logo)
        pygame.display.set_caption("Blino - Mind Wrestle")

        #Create a surface on screen that has the size of 240 x 180#
        self.displayInfo = pygame.display.Info()
        self.screen_width = self.displayInfo.current_w
        self.screen_height = self.displayInfo.current_h
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        #Static Positions#
        #@ToDo - Need to calculate form screen size#
        self.posBrainOne = [20,self.screen_height/2]
        self.posBadgeOne = [20,self.screen_height/2 + 120]
        self.posBrainTwo = [self.screen_width-120,self.screen_height/2]
        self.posBadgeTwo = [self.screen_width-180,self.screen_height/2+120]
        self.posConnectionOne = [0,0]
        self.posConnectionTwo = [0,0]
        self.posStartingPlasma = [(self.posBrainTwo[0] - self.posBrainOne[0])/2, self.screen_height/2 + 30]
        self.posBeamBlue = [self.posStartingPlasma[0] + 100,self.posStartingPlasma[1]+30]
        self.posBeamRed = [self.posBrainOne[0]+120,self.posStartingPlasma[1]+30]
        self.posMenu = [self.screen_width/2-400,self.screen_height/2-256]
        self.posPlayer = [self.posMenu[0] + 320, self.posMenu[1] + 350]

        #Plasma Sprite Setup#
        self.imgPlasma = []
        self.imgPlasma.append(pygame.image.load('resources/plasma/plasma00.png'))
        self.imgPlasma.append(pygame.image.load('resources/plasma/plasma01.png'))
        self.imgPlasma.append(pygame.image.load('resources/plasma/plasma02.png'))
        self.imgPlasma.append(pygame.image.load('resources/plasma/plasma03.png'))
        self.imgPlasma.append(pygame.image.load('resources/plasma/plasma04.png'))
        self.imgPlasma.append(pygame.image.load('resources/plasma/plasma05.png'))
        self.imgPlasma.append(pygame.image.load('resources/plasma/plasma06.png'))
        self.imgPlasma.append(pygame.image.load('resources/plasma/plasma07.png'))
        self.imgPlasma.append(pygame.image.load('resources/plasma/plasma08.png'))
        self.imgPlasma.append(pygame.image.load('resources/plasma/plasma09.png'))
        self.imgPlasma.append(pygame.image.load('resources/plasma/plasma10.png'))
        self.imgPlasma.append(pygame.image.load('resources/plasma/plasma11.png'))
        self.imgPlasma = [pygame.transform.flip(x, True, False) for x in self.imgPlasma]; self.imgPlasma
        self.sptPlasma = AnimatedObject(15, self.imgPlasma)
        self.sptPlasma.setImageSize([128,128])
        self.sptPlasma.setImagePos(self.posStartingPlasma)

        #Brain One#
        self.imgBrainOne = []
        self.imgBrainOne.append(pygame.image.load('resources/brainboi/brainboi0.png'))
        self.imgBrainOne.append(pygame.image.load('resources/brainboi/brainboi1.png'))
        #...#
        self.imgBrainOne = [pygame.transform.flip(x, True, False) for x in self.imgBrainOne]; self.imgBrainOne
        self.sptBrainOne = AnimatedObject(25, self.imgBrainOne)
        self.sptBrainOne.setImageSize([128,128])
        self.sptBrainOne.setImagePos(self.posBrainOne)
        #self.sptBrainOne = pygame.transform.flip(self.sptBrainOne, False, True)
        #self.grpGame.add(self.sptBrainOne)

        #Brain Two#
        self.imgBrainTwo = []
        self.imgBrainTwo.append(pygame.image.load('resources/brainboi/brainboi0.png'))
        self.imgBrainTwo.append(pygame.image.load('resources/brainboi/brainboi1.png'))
        #...#
        self.sptBrainTwo = AnimatedObject(25, self.imgBrainTwo)
        self.sptBrainTwo.setImageSize([128,128])
        self.sptBrainTwo.setImagePos(self.posBrainTwo)

        #Beam One#
        self.imgBeamBlue = []
        self.imgBeamBlue.append(pygame.image.load('resources/bluebeam/bluebeam0.png'))
        self.imgBeamBlue.append(pygame.image.load('resources/bluebeam/bluebeam1.png'))
        self.imgBeamBlue.append(pygame.image.load('resources/bluebeam/bluebeam2.png'))
        self.imgBeamBlue.append(pygame.image.load('resources/bluebeam/bluebeam3.png'))
        self.imgBeamBlue.append(pygame.image.load('resources/bluebeam/bluebeam4.png'))
        #...#
        self.sptBeamBlue = AnimatedObject(5, self.imgBeamBlue)
        self.sptBeamBlue.setImageSize([((self.screen_width/2) - 160)*2,64])
        self.sptBeamBlue.setImagePos(self.posBeamBlue)
        self.sptBeamBlue.convertAlpha()

        #Beam Two#
        self.imgBeamRed = []
        self.imgBeamRed.append(pygame.image.load('resources/redbeam/redbeam0.png'))
        self.imgBeamRed.append(pygame.image.load('resources/redbeam/redbeam1.png'))
        self.imgBeamRed.append(pygame.image.load('resources/redbeam/redbeam2.png'))
        self.imgBeamRed.append(pygame.image.load('resources/redbeam/redbeam3.png'))
        self.imgBeamRed.append(pygame.image.load('resources/redbeam/redbeam4.png'))
        self.imgBeamRed.append(pygame.image.load('resources/redbeam/redbeam5.png'))
        self.imgBeamRed.append(pygame.image.load('resources/redbeam/redbeam6.png'))
        self.imgBeamRed.append(pygame.image.load('resources/redbeam/redbeam7.png'))
        #...#
        self.sptBeamRed = AnimatedObject(2, self.imgBeamRed)
        self.sptBeamRed.setImageSize([(self.screen_width/2 - 160)*2,64])
        self.sptBeamRed.setImagePos(self.posBeamRed)
        self.sptBeamRed.convertAlpha()

        #Player One Badge#
        self.imgBadge = []
        self.imgBadge.append(pygame.image.load('resources/badge/player1badge.png'))
        self.imgBadge.append(pygame.image.load('resources/badge/player2badge.png'))
        self.sptBadgeOne = AnimatedObject(50, self.imgBadge)
        self.sptBadgeOne.setSpecialImages(self.imgBadge)
        self.sptBadgeOne.runSpecial(0)
        self.sptBadgeOne.setImageSize([160,100])
        self.sptBadgeOne.setImagePos(self.posBadgeOne)

        #Player Two Badge#
        self.sptBadgeTwo = AnimatedObject(50, self.imgBadge)
        self.sptBadgeTwo.setSpecialImages(self.imgBadge)
        self.sptBadgeTwo.runSpecial(1)
        self.sptBadgeTwo.setImageSize([160,100])
        self.sptBadgeTwo.setImagePos(self.posBadgeTwo)

        #Add sprites to group in order#
        self.grpGame = pygame.sprite.OrderedUpdates(self.sptBeamBlue)
        self.grpGame.add(self.sptBeamRed)
        self.grpGame.add(self.sptBrainOne)
        self.grpGame.add(self.sptBrainTwo)
        self.grpGame.add(self.sptPlasma)
        self.grpGame.add(self.sptBadgeOne)
        self.grpGame.add(self.sptBadgeTwo)

        #Menu#
        self.imgMenu = []
        self.imgMenu.append(pygame.image.load('resources/popups/menu_bothpoor.png'))
        self.imgMenu.append(pygame.image.load('resources/popups/menu_p1good.png'))
        self.imgMenu.append(pygame.image.load('resources/popups/menu_p2good.png'))
        self.imgMenu.append(pygame.image.load('resources/popups/menu_bothgood.png'))
        self.sptMenu = AnimatedObject(0, self.imgMenu)
        self.sptMenu.setSpecialImages(self.imgMenu)
        self.sptMenu.runSpecial(0)
        self.sptMenu.setImageSize([800,512])
        self.sptMenu.setImagePos(self.posMenu)

        self.grpMenu = pygame.sprite.OrderedUpdates(self.sptMenu)

        #Countdown#
        self.imgCountdown = []
        self.imgCountdown.append(pygame.image.load('resources/popups/starting1.png'))
        self.imgCountdown.append(pygame.image.load('resources/popups/starting2.png'))
        self.imgCountdown.append(pygame.image.load('resources/popups/starting3.png'))
        self.sptCountdown = AnimatedObject(1, self.imgCountdown)
        self.sptCountdown.setSpecialImages(self.imgCountdown)
        self.sptCountdown.setImageSize([800,512])
        self.sptCountdown.setImagePos(self.posMenu)

        self.grpCountdown = pygame.sprite.OrderedUpdates(self.sptCountdown)

        #Winner#
        self.imgWinner = []
        self.imgWinner.append(pygame.image.load('resources/popups/win1.png'))
        self.imgWinner.append(pygame.image.load('resources/popups/win2.png'))
        self.sptWinner = AnimatedObject(5, self.imgWinner)
        self.sptWinner.setSpecialImages(self.imgWinner)
        self.sptWinner.setImageSize([800,512])
        self.sptWinner.setImagePos(self.posMenu)

        #Player#
        self.imgPlayer = []
        self.imgPlayer.append(pygame.image.load('resources/badge/player1badge.png'))
        self.imgPlayer.append(pygame.image.load('resources/badge/player2badge.png'))
        self.sptPlayer = AnimatedObject(1, self.imgPlayer)
        self.sptPlayer.setSpecialImages(self.imgPlayer)
        self.sptPlayer.setImageSize([160,100])
        self.sptPlayer.setImagePos(self.posPlayer)

        self.grpWinner = pygame.sprite.OrderedUpdates(self.sptWinner)
        self.grpWinner.add(self.sptPlayer)

        #Explosion#
        self.imgExplosion = []
        self.imgExplosion.append(pygame.image.load('resources/boom/boom1.png'))
        self.imgExplosion.append(pygame.image.load('resources/boom/boom2.png'))
        self.imgExplosion.append(pygame.image.load('resources/boom/boom3.png'))
        self.imgExplosion.append(pygame.image.load('resources/boom/boom4.png'))
        self.imgExplosion.append(pygame.image.load('resources/boom/boom5.png'))
        self.imgExplosion.append(pygame.image.load('resources/boom/boom6.png'))
        self.sptExplosion = AnimatedObject(3, self.imgExplosion)
        #self.sptExplosion.setImageSize([800,512])
        #self.sptExplosion.setImagePos(self.posMenu)
        self.sptExplosion.setImageSize([self.screen_width, self.screen_height])
        self.sptExplosion.setImagePos([0,0])
        self.sptExplosion.convertAlpha()

        self.grpExplosion = pygame.sprite.OrderedUpdates(self.sptExplosion)

        #Set the alpha value to 128 (0 fully transparent, 255 opaque)#
        #image.set_alpha(128)
        #imgBackgrounds = []
        #imgBackgrounds.append(pygame.image.load("resources/background.png").convert_alpha())
        #sptBackground = AnimatedObject(1, imgBackgrounds)
        #sptBackground.imageSize([screen_width, screen_height])
        #Instead of blitting the background image you could fill it 
        #(uncomment the next line to do so)
        #screen.fill((255,0,0))
        #group = pygame.sprite.Group([sptBackground, sptPlasma])
        #self.imgBackground = pygame.image.load("resources/scenes/Beach.jpg")
        #self.imgBackground = pygame.transform.scale(self.imgBackground, [self.screen_width, self.screen_height])
        #self.imgBackground = self.imgBackground.convert_alpha()

        self.imageBackground = []
        self.imageBackground.append(pygame.image.load('resources/scenes/Beach.jpg'))
        self.imageBackground.append(pygame.image.load('resources/scenes/city.jpg'))
        self.imageBackground.append(pygame.image.load('resources/scenes/Forest.jpg'))
        self.imageBackground.append(pygame.image.load('resources/scenes/industrial.jpg'))
        self.imageBackground.append(pygame.image.load('resources/scenes/Mountains.jpg'))
        self.imageBackground.append(pygame.image.load('resources/scenes/Space.jpg'))
        self.sptBackground = AnimatedObject(1, self.imageBackground, self.imageBackground)
        self.sptBackground.setImageSize([self.screen_width, self.screen_height])
        self.sptBackground.setImagePos([0,0])
        self.sptBackground.convertAlpha()
        self.sptBackground.runSpecial(2)

        self.grpBackground = pygame.sprite.OrderedUpdates(self.sptBackground)


        #Pinaps#
        self.pinapsOne = PiNapsController()
        self.pinapsTwo = PiNapsController(0x98)
    
        self.pinapsOne.setControlInterfaceI2C()
        self.pinapsOne.setEEGSensorInterfaceI2C()
        self.pinapsOne.setBasicMode()

        self.pinapsTwo.setControlInterfaceI2C()
        self.pinapsTwo.setEEGSensorInterfaceI2C()
        self.pinapsTwo.setBasicMode()

        self.blinoParserOne = BlinoParser()
        self.blinoParserOne.qualityCallback = self.onQualityValueOne
        self.blinoParserOne.attentionCallback = self.onAttention
        self.blinoParserOne.meditationCallback = self.onMedititation
        self.blinoParserOne.eegPowersCallback = self.onEEGPowerReceived

        self.blinoParserTwo = BlinoParser()
        self.blinoParserTwo.qualityCallback = self.onQualityValueTwo
        self.blinoParserTwo.attentionCallback = self.onAttention
        self.blinoParserTwo.meditationCallback = self.onMedititation
        self.blinoParserTwo.eegPowersCallback = self.onEEGPowerReceived

        self.pinapsOne.deactivateAllLEDs() 

    def mainLoop(self):
        print("Main loop")
        while(self.isRunning):
            sctGameState = {
                GameState.Unconnected: self.unconnected,
                GameState.Begin: self.begin,
                GameState.InProgress: self.inProgress,
                GameState.End: self.end
            }
            currentGameState = sctGameState.get(self.state, lambda: "Invalid State")
            currentGameState()


    def unconnected(self):
        print "Displays Unconnected"

        self.screen.fill(BLACK)

        #Read EEG#
        while(self.pinapsOne.dataWaiting()):
            try:
                data = self.pinapsOne.readEEGSensor()
                self.blinoParserOne.parseByte(data)
            except:
                print("Parse error")
        while(self.pinapsTwo.dataWaiting()):
            try:
                data = self.pinapsTwo.readEEGSensor()
                self.blinoParserTwo.parseByte(data)
            except:
                print("Parse error")

        staMenu = 0
        if(self.blinoParserOne.quality < 25):
            staMenu += 1
        if(self.blinoParserTwo.quality < 25):
            staMenu += 2
        
        self.sptMenu.runSpecial(staMenu)

        self.grpMenu.draw(self.screen)
        self.grpMenu.update(self.globalTick)
        
        #And update the screen (dont forget that!)#
        pygame.display.flip()
        
        #This will slow it down to 10 fps, so you can watch it,#
        #Otherwise it would run too fast#
        self.clock.tick(1)
        self.globalTick = self.globalTick + 1  

        if(staMenu == 3):
            self.connectionCounter += 1
        else:
            self.connectionCounter = 0
        if(self.connectionCounter == 5):
            self.state = GameState.Begin
            self.countdown = 2
            self.connectionCounter = 0
    def begin(self):
        print "Displays countdown until begin"

        self.screen.fill(BLACK)

        #Read EEG#
        while(self.pinapsOne.dataWaiting()):
            try:
                data = self.pinapsOne.readEEGSensor()
                self.blinoParserOne.parseByte(data)
            except:
                print("Parse error")
        while(self.pinapsTwo.dataWaiting()):
            try:
                data = self.pinapsTwo.readEEGSensor()
                self.blinoParserTwo.parseByte(data)
            except:
                print("Parse error")

        self.sptCountdown.runSpecial(self.countdown)

        if(self.globalTick % 10):
            self.countdown -= 1

        self.grpCountdown.update(self.globalTick)
        self.grpCountdown.draw(self.screen)

        pygame.display.flip()

        self.clock.tick(1)
        self.globalTick = self.globalTick + 1

        if(self.countdown < 0):
            self.state = GameState.InProgress
            self.sptBackground.runSpecial(self.idxBackground)
    def inProgress(self):
        #self.screen.blit(self.imgBackground,(0,0))
        #print "Displays game in progress"
        #print("Player has won.")

        #Keyboard callbacks#
        for event in pygame.event.get():
            # only do something if the event if of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                self.isRunning = False
            # check for keypress and check if it was Esc
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.isRunning = False

        #Read EEG#
        while(self.pinapsOne.dataWaiting()):
            try:
                data = self.pinapsOne.readEEGSensor()
                self.blinoParserOne.parseByte(data)
            except:
                print("Parse error")
        while(self.pinapsTwo.dataWaiting()):
            try:
                data = self.pinapsTwo.readEEGSensor()
                self.blinoParserTwo.parseByte(data)
            except:
                print("Parse error")

        self.grpBackground.update(self.globalTick)
        self.grpBackground.draw(self.screen)

        self.grpGame.update(self.globalTick)
        self.grpGame.draw(self.screen)

        if(self.isExplosion == True):
            self.grpExplosion.update(self.globalTick)
            self.grpExplosion.draw(self.screen)
            self.tmrExplosion += 1
        else:
            if(self.blinoParserOne.quality > 25):
                self.state = GameState.Unconnected
            if(self.blinoParserTwo.quality > 25):
                self.state = GameState.Unconnected

            #Change plasma position#
            #@ToDo - Check moving in correct direction#
            posCurrentPlasma = self.sptPlasma.getImagePos()
            posCurrentPlasmaX = posCurrentPlasma[0]
            if(self.blinoParserOne.attention > self.blinoParserTwo.attention):
                posCurrentPlasmaX = (posCurrentPlasma[0] + self.tugSpeed) if (posCurrentPlasma[0] + self.tugSpeed < (self.screen_width - 240)) else posCurrentPlasma[0]
                self.isExplosion = False if posCurrentPlasma[0]+ self.tugSpeed < (self.screen_width - 240) else True
                self.winner = 0 if posCurrentPlasma[0]+ self.tugSpeed < (self.screen_width - 240) else 1
                #xpos = (xpos + step_x) if (xpos + step_x < (screen_width - 40)) else (xpos)
                #tugValue = tugValue + 10
            if(self.blinoParserOne.attention < self.blinoParserTwo.attention):
                posCurrentPlasmaX = (posCurrentPlasma[0] - self.tugSpeed) if (posCurrentPlasma[0] - self.tugSpeed > 120) else posCurrentPlasma[0]
                self.isExplosion = False if posCurrentPlasma[0]- self.tugSpeed > 120 else True
                self.winner = 0 if posCurrentPlasma[0]- self.tugSpeed > 120 else 2
                #xpos = (xpos - step_x) if (xpos - step_x > 0) else (xpos)
            self.sptPlasma.setImagePos([posCurrentPlasmaX, posCurrentPlasma[1]])
            cropRect = pygame.Rect(0,0,posCurrentPlasmaX-80,64)
            self.sptBeamRed.setClip(cropRect)
            self.sptBeamBlue.setImagePos([posCurrentPlasmaX+80, self.posBeamBlue[1]])
            cropRect = pygame.Rect(0,0,(((self.screen_width/2) - 120)*2) - posCurrentPlasmaX,64)
            self.sptBeamBlue.setClip(cropRect)

        #And update the screen (dont forget that!)#
        pygame.display.flip()
        
        #This will slow it down to 10 fps, so you can watch it,#
        #Otherwise it would run too fast#
        self.clock.tick(60)
        self.globalTick = self.globalTick + 1  

        if(self.tmrExplosion == 17):
            self.state = GameState.End
            self.idxBackground = random.randint(0,5)
            self.isExplosion = False
            self.tmrExplosion = 0
    def end(self):
        print "Displays game end"

        #Keyboard callbacks#
        for event in pygame.event.get():
            # only do something if the event if of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                self.isRunning = False
            # check for keypress and check if it was Esc
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.isRunning = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = GameState.Unconnected
                self.sptPlasma.setImagePos(self.posStartingPlasma)
                self.winner = 0

        #self.screen.fill(WHITE)

        if(self.winner == 1):
            print("Winner player 1")
            self.sptPlayer.runSpecial(0)
        if(self.winner == 2):
            print("Winner player 2")
            self.sptPlayer.runSpecial(1)

        self.grpWinner.update(self.globalTick)
        self.grpWinner.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(60)
        self.globalTick = self.globalTick + 1 

        #self.state = GameState.Unconnected

    def onQualityValueOne(self, quality):
        print("")
        print("Pinaps ONE")
        print("Quality value: %d" % quality)
        if quality > 10:
            self.pinapsOne.activateRedLED()
            self.pinapsOne.deactivateGreenLED()
            print ("RED");
        else:
            self.pinapsOne.deactivateRedLED()
            self.pinapsOne.activateGreenLED()
            print ("GREEN");

    def onQualityValueTwo(self, quality):
        print("")
        print("Pinaps TWO")
        print("Quality value: %d" % quality)
        if quality > 10:
            self.pinapsTwo.activateRedLED()
            self.pinapsTwo.deactivateGreenLED()
            print ("RED");
        else:
            self.pinapsTwo.deactivateRedLED()
            self.pinapsTwo.activateGreenLED()
            print ("GREEN");

    def onAttention(self, attention):
        print("Attention value: %d" % attention)

    def onMedititation(self, meditation):
        print("Meditation value: %d" % meditation)

    def onEEGPowerReceived(self, eegSignal):
        #print("Delta value: %d" % eegSignal.delta)
        #print("Theta value: %d" % eegSignal.theta)
        print("Low alpha value: %d" % eegSignal.lAlpha)
        print("High alpha value: %d" % eegSignal.hAlpha)
        #print("Low beta value: %d" % eegSignal.lBeta)
        #print("High beta value: %d" % eegSignal.hBeta)
        #print("Low Gamma value: %d" % eegSignal.lGamma)
        #print("Medium gamma value: %d" % eegSignal.mGamma)

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

class GameState(Enum):
    Unconnected = 1
    Begin = 2
    InProgress = 3
    End = 5

##def onQualityValue(quality):
##    print("Quality value: %d" % quality)
##    if quality > 10:
##        pinapsOne.activateRedLED()
##        pinapsOne.deactivateGreenLED()
##        print ("RED");
##    else:
##        pinapsOne.deactivateRedLED()
##        pinapsOne.activateGreenLED()
##        print ("GREEN");

#@ToDo - Need get piece of image using: pygame.transform.chop()#
class AnimatedObject(pygame.sprite.Sprite):
    def __init__(self, animationRate, animationImages, specialImages = []):
        super(AnimatedObject, self).__init__()

        self.animationIndex = 0
        self.animationRate = animationRate
        self.animationImages = animationImages
        self.image = self.animationImages[self.animationIndex]
        self.currentTick = 0
        self.rect = pygame.Rect(0, 0, 0, 0) #???

        self.specialIndex = -1
        self.isSpecial = False
        self.specialImages = specialImages

        self.rctArea = pygame.Rect(0,0,self.image.get_width(),self.image.get_height())
        #self.cropSurface = self.animationImages[0].subsurface(0,0,10,10)     
    
    def update(self, tick):
        '''This method iterates through the elements inside self.images and 
        displays the next one each tick. For a slower animation, you may want to 
        consider using a timer of some sort so it updates slower.'''

        if(self.isSpecial):
            self.image = self.specialImages[self.specialIndex]
        else:
            self.currentTick += 1
            if(self.currentTick >= self.animationRate):
                self.animationIndex += 1
                self.currentTick = 0
            if self.animationIndex >= len(self.animationImages):
                self.animationIndex = 0
            self.image = self.animationImages[self.animationIndex].subsurface(self.rctArea)


    def setImageSize(self, size):
        self.animationImages = [pygame.transform.scale(x, size) for x in self.animationImages]; self.animationImages
        self.specialImages = [pygame.transform.scale(x, size) for x in self.specialImages]; self.specialImages
        self.rctArea = pygame.Rect(0,0,self.animationImages[0].get_width(),self.animationImages[0].get_height())
        #self.rect = pygame.Rect(0, 0, size[0]/2, size[1]/2)

    def convertAlpha(self):
        self.animationImages = [x.convert_alpha() for x in self.animationImages]; self.animationImages
        self.specialImages = [x.convert_alpha() for x in self.specialImages]; self.specialImages

    def setClip(self, rect):
        #for x in self.animationImages:
        #    x.set_clip(pygame.Rect(0,0,10,10))
        #    self.animationImages[0] = x.get_clip
        #    x = x.get_clip()
        #for x in self.specialImages:
        #    x.set_clip(pygame.Rect(0,0,100,100))
        #self.specialImages = [.get_clip() for x in self.specialImages]; self.specialImages
        #self.modAnimationImages = [pygame.transform.chop(x, rect) for x in self.animationImages]; self.animationImages
        self.rctArea = rect  

    def setImagePos(self, pos):
        self.rect.center = pos

    def getImagePos(self):
        return self.rect.center

    def updateImagePos(self, pos):
        self.rect.center = [self.rect.center[0] + pos[0], self.rect.center[1] + pos[1]]

    def setSpecialImages(self, specialImages):
        self.specialImages = specialImages

    def runSpecial(self, idxSpecial):
        self.specialIndex = idxSpecial
        self.isSpecial = True
        
    def endSpecial(self):
        self.isSpecial = False


def main():    
    game = MindWrestle(0,0)
    game.mainLoop()






if __name__ == '__main__':
    main()
