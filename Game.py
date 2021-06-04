from pygame.image import load
from classes import *


# Main options
pg.init()
pg.mixer.set_num_channels(30)
pg.mouse.set_visible(False)
CLOCK = pg.time.Clock()
CURSOR = Cursor()
DIFFICULTY = 'Normal'
MENU_FONT = pg.font.SysFont('Calibri', 80)
HIGHLIGHTED_FONT = pg.font.SysFont('Calibri', 90)

ARROW_IMAGE = load_image('arrow.png', (30, 30))
ARROW_RECT = ARROW_IMAGE.get_rect()
ARROW_RECT.center = (50, 50)
ARROW_BIG_IMAGE = load_image('arrow.png', (40, 40), False)
ARROW_BIG_RECT = ARROW_BIG_IMAGE.get_rect()
ARROW_BIG_RECT.center = (50, 50)

running_pause = True
running_game = True
running_game_over = True
restart = False
transition = False


# -----------------------------------------------------------------------------------------------------------
#                                                 MAIN MENU
# -----------------------------------------------------------------------------------------------------------


# ============================  MENU  ============================

def menu():
    """Display the main menu of the game."""

    global restart, CURSOR
    transition_from = True
    transition_to = False
    alpha = 255   # Transparence
    go_to = ''

    play_music('menu_music.wav', MUSIC_VOLUME)

    background = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill((0, 0, 0))

    while True:
        SCREEN.fill((0, 0, 0))
        mx, my = pg.mouse.get_pos()  # Mouse position

        # Draw buttons
        play_button = draw_text('Play', (SCREEN_WIDTH/2, 200), MENU_FONT, (0, 200, 0))
        rules_button = draw_text('Rules', (SCREEN_WIDTH/2, 300), MENU_FONT, (255, 255, 255))
        options_button = draw_text('Options', (SCREEN_WIDTH/2, 400), MENU_FONT, (255, 255, 255))
        ranking_button = draw_text('Ranking', (SCREEN_WIDTH/2, 500), MENU_FONT, (255, 255, 255))
        author_button = draw_text('Author', (SCREEN_WIDTH/2, 600), MENU_FONT, (255, 255, 255))
        quit_button = draw_text('Quit', (SCREEN_WIDTH/2, 700), MENU_FONT, (200, 0, 0))

        # Transition from menu to other screen
        if transition_to:
            darken_screen(alpha)
            alpha += 10
            if alpha >= 255:
                if go_to == 'game':
                    restart = True
                    while restart:
                        game()
                    play_music('menu_music.wav', MUSIC_VOLUME)
                    CURSOR.image = CURSOR.arrow
                elif go_to == 'rules':
                    rules()
                elif go_to == 'options':
                    options()
                elif go_to == 'ranking':
                    ranking()
                elif go_to == 'author':
                    author()
                transition_from = True
                transition_to = False
                alpha = 255
            CLOCK.tick(60)
            CURSOR.update()
            pg.display.update()
            continue
        
        # Transition from pause or game over to menu
        if transition_from:
            darken_screen(alpha)
            alpha -= 10
            if alpha <= 0:
                transition_from = False

        click = False
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                click = True

        if play_button.collidepoint(mx, my):
            draw_text('Play', (SCREEN_WIDTH/2, 200), HIGHLIGHTED_FONT, (0, 200, 0), True)
            if click:
                transition_to = True
                pg.mixer.music.fadeout(500)   # Music fadeout
                go_to = 'game'
        elif rules_button.collidepoint(mx, my):
            draw_text('Rules', (SCREEN_WIDTH/2, 300), HIGHLIGHTED_FONT, (255, 255, 255), True)
            if click:
                transition_to = True
                go_to = 'rules'
        elif options_button.collidepoint(mx, my):
            draw_text('Options', (SCREEN_WIDTH/2, 400), HIGHLIGHTED_FONT, (255, 255, 255), True)
            if click:
                transition_to =True
                go_to = 'options'
        elif ranking_button.collidepoint(mx, my):
            draw_text('Ranking', (SCREEN_WIDTH/2, 500), HIGHLIGHTED_FONT, (255, 255, 255), True)
            if click:
                transition_to = True
                go_to = 'ranking'
        elif author_button.collidepoint(mx, my):
            draw_text('Author', (SCREEN_WIDTH/2, 600), HIGHLIGHTED_FONT, (255, 255, 255), True)
            if click:
                transition_to = True
                go_to = 'author'
        elif quit_button.collidepoint(mx, my):
            draw_text('Quit', (SCREEN_WIDTH/2, 700), HIGHLIGHTED_FONT, (200, 0, 0), True)
            if click:
                pg.quit()
                sys.exit()

        CURSOR.update()
        pg.display.update()
        CLOCK.tick(80)



