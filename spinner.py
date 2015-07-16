import sys, os
sys.path.insert(0, os.path.abspath('..'))
sys.path.append("E:\\bin\\apps\\Python27\\projects\\demo1")

import pygame
import pygbutton

from math import floor
from pygame.locals import *
from random import randint
from time import strftime, gmtime


FPS = 60
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
WINDOWCENTER = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
GREY  = (128, 128, 128)
RED   = (255,   0,   0)

ORING = pygame.image.load("ring_o.png")
IRING = pygame.image.load("ring_i.png")

class vokeButton(pygbutton.PygButton):
    def __init__(self, *args, **kwargs):
        super(vokeButton, self).__init__(*args, **kwargs)
        self.func=None
        self.funcargs=None
        
    def do(self):
        if self.func is not None and self.funcargs is None:
            self.func()
        elif self.func is not None and self.funcargs is not None:
            self.func(*self.funcargs)
        else:
            pass



class Spinner(object):
    """An object what spins.
    
       Takes a pygame Surface as the first positional argument, and a two-
       integer tuple as the 'location' keyword argument. The location represents
       where the center of the object should be placed using the draw() method
       of this object.  You can pass this class any kind of object, but the
       object should have square dimensions to avoid clipping."""
       
    def __init__(self, imageSurface=None, location=(0,0), rotspeed=0):
        if imageSurface is None:
            imageSurface = pygame.Surface((200, 200))
            imageSurface.fill(WHITE)
        self.origSurface = imageSurface
        self.origRect = self.origSurface.get_rect()
        self.origRect.center = location
        self.outSurface = self.origSurface.copy()
        self.angle = 0
        self.rotspeed = rotspeed
        self.cwr = True
        
    def spin(self, animated=True):
        if self.cwr:
            if self.rotspeed > 0:
                self.rotspeed = self.rotspeed * -1
        else:
            if self.rotspeed < 0:
                self.rotspeed = self.rotspeed * -1
                
        if self.angle > 360:
            self.angle -= 360
        if self.angle < 0:
            self.angle += 360
        self.outSurface = pygame.transform.rotozoom(self.origSurface, self.angle, 1)
        rotrect = self.origRect.copy()
        rotrect.center = self.outSurface.get_rect().center
        self.outSurface = self.outSurface.subsurface(rotrect).copy()
        if animated:
            self.angle += self.rotspeed

    
    def draw(self, surface, animated=True):
        self.spin(animated)
        surface.blit(self.outSurface, self.origRect)



class countdownTimer(object):
    def __init__(self, msecs=0, font=None, size=32, color=WHITE):
        if not pygame.font.get_init():
            pygame.font.init()
        self.font = pygame.font.Font(font, size)
        self.size = size
        self.color = color
        self.msecs = msecs
        self.timestring = self.formatTime()
        
    def formatTime(self):
        k = strftime('%M:%S', gmtime(self.msecs/1000)) + '.%03d' % (self.msecs % 1000)
        return k
        
    def update(self, tick):
        self.msecs -= tick
        if self.msecs < 0:
            self.msecs = 0
        self.timestring = self.formatTime()
        
    def draw(self, surface, tick):
        render = self.font.render(self.timestring, True, self.color)
        surface.blit(render, (0,0))
        self.update(tick)


        
class readySurf(object):
    """A text surface what fades in."""
    def __init__(self, font=None, size=32, color=WHITE, text='READY?', loc=(0,0), speed=1):
        if not pygame.font.get_init():
            pygame.font.init()
        self.font = pygame.font.Font(font, size)
        self.render = self.font.render(text, False, color)
        self.rect = self.render.get_rect()
        self.rect.center = loc
        self.speed = abs(speed)
        self.alpha = 0
        self.buttonwasdown = False
        
    def draw(self, surface):
        self.render.set_alpha(self.alpha)
        surface.blit(self.render, self.rect)
        if self.alpha < 255:
            self.alpha += self.speed
        if self.alpha > 255:
            self.alpha = 255
            
    def handleEvent(self, event):
        if event.type not in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
            return []
            
        retval = []
        
        if event.type == MOUSEBUTTONUP and self.buttonwasdown:
            retval.append('click')
            self.buttonwasdown = False
        if event.type == MOUSEBUTTONDOWN and self.alpha is 255:
            self.buttonwasdown = True
                
        return retval



