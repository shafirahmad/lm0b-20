# Mizatorian's LM0B #20 Game
# Theme: Dimensions
#
# Ball   is 2 Dimensional (move horiz, vertical)
# Ball has multiple faces ()
# Player is 1 Dimensional - only left right
import pygame, sys
import math, random

def generatePolygon(numVerts,  ctrX, ctrY, aveRadius=10, angle=0 ):
    ''' Creates a polygon with centre ctrX, ctrY 
        Params:
            numVerts - no of vertices
            ctrX, ctrY - coordinates of the "centre" of the polygon
            aveRadius - in px, the average radius of this polygon
            angle = rotation angle
        Returns a list of vertices
    '''
    angleStep =  2*math.pi / numVerts
    points = []
    bbox = {"l":9999, "r":-9999, "t":9999, "b":-9999}
    for i in range(numVerts) :
        r_i = aveRadius
        x = ctrX + r_i*math.cos(angle)
        y = ctrY + r_i*math.sin(angle)
        points.append( (int(x),int(y)) )
        angle = angle + angleStep
        if bbox["r"] < int(x) : bbox["r"] = int(x)
        if bbox["l"] > int(x) : bbox["l"] = int(x)
        if bbox["t"] > int(y) : bbox["t"] = int(y)
        if bbox["b"] < int(y) : bbox["b"] = int(y)

    return points, bbox

def clip(x, min, max) :
    if( min > max ) :  return x    
    elif( x < min ) :  return min
    elif( x > max ) :  return max
    else :             return x

################################################

clock = pygame.time.Clock()

#from pygame.locals import *
pygame.init() # initiates pygame
pygame.display.set_caption('Mizatorian LM0B#20')

WINDOW_SIZE = (400,550)

COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0,0,0)
COLOR_RED = (255,0,0)
COLOR_BLUE = (0,0,255)
COLOR_GREEN = (0,255,0)
COLOR_GRAY1 = (90,90,90)
COLOR_GRAY2 = (190,190,190)
COLOR_GRAY3 = (120,120,120)
FPS = 60

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

gamescreen = pygame.Surface(WINDOW_SIZE) # initiate the surface
gamemenu   = pygame.Surface(WINDOW_SIZE) # initiate the surface

menuscreen=True
moving_right = False
moving_left = False
ball_ymomentum = 0
ball_xmomentum = 0
ball_x = 200
ball_y = 100
ball_radius = 35

player_rect = pygame.Rect(100,500,200,10)

rotation = math.pi/40
ball_angle = 0
ball_faces = 3
frame=0
score=0
ball, ballbbox = generatePolygon(ball_faces,ball_x,ball_y,10,ball_angle)
firsttime=True

pygame.mixer.music.load("music.mid")
pygame.mixer.music.play(-1)
bouncesound = pygame.mixer.Sound("bounce.wav")
crashsound = pygame.mixer.Sound("crash.wav")
wallsound = pygame.mixer.Sound("wall.wav")

