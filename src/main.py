import pygame
import random
import math

size = (1000, 800)

limits = ((50, 50, -10), (size[0]-50, size[1]-50, 10000))

vec2 = pygame.math.Vector2
vec3 = pygame.math.Vector3

objects = []
should_split = False
split_lock = False
bounce_spread = 40
score = 0

def load_image(path):
    return pygame.image.load(path)

class Object:
    def __init__(self, x=0, y=0) -> None:
        self.size = pygame.math.Vector2(50, 50)
        self.pos =  pygame.math.Vector3(x, y, 0)
        self.vel =  pygame.math.Vector3(0, 0, 0)
        self.acc =  pygame.math.Vector3(0, 0, 0)
        self.forces = []
        self.one_forces = []
        self.friction = 0.4
        self.gravity = pygame.math.Vector3(0, 0, -3)
        self.mass = 2

    def update(self):
        self.acc = pygame.math.Vector3(0, 0, 0)
        
        for f in self.forces:
            self.acc = self.acc + f
        for f in self.one_forces:
            self.acc = self.acc + f
        self.one_forces = []
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
            if self.pos.z<limits[1][2]:
                self.pos.z += self.vel.z
        
        self.pos.z = max(0, self.pos.z)
        
        
        if(self.vel.length()<=0.1 and self.acc.length()<=0.1):
            self.vel = pygame.math.Vector3()

class Image:
    slimes = [
        'img/slime1.png',
        'img/slime2.png',
    ]
    balls = [
        'img/ball1.png',
    ]
    ball_shadow = 'img/ball1_shadow.png'

class Animated(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.advancement = 0
        self.sprites = []
        self.current_sprite = 0
        self.elapsed = 0
        self.selapsed = 0
        self.sprite_offset = pygame.math.Vector2(0,0)
        self.shadow_spr = load_image(Image.ball_shadow)
        self.scrouch = 1
        
        
    def draw(self):
        if len(self.sprites)>self.current_sprite:            
            self.shadow_spr = pygame.transform.scale(self.shadow_spr, (self.size.x, self.size.y))
            screen.blit(self.shadow_spr, self.pos.xy - self.size/2)
            
            self.sprites[self.current_sprite] = pygame.transform.scale(self.sprites[self.current_sprite], (self.scrouch*self.size.x, 1/self.scrouch*self.size.y))
            screen.blit(self.sprites[self.current_sprite], self.pos.xy - pygame.math.Vector2(0, self.pos.z) + self.sprite_offset - vec2(self.scrouch*self.size.x, 1/self.scrouch*self.size.y)/2)
            if self.elapsed > 10:
                self.current_sprite=(self.current_sprite+1)%len(self.sprites)
                self.elapsed = 0
            else:
                self.elapsed += 1
            
            if self.selapsed > 2:
                self.scrouch = max(1, (self.scrouch-1)*0.5+1)
                self.selapsed = 0
            else:
                self.selapsed +=1


class Player(Animated):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.sprites = [load_image(img) for img in Image.slimes]

        self.speed = 10
        self.size = vec2(200, 200)
        self.forces = [pygame.math.Vector3(0,0,0), vec3()]
        self.input_rate = 5

    def update(self):
        global split_lock
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
        
        if keys[pygame.K_SPACE]:
            if not split_lock: self.split()
            split_lock = True
        else:
            split_lock = False

        if self.forces[0].length()>0:
            self.forces[0].normalize_ip()
            self.forces[0]*=self.input_rate
        
        self.collide()
        
        if random.random()>0.9:
            self.forces[1] = vec3(random.random()-0.5, random.random()-0.5, random.random()-0.5).normalize()*random.random()*0.2
    
    def collide(self):
        others = [o for o in objects if o!=self and type(o)==Player]
        for other in others:
            if (other.pos-self.pos).length()<(self.size.x/2+other.size.x/2)*0.6:
                normal = (other.pos-self.pos).normalize()*10
                other.one_forces.append(normal)
                self.one_forces.append(-normal)

    def draw(self):
        super().draw()
    
    def split(self):
        global should_split
        should_split = True
        # objects.append(Player(self.size.x/2, self.size.y/2))
        # self.size /= 2
    
    def shrink(self):
        self.size *= 0.8
        self.mass *= 0.8
    
    def sploutch(self):
        self.scrouch = 1.8



class Ball(Animated):
    def __init__(self, x, y, initSize=10):
        super().__init__(x, y)
        self.sprites = [load_image(img) for img in Image.balls]
        
        self.pos.z = 10
        self.sprite_offset = pygame.math.Vector2(0,0)
        self.forces = [pygame.math.Vector3()]
        
        rand_ang = math.pi/4 + (math.pi/2) * random.random()#random.randint(0,3)
        spd = 5 + random.random() * 3
        self.vel.x = math.cos(rand_ang) * spd
        self.vel.y = math.sin(rand_ang) * spd
        self.vel.z = 20
        
        self.bounce_mult = 10
        
        # self.gravity = pygame.math.Vector3(0, 0, -3)
        self.mass = 10
        self.friction = 0.1
    
    def update(self):
        super().update()
        
        if self.pos.z < 0:
            self.one_forces.append(0.8 * vec3(0, 0, abs(self.vel.z) * self.bounce_mult))
            self.vel.z = 0
            self.pos.z = 0
            
        do_rand = False
        if not(0 <= self.pos.x < size[0]):
            self.vel.x *= -1
        if not(0 <= self.pos.y < size[1]):
            self.vel.y *= -1
        
        if do_rand:
            ang = math.atan2(self.vel.y, self.vel.x)
            ang += (random.random() - 0.5) * 0.1
            norm = self.vel.length()
            self.vel.x = norm * math.cos(ang)
            self.vel.y = norm * math.sin(ang)
        
        self.collide()
            

    def draw(self):
        super().draw()
    
    def collide(self):
        slimes = [o for o in objects if type(o)==Player]
        for slime in slimes:
            if (slime.pos-self.pos).length()<(self.size.x/2+slime.size.x/2)*1.2:
                self.one_forces.append(vec3(-self.vel.x+(2*random.random()-1)*5, -self.vel.y+(2*random.random()-1)*bounce_spread, 100))
                slime.sploutch()
                return


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
font = pygame.font.Font('Roboto-Regular.ttf', 16)

while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
    
    objects.sort(key = lambda x: x.pos.y)
    # --- Game logic should go here
    for object in objects:
        object.update()
    
    if should_split:
        balls = [o for o in objects if type(o)==Player]
        balls.sort(key=lambda x: x.size.x)
        balls[-1].shrink()
        np = Player(balls[-1].pos.x, balls[-1].pos.y)
        np.size = vec2(balls[-1].size.x, balls[-1].size.y)
        f = vec3(random.random()-0.5, random.random()-0.5, random.random()).normalize()*min(0.6, random.random())*100
        np.one_forces.append(f)
        balls[-1].one_forces.append(-f)
        objects.append(np)
    
    should_split = False

    # --- Drawing code should go here
    screen.fill(white)
    for object in objects:
        object.draw()
    
    img = font.render(str(score), True, black)
    screen.blit(img, (10, 10))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()