class heartContainer(object):
    def __init__(self, numhearts, heartimg=None, spacing=1):
        self.numhearts = numhearts
        self.maxhearts = numhearts
        if heartimg is None:
            self.heartimg = self.defaultheartimg()
        else:
            self.heartimg = heartimg
        self.spacing = spacing
        self.heartbox = self.heartBox()
     
    def heartBox(self):
        rect = self.heartimg.get_rect()
        surface = pygame.Surface(((rect.width * self.numhearts), rect.height))
        for item in range(self.numhearts):
            surface.blit(self.heartimg, (item*rect.width, 0))
        return surface

    def defaultheartimg(self):
        surface = pygame.Surface((17,17))
        rect = surface.get_rect()
        pygame.draw.circle(surface, RED, rect.center, 8)
        return surface
        
    def update(self):
        self.heartbox = self.heartBox()
        
    def addheart(self, amount=1):
        self.numhearts += amount
        if self.numhearts > self.maxhearts:
            self.numhearts = self.maxhearts
        self.update()
    
    def remheart(self, amount=1):
        self.numhearts -= amount
        if self.numhearts < 0:
            self.numhearts = 0
        self.update()
        
    def draw(self, surface, loc):
        self.update()
        surface.blit(self.heartbox, loc)


        
class Rings(object):
    def __init__(self, iring=None, oring=None):
        self.rings = [iring, oring]
        self.iring = self.rings[0]
        self.oring = self.rings[1]
        for ring in self.rings:
            randangle = randint(0, 360)
            ring.angle = randangle
        self.d_angle = self.delta_angle()
            
    def _newangle(self, ring):
        randangle = randint(0, 360)
        ring.angle = randangle

    def newoangle(self):
        ring = self.oring
        self._newangle(ring)
        
    def newiangle(self):
        ring = self.iring
        self._newangle(ring)
        
    def delta_angle(self):
        oring = self.oring
        iring = self.iring
        dangle = 180 - abs(abs(iring.angle - oring.angle) - 180)
        self.d_angle = dangle
        return self.d_angle

    def draw(self, surface, animated=True):
        for ring in self.rings:
            ring.draw(surface, animated)



class mainMenu(object):
    def __init__(self, buttonwidth, buttonheight, spacing, windowwidth, windowheight):
        self.buttonwidth = buttonwidth
        self.buttonheight = buttonheight
        self.spacing = spacing
        self.windowwidth = windowwidth
        self.windowheight = windowheight
        self.windowcenter = (windowwidth / 2, windowheight / 2)
        self.buttonrect = pygame.Rect(0, 0, buttonwidth, buttonheight)
        self.buttonlist = []
        
    def add(self, caption, func=None, funcargs=None):
        thisbutton = vokeButton(self.buttonrect, caption)
        thisbutton.func = func
        thisbutton.funcargs = funcargs
        self.buttonlist.append(thisbutton)
        
        
    def update(self):
        numbuttons = len(self.buttonlist)
        buttoncontainer = pygame.Rect(0, 0, self.buttonwidth, self.buttonheight * numbuttons + self.spacing * (numbuttons - 1))
        buttoncontainer.center = self.windowcenter

        for item in self.buttonlist:
            index = self.buttonlist.index(item)

            if index == 0:
                item.rect.top = buttoncontainer.top

            else:
                item.rect.top = buttoncontainer.top + (self.buttonheight + self.spacing) * index
            item.rect.left = buttoncontainer.left

    def draw(self, surface):
        self.update()
        for item in self.buttonlist:
            item.draw(surface)



class Player(object):
    def __init__(self, scorerect=None):
        self.maxhearts = 3
        self.hc = heartContainer(self.maxhearts)
        self.score = 0
        self.difficulty = 0
        self.updatedif()
        if scorerect is None:
            self.scorebox = feedbackBox(pygame.Rect(0,0,200,175))
        else:
            self.scorebox = feedbackBox(scorerect)
        
    def advLevel(self, levels=1):
        self.hearts = self.maxhearts
        self.hc.numhearts = self.maxhearts
        self.difficulty += levels
        self.updatedif()
        
    def updatedif(self):
        basehits = 10
        basespeed = 3
        self.needhits = basehits + (self.difficulty * 5)
        self.speed = basespeed + (0.4 * self.difficulty)
        
    def scoreupdate(self, dangle):
        scoreamt = None
        
        BASE = 10
        SUPERB = 20
        ASTONISHING = 50
        
        if self.difficulty is 0:
            MULTIPLIER = 1
        else:
            MULTIPLIER = self.difficulty * 2

        if dangle < 2.0:
            scoreamt = ASTONISHING
            self.scorebox.addtext("ASTONISHING!")
        elif 2.0 <= dangle <= 5.0:
            scoreamt = SUPERB
            self.scorebox.addtext("SUPERB!")
        elif 5.0 < dangle <= 15.0:
            scoreamt = BASE
            self.scorebox.addtext("BASE")
        else:
            scoreamt = 0
        
        adjscore = (scoreamt * MULTIPLIER)
        self.score += adjscore
        self.scorebox.addtext(str(adjscore) + " points!")
        
        
    def handleEvent(self, event):
        if event.type not in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
            return []
            
        retval = []
        
        if event.type == MOUSEBUTTONUP and self.buttonwasdown:
            retval.append('click')
            self.buttonwasdown = False
        if event.type == MOUSEBUTTONDOWN and self.alpha is 255:
            self.buttonwasdown = True
                
        return retval

        

