import random
import sys
import pygame
from pygame.locals import *


#global varibales 
FPS=32
SCREENWIDTH=289
SCREENHEIGHT=511
SCREEN=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY = (SCREENHEIGHT * 0.8)
GAME_SPRITES={}
GAME_SOUNDS={}
PLAYER='gallery/sprites/yellowbird-downflap.png'
BACKGROUND='gallery/sprites/background.png'
PIPE='gallery/sprites/pipe.png'

def messageScreen():
    playerx=int(SCREENWIDTH/5)
    playery=int((SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2)
    messagex=int((SCREENWIDTH-GAME_SPRITES['message'].get_width())/2)
    messagey=int(SCREENHEIGHT*0.13)
    basex=0
    while True:
        for event in pygame.event.get(): 
            #if user clicks on cross button or press esc key , exit the game
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            #if user press up or space key, strat game
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return    
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0)),
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery)),
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey)),
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score=0
    playerx=int(SCREENWIDTH/5)
    playery=int((SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2)
    basex=0

    #creating 2 pipes
    pipe1=randomPipe()
    pipe2=randomPipe()

    #upper pipes
    upperpipes=[
        {'x':SCREENWIDTH+200,'y':pipe1[0]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2), 'y':pipe2[0]['y']}
    ]

    #lower pipes
    lowerpipes=[
        {'x':SCREENWIDTH+200,'y':pipe1[1]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2), 'y':pipe2[1]['y']}
    ]

    pipeVx=-4 # velocity of pipes

    #player velocitis
    playerVy=-9
    playerVMaxY=10

    #player acceleration
    playerAy=1

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery>0:
                    playerVy=playerFlapAccv
                    playerFlapped=True
                    GAME_SOUNDS['wing'].play()
                    


        checkCrash=isCollide(playerx,playery,upperpipes,lowerpipes)# to check whether the player collided with pipe or not
        if checkCrash:
            SCREEN.blit(GAME_SPRITES['gameover'],(SCREENWIDTH/5,SCREENHEIGHT/3))
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            return

        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperpipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                GAME_SOUNDS['point'].play()  

        if playerVy<playerVMaxY and not playerFlapped:
            playerVy+=playerAy  

        if playerFlapped:
            playerFlapped=False
        playerHeight=GAME_SPRITES['player'].get_height()
        playery= playery + min(playerVy,GROUNDY-playerHeight-playery) 

        #moving pipes to left
        for upperpipe,lowerpipe in zip(upperpipes,lowerpipes):
            upperpipe['x']+=pipeVx
            lowerpipe['x']+=pipeVx

        #adding new pipe when first one is about to cross the leftmost part of the screen
        if 0 < upperpipes[0]['x'] < 5:
            newpipe = randomPipe()
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])

        # if pipe is moving out of the screen then remove it
        if upperpipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)    

        # bliting or sprites
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperpipe, lowerpipe in zip(upperpipes, lowerpipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperpipe['x'], upperpipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerpipe['x'], lowerpipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery)),
          

        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx,playery,upperpipes,lowerpipes):
    if playery>(GROUNDY-25) or playery<0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperpipes:
        pipeHeight=GAME_SPRITES['pipe'][0].get_height()
        if (playery<(pipeHeight+pipe['y'])) and abs(playerx-pipe['x']-25) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerpipes:
        pipeHeight=GAME_SPRITES['pipe'][0].get_height()
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True        
    return False

def randomPipe():
    pipeHeight=GAME_SPRITES['pipe'][0].get_height()
    offset=SCREENHEIGHT/3
    y2=offset+random.randrange(0,int(SCREENHEIGHT-GAME_SPRITES['base'].get_height()-1.2*offset))
    pipex=SCREENWIDTH + 10
    y1=pipeHeight-y2+offset
    pipe=[
        {'x':pipex, 'y':-y1}, #upper pipe
        {'x':pipex, 'y':y2}#lower pipe
    ]
    return pipe






if __name__ == "__main__":
    pygame.init()#initialize all pygame modules
    FPSCLOCK=pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')

    #game visuals
    GAME_SPRITES['numbers']=(
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha()
    )
    GAME_SPRITES['gameover']=pygame.image.load('gallery/sprites/gameover.png').convert_alpha()
    GAME_SPRITES['message']=pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base']=pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe']=(
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha()
    )

    #game sounds
    GAME_SOUNDS['hit']=pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point']=pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['wing']=pygame.mixer.Sound('gallery/audio/wing.wav')

    #games graphics
    GAME_SPRITES['background']=pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player']=pygame.image.load(PLAYER).convert_alpha()
    

    while True:
        messageScreen()
        mainGame()
        