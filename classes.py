"""A module with classes designed for creating objects in game.
List of classes:
 - main player
 - enemy
 - missile
 - explosion
 - scoreboard
"""

from tools import *


class Player(pg.sprite.Sprite):
    """A character who is controlled by the player."""

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(load_image('player.jpg'), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.x_velocity = 0
        self.y_velocity = 0
        self.life = 3

    def update(self):
        """Update the position of the player."""
        self.rect.move_ip((self.x_velocity, self.y_velocity))
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pg.sprite.Sprite):
    """An enemy who moves towards the player."""

    def __init__(self, starting_position:tuple, velocity:int, life:int, points:int):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(load_image('enemy.jpg'), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = starting_position
        self.x_velocity = 0
        self.y_velocity = 0
        self.velocity = velocity
        self.life = life
        self.points = points
    
    def update(self, player_coords:tuple):
        """Update the position of the enemy"""
        x_dist = player_coords[0] - self.rect.center[0]
        y_dist = player_coords[1] - self.rect.center[1]
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

        self.image = pg.transform.rotate(pg.transform.scale(load_image('laser.png'), (60, 20)), angle)
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


class ScoreBoard(pg.sprite.Sprite):
    """A scoreboard which displays the number of player's points."""

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.score = 0
        self.text = "Score: " + str(self.score)
        self.font = pg.font.SysFont('Calibri', 40)
        self.image = self.font.render(self.text, 1, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (50, 10)

    def update(self, new_points):
        """"""
        self.score += new_points
        self.text = "Score: " + str(self.score)
        self.image = self.font.render(self.text, 1, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (20, 10)


class Slider(pg.sprite.Sprite):
    def __init__(self, position:tuple, volume:float):
        pg.sprite.Sprite.__init__(self)
        self.volume = volume
        self.delta = 45  # Distance from both sides where the axis ends

        # Axis
        self.image = pg.transform.scale(load_image('axis.png'), (500, 80))
        self.rect = self.image.get_rect()
        self.rect.center = position

        # Slider
        self.slider_im = pg.transform.scale(load_image('slider.png'), (16, 40))
        self.slider_rect = self.slider_im.get_rect()
        self.length = self.rect.right - self.rect.left - 2 * self.delta - self.slider_rect.width   # Length of the axis
        self.slider_rect.center = (self.volume * self.length + self.rect.left + self.delta + self.slider_rect.width/2, position[1])

        SCREEN.blit(self.slider_im, self.slider_rect)

    def update(self, shift):
        """Update the position of the slider and draw it on the screen. Calculate the volume."""
        self.slider_rect.move_ip((shift, 0))
        # If goes out of range
        if self.slider_rect.right >= self.rect.right - self.delta:
            self.slider_rect.right = self.rect.right - self.delta
        elif self.slider_rect.left <= self.rect.left + self.delta:
            self.slider_rect.left = self.rect.left + self.delta
        # Calculate the volume
        self.volume = (self.slider_rect.center[0] - self.rect.left - self.delta - self.slider_rect.width/2) / self.length
        SCREEN.blit(self.slider_im, self.slider_rect)