class feedtbackText(object):
    def __init__(self):
        pass


        
class feedbackBox(object):
    def __init__(self, boxrect, fadespeed=3):
        self.boxrect = boxrect
        self.fadespeed = fadespeed
        self.textlist = []
        
    def addtext(self, text, font=None, size=32, color=WHITE):
        font = pygame.font.Font(font, size)
        output = font.render(text, False, color)
        rect = output.get_rect()
        output.set_alpha(255)
        self.textlist.append( (output, rect) )
        self.positiontext()

    def sizeoftext(self, textlist=None):
        linesize = 0
        textlist = self.textlist
        textlist.reverse()
        for out, rect in textlist:
            linesize += rect.height
        return linesize
        
    def update(self):
        for item in self.textlist:
            out = item[0]
            oldalpha = out.get_alpha()
            newalpha = oldalpha - self.fadespeed
            if newalpha <= 0:
                self.textlist.remove(item)
            else:
                out.set_alpha(newalpha)
        
    def positiontext(self):
        linesize = self.sizeoftext()
            
        while linesize >= self.boxrect.height:
            self.textlist.pop()
            linesize = sizeoftext()
        
        bottom = self.boxrect.bottom
        for out, rect in self.textlist:
            rect.left = self.boxrect.left
            rect.bottom = bottom
            bottom -= rect.height
            
    
    def draw(self, surface):
        textlist = self.textlist
        textlist.reverse()
        if textlist is None:
            textlist = []
        for item in textlist:
            out = item[0]
            rect = item[1]
            surface.blit(out, rect)
        self.update()

            

def textbox():
    pass

def readying(player, surface, fpsclock=None):
    rot_speed = player.speed

    inner_ring = Spinner(IRING, WINDOWCENTER, rot_speed)
    outer_ring = Spinner(ORING, WINDOWCENTER)

    rings = Rings(inner_ring, outer_ring)

    if fpsclock is None:
        fpsclock = pygame.time.Clock()

    readysurf = readySurf(size=200, loc=WINDOWCENTER, speed=10)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()

            # Once the "Ready?" prompt is fully opaque, allow user to click to
            # start the game. Breaks the loop (into the "playing" loop, ideally)
            if 'click' in readysurf.handleEvent(event):
                return rings

        # Update the drawing surface
        surface.fill(GREY)
        #for ring in rings:
        #    ring.draw(surface, False)
        rings.draw(surface, False)
        readysurf.draw(surface)
        pygame.display.update()
        
        # Tick the clock in time to limit our speed to FPS
        fpsclock.tick(FPS)

def lose(surface, rings=None, fpsclock=None, player=None):
        
    if fpsclock is None:
        fpsclock = pygame.time.Clock()
        
    font = pygame.font.Font(None, 32)

    losesurf = readySurf(size=180, text='You Lose!', loc=WINDOWCENTER, speed=10)
    scoretext = font.render("Score: " + str(player.score), True, WHITE)


    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()

            if 'click' in losesurf.handleEvent(event):
                return

        # Update the drawing surface
        surface.fill(GREY)
        #for ring in rings:
        #    ring.draw(surface, False)
        rings.draw(surface, False)
        losesurf.draw(surface)
        if losesurf.alpha is 255:
            surface.blit(scoretext, (0, 52))
        pygame.display.update()
        
        # Tick the clock in time to limit our speed to FPS
        fpsclock.tick(FPS)
    
def advlevel(surface, rings=None, fpsclock=None, player=None):
    if rings is None:
        rings=[Spinner(), Spinner()]
        
    if fpsclock is None:
        fpsclock = pygame.time.Clock()
        
    winsurf = readySurf(size=180, text='Great Job!', loc=WINDOWCENTER, speed=10)
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
                
            if 'click' in winsurf.handleEvent(event):
                player.advLevel()
                return
                
        # Update the drawing surface
        surface.fill(GREY)
        rings.draw(surface, False)
        #for ring in rings:
        #    ring.draw(surface, False)
        winsurf.draw(surface)
        pygame.display.update()
        
        # Tick the clock in time to limit our speed to FPS
        fpsclock.tick(FPS)

