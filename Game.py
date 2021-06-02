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
        play_button = draw_text('Play', (SCREEN_WIDTH/2, 100), MENU_FONT, (0, 200, 0))
        rules_button = draw_text('Rules', (SCREEN_WIDTH/2, 200), MENU_FONT, (255, 255, 255))
        options_button = draw_text('Options', (SCREEN_WIDTH/2, 300), MENU_FONT, (255, 255, 255))
        ranking_button = draw_text('Ranking', (SCREEN_WIDTH/2, 400), MENU_FONT, (255, 255, 255))
        author_button = draw_text('Author', (SCREEN_WIDTH/2, 500), MENU_FONT, (255, 255, 255))
        quit_button = draw_text('Quit', (SCREEN_WIDTH/2, 600), MENU_FONT, (200, 0, 0))

        # Transition from menu to other screen
        if transition_to:
            # Darken the SCREEN
            darken = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            darken.set_alpha(alpha)
            darken.fill((0, 0, 0))
            SCREEN.blit(darken, (0, 0))
            alpha += 10
            if alpha >= 255:
                if go_to == 'game':
                    restart = True
                    while restart:
                        game()
                    play_music('menu_music.wav', MUSIC_VOLUME)
                    CURSOR.image = CURSOR.arrow
                elif go_to == 'options':
                    options()
                elif go_to == 'ranking':
                    ranking()
                transition_from = True
                transition_to = False
                alpha = 255
            CLOCK.tick(60)
            CURSOR.update()
            pg.display.update()
            continue
        
        # Transition from pause or game over to menu
        if transition_from:
            darken = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            darken.set_alpha(alpha)
            darken.fill((0, 0, 0))
            SCREEN.blit(darken, (0, 0))
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
            draw_text('Play', (SCREEN_WIDTH/2, 100), HIGHLIGHTED_FONT, (0, 200, 0), True)
            if click:
                transition_to = True
                pg.mixer.music.fadeout(500)   # Music fadeout
                go_to = 'game'
        elif rules_button.collidepoint(mx, my):
            draw_text('Rules', (SCREEN_WIDTH/2, 200), HIGHLIGHTED_FONT, (255, 255, 255), True)
            if click:
                pass
        elif options_button.collidepoint(mx, my):
            draw_text('Options', (SCREEN_WIDTH/2, 300), HIGHLIGHTED_FONT, (255, 255, 255), True)
            if click:
                transition_to =True
                go_to = 'options'
        elif ranking_button.collidepoint(mx, my):
            draw_text('Ranking', (SCREEN_WIDTH/2, 400), HIGHLIGHTED_FONT, (255, 255, 255), True)
            if click:
                transition_to = True
                go_to = 'ranking'
        elif author_button.collidepoint(mx, my):
            draw_text('Author', (SCREEN_WIDTH/2, 500), HIGHLIGHTED_FONT, (255, 255, 255), True)
            if click:
                pass
        elif quit_button.collidepoint(mx, my):
            draw_text('Quit', (SCREEN_WIDTH/2, 600), HIGHLIGHTED_FONT, (200, 0, 0), True)
            if click:
                pg.quit()
                sys.exit()

        CURSOR.update()
        pg.display.update()
        CLOCK.tick(80)



# ============================  OPTIONS  ============================

