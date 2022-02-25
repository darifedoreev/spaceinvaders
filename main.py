import pygame
import os



class Game:
    screen = None
    aliens = []
    rockets = []
    lost = False
    aliens_speed_y = 0.05
    aliens_speed_x = 0.02
    aliens_direction = 'right'
    alien_sprite = pygame.image.load(os.path.join("alien.png"))
    

    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.alien_sprite.convert()
        self.clock = pygame.time.Clock()
        done = False

        hero = Hero(self, width / 2, height - 20)
        generator = Generator(self)
        rocket = None

        while not done:
            if len(self.aliens) == 0:
                self.displayText("VICTORY ACHIEVED")

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:  
                hero.x -= 2 if hero.x > 20 else 0  
            elif pressed[pygame.K_RIGHT]:  
                hero.x += 2 if hero.x < width - 20 else 0  

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.lost:
                    self.rockets.append(Rocket(self, hero.x, hero.y))

            pygame.display.flip()
            self.clock.tick(60)
            self.screen.fill((0, 0, 0))

            for alien in self.aliens:
                alien.draw()
                alien.checkCollision(self)
                if (alien.y > height):
                    self.lost = True
                    self.displayText("YOU DIED")

            for rocket in self.rockets:
                rocket.draw()

            if not self.lost: hero.draw()

    def displayText(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 50)
        textsurface = font.render(text, False, (44, 0, 62))
        self.screen.blit(textsurface, (110, 160))


class Alien:
    def __init__(self, game, x, y):
        self.x = x
        self.game = game
        self.y = y
        self.size = 30

    def draw(self):
        self.game.screen.blit(self.game.alien_sprite, (self.x, self.y))
        self.y += self.game.aliens_speed_y
        if self.x >= 970:
            self.game.aliens_direction = 'left'
        if self.x <= 30:
            self.game.aliens_direction = 'right'
        if self.game.aliens_direction == 'right':
            self.x += self.game.aliens_speed_x
        else:
            self.x -= self.game.aliens_speed_x

    def checkCollision(self, game):
        for rocket in game.rockets:
            if (rocket.x < self.x + self.size and
                    rocket.x > self.x - self.size and
                    rocket.y < self.y + self.size and
                    rocket.y > self.y - self.size):
                game.rockets.remove(rocket)
                game.aliens.remove(self)
                game.aliens_speed_y += 0.05
                game.aliens_speed_x += 0.04


class Hero:
    def __init__(self, game, x, y):
        self.x = x
        self.game = game
        self.y = y

    def draw(self):
        pygame.draw.rect(self.game.screen,
                         (210, 250, 251),
                         pygame.Rect(self.x, self.y, 8, 5))


class Generator:
    def __init__(self, game):
        margin = 200  
        width = 50  
        for x in range(margin, 1000 - margin, width):
            for y in range(30, int(600 / 2), width):
                game.aliens.append(Alien(game, x, y))

      


class Rocket:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game

    def draw(self):
        pygame.draw.rect(self.game.screen,  
                         (254, 52, 110),  
                         pygame.Rect(self.x, self.y, 2, 4))
        self.y -= 2  


if __name__ == '__main__':
    game = Game(1000, 800)
