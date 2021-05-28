import pygame as pg
from pygame.locals import *
import sys
import os
import math


# Main options
pg.init()
screen_width = 750
screen_height = 750
clock = pg.time.Clock()
menu_font = pg.font.SysFont('Calibri', 80, bold=False, italic=False)

running_options = True
running_pause = True
running_game = True
running_game_over = True


def load_image(filename:str, erase_bg=True):
    image = pg.image.load('files\\' + filename).convert()

    if erase_bg is True:   # Make the background of the image transparrent
        colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image


def load_sound(filename:str):
    return pg.mixer.Sound('files\\' + filename)


def draw_text(text:str, position:tuple, font:object, rgb_color:tuple):
    """Draw the text on the screen and return the rectangle in the position of the text."""
    text_obj = font.render(text, 1, rgb_color)
    text_rect = text_obj.get_rect()
    text_rect.center = position
    screen.blit(text_obj, text_rect)
    return text_rect


class Hero(pg.sprite.Sprite):
    """A character who is controlled by the player."""

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(load_image('hero.jpg'), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width/2, screen_height/2)
        self.x_velocity = 0
        self.y_velocity = 0
        self.life = 3

    def update(self):
        """Update the position of the hero."""
        self.rect.move_ip((self.x_velocity, self.y_velocity))
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > screen_height:
            self.rect.bottom = screen_height


