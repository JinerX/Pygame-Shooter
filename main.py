import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 400

ACTIVE = True

SPEED_CHANGE = 90
MAX_SPEED = 9000


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, *groups, deceleration_factor=0.1, max_speed=10000):
        super().__init__(*groups)
        self.image = pygame.surface.Surface((20,20), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center = pos)
        self.velocity = pygame.Vector2(0,0)
        self.deceleration_factor = deceleration_factor
        self.max_speed = max_speed
        pygame.draw.circle(self.image, "Red", (10,10), 10)
    
    def update(self, acc, dt):
        stopping = pygame.Vector2(- (self.deceleration_factor * self.velocity.x), -(self.deceleration_factor * self.velocity.y))
        self.velocity += acc + stopping

        if self.velocity.x > self.max_speed:
            self.velocity.x = self.max_speed
        if self.velocity.x < -self.max_speed:
            self.velocity.x = -self.max_speed
        if self.velocity.y > self.max_speed:
            self.velocity.y = self.max_speed
        if self.velocity.y < -self.max_speed:
            self.velocity.y = -self.max_speed
        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My game")
clock = pygame.time.Clock()
pos = (40,40)

player_group = pygame.sprite.GroupSingle()
player = Player(pos, player_group, max_speed=MAX_SPEED)

while ACTIVE:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    acc = pygame.Vector2(0,0)
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_RIGHT]:
        acc.x += SPEED_CHANGE
    if keys[pygame.K_LEFT]:
        acc.x -= SPEED_CHANGE
    if keys[pygame.K_UP]:
        acc.y -= SPEED_CHANGE
    if keys[pygame.K_DOWN]:
        acc.y += SPEED_CHANGE
    player_group.update(acc, dt)


    # all_sprites.update(pos)
    screen.fill("blue")
    player_group.draw(screen)

    pygame.display.update()


pygame.quit()