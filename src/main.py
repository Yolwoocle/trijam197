import pygame 

def load_image(path):
    return pygame.image.load(path)

class Object:
    def __init__(self, x, y) -> None:
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)


class Image:
    test = load_image('img/test.png')


    def update(self):
        ...
    
    def draw(self):
        super().draw()


class Animated(Object):
    def __init__(self):
        self.advancement = 0
        self.sprites = []
        
    def draw(self):
        ...


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
objects = []

while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False

    # --- Game logic should go here
    for object in objects:
        object.update()


    # --- Drawing code should go here
    for object in objects:
        screen.fill(WHITE)
        object.draw()
    
    # pygame.draw.rect(screen, RED, [55, 200, 100, 70],0)
    # pygame.draw.line(screen, GREEN, [0, 0], [100, 100], 5)
    # pygame.draw.ellipse(screen, BLACK, [20,20,250,100], 2)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()