class Enemy(pg.sprite.Sprite):
    """An enemy who moves towards the player."""

    def __init__(self, starting_position:tuple, velocity:int, lifes:int):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(load_image('enemy.jpg'), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = starting_position
        self.x_velocity = 0
        self.y_velocity = 0
        self.velocity = velocity
        self.lifes = lifes
    
    def update(self, hero_coords:tuple):
        """Update the position of the enemy"""
        x_dist = hero_coords[0] - self.rect.center[0]
        y_dist = hero_coords[1] - self.rect.center[1]
        dist = math.sqrt(x_dist**2 + y_dist**2)
        try:
            self.x_velocity = (self.velocity * x_dist) / dist
            self.y_velocity = (self.velocity * y_dist) / dist 
        except ZeroDivisionError:
            pass
        self.rect.move_ip((self.x_velocity, self.y_velocity))


class Missile(pg.sprite.Sprite):
    """A missile which moves towards the aim."""

    def __init__(self, start_position:tuple, aim:tuple, velocity:int):
        pg.sprite.Sprite.__init__(self)
        self.velocity = velocity
        self.aim = aim

        x_dist = self.aim[0] - start_position[0]
        y_dist = self.aim[1] - start_position[1]
        dist = math.sqrt(x_dist**2 + y_dist**2)
        self.x_velocity = (self.velocity * x_dist) / dist
        self.y_velocity = (self.velocity * y_dist) / dist

        # Find an angle of rotation
        if y_dist <= 0:
            angle = 180 * math.acos((x_dist / dist)) / math.pi
        else:
            angle = 180 * math.acos(-x_dist / dist) / math.pi + 180

        self.image = pg.transform.rotate(pg.transform.scale(load_image('rocket.png'), (80, 40)), angle)
        self.rect = self.image.get_rect()
        self.rect.center = start_position
        
    def update(self):
        """Update the position of the missile"""
        self.rect.move_ip((self.x_velocity, self.y_velocity))


class Explosion(pg.sprite.Sprite):
    """An animation of explosion displayed when an enemy is destroyed."""

    def __init__(self, position:tuple):
        pg.sprite.Sprite.__init__(self)
        self.position = position
        self.images = [pg.transform.scale(load_image('explosion\\' + image), (150, 150)) for image in os.listdir('files\explosion')]
        self.image_number = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = position
    
    def update(self):
        """Display next frame."""
        self.image_number += 1
        self.image = self.images[self.image_number]
        if self.image_number + 1 >= len(self.images):
            self.kill()


def menu():
    """Display the main menu of the game."""

    while True:
        screen.fill((0, 0, 0))
        mx, my = pg.mouse.get_pos()  # Mouse position

        # Draw buttons
        play_button = draw_text('Play', (screen_width/2, 100), menu_font, (0, 200, 0))
        rules_button = draw_text('Rules', (screen_width/2, 200), menu_font, (255, 255, 255))
        options_button = draw_text('Options', (screen_width/2, 300), menu_font, (255, 255, 255))
        ranking_button = draw_text('Ranking', (screen_width/2, 400), menu_font, (255, 255, 255))
        author_button = draw_text('Author', (screen_width/2, 500), menu_font, (255, 255, 255))
        quit_button = draw_text('Quit', (screen_width/2, 600), menu_font, (200, 0, 0))

        click = False
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                click = True

        if play_button.collidepoint(mx, my) and click:
            game_over()
        if rules_button.collidepoint(mx, my) and click:
            pass
        if options_button.collidepoint(mx, my) and click:
            options()
        if ranking_button.collidepoint(mx, my) and click:
            pass
        if author_button.collidepoint(mx, my) and click:
            pass
        if quit_button.collidepoint(mx, my) and click:
            pg.quit()
            sys.exit()

        pg.display.update()
        clock.tick(60)


def options():
    """Display the game options and allow the user to customize them."""

    global running_options
    running_options = True

    while running_options:
        screen.fill((0, 100, 200))
        mx, my = pg.mouse.get_pos()  # Mouse position

        button1 = draw_text('Option 1', (screen_width/2, 50), menu_font, (255, 255, 255))
        button2 = draw_text('Option 2', (screen_width/2, 150), menu_font, (255, 255, 255))

        click = False
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running_options = False
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                click = True

        if button1.collidepoint(mx, my) and click:
            pass
        if button2.collidepoint(mx, my) and click:
            pass

        pg.display.update()
        clock.tick(60)


def pause():
    """Pause the game and display a pause screen."""

    global running_game
    global running_pause
    running_pause = True

    while running_pause:
        screen.fill((0, 0, 0))
        mx, my = pg.mouse.get_pos()  # Mouse position

        resume_button = draw_text('Resume', (screen_width/2, 100), menu_font, (0, 200, 0))
        menu_button = draw_text('Return to menu', (screen_width/2, 200), menu_font, (200, 0, 0))

        click = False
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                click = True

        if resume_button.collidepoint(mx, my) and click:
            running_pause = False
        if menu_button.collidepoint(mx, my) and click:
            running_pause = False
            running_game = False

        pg.display.update()
        clock.tick(60)
    
    # Restore the background
    background = load_image('background.jpg', False)
    screen.blit(background, (0, 0))


def game_over():
    """Display a 'game over' screen."""
    
    global running_game_over
    running_game_over = True
    game()  # Start game

    while running_game_over:
        screen.fill((0, 0, 0))
        mx, my = pg.mouse.get_pos()  # Mouse position

        restart_button = draw_text('Restart', (screen_width/2, 100), menu_font, (0, 200, 0))
        menu_button = draw_text('Return to menu', (screen_width/2, 200), menu_font, (200, 0, 0))

        click = False
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                click = True

        if restart_button.collidepoint(mx, my) and click:
            game()
        if menu_button.collidepoint(mx, my) and click:
            running_game_over = False

        pg.display.update()
        clock.tick(60)


def game():
    """Start the game."""

    global running_game
    running_game = True

    # Background
    background = load_image('background.jpg', False)
    screen.blit(background, (0, 0))

    # Character
    hero_sprite = pg.sprite.Group()
    hero = Hero()
    hero_sprite.add(hero)

    # Enemy
    enemy_sprite = pg.sprite.Group()
    enemy_sprite.add(Enemy((50, 50), 3, 3))
    add_enemy_counter = 0

    # Lasers
    missile_sprite = pg.sprite.Group()

    # Explosions
    explosion_sprite = pg.sprite.Group()

    while running_game:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pause()

                # WSAD - moving the character
                if event.key == K_a:
                    hero.x_velocity = -4
                if event.key == K_d:
                    hero.x_velocity = 4
                if event.key == K_w:
                    hero.y_velocity = -4
                if event.key == K_s:
                    hero.y_velocity = 4

            elif event.type == KEYUP:
                if event.key == K_a:
                    hero.x_velocity = 0
                if event.key == K_d:
                    hero.x_velocity = 0
                if event.key == K_w:
                    hero.y_velocity = 0
                if event.key == K_s:
                    hero.y_velocity = 0
            
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                aim = pg.mouse.get_pos()
                missile_sprite.add(Missile(hero.rect.center, aim, 8))

        # Add enemies
        add_enemy_counter += 1
        if add_enemy_counter == 150:
            enemy_sprite.add(Enemy((50, 50), 3, 3))
            add_enemy_counter = 0

        # Update all the objects
        hero.update()

        for enemy in enemy_sprite:
            enemy.update((hero.rect.center[0], hero.rect.center[1]))

            # If the enemy caught up with the hero
            if hero.rect.collidepoint(enemy.rect.center):
                explosion_sprite.add(Explosion(enemy.rect.center))  # Draw the explosion of the enemy
                enemy.kill()
                hero.life -= 1
                if hero.life <= 0:  # If the hero's life has ended
                    running_game = False
            
            for missile_obj in missile_sprite:
                if enemy.rect.collidepoint(missile_obj.rect.center):  # If the missile hit the enemy
                    enemy.lifes -= 1
                    if enemy.lifes <= 0:   # If the enemy dies
                        explosion_sprite.add(Explosion(enemy.rect.center))  # Draw the explosion
                        enemy.kill()
                    missile_obj.kill()
        
        for missile_obj in missile_sprite:
            missile_obj.update()
            if 0 <= missile_obj.rect.center[0] >= screen_width or 0 >= missile_obj.rect.center[1] >= screen_height:
                missile_obj.kill()
        
        for explosion in explosion_sprite:
            explosion.update()

        # Clear the screen
        hero_sprite.clear(screen, background)
        enemy_sprite.clear(screen, background)
        explosion_sprite.clear(screen, background)
        missile_sprite.clear(screen, background)

        # Draw the objects
        hero_sprite.draw(screen)
        enemy_sprite.draw(screen)
        explosion_sprite.draw(screen)
        missile_sprite.draw(screen)

        pg.display.update()


screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("fajna gra")
menu()
