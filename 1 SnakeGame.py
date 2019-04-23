#########################################
# Programmer: Omri Daniel
# Date: 1-05-18
# File Name: snake_game.py
# Description: This program is a Snake Game.
#                     Try to see how long you can survive and get the snake!
#########################################

import pygame
pygame.init()

from math import sqrt
from random import randint


#####################
#Window Properties
#####################
HEIGHT = 600
WIDTH  = 900

screen=pygame.display.set_mode((WIDTH,HEIGHT))

WHITE = (255,255,255)
BLACK = (  0,  0,  0)
YELLOW = (255,255,0)
outline=0

font=pygame.font.SysFont('Ariel Black',50)

back=pygame.image.load('background.jpg')
back=back.convert_alpha()
back=pygame.transform.scale(back,(WIDTH,HEIGHT))

intro=pygame.image.load('intro.jpg')
intro=intro.convert_alpha()

end=pygame.image.load('end.png')
end=end.convert_alpha()

song=pygame.mixer.Sound('song.ogg')
song.play(-1)

game_speed=80

origTime=20
start_time=0
time=origTime

inPlay=0                                                    #InPlay is what screen to show, 0=intro, 1=game, 2=end, 3=close game
#####################
#Snake Properties
#####################
BODY_SIZE = 15
HSPEED = 30
VSPEED = 30

head=pygame.image.load('head.png')
head=head.convert_alpha()
head=pygame.transform.scale(head, (60,60))
recthead= head.get_rect ()

bod=pygame.image.load('bod.png')
bod=bod.convert_alpha()
bod=pygame.transform.scale(bod, (30,30))
rectbod= bod.get_rect ()

speedX =0
speedY = -VSPEED
segx = [int(WIDTH/2.)]*3
segy = [HEIGHT, HEIGHT+VSPEED, HEIGHT+2*VSPEED]

#####################
#Apple Properties
#####################
appleb=pygame.image.load('bad.png')
appleb=appleb.convert_alpha()
appleb=pygame.transform.scale(appleb, (30,30))
rectappleb= appleb.get_rect ()

apple=pygame.image.load('apple.png')
apple=apple.convert_alpha()
apple=pygame.transform.scale(apple, (30,30))
rectapple= apple.get_rect ()

applex=randint(1,WIDTH/30-1)*30
appley=randint(1,HEIGHT/30-1)*30
score=int(0)

eat=pygame.mixer.Sound('eat.ogg')

bad=pygame.mixer.Sound('bad.ogg')

badx=randint(1,WIDTH/30-1)*30
bady=randint(1,HEIGHT/30-1)*30


#####################
#Game intro function
#####################
def game_intro():
    screen.blit(intro,(0,0))
    pygame.display.update()

#####################
#Function to redraw screen
#####################
def redraw_screen():
    screen.blit(back,(0,0))
    for i in range(len(segx)):
        recthead.center = [segx[0], segy[0]]                                        #Center the head and body images
        rectbod.center = [segx[i], segy[i]]
        screen.blit(head, recthead)                                                     #Draw head and body
        screen.blit(bod, rectbod)
        
    scoreTxt=font.render('Score:'+str(score),1,WHITE)                      #Render and constantly update score/time
    screen.blit(scoreTxt,(10,0))                                                          #Draw score/time on screen
    
    timeTxt=font.render('Time:'+str(time),1,WHITE)
    screen.blit(timeTxt,(10,HEIGHT-30))
    
    rectappleb.center = [badx, bady]                                                #Center bad/good apple
    screen.blit(appleb, rectappleb)                                                   #Draw out apples

    rectapple.center = [applex,appley]
    screen.blit(apple, rectapple)
    
    pygame.display.update()                                                             # display must be updated, in order
                                                                                                        # to show the drawings

#####################
#Function to calculate distance
#####################
def dist(x1, y1, x2, y2):                                                       
    return sqrt((x1-x2)**2+(y1-y2)**2)

#####################
#Function checks if snake collides with itself
#####################
def snake_collosion():
    if len(segx)>1:                                                                             #Only checks if snake length bigger than 1
        for i in range(1,len(segx)):
            d=dist(segx[0],segy[0],segx[i],segy[i])                                  #Checks distance between head and each seg
            if d<5:                                                                                  #Returns true if head and seg collide(quits game)
                return True

