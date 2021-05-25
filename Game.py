import pygame as pg
import sys


# Main options
pg.init()
screen_width = 1200
screen_height = 800
clock = pg.time.Clock()
menu_font = pg.font.SysFont('Calibri', 80, bold=False, italic=False)


def load_image(filename:str): 
    return pg.image.load('files\\' + filename).convert()


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


def menu():
    """Display the main menu of the game."""

    while True:
        screen.fill((0, 0, 0))
        mx, my = pg.mouse.get_pos()  # Mouse position

        play_button = draw_text('Play', (screen_width/2, 50), menu_font, (0, 200, 0))
        options_button = draw_text('Options', (screen_width/2, 150), menu_font, (200, 0, 0))

        click = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        if play_button.collidepoint(mx, my) and click:
            game()
        if options_button.collidepoint(mx, my) and click:
            options()

        pg.display.update()
        clock.tick(60)


def options():
    """Display the game options and allow the user to customize them."""

    running = True
    while running:
        screen.fill((0, 100, 200))
        mx, my = pg.mouse.get_pos()  # Mouse position

        button1 = draw_text('Option 1', (screen_width/2, 50), menu_font, (255, 255, 255))
        button2 = draw_text('Option 2', (screen_width/2, 150), menu_font, (255, 255, 255))

        click = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        if button1.collidepoint(mx, my) and click:
            pass
        if button2.collidepoint(mx, my) and click:
            pass

        pg.display.update()
        clock.tick(60)


def game():
    """Start the game."""

    # Background
    background = load_image('background.jpg')
    screen.blit(background, (0, 0))

    # Character
    hero_sprite = pg.sprite.RenderClear()
    hero = Hero()
    hero_sprite.add(hero)

    running = True

    while running:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                # WSAD - moving the character
                if event.key == pg.K_a:
                    hero.x_velocity = -4
                if event.key == pg.K_d:
                    hero.x_velocity = 4
                if event.key == pg.K_w:
                    hero.y_velocity = -4
                if event.key == pg.K_s:
                    hero.y_velocity = 4

            elif event.type == pg.KEYUP:
                if event.key == pg.K_a:
                    hero.x_velocity = 0
                if event.key == pg.K_d:
                    hero.x_velocity = 0
                if event.key == pg.K_w:
                    hero.y_velocity = 0
                if event.key == pg.K_s:
                    hero.y_velocity = 0

        hero.update()
        hero_sprite.clear(screen, background)
        hero_sprite.draw(screen)
        pg.display.update()


screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("fajna gra")
menu()
