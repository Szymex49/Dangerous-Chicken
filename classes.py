"""A module with classes designed for creating objects in game.
List of classes:
 - player
 - enemy
 - shooting tower
 - horse
 - missile
 - fireball
 - explosion
 - scoreboard
 - slider
 - cursor
"""

from tools import *


class Player(pg.sprite.Sprite):
    """A character who is controlled by the player."""

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image_right = load_image('player.png', (100, 100))
        self.image_left = pg.transform.flip(self.image_right, True, False)
        self.image_left_bright = load_image('brighten_player.png', (100, 100))
        self.image_right_bright = pg.transform.flip(self.image_left_bright, True, False)
        self.image = self.image_right
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
        # Turn the player towards the cursor
        if self.rect.center[0] < pg.mouse.get_pos()[0]:
            self.image = self.image_right
        else:
            self.image = self.image_left
    
    def brighten(self):
        """Brighten the image when hit."""
        if self.rect.center[0] < pg.mouse.get_pos()[0]:
            self.image = self.image_right_bright
        else:
            self.image = self.image_left_bright


class Enemy(pg.sprite.Sprite):
    """An enemy who moves towards the player."""

    def __init__(self, starting_position:tuple, velocity:int, life:int, points:int):
        pg.sprite.Sprite.__init__(self)
        self.image_right = load_image('rooster.png', (100, 100))
        self.image_left = pg.transform.flip(self.image_right, True, False)
        self.image_right_bright = load_image('brighten_rooster.png', (100, 100))
        self.image_left_bright = pg.transform.flip(self.image_right_bright, True, False)
        self.image = self.image_right
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
        # Turn the enemy towards the player
        if self.rect.center[0] < player_coords[0]:
            self.image = self.image_right
        else:
            self.image = self.image_left
    
    def brighten(self, player_position:tuple):
        """Brighten the image when hit."""
        if self.rect.center[0] < player_position[0]:
            self.image = self.image_right_bright
        else:
            self.image = self.image_left_bright



class ShootingTower(pg.sprite.Sprite):
    """An enemy who doesn't move but shoots to the player."""

    def __init__(self, position:tuple, life:int, points:int):
        pg.sprite.Sprite.__init__(self)
        self.image_left = load_image('cow.png', (120, 120))
        self.image_right = pg.transform.flip(self.image_left, True, False)
        self.image_left_bright = load_image('brighten_cow.png', (120, 120))
        self.image_right_bright = pg.transform.flip(self.image_left_bright, True, False)
        self.image = self.image_left
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.life = life
        self.points = points
    
    def update(self, player_position:tuple):
        """Update the direction of looking."""
        if self.rect.center[0] < player_position[0]:
            self.image = self.image_right
        else:
            self.image = self.image_left
    
    def brighten(self, player_position):
        """Brighten the image when hit."""
        if self.rect.center[0] < player_position[0]:
            self.image = self.image_right_bright
        else:
            self.image = self.image_left_bright


class Horse(pg.sprite.Sprite):
    """An enemy who moves randomly on one side of the screen and shoots to the player."""

    def __init__(self, position:int, side:str, life:int, points:int):
        pg.sprite.Sprite.__init__(self)
        self.side = side
        self.image_norm = load_image('horse.jpg', (150, 150))
        self.image_bright = load_image('brighten_horse.jpg', (150, 150))
        self.rect = self.image_norm.get_rect()
        if side == 'left':
            self.rect.center = (100, position)
        elif side == 'right':
            self.rect.center = (SCREEN_WIDTH - 100, position)
            self.image_norm = pg.transform.flip(self.image_norm, True, False)
            self.image_bright = pg.transform.flip(self.image_bright, True, False)
        self.image = self.image_norm
        self.life = life
        self.points = points
        self.velocity = 3
    
    def update(self):
        """Update the position of the horse."""
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT or random.randint(1, 250) == 1:
            self.velocity = -self.velocity
        self.rect.move_ip((0, self.velocity))
        self.image = self.image_norm
    
    def brighten(self):
        """Brighten the image when hit."""
        self.image = self.image_bright


class Missile(pg.sprite.Sprite):
    """A missile which moves towards the aim."""

    def __init__(self, start_position:tuple, aim:tuple, velocity:int, kind:str):
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
        
        # Choose the image depending on what kind was chosen
        if kind == 'blue':
            filename = 'blue_laser.png'
        elif kind == 'red':
            filename = 'red_laser.png'
        elif kind == 'orange':
            filename = 'orange_laser.png'
        elif kind == 'harnold':
            filename = 'harnold.jpg'
        
        self.image = pg.transform.rotate(load_image(filename, (35, 12)), angle)
        self.rect = self.image.get_rect()
        self.rect.center = start_position
        
    def update(self):
        """Update the position of the missile."""
        self.rect.move_ip((self.x_velocity, self.y_velocity))
        if self.rect.left >= SCREEN_WIDTH or self.rect.right <= 0 or self.rect.top >= SCREEN_HEIGHT or self.rect.bottom <= 0:
                self.kill()


class FireBall(pg.sprite.Sprite):
    """An animated fireball which moves only vertically."""
    
    def __init__(self, start_position:tuple, side:str):
        pg.sprite.Sprite.__init__(self)
        self.side = side
        if side == 'left':
            self.images = [load_image('fireball\\' + image, (150, 150)) for image in os.listdir('files\\fireball')]
            self.velocity = 3
        elif side == 'right':
            self.images = [pg.transform.flip(load_image('fireball\\' + image, (150, 150)), True, False)
                            for image in os.listdir('files\\fireball')]
            self.velocity = -3
        self.image_number = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = start_position
    
    def update(self):
        self.image_number += 1
        if self.image_number >= len(self.images):
            self.image_number = 0
        self.image = self.images[self.image_number]
        self.rect.move_ip((self.velocity, 0))


class Explosion(pg.sprite.Sprite):
    """An animation of explosion displayed when an enemy is destroyed."""

    def __init__(self, position:tuple, kind:str, size:tuple):
        pg.sprite.Sprite.__init__(self)
        self.position = position
        self.images = [load_image(kind + '\\' + image, size) for image in os.listdir('files\\' + kind)]
        self.image_number = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = position
    
    def update(self):
        """Display next frame."""
        self.image_number += 1
        if self.image_number >= len(self.images):
            self.kill()
            return
        self.image = self.images[self.image_number]


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
        """Update and display the current score."""
        self.score += new_points
        self.text = "Score: " + str(self.score)
        self.image = self.font.render(self.text, 1, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (20, 10)


class Slider(pg.sprite.Sprite):
    """A slider composed of the axis and the marker, containing chosen value."""

    def __init__(self, position:tuple, volume:float):
        pg.sprite.Sprite.__init__(self)
        self.volume = volume
        self.delta = 45  # Distance from both sides where the axis ends

        # Axis
        self.image = load_image('axis.png', (500, 80))
        self.rect = self.image.get_rect()
        self.rect.center = position

        # Slider
        self.slider_im = load_image('slider.png', (16, 40))
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


class Cursor(pg.sprite.Sprite):

    def __init__(self):
        self.arrow = load_image('cursor.png', (20, 20))
        self.crosshair = load_image('crosshair.png', (20, 20))
        self.image = self.arrow
        self.rect = self.image.get_rect()
        self.rect.topleft = pg.mouse.get_pos()
    
    def update(self):
        self.rect.topleft = pg.mouse.get_pos()
        SCREEN.blit(self.image, self.rect)
