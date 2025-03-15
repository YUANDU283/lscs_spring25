import pygame 
#import sys 
from gamelogic import *
    
while running: 
    #print(cookies)
    mouse = pygame.mouse.get_pos() 
    clickcps = max(0.05*cookies, 1)
    for event in pygame.event.get(): 
          
        if event.type == pygame.QUIT: 
            pygame.quit()
            running = False
        #checks if a mouse is clicked 
        if event.type == pygame.MOUSEBUTTONDOWN: 
              
            #if the mouse is clicked on the 
            # button the game is terminated 
            if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
                cookies += clickcps
            cookies, buildings = add_buildings(mouse, cookies, buildings)
            cookies, buildings = click_save(mouse, cookies, buildings)
            click_achieve(mouse)
        if event.type == pygame.KEYDOWN:
            shift = updateshift(event, shift)

    # fills the screen with a color 
    screen.fill(BACKGROUND) 
    cookies, cps = update_cps(cookies, buildings)
    loadsave_button(mouse, screen)
    display_cookie(screen, mouse)   
    display_cookie_stats(cookies, cps)
    buy_buttons(mouse, screen, buildings)       
    # updates the frames of the game 
    pygame.display.update() 
    #time += 1
    clock.tick(framerate)

save_game()


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
# 1. Clean up code(abstraction, paramaterize)<------done
# 2. Upgrades and achievments<-Do this
# 3. OOP(classes)
# 6. Make user interface better and sound<-Do this
# 5. Cookie/milk effects