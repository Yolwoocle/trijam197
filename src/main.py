import pygame 

def load_image(path):
    return pygame.image.load(path)

class Object:
    def __init__(self, x, y) -> None:
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)


class Image:
    test = load_image('img/test.png')



class Animated(Object):
    def __init__(self):
        self.advancement = 0
        self.sprites = []


class Player(Animated):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.image = Image.test

class Ball(Object):
    def __init__(self, initSize=10):
        self.size = initSize
    
    def split(self):
        self.size /= 2


pygame.init()

# Define some colors
black = ( 0, 0, 0)
white = ( 255, 255, 255)
green = ( 0, 255, 0)
red   = ( 255, 0, 0)

# Open a new window
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My First Game")

# The loop will carry on until the user exits the game (e.g. clicks the close button).
carryOn = True

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

player = Player(size[0]/2, size[1]/2)

# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            carryOn = False # Flag that we are done so we can exit the while loop

    # --- Drawing code should go here
    # First, clear the screen to white. 
    screen.fill(white)
    #The you can draw different shapes and lines or add text to your background stage.
    player.draw()

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

#Once we have exited the main program loop we can stop the game engine:
pygame.quit()