# ============================  RULES  ============================

def rules():
    """Display the screen with game rules."""

    global CURSOR
    running_rules = True
    transition_from = True
    transition_to = False
    alpha = 255

    rules_text = ["1. You are a chicken.",
                "2. You can shoot laser.",
                "3. Other animals don't like you and want to kill you.",
                "4. Kill them."]
    rules_font = pg.font.SysFont('Calibri', 40)

    wsad_image = load_image('controls1.jpg', (250, 250))
    wsad_rect = wsad_image.get_rect()
    wsad_rect.center = (SCREEN_WIDTH/2 + 400, 320)

    mouse_image = load_image('controls2.png', (200, 200))
    mouse_rect = mouse_image.get_rect()
    mouse_rect.center = (SCREEN_WIDTH/2 + 400, 650)

    while running_rules:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(ARROW_IMAGE, ARROW_RECT)

        draw_text('RULES', (SCREEN_WIDTH/2 - 400, 100), MENU_FONT, (0, 0, 240))
        position = 200
        for rule in rules_text:
            draw_text(rule, (SCREEN_WIDTH/2 - 700, position), rules_font, (255, 255, 255), point='topleft')
            position += 100

        draw_text('CONTROLS', (SCREEN_WIDTH/2 + 400, 100), MENU_FONT, (0, 0, 240))
        draw_text('Moving', (SCREEN_WIDTH/2 + 400, 200), rules_font, (255, 255, 255))
        SCREEN.blit(wsad_image, wsad_rect)
        draw_text('Shooting', (SCREEN_WIDTH/2 + 400, 500), rules_font, (255, 255, 255))
        SCREEN.blit(mouse_image, mouse_rect)

        # Transition from rules to menu
        if transition_to:
            darken_screen(alpha)
            alpha += 10
            if alpha >= 255:
                running_rules = False
            CURSOR.update()
            pg.display.update()
            CLOCK.tick(60)
            continue

        # Transition from menu to rules
        if transition_from:
            darken_screen(alpha)
            alpha -= 10
            if alpha <= 0:
                transition_from = False
        
        click = False
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                transition_to = True
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                click = True
        
        if ARROW_RECT.collidepoint(pg.mouse.get_pos()):
            SCREEN.blit(ARROW_BIG_IMAGE, ARROW_BIG_RECT)
            if click:
                transition_to = True

        
        CURSOR.update()
        pg.display.update()
        CLOCK.tick(60)



# ============================  OPTIONS  ============================

