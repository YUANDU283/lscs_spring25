from settings import *
import json

# Displaying stuff--------------------------------------------------------------------------------
def display_cookie(screen, mouse):
    # Displays the cookie; if mouse hovered over, changes color
    if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
        pygame.draw.rect(screen,color_light,[width/2,height/2,140,40]) 
    else: 
        pygame.draw.rect(screen,color_dark,[width/2,height/2,140,40]) 
    screen.blit(cookie_text , cookie_pos) 

def display_cookie_stats(cookies, cps):
    # Displays number of cookies, cps
    tmp_cookies = round(cookies, 1)
    cookie_num_text = smallfont.render(f"Cookies: {tmp_cookies}" , True , color) 
    cps_text = tinyfont.render(f"CPS: {cps}" , True , color)
    screen.blit(cookie_num_text , cookie_num_pos)
    screen.blit(cps_text, (cookie_num_pos[0], cookie_num_pos[1]+30))

def buy_buttons(mouse, screen, buildings):
    # Code to display buttons
    for building in buildings.keys():
        buy_width, buy_height = buildings[building]["button"]["dim"]
        pos = buildings[building]["button"]["pos"]
        
        if pos[0] <= mouse[0] <= pos[0]+buy_width and pos[1] <= mouse[1] <= pos[1]+buy_height: 
            pygame.draw.rect(screen,color_light,[pos[0], pos[1],buy_width, buy_height])    
        else: 
            pygame.draw.rect(screen,color_dark,[pos[0], pos[1],buy_width, buy_height]) 

        building_text = smallfont.render(f" {building}   {buildings[building]["num"]}" , True , color) 
        price_text = tinyfont.render(f"     {buildings[building]["price"]} cookies", True, color)
        image = pygame.image.load(buildings[building]["image"])
        screen.blit(building_text , pos) 
        screen.blit(price_text, (pos[0], pos[1] + 30))
        screen.blit(image, (pos[0] + buy_dim[0], pos[1]))

def loadsave_button(mouse, screen):
    # Display the load and save game buttons
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

# Game mechanics stuff----------------------------------------------------------------------------
def add_buildings(mouse, cookies, buildings):
    # Code to buy buildings
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
    return cookies, buildings

def update_cps(cookies, buildings):
    # Code to add cookies
    cps = 0
    for building in buildings.keys():
        cps += buildings[building]["num"]*buildings[building]["cps"]
    if pygame.time.get_ticks() % (framerate//ticks_per_frame) == 0:
        cookies += cps/ticks_per_frame
    return cookies, cps

def updateshift(event, shift):
    if event.key == pygame.K_w:
        shift[1] -= shiftspeed
    if event.key == pygame.K_s:
        shift[1] += shiftspeed
    if event.key == pygame.K_a:
        shift[0] -= shiftspeed
    if event.key == pygame.K_d:
        shift[0] += shiftspeed
# Saving and loading the game stuff---------------------------------------------------------------
def save_game():
    save_file = os.getcwd()+"/saves/"+str(input("What file to save: "))+".json"
    if len(save_file) == 0:
        return 1
    game_state = {"buildings": buildings, "cookies": cookies}
    with open(save_file, "w") as fileo:
        json.dump(game_state, fileo)

def load_game():
    load_file = os.getcwd()+"/saves/" +str(input("What file to load from: "))+".json"
    with open(load_file, "r") as fileo:
        save = json.load(fileo)
    buildings = save["buildings"]
    cookies = save["cookies"]
    return cookies, buildings

def click_save(mouse, c, b):
    if save_pos[0] <= mouse[0] <= save_pos[0]+save_dim[0] and save_pos[1] <= mouse[1] <= save_pos[1]+save_dim[1]:
        c, b = load_game()
    elif save_pos[0] <= mouse[0] <= save_pos[0]+save_dim[0] and save_pos[1]+save_dim[1]+10 <= mouse[1] <= save_pos[1]+save_dim[1]+save_dim[1]+10:
        save_game()
    #print(c, b)
    return c, b

# Achievements stuff------------------------------------------------------------------------------
def achievements_button(mouse, screen):
    if achieve_pos[0] <= mouse[0] <= achieve_pos[0]+achieve_dim[0] and achieve_pos[1] <= mouse[1] <= achieve_pos[1]+achieve_dim[1]:
        pygame.draw.rect(screen, color_light, [achieve_pos[0], achieve_pos[1], achieve_dim[0], achieve_dim[1]])
    else:
        pygame.draw.rect(screen, color_dark, [achieve_pos[0], achieve_pos[1], achieve_dim[0], achieve_dim[1]])

def click_achieve(mouse):
    if not(achieve_pos[0] <= mouse[0] <= achieve_pos[0]+achieve_dim[0] and achieve_pos[1] <= mouse[1] <= achieve_pos[1]+achieve_dim[1]):
        return
    screen2 = pygame.display.set_mode((width, height))
    while True:
        mouse = pygame.mouse.get_pos()
        mouserect = pygame.Rect(mouse[0], mouse[1], 1, 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen2.fill(BACKGROUND)
        for achieve in achieves.keys():
            achieve_rect = pygame.Rect(achieves[achieve]["pos"][0], achieves[achieve]["pos"][1], achieves[achieve]["dim"][0], achieves[achieve]["dim"][1])
            if mouserect.colliderect(achieve_rect):
                pygame.draw.rect(screen2, color_light, achieve_rect)
                text_surface = millifont.render(achieves[achieve]["description"], True, color)
                screen2.blit(text_surface, mouse)
            else:
                pygame.draw.rect(screen2, color_dark, achieve_rect)
                image_surface = pygame.image.load(achieves[achieve]["image"])
                screen2.blit(image_surface, achieves[achieve]["pos"])
                text_surface = tinyfont.render(achieves[achieve]["name"], True, color)
                screen2.blit(text_surface, mouse)
        pygame.display.update()
        clock.tick(framerate)















#  /////     //////   ////////   ////////
# //   //      //          //         //   
# //   //      //         //         //
# // //        //        //         //
# //  //       //       //         //
# //   //      //      //         //
# //    //   //////   ////////   ////////