#####################
#Function for countdown
#####################
def timer():
    global time                                                                                 #Pulls assaigned value of time variables
    global start_time
    time=origTime
    time-=(pygame.time.get_ticks()-start_time)//1000                        #Removes time passed from current time
    if time<=0:                                                                                  #If time is done, end game
        return True

#####################
#Function for end screen
#####################
def outro():
    screen.blit(end,(0,0))
    font=pygame.font.SysFont('Ariel Black',150)                              #Resize the current font
    scoreTxt=font.render('Final Score:'+str(score),1,YELLOW)            #Print out final score
    screen.blit(scoreTxt,(80,0))
    pygame.display.update()


#####################
#Main Program
#####################
#Intro Screen:
while inPlay==0:
    start_time=pygame.time.get_ticks()                                          #Calculates time spent on intro
    game_intro()
    pygame.event.get()
    for event in pygame.event.get():                                              #Check for any events
        if event.type == pygame.QUIT:                                            #If user clicked close
            inPlay= 3                                                                         #Flag that we are done so we exit this loop
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:                                                     #If space pressed exit intro screen
        break
    
inPlay=1

#Main Game:
while inPlay==1:
    pygame.event.get()
    for event in pygame.event.get():                                             #Check for any events
        if event.type == pygame.QUIT:                                           #If user clicked close
            inPlay==3                                                                       #Flag that we are done so we exit this loop
            
#Check user input
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and speedX==0 :
        speedX = -HSPEED
        speedY = 0
        
    if keys[pygame.K_RIGHT] and speedX==0:
        speedX = HSPEED
        speedY = 0
        
    if keys[pygame.K_UP] and speedY==0:
        speedX = 0
        speedY = -VSPEED
        
    if keys[pygame.K_DOWN] and speedY==0:
        speedX = 0
        speedY = VSPEED
        
    if applex==segx[0] and appley==segy[0]:                              #Actions if apple eaten
        segx.append(segx[-1])                                                       #Assign the same x and y coordinates
        segy.append(segy[-1])                                                       # as those of the last segment
        applex=randint(1,WIDTH/30-1)*30                                     #Generates new x,y for apple
        appley=randint(1,HEIGHT/30-1)*30
        score+=1
        origTime+=3
        eat.play()
        badx=randint(1,WIDTH/30-1)*30                                       #Generate new x,y for bad apple too
        bady=randint(1,HEIGHT/30-1)*30
        if score==10 or score==20 or score==30 or score==40 or score==50: #Increase speed every 10 apples until lvl50
            game_speed-=10
            
    if badx==segx[0] and bady==segy[0]:                                     #Action if poison apple eaten
        segx.remove(segx[-1])                                                        #assign the same x and y coordinates
        segy.remove(segy[-1])                                                        # as those of the last segment
        score-=1
        origTime-=5
        badx=randint(1,WIDTH/30-1)*30                                         #Generate new x,y for bad apple
        bady=randint(1,HEIGHT/30-1)*30
        bad.play()

#Moving the segments
    for i in range(len(segx)-1,0,-1):                                               #Start from the tail, and go backwards:
        segx[i]=segx[i-1]                                                                #Every segment takes the coordinates
        segy[i]=segy[i-1]                                                                # of the previous one

#Moving the head
    segx[0] = segx[0] + speedX
    segy[0] = segy[0] + speedY
    
#Quit game if length is 0, snake leaves screen, collosion or timer ends
    if len(segx)==1 or segx[0]>=WIDTH-BODY_SIZE or segx[0]<=BODY_SIZE or segy[0]>=HEIGHT-BODY_SIZE or segy[0]<=BODY_SIZE or timer()==True or snake_collosion()==True:
        inPlay=2

#Update the screen
    redraw_screen()
    timer()
    pygame.time.delay(game_speed)

#End screen;
while inPlay==2:
    outro()
    pygame.event.get()
    for event in pygame.event.get():       
        if event.type == pygame.QUIT:       
            inPlay= 3                         
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:                                                    #If space pressed exit game
        pygame.quit()                                                                            #Always quit pygame when done!
