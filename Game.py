from classes import *


# Main options
pg.init()
pg.mixer.set_num_channels(20)
CLOCK = pg.time.Clock()
MENU_FONT = pg.font.SysFont('Calibri', 80)

running_options = True
running_pause = True
running_game = True
running_game_over = True
restart = False
transition = False


def menu():
    """Display the main menu of the game."""

    global restart
    transition_from = True
    transition_to = False
    alpha = 255   # Transparence
    go_to = ''

    play_music('bg_music.wav', MUSIC_VOLUME)

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

        # Make transition from menu to other screen
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
                    play_music('bg_music.wav', MUSIC_VOLUME)
                elif go_to == 'options':
                    options()
                elif go_to == 'ranking':
                    ranking()
                transition_from = True
                transition_to = False
                alpha = 255
            CLOCK.tick(60)
            pg.display.update()
            continue
        
        # If we come back from pause SCREEN or 'game over' SCREEN, make smooth transition
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

        if play_button.collidepoint(mx, my) and click:
            transition_to = True
            go_to = 'game'
        elif rules_button.collidepoint(mx, my) and click:
            pass
        elif options_button.collidepoint(mx, my) and click:
            transition_to =True
            go_to = 'options'
        elif ranking_button.collidepoint(mx, my) and click:
            transition_to = True
            go_to = 'ranking'
        elif author_button.collidepoint(mx, my) and click:
            pass
        elif quit_button.collidepoint(mx, my) and click:
            pg.quit()
            sys.exit()

        pg.display.update()
        CLOCK.tick(60)


def options():
    """Display the game options and allow the user to customize them."""

    global running_options
    running_options = True
    transition_from = True
    transition_to = False
    alpha = 255
    music_slide = False
    sounds_slide = False

    SCREEN.fill((0, 0, 0))
    background = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill((0, 0, 0))
    axis_im = pg.transform.scale(load_image('axis.png'), (500, 80))

    # Music volume slider
    draw_text('Music volume', (SCREEN_WIDTH/2, 100), MENU_FONT, (255, 255, 255))
    music_vol_im = axis_im.get_rect()
    music_vol_im.center = (SCREEN_WIDTH/2, 200)
    SCREEN.blit(axis_im, music_vol_im)
    music_slider = Slider((SCREEN_WIDTH/2, 200))

    # Sounds volume slider
    draw_text('Sounds volume', (SCREEN_WIDTH/2, 300), MENU_FONT, (255, 255, 255))
    sounds_vol_im = axis_im.get_rect()
    sounds_vol_im.center = (SCREEN_WIDTH/2, 400)
    SCREEN.blit(axis_im, sounds_vol_im)
    sounds_slider = Slider((SCREEN_WIDTH/2, 400))

    slider_sprite = pg.sprite.Group()
    slider_sprite.add(music_slider)
    slider_sprite.add(sounds_slider)

    while running_options:
        mx, my = pg.mouse.get_pos()  # Mouse position
        music_shift = 0
        sounds_shift = 0

        click = False
        for event in pg.event.get():

            if event.type == QUIT:
                pg.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running_options = False

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                click = True
                if music_slider.rect.collidepoint(event.pos):
                    music_slide = True
                    dist_x = music_slider.rect.center[0] - mx
                elif sounds_slider.rect.collidepoint(event.pos):
                    sounds_slide = True
                    dist_x = sounds_slider.rect.center[0] - mx

            elif event.type == MOUSEBUTTONUP and event.button == 1:
                music_slide = False
                sounds_slide =False

            elif event.type == MOUSEMOTION:
                if music_slide:
                    music_shift = mx + dist_x - music_slider.rect.center[0]
                elif sounds_slide:
                    sounds_shift = mx + dist_x - sounds_slider.rect.center[0]

        SCREEN.blit(axis_im, music_vol_im)
        SCREEN.blit(axis_im, sounds_vol_im)

        music_slider.update(music_shift)
        sounds_slider.update(sounds_shift)
        slider_sprite.clear(SCREEN, background)
        slider_sprite.draw(SCREEN)

        pg.display.update()
        CLOCK.tick(60)


def ranking():
    """Display the screen with ranking of the best scores."""

    running_ranking = True
    transition_from = True
    transition_to = False
    alpha = 255

    SCREEN.fill((0, 0, 0))
    draw_text('RANKING', (SCREEN_WIDTH/2, 100), MENU_FONT, (0, 0, 200))

    position = 200
    for score, date in zip(RANKING.keys(), RANKING.values()):
        draw_text(str(score), (150, position), MENU_FONT, (255, 255, 255))
        draw_text(str(date), (500, position), MENU_FONT, (255, 255, 255))
        position += 100

    while running_ranking:
        SCREEN.fill((0, 0, 0))
        draw_text('RANKING', (SCREEN_WIDTH/2, 100), MENU_FONT, (0, 0, 200))

        position = 200
        for score, date in zip(RANKING.keys(), RANKING.values()):
            draw_text(str(score), (150, position), MENU_FONT, (255, 255, 255))
            draw_text(str(date), (500, position), MENU_FONT, (255, 255, 255))
            position += 100

        # Make transition from ranking to menu
        if transition_to:
            # Darken the screen
            darken = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            darken.set_alpha(alpha)
            darken.fill((0, 0, 0))
            SCREEN.blit(darken, (0, 0))
            alpha += 10
            if alpha >= 255:
                running_ranking = False
            CLOCK.tick(60)
            pg.display.update()
            continue

        # Make transition from menu to ranking
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
        
        pg.display.update()
        CLOCK.tick(60)


