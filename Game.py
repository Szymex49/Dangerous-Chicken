import pygame as pg
from pygame.locals import *
from tools import *
from classes import *
import sys


# Main options
pg.init()
clock = pg.time.Clock()
menu_font = pg.font.SysFont('Calibri', 80)

running_options = True
running_pause = True
running_game = True
running_game_over = True
restart = False
transition = False


def menu():
    """Display the main menu of the game."""

    global restart
    transition = True
    transition_to = False
    alpha = 255   # Transparence

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

        # Darken
        if transition_to:
            # Darken the screen
            darken = pg.Surface((screen_width, screen_height))
            darken.set_alpha(alpha)
            darken.fill((0, 0, 0))
            screen.blit(darken, (0, 0))
            alpha += 10
            if alpha >= 255:
                restart = True
                while restart:
                    game()
                transition = True
                transition_to = False
                alpha = 255
            clock.tick(60)
            pg.display.update()
            continue
        
        # If we come back from pause screen or 'game over' screen, make smooth transition
        if transition:
            darken = pg.Surface((screen_width, screen_height))
            darken.set_alpha(alpha)
            darken.fill((0, 0, 0))
            screen.blit(darken, (0, 0))
            alpha -= 10
            if alpha <= 0:
                transition = False

        click = False
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                click = True

        if play_button.collidepoint(mx, my) and click:
            transition_to = True
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

    global running_game, running_pause, restart
    pause_end = False
    alpha = 0   # Transparence
    go_to = ''
    background = load_image('background.jpg', False)
    running_pause = True

    while running_pause:
        screen.fill((0, 0, 0))
        screen.set_alpha(100)
        mx, my = pg.mouse.get_pos()  # Mouse position

        resume_button = draw_text('Resume', (screen_width/2, 100), menu_font, (0, 200, 0))
        restart_button = draw_text('Restart', (screen_width/2, 200), menu_font, (0, 0, 200))
        menu_button = draw_text('Return to menu', (screen_width/2, 300), menu_font, (200, 0, 0))

        # Transition to other screen
        if pause_end:
            # Darken the screen
            darken = pg.Surface((screen_width, screen_height))
            darken.set_alpha(alpha)
            darken.fill((0, 0, 0))
            screen.blit(darken, (0, 0))
            alpha += 10
            if alpha >= 255:
                running_pause = False
                running_game = False
                if go_to == 'menu':  # If menu was chosen, do not restart the game
                    restart = False
            clock.tick(60)
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
                screen.blit(background, (0, 0))   # Restore the background

        if resume_button.collidepoint(mx, my) and click:
            running_pause = False
            screen.blit(background, (0, 0))   # Restore the background
        if restart_button.collidepoint(mx, my) and click:
            pause_end = True
            alpha = 0
        if menu_button.collidepoint(mx, my) and click:
            pause_end = True
            alpha = 0
            go_to = 'menu'

        pg.display.update()
        clock.tick(60)


def game_over():
    """Display a 'game over' screen."""

    global running_game, running_game_over, restart
    game_over_end = False
    alpha = 0   # Transparence
    go_to = ''
    running_game_over = True

    while running_game_over:
        screen.fill((0, 0, 0))
        mx, my = pg.mouse.get_pos()  # Mouse position

        restart_button = draw_text('Restart', (screen_width/2, 100), menu_font, (0, 200, 0))
        menu_button = draw_text('Return to menu', (screen_width/2, 200), menu_font, (200, 0, 0))

        # Transition to other screen
        if game_over_end:
            # Darken the screen
            darken = pg.Surface((screen_width, screen_height))
            darken.set_alpha(alpha)
            darken.fill((0, 0, 0))
            screen.blit(darken, (0, 0))
            alpha += 10
            if alpha >= 255:
                running_game_over = False
                running_game = False
                if go_to == 'menu':   # If menu was chosen, do not restart the game
                    restart = False
            clock.tick(60)
            pg.display.update()
            continue

        click = False
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                click = True

        if restart_button.collidepoint(mx, my) and click:
            game_over_end = True
            alpha = 0
        if menu_button.collidepoint(mx, my) and click:
            game_over_end = True
            alpha = 0
            go_to = 'menu'

        pg.display.update()
        clock.tick(60)


def game():
    """Start the game."""

    global running_game
    transition = True
    alpha = 255   # Transparence
    running_game = True

    # Background
    background = load_image('background.jpg', False)

    # Character
    hero_sprite = pg.sprite.Group()
    hero = Hero()
    hero_sprite.add(hero)

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
        clock.tick(60)
        screen.blit(background, (0, 0))
        points = 0

        # Clear the screen
        hero_sprite.clear(screen, background)
        enemy_sprite.clear(screen, background)
        explosion_sprite.clear(screen, background)
        missile_sprite.clear(screen, background)
        scoreboard_sprite.clear(screen, background)

        # Draw the objects
        hero_sprite.draw(screen)
        enemy_sprite.draw(screen)
        explosion_sprite.draw(screen)
        missile_sprite.draw(screen)
        scoreboard_sprite.draw(screen)

        # Draw lifes
        if hero.life == 0:
            draw_lifes(0)
        if hero.life == 1:
            draw_lifes(1)
        if hero.life == 2:
            draw_lifes(2)
        if hero.life == 3:
            draw_lifes(3)

        # If the game has just started, display transition
        if transition:
            darken = pg.Surface((screen_width, screen_height))
            darken.set_alpha(alpha)
            darken.fill((0, 0, 0))
            screen.blit(darken, (0, 0))
            alpha -= 10
            if alpha <= 0:
                transition = False

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
            enemy_sprite.add(Enemy((50, 50), 3, 3, 1))
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
                if hero.life <= 0:  # If the hero's life has ended - GAME OVER
                    game_over()
            
            for missile_obj in missile_sprite:
                if enemy.rect.collidepoint(missile_obj.rect.center):  # If the missile hit the enemy
                    enemy.life -= 1
                    if enemy.life <= 0:   # If the enemy dies
                        explosion_sprite.add(Explosion(enemy.rect.center))  # Draw the explosion
                        enemy.kill()
                        points += enemy.points
                    missile_obj.kill()
        
        for missile_obj in missile_sprite:
            missile_obj.update()
            if 0 <= missile_obj.rect.center[0] >= screen_width or 0 >= missile_obj.rect.center[1] >= screen_height:
                missile_obj.kill()
        
        for explosion in explosion_sprite:
            explosion.update()

        scoreboard.update(points)

        pg.display.update()


pg.display.set_caption("fajna gra")
menu()
