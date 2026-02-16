import pygame
import math
import random

# ---------------- INITIAL SETUP ---------------- #
pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("OOP Game Version")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# ---------------- LOAD IMAGES (LOAD ONCE ONLY) ---------------- #
bg_image = pygame.image.load('./img/bg.jpg').convert()
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

ship_image = pygame.image.load("./img/spaceship.png").convert_alpha()
ship_image = pygame.transform.scale(ship_image, (70, 70))


# ---------------- SHIP CLASS ---------------- #
class Ship:
    def __init__(self, image):
        self.image = image
        self.x = 350
        self.y = 500
        self.velocity = 5
        self.velocity_x = 0

    def move(self):
        self.x += self.velocity_x

        if self.x <= 0:
            self.x = 0
        elif self.x >= WIDTH - 70:
            self.x = WIDTH - 70

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


# ---------------- BULLET CLASS ---------------- #
class Bullet:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 10
        self.height = 20
        self.velocity = -8
        self.state = "ready"

    def fire(self, ship_x, ship_y):
        if self.state == "ready":
            self.state = "fire"
            self.x = ship_x + 30
            self.y = ship_y

    def move(self):
        if self.state == "fire":
            self.y += self.velocity
            if self.y < 0:
                self.state = "ready"

    def draw(self, screen):
        if self.state == "fire":
            pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))


# ---------------- BLOCK CLASS ---------------- #
class Block:
    def __init__(self):
        self.size = 35
        self.x = random.randint(0, WIDTH - self.size)
        self.y = 50
        self.velocity_x = 2
        self.velocity_y = 1
        self.number = random.randint(1, 9)

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce from walls
        if self.x <= 0 or self.x >= WIDTH - self.size:
            self.velocity_x = -self.velocity_x

    def draw(self, screen):
        rect = pygame.draw.rect(
            screen, BLUE, (self.x, self.y, self.size, self.size), border_radius=4
        )

        font = pygame.font.SysFont(None, 24)
        text = font.render(str(self.number), True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    def collision(self, bullet):
        distance = math.sqrt((self.x - bullet.x) ** 2 + (self.y - bullet.y) ** 2)
        return distance < 30


# ---------------- GAME CLASS ---------------- #
class Game:
    def __init__(self):
        self.ship = Ship(ship_image)
        self.bullet = Bullet()
        self.block = Block()
        self.running = True

    def run(self):
        while self.running:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.ship.velocity_x = self.ship.velocity
                    if event.key == pygame.K_LEFT:
                        self.ship.velocity_x = -self.ship.velocity
                    if event.key == pygame.K_b:
                        self.bullet.fire(self.ship.x, self.ship.y)

                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_RIGHT, pygame.K_LEFT):
                        self.ship.velocity_x = 0

            # -------- UPDATE -------- #
            self.ship.move()
            self.bullet.move()
            self.block.move()

            # Collision check
            if self.block.collision(self.bullet):
                self.block = Block()
                self.bullet.state = "ready"

            # -------- DRAW -------- #
            screen.blit(bg_image, (0, 0))
            self.ship.draw(screen)
            self.bullet.draw(screen)
            self.block.draw(screen)

            pygame.display.update()

        pygame.quit()


# ---------------- RUN GAME ---------------- #
game = Game()
game.run()
