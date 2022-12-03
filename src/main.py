import pygame

size = (700, 500)

limits = ((0, 0, -1000), (700, 500, 10000))


def load_image(path):
    return pygame.image.load(path)

class Object:
    def __init__(self, x=0, y=0) -> None:
        self.size = pygame.math.Vector2(50, 50)
        self.pos =  pygame.math.Vector3(x, y, 0)
        self.vel =  pygame.math.Vector3(0, 0, 0)
        self.acc =  pygame.math.Vector3(0, 0, 0)
        self.forces = []
        self.friction = 0.7
        self.gravity = 0
        self.mass = 2

    def update(self):
        self.acc = pygame.math.Vector3(0, 0, 0)
        
        for f in self.forces:
            self.acc = self.acc + f
        self.acc += self.gravity
        
        if(self.vel.length()>0):
            self.acc -= self.friction * self.vel.normalize()*(self.vel.length()**1.2)
        self.vel += self.acc / self.mass

        if self.vel.x>0:
            if self.pos.x<limits[1][0]:
                self.pos.x += self.vel.x
        
        if self.vel.x<0:
            if self.pos.x>limits[0][0]:
                self.pos.x += self.vel.x
        
        if self.vel.y>0:
            if self.pos.y<limits[1][1]:
                self.pos.y += self.vel.y

        if self.vel.y<0:
            if self.pos.y>limits[0][1]:
                self.pos.y += self.vel.y
        
        if self.vel.z<0:
            if self.pos.z>limits[0][2]:
                self.pos.z += self.vel.z
        
        if self.vel.z>0:
            if self.pos.z>limits[1][2]:
                self.pos.z += self.vel.z
        
        
        if(self.vel.length()<=0.1 and self.acc.length()<=0.1):
            self.vel = pygame.math.Vector3()

class Image:
    slimes = [
        load_image('img/slime1.png'),
        load_image('img/slime2.png'),
    ]
    balls = [
        load_image('img/ball1.png'),
    ]

class Animated(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.advancement = 0
        self.sprites = []
        self.current_sprite = 0
        self.elapsed = 0
        self.sprite_offset = pygame.math.Vector2(0,0)
        
    def draw(self):
        if len(self.sprites)>self.current_sprite:
            self.sprites[self.current_sprite] = pygame.transform.scale(self.sprites[self.current_sprite], (self.size.x, self.size.y))
            screen.blit(self.sprites[self.current_sprite], self.pos.xy - pygame.math.Vector2(0, self.pos.z) + self.sprite_offset - self.size/2)
            if self.elapsed > 10:
                self.current_sprite=(self.current_sprite+1)%len(self.sprites)
                self.elapsed = 0
            else:
                self.elapsed += 1

class Player(Animated):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.sprites = Image.slimes

        self.speed = 10
        self.forces = [pygame.math.Vector3(0,0,0)]
        self.input_rate = 5

    def update(self):
        super().update()

        keys = pygame.key.get_pressed()
        self.forces[0] = pygame.math.Vector3()
        if keys[pygame.K_LEFT]: # We can check if a key is pressed like this
            self.forces[0].x += -1
        
        if keys[pygame.K_RIGHT]:
            self.forces[0].x += 1

        if keys[pygame.K_UP]:
            self.forces[0].y += -1

        if keys[pygame.K_DOWN]:
            self.forces[0].y += 1

        if self.forces[0].length()>0:
            self.forces[0].normalize_ip()
            self.forces[0]*=self.input_rate

    def draw(self):
        super().draw()


class Ball(Animated):
    def __init__(self, x, y, initSize=10):
        super().__init__(x, y)
        self.size = initSize
        self.sprites = Image.balls
        self.sprite_offset = pygame.math.Vector2(0,0)
        self.forces = [pygame.math.Vector3()]
        
        self.bounce_force = -30
        
        self.mass = 10
    
    def update(self):
        super().update()
        
        self.forces[0] = pygame.math.Vector3()        
        if self.pos.z < 0:
            self.forces[0].z = -self.bounce_force
        

    def draw(self):
        super.draw()


pygame.init()

# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red   = (255, 0, 0)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Trijam 197")

carryOn = True

clock = pygame.time.Clock()

# -------- Main Program Loop -----------
objects = [
    Player(size[0]/2, size[1]/2),
    Ball(100, 100),
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
        screen.fill(white)
        object.draw()
    
    pygame.display.flip()

    clock.tick(60)

pygame.quit()