def options():
    """Display the game options and allow the user to customize them."""

    global MUSIC_VOLUME, SOUNDS_VOLUME, DIFFICULTY, CURSOR
    running_options = True
    transition_from = True
    transition_to = False
    slide = False
    alpha = 255
    difficulties = ['Easy', 'Normal', 'Hard', 'Hardcore']
    difficulty_number = difficulties.index(DIFFICULTY)
    text_font = pg.font.SysFont('Calibri', 50)

    background = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill((0, 0, 0))

    music_slider = Slider((SCREEN_WIDTH/2, 300), MUSIC_VOLUME)
    sounds_slider = Slider((SCREEN_WIDTH/2, 500), SOUNDS_VOLUME)

    slider_sprite = pg.sprite.Group()
    slider_sprite.add(music_slider)
    slider_sprite.add(sounds_slider)

    triangle_left = load_image('triangle.png', (40, 40))
    triangle_left_rect = triangle_left.get_rect()
    triangle_left_rect.center = (SCREEN_WIDTH/2 - 200, 700)
    triangle_left_big = load_image('triangle.png', (45, 45))
    triangle_left_big_rect = triangle_left_big.get_rect()
    triangle_left_big_rect.center = (SCREEN_WIDTH/2 - 200, 700)

    triangle_right = pg.transform.flip(triangle_left, True, False)
    triangle_right_rect = triangle_right.get_rect()
    triangle_right_rect.center = (SCREEN_WIDTH/2 + 200, 700)
    triangle_right_big = pg.transform.flip(triangle_left_big, True, False)
    triangle_right_big_rect = triangle_right_big.get_rect()
    triangle_right_big_rect.center = (SCREEN_WIDTH/2 + 200, 700)

    while running_options:
        mx, my = pg.mouse.get_pos()  # Mouse position
        music_slider_pos = music_slider.slider_rect.center[0]
        sounds_slider_pos = sounds_slider.slider_rect.center[0]
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(ARROW_IMAGE, ARROW_RECT)


        # EVENTS
        click = False
        for event in pg.event.get():

            if event.type == QUIT:
                pg.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                transition_to = True
                alpha = 0

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                click = True
                slide = True

            elif event.type == MOUSEBUTTONUP and event.button == 1:
                slide = False
        

        # BUTTONS
        if music_slider.rect.collidepoint((mx, my)) and slide:
            music_slider_pos = mx
        elif sounds_slider.rect.collidepoint((mx, my)) and slide:
            sounds_slider_pos = mx

        elif triangle_left_rect.collidepoint((mx, my)):
            SCREEN.blit(triangle_left_big, triangle_left_big_rect)
            if click:
                difficulty_number -= 1
        elif triangle_right_rect.collidepoint((mx, my)):
            SCREEN.blit(triangle_right_big, triangle_right_big_rect)
            if click:
                difficulty_number += 1
        
        elif ARROW_RECT.collidepoint((mx, my)):
            SCREEN.blit(ARROW_BIG_IMAGE, ARROW_BIG_RECT)
            if click:
                transition_to = True


        # DRAWING
        draw_text('OPTIONS', (SCREEN_WIDTH/2, 100), MENU_FONT, (0, 0, 240))

        draw_text('Music volume', (SCREEN_WIDTH/2, 220), text_font, (255, 255, 255))
        draw_text('Sounds volume', (SCREEN_WIDTH/2, 420), text_font, (255, 255, 255))

        draw_text('Difficulty level', (SCREEN_WIDTH/2, 620), text_font, (255, 255, 255))
        draw_text(DIFFICULTY, (SCREEN_WIDTH/2, 700), text_font, (255, 255, 255), True)

        SCREEN.blit(triangle_left, triangle_left_rect)
        SCREEN.blit(triangle_right, triangle_right_rect)

        slider_sprite.clear(SCREEN, background)
        slider_sprite.draw(SCREEN)

        music_slider.update(music_slider_pos)
        sounds_slider.update(sounds_slider_pos)


        # Transition from menu to options
        if transition_from:
            darken_screen(alpha)
            alpha -= 10
            if alpha <= 0:
                transition_from = False
        
        # Transition from options to menu
        if transition_to:
            darken_screen(alpha)
            alpha += 10
            if alpha >= 255:
                running_options = False


        if difficulty_number > 3:
            difficulty_number = 0
        elif difficulty_number < 0:
            difficulty_number = 3
        DIFFICULTY = difficulties[difficulty_number]

        MUSIC_VOLUME = music_slider.volume
        SOUNDS_VOLUME = sounds_slider.volume

        pg.mixer.music.set_volume(MUSIC_VOLUME)

        CURSOR.update()
        pg.display.update()
        CLOCK.tick(60)



# ============================  RANKING  ============================

