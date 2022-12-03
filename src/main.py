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
        
    def draw(self):
        ...


class Player(Animated):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.sprites = [Image.test]

        self.image = Image.test
        self.friction = 0.97

    def update(self):
        self.pos += self.vel * self.friction

    def draw(self):
        ...

        

class Ball(Animated):
    def __init__(self, initSize=10):
        self.size = initSize
    
    def split(self):
        self.size /= 2


pygame.init()

# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red   = (255, 0, 0)

size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Trijam 197")

carryOn = True

clock = pygame.time.Clock()

# -------- Main Program Loop -----------
objects = [
    Player(size[0]/2, size[1]/2)
]

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
    
    pygame.display.flip()

    clock.tick(60)

pygame.quit()