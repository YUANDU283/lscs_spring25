import pygame 
#import sys 
#import math
import os
import json
  
  
# pygame stuff 
pygame.init() 
res = (720,600) 
screen = pygame.display.set_mode(res) 
width = screen.get_width()  
height = screen.get_height() 
clock = pygame.time.Clock() # pygame clock
  
# Color stuff
color = (255,255,255) # White color
color_light = (170,170,170) # Light gray color for buy button
color_dark = (100,100,100) # Dark gray color for buy button
BACKGROUND = (60,25,60)

# Font stuff
smallfont = pygame.font.SysFont('Corbel',35) # big font
tinyfont = pygame.font.SysFont('Corbel', 15) # small font

# Time stuff
framerate = 60 # framerate of game(different from ticks)
ticks_per_frame = 20 # when the game updates vs when program updates

# Button stuff
cookie_text = smallfont.render('cookie' , True , color) # Cookie text <-----------replace with image
cookie_num_pos = (width//2, height//4) # Position of cookie stats
cookie_pos = (width//2, height//2) # Position of cookie
buy_dim = (200, 50) # dimensions of the buy button
save_pos = (4*width//5, height//5)
save_dim = (80, 30)

# Game mechanics stuff
cookies = 0
buy_scale = 1.1
cps = 0
buildings = {"cursor": {"image": os.getcwd()+"/sprites/cursor.png", 
                        "num": 0, 
                        "cps": 0.1, 
                        "price": 10, 
                        "button": {"pos": (30, 30), 
                                  "dim": buy_dim}}, 
            "grandma": {"image": os.getcwd()+"/sprites/grandma.png", 
                        "num": 0, 
                        "cps": 20, 
                        "price": 100, 
                        "button": {"pos": (30, 90), 
                                   "dim": buy_dim}}, 
             "farm": {"image": os.getcwd()+"/sprites/farm.png", 
                        "num": 0, 
                        "cps": 400, 
                        "price": 1000, 
                        "button": {"pos": (30, 150), 
                                   "dim": buy_dim}}, 
             "mine": {"image": os.getcwd()+"/sprites/mine.png", 
                        "num": 0, 
                        "cps": 8000, 
                        "price": 10000, 
                        "button": {"pos": (30, 210), 
                                   "dim": buy_dim}}, 
            "factory": {"image": os.getcwd()+"/sprites/factory.png", 
                        "num": 0, 
                        "cps": 16000, 
                        "price": 100000, 
                        "button": {"pos": (30, 270), 
                                   "dim": buy_dim}}}


def display_cookie(screen, mouse):
    # Displays the cookie
      
    # if mouse is hovered on a button it 
    # changes to lighter shade  
    if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
        pygame.draw.rect(screen,color_light,[width/2,height/2,140,40]) 
          
    else: 
        pygame.draw.rect(screen,color_dark,[width/2,height/2,140,40]) 
      
    # superimposing the text onto our button 
    screen.blit(cookie_text , cookie_pos) 

def display_cookie_stats():
    # Displays number of cookies, cps
    tmp_cookies = round(cookies, 1)
    cookie_num_text = smallfont.render(f"Cookies: {tmp_cookies}" , True , color) 
    cps_text = tinyfont.render(f"CPS: {cps}" , True , color)
    screen.blit(cookie_num_text , cookie_num_pos)
    screen.blit(cps_text, (cookie_num_pos[0], cookie_num_pos[1]+30))


def buy_buttons(mouse, screen):
    # Code to display buttons
    for building in buildings.keys():
        buy_width, buy_height = buildings[building]["button"]["dim"]
        pos = buildings[building]["button"]["pos"]
        
        # if mouse is hovered on a button it 
        # changes to lighter shade  
        if pos[0] <= mouse[0] <= pos[0]+buy_width and pos[1] <= mouse[1] <= pos[1]+buy_height: 
            pygame.draw.rect(screen,color_light,[pos[0], pos[1],buy_width, buy_height]) 
            
        else: 
            pygame.draw.rect(screen,color_dark,[pos[0], pos[1],buy_width, buy_height]) 
        
        # superimposing the text onto our button 

        building_text = smallfont.render(f" {building}   {buildings[building]["num"]}" , True , color) 
        price_text = tinyfont.render(f"     {buildings[building]["price"]} cookies", True, color)
        screen.blit(building_text , pos) 
        screen.blit(price_text, (pos[0], pos[1] + 30))

        image = pygame.image.load(buildings[building]["image"])
        screen.blit(image, (pos[0] + buy_dim[0], pos[1]))

def add_buildings(mouse):
    # Code to buy buildings
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
            buildings[building]["price"] = round(buildings[building]["price"])

def update_cps():
    # Code to add cookies
    global cookies
    global cps
    cps = 0
    for building in buildings.keys():
        cps += buildings[building]["num"]*buildings[building]["cps"]
    if pygame.time.get_ticks() % (framerate//ticks_per_frame) == 0:
        cookies += cps/ticks_per_frame


def save_game():
    save_file = os.getcwd()+"/saves/"+str(input("What file to save: "))+".json"
    if len(save_file) == 0:
        return 1
    game_state = {"buildings": buildings, "cookies": cookies}
    with open(save_file, "w") as fileo:
        json.dump(game_state, fileo)

def load_game():
    global cookies, buildings
    load_file = os.getcwd()+"/saves/" +str(input("What file to load from: "))+".json"
    with open(load_file, "r") as fileo:
        save = json.load(fileo)
    buildings = save["buildings"]
    cookies = save["cookies"]

def loadsave_button(mouse, screen):
    if save_pos[0] <= mouse[0] <= save_pos[0]+save_dim[0] and save_pos[1] <= mouse[1] <= save_pos[1]+save_dim[1]:
        pygame.draw.rect(screen, color_light, [save_pos[0], save_pos[1], save_dim[0], save_dim[1]])
        pygame.draw.rect(screen, color_dark, [save_pos[0], save_pos[1]+save_dim[1]+10, save_dim[0], save_dim[1]])
    elif save_pos[0] <= mouse[0] <= save_pos[0]+save_dim[0] and save_pos[1]+save_dim[1]+10 <= mouse[1] <= save_pos[1]+save_dim[1]+save_dim[1]+10:
        pygame.draw.rect(screen, color_light, [save_pos[0], save_pos[1]+save_dim[1]+10, save_dim[0], save_dim[1]])
        pygame.draw.rect(screen, color_dark, [save_pos[0], save_pos[1], save_dim[0], save_dim[1]])
    else:
        pygame.draw.rect(screen, color_dark, [save_pos[0], save_pos[1], save_dim[0], save_dim[1]])
        pygame.draw.rect(screen, color_dark, [save_pos[0], save_pos[1]+save_dim[1]+10, save_dim[0], save_dim[1]])
    
    load_text = tinyfont.render("Load game", True, color)
    save_text = tinyfont.render("Save game", True, color)
    screen.blit(load_text, save_pos)
    screen.blit(save_text, (save_pos[0], save_pos[1]+save_dim[1]+10))

def click_save(mouse):
    if save_pos[0] <= mouse[0] <= save_pos[0]+save_dim[0] and save_pos[1] <= mouse[1] <= save_pos[1]+save_dim[1]:
        load_game()
    elif save_pos[0] <= mouse[0] <= save_pos[0]+save_dim[0] and save_pos[1]+save_dim[1]+10 <= mouse[1] <= save_pos[1]+save_dim[1]+save_dim[1]+10:
        save_game()

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
            click_save(mouse)

    # fills the screen with a color 
    screen.fill(BACKGROUND) 
    update_cps()
    loadsave_button(mouse, screen)
    display_cookie(screen, mouse)   
    display_cookie_stats()
    buy_buttons(mouse, screen)       
    # updates the frames of the game 
    pygame.display.update() 
    #time += 1
    clock.tick(framerate)




# To do:
# 1. More buildings<---done
# 2. Images for buildings<---done
# 3. Upgrades
# 4. Achievements
# 5. Game mechanics(grandmapocypse...)
# 6. Fix rounding issue<---done
# 7. Effects
# 8. JSON save file<---done


# New To Do(3/8/25):
# 1. Clean up code(abstraction, paramaterize)
# 2. Upgrades and achievments
# 3. OOP(classes)
# 6. Make user interface better and sound
# 5. Cookie/milk effects