def ranking():
    """Display the screen with ranking of the best scores."""

    global CURSOR
    running_ranking = True
    transition_from = True
    transition_to = False
    alpha = 255
    
    ranking_file = open('files\\ranking', 'rb')
    RANKING = pickle.load(ranking_file)
    ranking_file.close()

    heading_font = pg.font.SysFont('Calibri', 55)
    text_font = pg.font.SysFont('Calibri', 35)

    while running_ranking:

        SCREEN.fill((0, 0, 0))
        SCREEN.blit(ARROW_IMAGE, ARROW_RECT)
        draw_text('BEST SCORES', (SCREEN_WIDTH/2, 100), MENU_FONT, (0, 0, 240))

        # Draw the best scores and their dates
        draw_text('Easy', (SCREEN_WIDTH/4, 180), heading_font, (255, 255, 255))
        position = 450
        for score, date in zip(RANKING[0][0], RANKING[1][1]):
            draw_text(str(score), (SCREEN_WIDTH/4 - 100, position), text_font, (255, 255, 255))
            draw_text(str(date), (SCREEN_WIDTH/4 + 50, position), text_font, (255, 255, 255))
            position -= 50
        
        draw_text('Normal', (SCREEN_WIDTH/4, 530), heading_font, (255, 255, 255))
        position = 800
        for score, date in zip(RANKING[1][0], RANKING[1][1]):
            draw_text(str(score), (SCREEN_WIDTH/4 - 100, position), text_font, (255, 255, 255))
            draw_text(str(date), (SCREEN_WIDTH/4 + 50, position), text_font, (255, 255, 255))
            position -= 50

        draw_text('Hard', (3*SCREEN_WIDTH/4, 180), heading_font, (255, 255, 255))
        position = 450
        for score, date in zip(RANKING[2][0], RANKING[1][1]):
            draw_text(str(score), (3*SCREEN_WIDTH/4 - 100, position), text_font, (255, 255, 255))
            draw_text(str(date), (3*SCREEN_WIDTH/4 + 50, position), text_font, (255, 255, 255))
            position -= 50

        draw_text('Hardcore', (3*SCREEN_WIDTH/4, 530), heading_font, (255, 255, 255))
        position = 800
        for score, date in zip(RANKING[3][0], RANKING[1][1]):
            draw_text(str(score), (3*SCREEN_WIDTH/4 - 100, position), text_font, (255, 255, 255))
            draw_text(str(date), (3*SCREEN_WIDTH/4 + 50, position), text_font, (255, 255, 255))
            position -= 50

        # Transition from ranking to menu
        if transition_to:
            darken_screen(alpha)
            alpha += 10
            if alpha >= 255:
                running_ranking = False
            CURSOR.update()
            pg.display.update()
            CLOCK.tick(60)
            continue

        # Transition from menu to ranking
        if transition_from:
            darken_screen(alpha)
            alpha -= 10
            if alpha <= 0:
                transition_from = False

        click = False
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                transition_to = True
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                click = True

        if ARROW_RECT.collidepoint(pg.mouse.get_pos()):
            SCREEN.blit(ARROW_BIG_IMAGE, ARROW_BIG_RECT)
            if click:
                transition_to = True
        
        CURSOR.update()
        pg.display.update()
        CLOCK.tick(60)



# ============================  AUTHOR  ============================

def author():
    """Display the screen with information about me."""

    global CURSOR
    running_author = True
    transition_from = True
    transition_to = False
    alpha = 255

    author_image = load_image('author.jpg', (500, 500), False)
    author_rect = author_image.get_rect()
    author_rect.center = (320, 500)

    text = ["Hi, my name is Szymon and I'm a student of",
            "the Wrocław Uniwersity of Science and Technology",
            "in the field of applied mathematics. I made",
            "this game for a programming assignment. I was",
            "always interested in video games so working on",
            "this game was fun and great experience.",
            "I hope you'll enjoy it."]
    text_font = pg.font.SysFont('Calibri', 40)

    while running_author:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(ARROW_IMAGE, ARROW_RECT)
        draw_text('ABOUT THE AUTHOR', (SCREEN_WIDTH/2, 100), MENU_FONT, (0, 0, 240))

        SCREEN.blit(author_image, author_rect)

        position = 330
        for line in text:
            draw_text(line, (SCREEN_WIDTH/2 - 120, position), text_font, (255, 255, 255), point='topleft')
            position += 50

        # Transition from rules to menu
        if transition_to:
            darken_screen(alpha)
            alpha += 10
            if alpha >= 255:
                running_author = False
            CURSOR.update()
            pg.display.update()
            CLOCK.tick(60)
            continue

        # Transition from menu to rules
        if transition_from:
            darken_screen(alpha)
            alpha -= 10
            if alpha <= 0:
                transition_from = False
        
        click = False
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                transition_to = True
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                click = True
        
        if ARROW_RECT.collidepoint(pg.mouse.get_pos()):
            SCREEN.blit(ARROW_BIG_IMAGE, ARROW_BIG_RECT)
            if click:
                transition_to = True

        
        CURSOR.update()
        pg.display.update()
        CLOCK.tick(60)



# -----------------------------------------------------------------------------------------------------------
#                                                 GAME
# -----------------------------------------------------------------------------------------------------------


# ============================  GAME  ============================

