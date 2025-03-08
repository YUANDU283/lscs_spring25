import pygame 
import sys 
import math
import os
  
  
# initializing the constructor 
pygame.init() 

res = (720,600) 
screen = pygame.display.set_mode(res) 
  
color = (255,255,255) 
color_light = (170,170,170) 
color_dark = (100,100,100) 
width = screen.get_width()  
height = screen.get_height() 
smallfont = pygame.font.SysFont('Corbel',35) 
cookie_text = smallfont.render('cookie' , True , color) 
cookies = 0
cookie_num_pos = (width//4, height//4)
cookie_pos = (width//2, height//2)
time = 0
framerate = 60
clock = pygame.time.Clock()
buy_dim = (150, 30)
buildings = {"cursor": {"image": os.getcwd()+"/sprites/cursor.png", "num": 0, "cps": 0.1, "price": 10, "button":{"pos":(30, 30), "dim":buy_dim}}}
buy_scale = 1.1
cps = 0

def display_cookie(screen, mouse):
    # stores the (x,y) coordinates into 
    # the variable as a tuple 
      
    # if mouse is hovered on a button it 
    # changes to lighter shade  
    if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
        pygame.draw.rect(screen,color_light,[width/2,height/2,140,40]) 
          
    else: 
        pygame.draw.rect(screen,color_dark,[width/2,height/2,140,40]) 
      
    # superimposing the text onto our button 
    screen.blit(cookie_text , cookie_pos) 

def display_cookie_stats():
    cookie_num_text = smallfont.render(f"Cookies: {cookies}" , True , color) 
    cps_text = smallfont.render(f"CPS: {cps}" , True , color)
    screen.blit(cookie_num_text , cookie_num_pos)
    screen.blit(cps_text, (cookie_num_pos[0], cookie_num_pos[1]+30))


def buy_button(building, pos, mouse, screen):
# stores the (x,y) coordinates into 
    # the variable as a tuple 

    buy_width, buy_height = buildings[building]["button"]["dim"]
      
    # if mouse is hovered on a button it 
    # changes to lighter shade  
    if pos[0] <= mouse[0] <= pos[0]+buy_width and pos[1] <= mouse[1] <= pos[1]+buy_height: 
        pygame.draw.rect(screen,color_light,[pos[0], pos[1],buy_width, buy_height]) 
          
    else: 
        pygame.draw.rect(screen,color_dark,[pos[0], pos[1],buy_width, buy_height]) 
      
    # superimposing the text onto our button 

    building_text = smallfont.render(f"{building} Num: {buildings[building]["num"]} Price: {buildings[building]["price"]}" , True , color) 
    screen.blit(building_text , pos) 


def add_buildings(mouse):
    global cookies
    for building in buildings.keys():
        pos = buildings[building]["button"]["pos"]
        dim = buildings[building]["button"]["dim"]
        if pos[0] <= mouse[0] <= pos[0]+dim[0] and pos[1] <= mouse[1] <= pos[1]+dim[1]:
            if cookies < buildings[building]["price"]:
                print(f"Not enough money for {building}")
                continue
            buildings[building]["num"] += 1
            cookies -= buildings[building]["price"]
            buildings[building]["price"] *= buy_scale
            buildings[building]["price"] = math.trunc(buildings[building]["price"])

def cps_buildings():
    global cookies
    global cps
    cps = 0
    for building in buildings.keys():
        cps += buildings[building]["num"]*buildings[building]["cps"]
    if time % framerate == 0:
        cookies += cps


while True: 
    mouse = pygame.mouse.get_pos() 
    for event in pygame.event.get(): 
          
        if event.type == pygame.QUIT: 
            pygame.quit() 
              
        #checks if a mouse is clicked 
        if event.type == pygame.MOUSEBUTTONDOWN: 
              
            #if the mouse is clicked on the 
            # button the game is terminated 
            if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
                cookies += 1

            add_buildings(mouse)

    # fills the screen with a color 
    screen.fill((60,25,60)) 
    cookies = round(cookies, 1)
    cps_buildings()
    display_cookie(screen, mouse)   
    display_cookie_stats()
    buy_button("cursor", (30, 30), mouse, screen)       
    # updates the frames of the game 
    pygame.display.update() 
    time += 1
    clock.tick(framerate)


# To do:
# 1. More buildings
# 2. Images for buildings
# 3. Upgrades
# 4. Achievements
# 5. Game mechanics(grandmapocypse...)