while True: # main game loop
    gamescreen.fill(COLOR_GRAY1) # Grey background
    gamemenu.fill(COLOR_GRAY2)
    frame += 1

    if not menuscreen:
        # Player Movement
        player_movement = [0,0]
        if moving_right == True:
            player_movement[0] += 2
        if moving_left == True:
            player_movement[0] -= 2
        player_rect.left += player_movement[0]
        #player_movement[1] += vertical_momentum

        # Player collide with wall
        if player_rect.right > 400 - 10: player_rect.right = 390
        if player_rect.left < 10: player_rect.left = 10 

        # Ball Acceleration
        ball_ymomentum += 0.1
        if ball_ymomentum > 8.9:
            ball_ymomentum = 8.9
        
        # Ball Movement
        ball_x = ball_x + ball_xmomentum
        ball_y = ball_y + ball_ymomentum
        ball_angle = ball_angle + rotation
        ball, ballbbox = generatePolygon(ball_faces,ball_x,ball_y,ball_radius,ball_angle)
    #    if (frame % 20) == 0: ball_faces += (1 if ball_faces <8 else 0)

        # Check if ball collided with player. if yes, bounce up
        if ballbbox["b"]>player_rect.top and ballbbox["b"] > player_rect.bottom:
            if ballbbox["l"] <player_rect.right:
                if ballbbox["r"] > player_rect.left:
                    # Collided, 
                    ball_y = ball_y - ball_ymomentum * 2
                    ball_ymomentum = -random.choice(range(70,89))/10 # change direction
                    score += 1
                    ball_faces += (1 if ball_faces <10 else 0)
                    if ball_faces ==10: ball_faces = random.choice(range(5,10))
                    ball_radius -= (1 if ball_radius >6 else 0)
                    ball_xmomentum = random.choice(range(-15,15))/10
                    rotation = random.choice(range(-15,15))/100
                    ball, ballbbox = generatePolygon(ball_faces,ball_x,ball_y,ball_radius,ball_angle)
                    # Increase speed
                    FPS += (1 if FPS < 150 else 0)
                    # Player rect will get smaller
                    if player_rect.w > 16:
                        player_rect.w -= 4
                        player_rect.left += 2
                    # Play sound
                    bouncesound.play()

        # Check if ball collided with wall, if yes, flip horizontal movement  
        if ballbbox["r"] > 390:
            ball_xmomentum *= -1
            ball_x = ball_x + ball_xmomentum *2
            wallsound.play()

        if ballbbox["l"] < 10:
            ball_xmomentum *= -1
            ball_x = ball_x + ball_xmomentum *2
            wallsound.play()

        # Check if ball missed and is below player, player loses, back to menu
        if ballbbox["t"] > player_rect.top:
            menuscreen = True
            crashsound.play()



        # Draw walls
        pygame.draw.rect(gamescreen, COLOR_GRAY2, pygame.Rect(0, 0, 10, 550))
        pygame.draw.rect(gamescreen, COLOR_GRAY2, pygame.Rect(390, 0, 10, 550))
        pygame.draw.rect(gamescreen, COLOR_GRAY2, pygame.Rect(0, 0, 400, 40 ))

        # Display Player and Ball (rects)
        # gamescreen.blit(player_img,(player_rect.x-scroll[0],player_rect.y-scroll[1]))
        pygame.draw.rect(gamescreen, COLOR_GREEN, player_rect)
        pygame.draw.polygon(gamescreen, COLOR_RED, ball)
        pygame.draw.line(gamescreen, COLOR_WHITE, (ball_x, ball_y), ball[0])

        font = pygame.font.Font('at01.ttf', 32)
        text = font.render('Score: ' + str(score), True, COLOR_BLACK, COLOR_GRAY2 )
        textRect = text.get_rect()
        textRect.center = (200,20)
        gamescreen.blit(text, textRect)


    if menuscreen:
        if not firsttime:
            pygame.draw.rect(gamemenu, COLOR_GRAY1, (50,50,300,100))
            font = pygame.font.Font('at01.ttf', 32)
            text = font.render('Score: ' + str(score), True, COLOR_WHITE, COLOR_GRAY1 )
            textRect = text.get_rect()
            textRect.center = (200,100)
            gamemenu.blit(text, textRect)
        #pygame.draw.rect(gamemenu, COLOR_GRAY1, textRect)
        pygame.draw.rect(gamemenu, COLOR_GRAY1, (50,200,300,300))
        font = pygame.font.Font('at01.ttf', 24)
        textlist = ["Mizatorian's LM0B#20 Dimension",
                    " ",
                    "(You move in 1D left-right)",
                    "(The 'ball' moves in 2D)",
                    "(The 'ball' changes its dimensions",
                    "                   (size & faces))",
                    " ",
                    "Press SPACE to start",
                    " ",
                    "LEFT Arrow = move left",
                    "RIGHT Arrow = move right",
                    "Q = Quit"]
        start = 240
        for item in textlist:
            text = font.render(item, True, COLOR_WHITE, COLOR_GRAY1)
            textRect = text.get_rect()
            textRect.center = (200,start)
            start += 20
            gamemenu.blit(text, textRect)

    # Event handler loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_SPACE and menuscreen == True:
                menuscreen = True # should we wait for user to keyup
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_SPACE and menuscreen == True:
                menuscreen = False
                #Reset game variables, start game
                firsttime = False
                moving_right = False
                moving_left = False
                ball_ymomentum = 0
                ball_xmomentum = 0
                ball_x = 200
                ball_y = 100
                ball_radius = 35
                player_rect = pygame.Rect(100,500,200,10)
                ball_angle = 0
                ball_faces = 3
                score=0
                FPS=45
                ball, ballbbox = generatePolygon(ball_faces,ball_x,ball_y,10,ball_angle)
        
    if menuscreen:
        screen.blit(pygame.transform.scale(gamemenu,WINDOW_SIZE),(0,0))
    else:
        screen.blit(pygame.transform.scale(gamescreen,WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(FPS)
