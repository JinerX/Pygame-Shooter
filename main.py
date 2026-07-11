import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 400

ACTIVE = True

class CharacterTests:
    def __init__(self) -> None:
        self.pos = (20,20)

    def draw(self, screen):
        pygame.draw.circle(screen, "Red", self.pos, 10)
    
    def update_pos(self, new_pos):
        self.pos = new_pos




test_char = CharacterTests()
pos = (20,20)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My game")
clock = pygame.time.Clock()

while ACTIVE:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        pos = (pos[0]+1, pos[1])
        test_char.update_pos(pos)
        test_char.draw(screen)

        print("Hello world")
    # pygame.draw.circle(screen, "Red", (40,40), 20)
    # pygame.display.update()


pygame.quit()