def game():
    """Start the game."""

    global running_game
    running_game = True
    transition_from = True
    game_end = False
    alpha = 255   # Transparence
    time = 0

    # Background
    background = load_image('background.jpg', False)

    # Sounds
    explosion_sound = load_sound('explosion_sound.mp3', SOUNDS_VOLUME)
    laser_sound = load_sound('laser_sound.mp3', SOUNDS_VOLUME)

    # Character
    player_sprite = pg.sprite.Group()
    player = Player()
    player_sprite.add(player)

    # Enemy
    enemy_sprite = pg.sprite.Group()
    enemy_sprite.add(Enemy((50, 50), 3, 3, 1))
    add_enemy_counter = 0

    # Lasers
    missile_sprite = pg.sprite.Group()

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

        # Clear the SCREEN
        player_sprite.clear(SCREEN, background)
        enemy_sprite.clear(SCREEN, background)
        explosion_sprite.clear(SCREEN, background)
        missile_sprite.clear(SCREEN, background)
        scoreboard_sprite.clear(SCREEN, background)

        # Draw the objects
        player_sprite.draw(SCREEN)
        enemy_sprite.draw(SCREEN)
        explosion_sprite.draw(SCREEN)
        missile_sprite.draw(SCREEN)
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
                game_over()

        # If the game has just started, display transition
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

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pause()

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
                aim = pg.mouse.get_pos()
                missile_sprite.add(Missile(player.rect.center, aim, 8))
                laser_sound.play()

        # Add enemies
        add_enemy_counter += time**(1.0/6.0)
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

        # Update all the objects
        player.update()

        for enemy in enemy_sprite:
            enemy.update((player.rect.center[0], player.rect.center[1]))

            # If the enemy caught up with the player
            if player.rect.collidepoint(enemy.rect.center):
                explosion_sprite.add(Explosion(enemy.rect.center))  # Draw the explosion of the enemy
                explosion_sound.play()
                enemy.kill()
                player.life -= 1
                if player.life <= 0:  # If the player's life has ended - GAME OVER
                    explosion_sprite.add(Explosion(player.rect.center))
                    pg.mixer.music.fadeout(2000)   # Music fadeout
                    player.kill()
                    update_ranking(scoreboard.score)
                    game_end = True
                    alpha = -700
            
            for missile_obj in missile_sprite:
                if enemy.rect.collidepoint(missile_obj.rect.center):  # If the missile hit the enemy
                    enemy.life -= 1
                    if enemy.life <= 0:   # If the enemy dies
                        explosion_sprite.add(Explosion(enemy.rect.center))  # Draw the explosion
                        explosion_sound.play()
                        enemy.kill()
                        points += enemy.points
                    missile_obj.kill()
        
        for missile_obj in missile_sprite:
            missile_obj.update()
            if 0 <= missile_obj.rect.center[0] >= SCREEN_WIDTH or 0 >= missile_obj.rect.center[1] >= SCREEN_HEIGHT:
                missile_obj.kill()

        scoreboard.update(points)

        pg.display.update()


def pause():
    """Pause the game and display a pause screen."""

    global running_game, running_pause, restart
    transition_to = False
    alpha = 0   # Transparence
    go_to = ''
    background = load_image('background.jpg', False)
    running_pause = True

    while running_pause:
        SCREEN.fill((0, 0, 0))
        SCREEN.set_alpha(100)
        mx, my = pg.mouse.get_pos()  # Mouse position

        resume_button = draw_text('Resume', (SCREEN_WIDTH/2, 100), MENU_FONT, (0, 200, 0))
        restart_button = draw_text('Restart', (SCREEN_WIDTH/2, 200), MENU_FONT, (0, 0, 200))
        menu_button = draw_text('Return to menu', (SCREEN_WIDTH/2, 300), MENU_FONT, (200, 0, 0))

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
            pg.display.update()
            continue

        click = False
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                click = True
            if event.type == KEYDOWN and event.key == K_ESCAPE:   # Resume
                running_pause = False
                SCREEN.blit(background, (0, 0))   # Restore the background

        if resume_button.collidepoint(mx, my) and click:
            running_pause = False
            SCREEN.blit(background, (0, 0))   # Restore the background
        if restart_button.collidepoint(mx, my) and click:
            transition_to = True
            alpha = 0
        if menu_button.collidepoint(mx, my) and click:
            transition_to = True
            alpha = 0
            go_to = 'menu'

        pg.display.update()
        CLOCK.tick(60)


def game_over():
    """Display a 'game over' screen."""

    global running_game, running_game_over, restart
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
                running_game_over = False
                running_game = False
                if go_to == 'menu':   # If menu was chosen, do not restart the game
                    restart = False
            CLOCK.tick(60)
            pg.display.update()
            continue
        
        # If the game has just ended, make transition to 'game over' screen
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

        if restart_button.collidepoint(mx, my) and click:
            transition_to = True
            alpha = 0
        if menu_button.collidepoint(mx, my) and click:
            transition_to = True
            alpha = 0
            go_to = 'menu'

        pg.display.update()
        CLOCK.tick(60)


pg.display.set_caption("fajna gra")
menu()