def options():
    """Display the game options and allow the user to customize them."""

    global MUSIC_VOLUME, SOUNDS_VOLUME, DIFFICULTY, CURSOR
    running_options = True
    transition_from = True
    transition_to = False
    alpha = 255
    music_slide = False
    sounds_slide = False
    difficulties = ['Easy', 'Normal', 'Hard', 'Hardcore']
    difficulty_number = difficulties.index(DIFFICULTY)

    background = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill((0, 0, 0))

    music_slider = Slider((SCREEN_WIDTH/2, 200), MUSIC_VOLUME)
    sounds_slider = Slider((SCREEN_WIDTH/2, 400), SOUNDS_VOLUME)

    slider_sprite = pg.sprite.Group()
    slider_sprite.add(music_slider)
    slider_sprite.add(sounds_slider)

    triangle_left = load_image('triangle.png', (40, 40))
    triangle_left_rect = triangle_left.get_rect()
    triangle_left_rect.center = (SCREEN_WIDTH/2 - 200, 600)
    triangle_left_big = load_image('triangle.png', (45, 45))
    triangle_left_big_rect = triangle_left_big.get_rect()
    triangle_left_big_rect.center = (SCREEN_WIDTH/2 - 200, 600)

    triangle_right = pg.transform.flip(triangle_left, True, False)
    triangle_right_rect = triangle_right.get_rect()
    triangle_right_rect.center = (SCREEN_WIDTH/2 + 200, 600)
    triangle_right_big = pg.transform.flip(triangle_left_big, True, False)
    triangle_right_big_rect = triangle_right_big.get_rect()
    triangle_right_big_rect.center = (SCREEN_WIDTH/2 + 200, 600)

    while running_options:
        mx, my = pg.mouse.get_pos()  # Mouse position
        music_shift = 0
        sounds_shift = 0
        SCREEN.fill((0, 0, 0))


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
                if music_slider.slider_rect.collidepoint(event.pos):
                    music_slide = True
                    dist_x = music_slider.slider_rect.center[0] - mx
                elif sounds_slider.slider_rect.collidepoint(event.pos):
                    sounds_slide = True
                    dist_x = sounds_slider.slider_rect.center[0] - mx

            elif event.type == MOUSEBUTTONUP and event.button == 1:
                music_slide = False
                sounds_slide =False

            elif event.type == MOUSEMOTION:
                if music_slide:
                    music_shift = mx + dist_x - music_slider.slider_rect.center[0]
                elif sounds_slide:
                    sounds_shift = mx + dist_x - sounds_slider.slider_rect.center[0]
        

        # BUTTONS
        if triangle_left_rect.collidepoint((mx, my)):
            SCREEN.blit(triangle_left_big, triangle_left_big_rect)
            if click:
                difficulty_number -= 1
        elif triangle_right_rect.collidepoint((mx, my)):
            SCREEN.blit(triangle_right_big, triangle_right_big_rect)
            if click:
                difficulty_number += 1


        # DRAWING
        draw_text('Music volume', (SCREEN_WIDTH/2, 100), MENU_FONT, (255, 255, 255))
        draw_text('Sounds volume', (SCREEN_WIDTH/2, 300), MENU_FONT, (255, 255, 255))

        draw_text('Difficulty level', (SCREEN_WIDTH/2, 500), MENU_FONT, (255, 255, 255))
        draw_text(DIFFICULTY, (SCREEN_WIDTH/2, 600), MENU_FONT, (255, 255, 255), True)

        SCREEN.blit(triangle_left, triangle_left_rect)
        SCREEN.blit(triangle_right, triangle_right_rect)

        slider_sprite.clear(SCREEN, background)
        slider_sprite.draw(SCREEN)

        music_slider.update(music_shift)
        sounds_slider.update(sounds_shift)


        # Transition from menu to options
        if transition_from:
            darken = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            darken.set_alpha(alpha)
            darken.fill((0, 0, 0))
            SCREEN.blit(darken, (0, 0))
            alpha -= 10
            if alpha <= 0:
                transition_from = False
        
        # Transition from options to menu
        if transition_to:
            # Darken the screen
            darken = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            darken.set_alpha(alpha)
            darken.fill((0, 0, 0))
            SCREEN.blit(darken, (0, 0))
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

    while running_ranking:

        SCREEN.fill((0, 0, 0))
        draw_text('RANKING', (SCREEN_WIDTH/2, 100), MENU_FONT, (0, 0, 200))

        # Draw the best scores and their dates
        position = 600
        for score, date in zip(RANKING[0], RANKING[1]):
            draw_text(str(score), (SCREEN_WIDTH/2 - 300, position), MENU_FONT, (255, 255, 255))
            draw_text(str(date), (SCREEN_WIDTH/2 + 400, position), MENU_FONT, (255, 255, 255))
            position -= 100

        # Transition from ranking to menu
        if transition_to:
            # Darken the screen
            darken = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            darken.set_alpha(alpha)
            darken.fill((0, 0, 0))
            SCREEN.blit(darken, (0, 0))
            alpha += 10
            if alpha >= 255:
                running_ranking = False
            CURSOR.update()
            pg.display.update()
            CLOCK.tick(60)
            continue

        # Transition from menu to ranking
        if transition_from:
            darken = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            darken.set_alpha(alpha)
            darken.fill((0, 0, 0))
            SCREEN.blit(darken, (0, 0))
            alpha -= 10
            if alpha <= 0:
                transition_from = False

        for event in pg.event.get():

            if event.type == QUIT:
                pg.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_ESCAPE:
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
    fireball_sound = load_sound('fireball_sound.mp3', 1.6*SOUNDS_VOLUME)
    damage_sound = load_sound('damage_sound.mp3', 1.2*SOUNDS_VOLUME)
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
        elif DIFFICULTY == 'Normal':
            difficulty = time**(1.0/6.0)
        elif DIFFICULTY == 'Hard':
            difficulty = time**(1.0/4.0)
        elif DIFFICULTY == 'Hardcore':
            difficulty = time**(1.0/2.0)

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
            # Darken the screen
            darken = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            darken.set_alpha(alpha)
            darken.fill((0, 0, 0))
            SCREEN.blit(darken, (0, 0))
            alpha += 10
            if alpha >= 255:
                game_over(scoreboard.score)

        # Transition from menu to game
        if transition_from:
            darken = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            darken.set_alpha(alpha)
            darken.fill((0, 0, 0))
            SCREEN.blit(darken, (0, 0))
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
                    pause(scoreboard.score)
                    CURSOR.image = CURSOR.crosshair

                # WSAD - moving the character
                if event.key == K_a:
                    player.x_velocity = -4
                if event.key == K_d:
                    player.x_velocity = 4
                if event.key == K_w:
                    player.y_velocity = -4
                if event.key == K_s:
                    player.y_velocity = 4

            elif event.type == KEYUP:
                if event.key == K_a:
                    player.x_velocity = 0
                if event.key == K_d:
                    player.x_velocity = 0
                if event.key == K_w:
                    player.y_velocity = 0
                if event.key == K_s:
                    player.y_velocity = 0
            
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
        if add_horse_counter >= 3500 and time > 1000:
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
        if player_shooting:
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
                    update_ranking(scoreboard.score)
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
                laser_sound.play()
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
                    update_ranking(scoreboard.score)
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
            if horse_shooting_counter >= 200:
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
                    update_ranking(scoreboard.score)
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
                    update_ranking(scoreboard.score)
                    game_end = True
                    alpha = -700


        scoreboard.update(points)
        CURSOR.update()
        pg.display.update()



# ============================  PAUSE  ============================

def pause(score=None):
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
            # Darken the screen
            darken = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            darken.set_alpha(alpha)
            darken.fill((0, 0, 0))
            SCREEN.blit(darken, (0, 0))
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
                update_ranking(score)
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
                update_ranking(score)
                transition_to = True
                alpha = 0
        if menu_button.collidepoint(mx, my):
            draw_text('Return to menu', (SCREEN_WIDTH/2, 500), HIGHLIGHTED_FONT, (255, 255, 255), True)
            if click:
                update_ranking(score)
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
            # Darken the screen
            darken = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            darken.set_alpha(alpha)
            darken.fill((0, 0, 0))
            SCREEN.blit(darken, (0, 0))
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
            darken = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            darken.set_alpha(alpha)
            darken.fill((0, 0, 0))
            SCREEN.blit(darken, (0, 0))
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
