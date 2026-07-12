import pygame
import sys
import math
import time

pygame.init()

WIDTH, HEIGHT = 800, 400

ACTIVE = True

SPEED_CHANGE = 90
MAX_SPEED = 9000
PROJECTILE_SPEED = 50
SHOOTING_RATE = 0.1
ACC_SCALING = 100

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, *groups, deceleration_factor=0.1, max_speed=10000, proj_group=None):
        super().__init__(*groups)

        # drawing
        self.image = pygame.surface.Surface((20,20), pygame.SRCALPHA)
        self.pos = pygame.Vector2(pos)
        self.rect = self.image.get_rect(center = self.pos)
        pygame.draw.circle(self.image, "Pink", (10,10), 10)

        # movement
        self.velocity = pygame.Vector2(0,0)
        self.deceleration_factor = deceleration_factor
        self.max_speed = max_speed

        # shooting
        self.proj_group = proj_group
        self.projectile_speed = PROJECTILE_SPEED
        self.shooting_rate = SHOOTING_RATE
        self.projectiles = []
        self.last_shot = None
    
    def update(self, acc, shoot_dir, dt):
        self.update_speed(acc, dt)
        self.update_shoot(shoot_dir, dt)
    
    def update_speed(self, acc, dt):
        stopping = pygame.Vector2(- (self.deceleration_factor * self.velocity.x), -(self.deceleration_factor * self.velocity.y))
        self.velocity += ACC_SCALING * (acc + stopping) * dt

        if self.velocity.x > self.max_speed:
            self.velocity.x = self.max_speed
        if self.velocity.x < -self.max_speed:
            self.velocity.x = -self.max_speed
        if self.velocity.y > self.max_speed:
            self.velocity.y = self.max_speed
        if self.velocity.y < -self.max_speed:
            self.velocity.y = -self.max_speed
        self.pos.x += self.velocity.x * dt
        self.pos.y += self.velocity.y * dt
        self.rect.center = self.pos
    
    def update_shoot(self, shoot_dir, dt):
        if shoot_dir is None:
            return
        if not self.can_shoot():
            return
        velocity = (self.projectile_speed * shoot_dir[0], self.projectile_speed * shoot_dir[1])
        proj = Projectile(True, velocity, self.pos, self.proj_group)
        self.projectiles.append(proj)
        self.clear_projectiles()
    
    def clear_projectiles(self):
        for proj in self.projectiles:
            if proj.pos.x < -10 or proj.pos.y < -10 or proj.pos.x > WIDTH or proj.pos.y > HEIGHT:
                del proj
    
    def can_shoot(self):
        if self.last_shot is None:
            self.last_shot = time.time()
            return True
        elif (time.time() - self.last_shot) > self.shooting_rate:
            print(time.time() - self.last_shot)
            self.last_shot = time.time()
            return True
        return False

class Projectile(pygame.sprite.Sprite):
    def __init__(self, friendly,velocity,pos, *groups):
        super().__init__(*groups)
        self.friendly = friendly
        self.velocity = pygame.Vector2(velocity)
        self.pos = pygame.Vector2(pos)
        self.image = pygame.surface.Surface((4,4), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center = self.pos)
        pygame.draw.circle(self.image, "Green", (2,2), 2)
    
    def update(self, dt):
        self.pos += self.velocity * dt
        self.rect.center = self.pos

# class Blocade()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My game")
clock = pygame.time.Clock()
pos = (40,40)
pos_proj = (20,20)

player_group = pygame.sprite.GroupSingle()

fr_projectile_group = pygame.sprite.Group()
test_projectile = Projectile(True, (100,200), pos_proj, fr_projectile_group)

player = Player(pos, player_group, max_speed=MAX_SPEED, proj_group=fr_projectile_group)


while ACTIVE:
    dt = clock.tick(120) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    
    acc = pygame.Vector2(0,0)
    shoot_dir = None

    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    
    if keys[pygame.K_RIGHT]:
        acc.x += SPEED_CHANGE
    if keys[pygame.K_LEFT]:
        acc.x -= SPEED_CHANGE
    if keys[pygame.K_UP]:
        acc.y -= SPEED_CHANGE
    if keys[pygame.K_DOWN]:
        acc.y += SPEED_CHANGE
    if mouse[0]:
        mouse_pos = pygame.mouse.get_pos()
        relative_pos = (mouse_pos[0] - player.pos[0], mouse_pos[1] - player.pos[1])
        length = math.sqrt(relative_pos[0] ** 2 + relative_pos[1] ** 2)
        pos_scaled = (relative_pos[0] / length, relative_pos[1] / length)
        shoot_dir = pos_scaled
    player_group.update(acc, shoot_dir, dt)
    fr_projectile_group.update(dt)


    screen.fill("blue")
    player_group.draw(screen)
    fr_projectile_group.draw(screen)

    pygame.display.update()


pygame.quit()