def game():
    """Start the game."""

    global running_game, CURSOR
    CURSOR.image = CURSOR.crosshair
    running_game = True
    transition_from = True
    game_end = False
    alpha = 255   # Transparence
    time = 0

    # Background
    background = load_image('background.jpg', (SCREEN_WIDTH, SCREEN_HEIGHT), False)

    # Music
    play_music('game_music.wav', MUSIC_VOLUME)

    # Sounds
    explosion_sound = load_sound('explosion_sound.mp3', SOUNDS_VOLUME)
    laser_sound = load_sound('laser_sound.mp3', SOUNDS_VOLUME)
    enemy_laser_sound = load_sound('enemy_laser_sound.mp3', SOUNDS_VOLUME*0.8)
    fireball_sound = load_sound('fireball_sound.mp3', SOUNDS_VOLUME*1.6)
    damage_sound = load_sound('damage_sound.mp3', SOUNDS_VOLUME*1.2)
    player_death_sound = load_sound('player_death_sound.mp3', SOUNDS_VOLUME*1.5)

    # Character
    player_sprite = pg.sprite.Group()
    player = Player()
    player_sprite.add(player)
    player_shooting = False
    player_shooting_counter = 10

    # Enemies
    enemy_sprite = pg.sprite.Group()
    add_enemy_counter = 0
    tower_sprite = pg.sprite.Group()
    add_tower_counter = 0
    tower_shooting_counter = 0
    horse_sprite = pg.sprite.Group()
    add_horse_counter = 0
    horse_shooting_counter = 0

    # Missiles
    missile_sprite = pg.sprite.Group()
    enemy_missile_sprite = pg.sprite.Group()

    # Explosions
    explosion_sprite = pg.sprite.Group()

    # Scoreboard
    scoreboard_sprite = pg.sprite.Group()
    scoreboard = ScoreBoard()
    scoreboard_sprite.add(scoreboard)

    while running_game:
        CLOCK.tick(60)
        SCREEN.blit(background, (0, 0))
        points = 0
        time += 1

        # Set difficulty level
        if DIFFICULTY == 'Easy':
            difficulty = time**(1.0/8.0)
            level = 0
        elif DIFFICULTY == 'Normal':
            difficulty = time**(1.0/6.0)
            level = 1
        elif DIFFICULTY == 'Hard':
            difficulty = time**(1.0/5.0)
            level = 2
        elif DIFFICULTY == 'Hardcore':
            difficulty = time**(1.0/3.0)
            level = 3

        # Clear the SCREEN
        horse_sprite.clear(SCREEN, background)
        tower_sprite.clear(SCREEN, background)
        player_sprite.clear(SCREEN, background)
        enemy_sprite.clear(SCREEN, background)
        explosion_sprite.clear(SCREEN, background)
        missile_sprite.clear(SCREEN, background)
        enemy_missile_sprite.clear(SCREEN, background)
        scoreboard_sprite.clear(SCREEN, background)

        # Draw the objects
        horse_sprite.draw(SCREEN)
        tower_sprite.draw(SCREEN)
        player_sprite.draw(SCREEN)
        enemy_sprite.draw(SCREEN)
        explosion_sprite.draw(SCREEN)
        missile_sprite.draw(SCREEN)
        enemy_missile_sprite.draw(SCREEN)
        scoreboard_sprite.draw(SCREEN)

        # Draw lifes
        if player.life == 0:
            draw_lifes(0)
        if player.life == 1:
            draw_lifes(1)
        if player.life == 2:
            draw_lifes(2)
        if player.life == 3:
            draw_lifes(3)

        # Update explosions
        for explosion in explosion_sprite:
            explosion.update()


        # If the player lost
        if game_end:
            darken_screen(alpha)
            alpha += 10
            if alpha >= 255:
                game_over(scoreboard.score)

        # Transition from menu to game
        if transition_from:
            darken_screen(alpha)
            alpha -= 10
            if alpha <= 0:
                transition_from = False


        # EVENTS
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pause(level, scoreboard.score)
                    CURSOR.image = CURSOR.crosshair

                # WSAD - moving the character
                if event.key == K_a:
                    player.x_velocity += -4
                if event.key == K_d:
                    player.x_velocity += 4
                if event.key == K_w:
                    player.y_velocity += -4
                if event.key == K_s:
                    player.y_velocity += 4

            elif event.type == KEYUP:
                if event.key == K_a:
                    player.x_velocity += 4
                if event.key == K_d:
                    player.x_velocity += -4
                if event.key == K_w:
                    player.y_velocity += 4
                if event.key == K_s:
                    player.y_velocity += -4
            
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                player_shooting = True
                player_shooting_counter = 10
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                player_shooting = False

        # Add enemies
        add_enemy_counter += difficulty
        if add_enemy_counter >= 500:
            spawn_points = [(SCREEN_WIDTH/2, -100),
                            (SCREEN_WIDTH/2, SCREEN_HEIGHT+100),
                            (-100, SCREEN_HEIGHT/2),
                            (SCREEN_WIDTH+100, SCREEN_HEIGHT/2),
                            (SCREEN_WIDTH+100, SCREEN_HEIGHT+100),
                            (-100, SCREEN_HEIGHT),
                            (SCREEN_WIDTH, -100),
                            (-100, -100)]
            spawn_point = random.choice(spawn_points)
            enemy_sprite.add(Enemy(spawn_point, 3, 3, 1))
            add_enemy_counter = 0
        
        # Add towers
        add_tower_counter += difficulty
        if add_tower_counter >= 2000:
            spawn_point = [0, 0]
            if player.rect.center[0] >= SCREEN_WIDTH/2:
                spawn_point[0] = random.randint(70, SCREEN_WIDTH/2 - 70)
            elif player.rect.center[0] < SCREEN_WIDTH/2:
                spawn_point[0] = random.randint(SCREEN_WIDTH/2 + 70, SCREEN_WIDTH - 70)
            if player.rect.center[1] >= SCREEN_HEIGHT/2:
                spawn_point[1] = random.randint(70, SCREEN_HEIGHT/2 - 70)
            elif player.rect.center[1] < SCREEN_HEIGHT/2:
                spawn_point[1] = random.randint(SCREEN_HEIGHT/2 + 70, SCREEN_HEIGHT - 70)
            spawn_point = tuple(spawn_point)
            explosion_sprite.add(Explosion(spawn_point, 'blue_explosion', (200, 200)))
            tower_sprite.add(ShootingTower(spawn_point, 6, 3))
            add_tower_counter = 0

        # Add horses
        add_horse_counter += difficulty
        if add_horse_counter >= 3500 and time > 2000:
            side = random.choice(['left', 'right'])
            spawn_position = random.randint(100, SCREEN_HEIGHT - 100)
            horse = Horse(spawn_position, side, 6, 5)
            horse_sprite.add(horse)
            explosion_sprite.add(Explosion(horse.rect.center, 'blue_explosion', (200, 200)))
            add_horse_counter = 0


        # --- Update all the objects --- 

        # PLAYER
        player.update()

        # If player is shooting
        if player_shooting and not game_end:
            player_shooting_counter += 1
            if player_shooting_counter >= 10:
                aim = pg.mouse.get_pos()
                missile_sprite.add(Missile(player.rect.center, aim, 12, 'blue'))
                laser_sound.play()
                player_shooting_counter = 0


        # ENEMIES
        for enemy in enemy_sprite:
            enemy.update((player.rect.center[0], player.rect.center[1]))

            # If the enemy caught up with the player
            if player.rect.collidepoint(enemy.rect.center) and not game_end:
                
                explosion_sprite.add(Explosion(enemy.rect.center, 'explosion', (150, 150)))
                explosion_sound.play()
                damage_sound.play()
                enemy.kill()
                player.brighten()
                player.life -= 1

                if player.life <= 0:   # ====== GAME OVER ======
                    explosion_sprite.add(Explosion(player.rect.center, 'explosion', (150, 150)))
                    explosion_sound.play()
                    player_death_sound.play()
                    pg.mixer.music.fadeout(2000)   # Music fadeout
                    player.kill()
                    update_ranking(level, scoreboard.score)
                    game_end = True
                    alpha = -700
            
            # Check if the missile hit the enemy
            for missile in missile_sprite:
                if enemy.rect.collidepoint(missile.rect.center):
                    enemy.life -= 1
                    missile.kill()
                    enemy.brighten(player.rect.center)

                    if enemy.life <= 0:   # If the enemy dies
                        explosion_sprite.add(Explosion(enemy.rect.center, 'explosion', (150, 150)))
                        explosion_sound.play()
                        points += enemy.points
                        enemy.kill()

        # TOWERS
        for tower in tower_sprite:
            tower.update(player.rect.center)

            tower_shooting_counter += 1
            if tower_shooting_counter >= 61:
                enemy_missile_sprite.add(Missile(tower.rect.center, player.rect.center, 6, 'red'))
                enemy_laser_sound.play()
                tower_shooting_counter = 0

            # Check if  the player collided with the tower
            if player.rect.collidepoint(tower.rect.center) and not game_end:

                explosion_sprite.add(Explosion(tower.rect.center, 'explosion', (200, 200)))
                explosion_sound.play()
                damage_sound.play()
                tower.kill()
                player.brighten()
                player.life -= 1

                if player.life <= 0:   # ====== GAME OVER ======
                    explosion_sprite.add(Explosion(player.rect.center, 'explosion', (150, 150)))
                    explosion_sound.play()
                    player_death_sound.play()
                    pg.mixer.music.fadeout(2000)
                    player.kill()
                    update_ranking(level, scoreboard.score)
                    game_end = True
                    alpha = -700

            # Check if the missile hit the tower
            for missile in missile_sprite:
                if tower.rect.collidepoint(missile.rect.center):
                    tower.life -= 1
                    missile.kill()
                    tower.brighten(player.rect.center)
                    if tower.life <= 0:   # If the tower dies
                        explosion_sprite.add(Explosion(tower.rect.center, 'explosion', (200, 200)))
                        explosion_sound.play()
                        tower.kill()
                        points += tower.points
        

        # HORSES
        for horse in horse_sprite:
            horse.update()

            horse_shooting_counter += 1
            if horse_shooting_counter >= 170:
                enemy_missile_sprite.add(FireBall(horse.rect.center, horse.side))
                fireball_sound.play()
                horse_shooting_counter = 0

            # Check if  the player collided with the horse
            if player.rect.collidepoint(horse.rect.center) and not game_end:

                explosion_sprite.add(Explosion(horse.rect.center, 'explosion', (200, 200)))
                explosion_sound.play()
                damage_sound.play()
                horse.kill()
                player.brighten()
                player.life -= 1

                if player.life <= 0:   # ====== GAME OVER ======
                    explosion_sprite.add(Explosion(player.rect.center, 'explosion', (150, 150)))
                    explosion_sound.play()
                    player_death_sound.play()
                    pg.mixer.music.fadeout(2000)
                    player.kill()
                    update_ranking(level, scoreboard.score)
                    game_end = True
                    alpha = -700

            # Check if the missile hit the horse
            for missile in missile_sprite:
                if horse.rect.collidepoint(missile.rect.center):
                    horse.life -= 1
                    missile.kill()
                    horse.brighten()
                    if horse.life <= 0:   # If the horse dies
                        explosion_sprite.add(Explosion(horse.rect.center, 'explosion', (200, 200)))
                        explosion_sound.play()
                        horse.kill()
                        points += horse.points
        
        
        # Update all the player's missiles
        for missile in missile_sprite:
            missile.update()
        
        # Update all the enemies' missiles
        for missile in enemy_missile_sprite:
            missile.update()

            # If the missile hit the player
            if player.rect.collidepoint(missile.rect.center) and not game_end:

                missile.kill()
                player.brighten()
                damage_sound.play()
                player.life -= 1

                if player.life <= 0:   # ====== GAME OVER ======
                    explosion_sprite.add(Explosion(player.rect.center, 'explosion', (150, 150)))
                    explosion_sound.play()
                    player_death_sound.play()
                    pg.mixer.music.fadeout(2000)   # Music fadeout
                    player.kill()
                    update_ranking(level, scoreboard.score)
                    game_end = True
                    alpha = -700


        if not game_end:
            scoreboard.update(points)
        CURSOR.update()
        pg.display.update()



