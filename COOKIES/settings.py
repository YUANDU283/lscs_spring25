import pygame
import os

# pygame stuff 
pygame.init() 
res = (720,600) 
#res = (1440, 1050)#big screen
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
millifont = pygame.font.SysFont('Corbel', 5)

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
achieve_pos = (3*width//4, 3*height//4)
achieve_dim = (80, 30)

# Game mechanics stuff
running = True
shift = (0,0)
shiftspeed = 3
cookies = 0
buy_scale = 1.1
cps = 0
clickcps = 1
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
                                   "dim": buy_dim}},
            "bank": {"image": os.getcwd()+"/sprites/bank.png", 
                        "num": 0, 
                        "cps": 320000, 
                        "price": 1000000, 
                        "button": {"pos": (30, 330), 
                                   "dim": buy_dim}},
            "temple": {"image": os.getcwd()+"/sprites/bank.png", 
                        "num": 0, 
                        "cps": 6400000, 
                        "price": 10000000, 
                        "button": {"pos": (30, 390), 
                                   "dim": buy_dim}},
            "wiz tower": {"image": os.getcwd()+"/sprites/bank.png", 
                        "num": 0, 
                        "cps": 128000000, 
                        "price": 100000000, 
                        "button": {"pos": (30, 450), 
                                   "dim": buy_dim}},
            "shipment": {"image": os.getcwd()+"/sprites/bank.png", 
                        "num": 0, 
                        "cps": 2560000000, 
                        "price": 1000000000, 
                        "button": {"pos": (30, 510), 
                                   "dim": buy_dim}},
            "alch lab": {"image": os.getcwd()+"/sprites/bank.png", 
                        "num": 0, 
                        "cps": 5120000, 
                        "price": 10000000000, 
                        "button": {"pos": (30, 570), 
                                   "dim": buy_dim}},
            "portal": {"image": os.getcwd()+"/sprites/bank.png", 
                        "num": 0, 
                        "cps": 1024000, 
                        "price": 100000000000, 
                        "button": {"pos": (30, 630), 
                                   "dim": buy_dim}},
            "time mach": {"image": os.getcwd()+"/sprites/bank.png", 
                        "num": 0, 
                        "cps": 20480000000, 
                        "price": 1000000000000, 
                        "button": {"pos": (30, 690), 
                                   "dim": buy_dim}},
            "antim condens": {"image": os.getcwd()+"/sprites/bank.png", 
                        "num": 0, 
                        "cps": 4096000000000, 
                        "price": 10000000000000, 
                        "button": {"pos": (30, 750), 
                                   "dim": buy_dim}},
            "prism": {"image": os.getcwd()+"/sprites/bank.png", 
                        "num": 0, 
                        "cps": 81920000000000, 
                        "price": 100000000000000, 
                        "button": {"pos": (30, 810), 
                                   "dim": buy_dim}},
            "chancemaker": {"image": os.getcwd()+"/sprites/bank.png", 
                        "num": 0, 
                        "cps": 163840000000000, 
                        "price": 1000000000000000, 
                        "button": {"pos": (30, 870), 
                                   "dim": buy_dim}},
            "fract engin": {"image": os.getcwd()+"/sprites/bank.png", 
                        "num": 0, 
                        "cps": 3276800000000000, 
                        "price": 10000000000000000, 
                        "button": {"pos": (30, 930), 
                                   "dim": buy_dim}},
            "java cons": {"image": os.getcwd()+"/sprites/bank.png", 
                        "num": 0, 
                        "cps": 65536000000000000, 
                        "price": 100000000000000000, 
                        "button": {"pos": (30, 990), 
                                   "dim": buy_dim}},
            "idleverse": {"image": os.getcwd()+"/sprites/bank.png", 
                        "num": 0, 
                        "cps": 131072000000000000, 
                        "price": 1000000000000000000, 
                        "button": {"pos": (30, 1050), 
                                   "dim": buy_dim}},}

achieves = {"Million": {"image": os.getcwd()+f"/sprites/achievements/million.png", 
                        "name": "million", 
                        "description": "Bake one million cookies", 
                        "pos": (30, 30),
                        "dim": buy_dim}}
