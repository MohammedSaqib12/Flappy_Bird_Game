import random
import button
import sys
import pygame
from pygame.locals import*

black = (0 , 0 , 0)

FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_ASSET = {}
GAME_SOUNDS = {}
PLAYER = 'asset/bird.png'
BACKGROUND = 'asset/background.jpg'
PIPE = 'asset/pipe.png'

def text_screen( text , color ,x,y):
    screen_text = font . render(text , True , color)
    SCREEN.blit(screen_text , [x,y])

def welcomeScreen():

    playerx = int(SCREENWIDTH/7)
    playery = int((SCREENHEIGHT - GAME_ASSET['player'].get_height())/1.7)
    messagex = int((SCREENWIDTH - GAME_ASSET['player'].get_width())/5)
    messagey = int(SCREENHEIGHT * 0.24)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.type == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN or (event.type == K_SPACE and event.type == K_UP):
                return
            else:
                SCREEN.blit(GAME_ASSET['background'], (0, 0))
                SCREEN.blit(GAME_ASSET['player'], (playerx,playery ))
                SCREEN.blit(GAME_ASSET['message'], (messagex,messagey ))
                SCREEN.blit(GAME_ASSET['base'], (basex,GROUNDY ))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score=0
    playerx= int(SCREENWIDTH/5)
    playery= int(SCREENHEIGHT/2)
    basex=0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperpipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
  ]

    lowerpipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
  ]

    pipevelx = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAcc = -8
    playerFlapped = False
    nextpipemidpos = 4
    uppipe = 5
    with open ("hiscore_easy.txt" , "r") as f:
        hiscore_easy = f.read()

    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.type==K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN or (event.type == K_SPACE and event.type == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAcc
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashtest = iscollide(playerx , playery , upperpipes , lowerpipes)
        
        if crashtest:
            with open ("hiscore_easy.txt" , "w") as f:
                f.write(str(hiscore_easy))
            return

        playerMidPos = playerx + GAME_ASSET['player'].get_width()/2
        for pipe in upperpipes:
            pipeMidpos = pipe['x'] + GAME_ASSET['player'].get_width()/2
            if pipeMidpos<= playerMidPos<pipeMidpos + nextpipemidpos:
                score +=1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()
                if score > int(hiscore_easy):
                    hiscore_easy = score

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_ASSET['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        for upperpipe , lowerpipe in zip(upperpipes , lowerpipes):
            upperpipe['x'] += pipevelx
            lowerpipe['x'] += pipevelx

        if 0<upperpipes[0]['x']<uppipe:
            newpipe = getRandomPipe()
            upperpipes . append(newpipe[0])
            lowerpipes . append(newpipe[1])

        if upperpipes[0]['x'] < -GAME_ASSET['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)
        SCREEN.blit(GAME_ASSET['background'],(0 , 0))
        # text_screen("hiscore : " +str(hiscore_easy) ,red, 0,0)
        for upperpipe , lowerpipe in zip(upperpipes, lowerpipes):
            SCREEN.blit(GAME_ASSET['pipe'][0],(upperpipe['x'] , upperpipe['y']))
            SCREEN.blit(GAME_ASSET['pipe'][1],(lowerpipe['x'] , lowerpipe['y']))

        SCREEN.blit(GAME_ASSET['base'],(basex , GROUNDY))
        SCREEN.blit(GAME_ASSET['player'],(playerx , playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_ASSET['numbers'][digit].get_width()
        
        xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_ASSET['numbers'][digit], (xoffset, SCREENHEIGHT* 0.12))
            text_screen("Hiscore : " +str(hiscore_easy) ,black, 0,0)
            xoffset += GAME_ASSET['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS) 

def mainGame2():
    score=0
    playerx= int(SCREENWIDTH/5)
    playery= int(SCREENHEIGHT/2)
    basex=0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperpipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
  ]

    lowerpipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
  ]

    pipevelx = -6

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAcc = -8
    playerFlapped = False
    nextpipemidpos = 6
    uppipe = 7
    with open ("hiscore_medium.txt" , "r") as f:
        hiscore_medium = f.read()


    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.type==K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN or (event.type == K_SPACE and event.type == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAcc
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashtest = iscollide(playerx , playery , upperpipes , lowerpipes)
        if crashtest:
            with open ("hiscore_medium.txt" , "w") as f:
                f.write(str(hiscore_medium))
            return

        playerMidPos = playerx + GAME_ASSET['player'].get_width()/2
        for pipe in upperpipes:
            pipeMidpos = pipe['x'] + GAME_ASSET['player'].get_width()/2
            if pipeMidpos<= playerMidPos<pipeMidpos + nextpipemidpos:
                score +=1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()
                if score > int(hiscore_medium):
                    hiscore_medium = score

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_ASSET['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        for upperpipe , lowerpipe in zip(upperpipes , lowerpipes):
            upperpipe['x'] += pipevelx
            lowerpipe['x'] += pipevelx

        if 0<upperpipes[0]['x']<uppipe:
            newpipe = getRandomPipe()
            upperpipes . append(newpipe[0])
            lowerpipes . append(newpipe[1])

        if upperpipes[0]['x'] < -GAME_ASSET['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)
        SCREEN.blit(GAME_ASSET['background'],(0 , 0))
        for upperpipe , lowerpipe in zip(upperpipes, lowerpipes):
            SCREEN.blit(GAME_ASSET['pipe'][0],(upperpipe['x'] , upperpipe['y']))
            SCREEN.blit(GAME_ASSET['pipe'][1],(lowerpipe['x'] , lowerpipe['y']))

        SCREEN.blit(GAME_ASSET['base'],(basex , GROUNDY))
        SCREEN.blit(GAME_ASSET['player'],(playerx , playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_ASSET['numbers'][digit].get_width()
        
        xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_ASSET['numbers'][digit], (xoffset, SCREENHEIGHT* 0.12))
            text_screen("Hiscore : " +str(hiscore_medium) ,black, 0,0)
            xoffset += GAME_ASSET['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS) 

def mainGame3():
    score=0
    playerx= int(SCREENWIDTH/5)
    playery= int(SCREENHEIGHT/2)
    basex=0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperpipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
  ]

    lowerpipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
  ]

    pipevelx = -7

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAcc = -8
    playerFlapped = False
    nextpipemidpos = 6
    uppipe = 8
    with open ("hiscore_hard.txt" , "r") as f:
        hiscore_hard = f.read()


    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.type==K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN or (event.type == K_SPACE and event.type == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAcc
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashtest = iscollide(playerx , playery , upperpipes , lowerpipes)
        if crashtest:
            with open ("hiscore_hard.txt" , "w") as f:
                f.write(str(hiscore_hard))
            return

        playerMidPos = playerx + GAME_ASSET['player'].get_width()/2
        for pipe in upperpipes:
            pipeMidpos = pipe['x'] + GAME_ASSET['player'].get_width()/2
            if pipeMidpos<= playerMidPos<pipeMidpos + nextpipemidpos:
                score +=1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()
                if score > int(hiscore_hard):
                    hiscore_hard = score

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_ASSET['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        for upperpipe , lowerpipe in zip(upperpipes , lowerpipes):
            upperpipe['x'] += pipevelx
            lowerpipe['x'] += pipevelx

        if 0<upperpipes[0]['x']<uppipe:
            newpipe = getRandomPipe()
            upperpipes . append(newpipe[0])
            lowerpipes . append(newpipe[1])

        if upperpipes[0]['x'] < -GAME_ASSET['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)
        SCREEN.blit(GAME_ASSET['background'],(0 , 0))
        for upperpipe , lowerpipe in zip(upperpipes, lowerpipes):
            SCREEN.blit(GAME_ASSET['pipe'][0],(upperpipe['x'] , upperpipe['y']))
            SCREEN.blit(GAME_ASSET['pipe'][1],(lowerpipe['x'] , lowerpipe['y']))

        SCREEN.blit(GAME_ASSET['base'],(basex , GROUNDY))
        SCREEN.blit(GAME_ASSET['player'],(playerx , playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_ASSET['numbers'][digit].get_width()
        
        xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_ASSET['numbers'][digit], (xoffset, SCREENHEIGHT* 0.12))
            text_screen("Hiscore : " +str(hiscore_hard) ,black, 0,0)
            xoffset += GAME_ASSET['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS) 

def iscollide(playerx , playery , upperpipes , lowerpipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperpipes:
        pipeHeight = GAME_ASSET['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_ASSET['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerpipes:
        if (playery + GAME_ASSET['player'].get_height() > pipe['y']) and abs(playerx  - pipe['x']) < GAME_ASSET['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe():

    pipeheight = GAME_ASSET['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_ASSET['base'].get_height() - 1.2*offset))
    pipex = SCREENWIDTH + 10
    y1 = pipeheight - y2 + offset
    pipe = [
        {'x': pipex, 'y': -y1}, #upper pipe
        {'x': pipex, 'y': y2} #lower pipe
    ]
    return pipe

if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird Game')

    game_State = False
    menu_state = "main"

    # define fonts
    font = pygame.font.SysFont("arialblack" , 18)

    # define color
    TEXT_COL = (255,255,255)

    start = pygame.image.load("buttons/start.png").convert_alpha()
    # resume = pygame.image.load("buttons/resume.png").convert_alpha()
    option = pygame.image.load("buttons/option.png").convert_alpha()
    exit = pygame.image.load("buttons/exit.png").convert_alpha()
    easy = pygame.image.load("buttons/easy.png").convert_alpha()
    medium = pygame.image.load("buttons/medium.png").convert_alpha()
    hard = pygame.image.load("buttons/hard.png").convert_alpha()
    back = pygame.image.load("buttons/back.png").convert_alpha()

    # creating button instances
    startbtn = button.Button (75 , 150 , start ,1)
    optionbtn = button.Button (70 , 225 , option ,1)
    exitbtn = button.Button (70 , 300 , exit ,1)
    easybtn = button.Button (70 , 125 , easy ,1)
    mediumbtn = button.Button (70 , 200 , medium ,1)
    hardbtn = button.Button (70 , 275 , hard ,1)
    backbtn = button.Button (65 , 350 , back ,1)

    def draw_text (text , font , text_col , x, y):
        img = font.render(text , True , text_col)
        SCREEN.blit(img,(x,y))

    GAME_ASSET['numbers'] = (
        pygame.image.load('asset/0.png').convert_alpha(),
        pygame.image.load('asset/1.png').convert_alpha(),
        pygame.image.load('asset/2.png').convert_alpha(),
        pygame.image.load('asset/3.png').convert_alpha(),
        pygame.image.load('asset/4.png').convert_alpha(),
        pygame.image.load('asset/5.png').convert_alpha(),
        pygame.image.load('asset/6.png').convert_alpha(),
        pygame.image.load('asset/7.png').convert_alpha(),
        pygame.image.load('asset/8.png').convert_alpha(),
        pygame.image.load('asset/9.png').convert_alpha(),
    )

    GAME_ASSET['message'] = pygame.image.load('asset/message_2.png').convert_alpha()
    GAME_ASSET['base'] = pygame.image.load('asset/base.png').convert_alpha()
    GAME_ASSET['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )

    GAME_SOUNDS['die'] = pygame.mixer.Sound('audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('audio/wing.wav')

    GAME_ASSET['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_ASSET['player'] = pygame.image.load(PLAYER).convert_alpha()
    # def message():
    #     welcomeScreen()
    run = True
    while run:

        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.type==K_ESCAPE):
                pygame.quit()
                sys.exit()

        SCREEN.blit(GAME_ASSET['background'], (0, 0))

        if game_State  == True :
            if menu_state == "main":
                if startbtn.draw(SCREEN):
                  mainGame()
                if optionbtn.draw(SCREEN):
                #   menu_state = "options"
                  menu_state = 'options'
                if exitbtn.draw(SCREEN):
                  run = False

            if menu_state == "options" :
        #draw the different options buttons
                if easybtn.draw(SCREEN):
                  mainGame()
                if mediumbtn.draw(SCREEN):
                  mainGame2()
                if hardbtn.draw(SCREEN):
                  mainGame3()
                if backbtn.draw(SCREEN):
                  menu_state = "main"
        
        else :
            draw_text("press space to Continue ", font , TEXT_COL , 30 ,240)
            # message()
            # welcomeScreen()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_State = True
                if event.type == pygame.QUIT:
                    run = False

        # welcomeScreen()
        # mainGame()
        pygame.display.update()

    pygame.quit()