# ============================  PAUSE  ============================

def pause(level, score=None):
    """Pause the game and display a pause screen."""

    global running_game, running_pause, restart, CURSOR
    CURSOR.image = CURSOR.arrow
    transition_to = False
    alpha = 0   # Transparence
    go_to = ''
    background = load_image('background.jpg', (SCREEN_WIDTH, SCREEN_HEIGHT), False)
    running_pause = True

    while running_pause:
        SCREEN.fill((0, 0, 0))
        SCREEN.set_alpha(100)
        mx, my = pg.mouse.get_pos()  # Mouse position

        resume_button = draw_text('Resume', (SCREEN_WIDTH/2, 300), MENU_FONT, (255, 255, 255))
        restart_button = draw_text('Restart', (SCREEN_WIDTH/2, 400), MENU_FONT, (255, 255, 255))
        menu_button = draw_text('Return to menu', (SCREEN_WIDTH/2, 500), MENU_FONT, (255, 255, 255))

        # Transition to other screen
        if transition_to:
            darken_screen(alpha)
            alpha += 10
            if alpha >= 255:
                running_pause = False
                running_game = False
                if go_to == 'menu':  # If menu was chosen, do not restart the game
                    restart = False
            CLOCK.tick(60)
            CURSOR.update()
            pg.display.update()
            continue

        click = False
        for event in pg.event.get():
            if event.type == QUIT:
                update_ranking(level, score)
                pg.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                click = True
            if event.type == KEYDOWN and event.key == K_ESCAPE:   # Resume
                running_pause = False
                SCREEN.blit(background, (0, 0))   # Restore the background

        if resume_button.collidepoint(mx, my):
            draw_text('Resume', (SCREEN_WIDTH/2, 300), HIGHLIGHTED_FONT, (255, 255, 255), True)
            if click:
                running_pause = False
                SCREEN.blit(background, (0, 0))   # Restore the background
        if restart_button.collidepoint(mx, my):
            draw_text('Restart', (SCREEN_WIDTH/2, 400), HIGHLIGHTED_FONT, (255, 255, 255), True)
            if click:
                update_ranking(level, score)
                transition_to = True
                alpha = 0
        if menu_button.collidepoint(mx, my):
            draw_text('Return to menu', (SCREEN_WIDTH/2, 500), HIGHLIGHTED_FONT, (255, 255, 255), True)
            if click:
                update_ranking(level, score)
                pg.mixer.music.fadeout(1000)
                transition_to = True
                alpha = 0
                go_to = 'menu'

        CURSOR.update()
        pg.display.update()
        CLOCK.tick(60)