def playing(player, surface, rings=None, fpsclock=None):
    #if rings is None:
    #    rings=[Spinner(), Spinner()]

    EXITBUTTONWIDTH = 100
    EXITBUTTONHEIGHT = 40
    SPACING = 5
    MSECS = 6000
    
    frametick = 0
    timer = countdownTimer(MSECS)
    
    curhits = 0
    maxhits = player.needhits
    heartcontainer = player.hc

    exitbuttonrect = pygame.Rect(0, 0, EXITBUTTONWIDTH, EXITBUTTONHEIGHT)
    exitbuttonrect.right = WINDOWWIDTH - SPACING
    exitbuttonrect.bottom = WINDOWHEIGHT - SPACING
    exitbutton = vokeButton(exitbuttonrect, 'Exit')
    
    font = pygame.font.Font(None, 36)
    delta_angle = rings.delta_angle()
    #fbrect = pygame.Rect(0,0,210,175)
    fbrect = player.scorebox.boxrect
    #fbrect.bottom = surface.get_rect().bottom + 5
    #fbrect.centerx = surface.get_rect().centerx


    while True:
        numhearts = heartcontainer.numhearts

        #play
        if curhits >= maxhits:
            advlevel(surface, rings, fpsclock, player)
            return True
        if heartcontainer.numhearts == 0:
            lose(surface, rings, fpsclock, player)
            return False
        dangletext = font.render("Delta Angle: " + str(delta_angle), True, WHITE)
        hitstext = font.render(str(curhits) + " / " + str(maxhits) + " Hits", True, WHITE)
        scoretext = font.render("Score: " + str(player.score), True, WHITE)
        #heartstext = font.render(str(heartcontainer.numhearts), True, WHITE)
        leveltext = font.render("Level: " + str(player.difficulty + 1), True, WHITE)
        ltrect = leveltext.get_rect()
        ltrect.centerx = WINDOWWIDTH / 2
        ltloc = ltrect.topleft
        #handle events
        eventlist = pygame.event.get()
        for event in eventlist: # event handling loop
            if event.type == QUIT:
                quit()

            if 'click' in exitbutton.handleEvent(event):
                return
                
            #I want to change this to something like:
            #player.handleEvent(event)
            #the difficulty (how close should delta_angle be to 0 to be considered
            #a good hit) should be a property of an object, and probably so should
            #things like cur/max hits, the heart container, etc....
            
            else:
                if event.type == MOUSEBUTTONDOWN:
                    if delta_angle <= 15:
                        curhits += 1
                        player.scoreupdate(delta_angle)
                        #rings[0].cwr = not rings[0].cwr
                        rings.iring.cwr = not rings.iring.cwr
                        rings.newoangle()
                        #randangle = randint(0,360)
                        #rings[1].angle = randangle
                    else:
                        heartcontainer.remheart()

        #draw update
        surface.fill(GREY)
        rings.draw(surface)
        surface.blit(hitstext, (0, 26))
        surface.blit(scoretext, (0, 52))
        surface.blit(dangletext, (0, 78))
        #surface.blit(heartstext, (0, 78))
        surface.blit(leveltext, ltloc)
        heartcontainer.draw(surface, (0, 0))
        exitbutton.draw(surface)
        player.scorebox.draw(surface)
        #pygame.draw.rect(surface, WHITE, fbrect, 2)

        pygame.display.update()
        delta_angle = rings.delta_angle()
        frametick = fpsclock.tick(FPS)
    
def spinner(surface, fpsclock):
    #this defines the spinner part of the game
    PLAYING = True

    fbrect = pygame.Rect(0,0,210,175)
    fbrect.bottom = 480
    fbrect.centerx = 640 / 2


    player = Player(scorerect=fbrect)

    while PLAYING:

        rings = readying(player, surface, fpsclock)
    
        PLAYING = playing(player, surface, rings, fpsclock)

def quit():
    pygame.quit()
    sys.exit()

def main():
    MMBUTTONWIDTH  = 150
    MMBUTTONHEIGHT = 75
    SPACING = 5
    TOTALSCORE = 0

    pygame.init()
    
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('RINGS')
    
    main_menu = mainMenu(MMBUTTONWIDTH, MMBUTTONHEIGHT, SPACING, WINDOWWIDTH, WINDOWHEIGHT)
    main_menu.add('Play', spinner, [DISPLAYSURFACE, FPSCLOCK])
    main_menu.add('High Scores')
    main_menu.add('Quit', quit)


    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                quit()

            for button in main_menu.buttonlist:
                if 'click' in button.handleEvent(event):
                    button.do()
                
        DISPLAYSURFACE.fill(BLACK)
        main_menu.draw(DISPLAYSURFACE)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()