# ============================  GAME OVER  ============================

def game_over(score):
    """Display a 'game over' screen."""

    global running_game, running_game_over, restart, CURSOR
    CURSOR.image = CURSOR.arrow
    transition_from = True
    transition_to = False
    running_game_over = True
    alpha = 255   # Transparence
    go_to = ''

    game_over_sound = load_sound('game_over_sound.wav', MUSIC_VOLUME)
    game_over_sound.play()

    while running_game_over:
        SCREEN.fill((0, 0, 0))
        mx, my = pg.mouse.get_pos()  # Mouse position

        draw_text('GAME OVER', (SCREEN_WIDTH/2, 100), MENU_FONT, (200, 0, 0))
        draw_text('Your score: ' + str(score), (SCREEN_WIDTH/2, 300), MENU_FONT, (255, 255, 255))
        restart_button = draw_text('Restart', (SCREEN_WIDTH/2, 500), MENU_FONT, (255, 255, 255))
        menu_button = draw_text('Return to menu', (SCREEN_WIDTH/2, 600), MENU_FONT, (255, 255, 255))

        # Transition to other screen
        if transition_to:
            darken_screen(alpha)
            alpha += 10
            if alpha >= 255:
                running_game_over = False
                running_game = False
                if go_to == 'menu':   # If menu was chosen, do not restart the game
                    restart = False
            CLOCK.tick(60)
            CURSOR.update()
            pg.display.update()
            continue
        
        # Transition from game to game over
        if transition_from:
            darken_screen(alpha)
            alpha -= 10
            if alpha <= 0:
                transition_from = False

        click = False
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                click = True

        if restart_button.collidepoint(mx, my):
            draw_text('Restart', (SCREEN_WIDTH/2, 500), HIGHLIGHTED_FONT, (255, 255, 255), True)
            if click:
                transition_to = True
                alpha = 0
        if menu_button.collidepoint(mx, my):
            draw_text('Return to menu', (SCREEN_WIDTH/2, 600), HIGHLIGHTED_FONT, (255, 255, 255), True)
            if click:
                transition_to = True
                alpha = 0
                go_to = 'menu'

        CURSOR.update()
        pg.display.update()
        CLOCK.tick(60)


icon = load_image('icon.png', (100, 100))
pg.display.set_icon(icon)
pg.display.set_caption('Dangerous Chicken')
menu()
