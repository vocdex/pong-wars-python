"""
Main for pong wars.
"""

import pygame
import numpy
import random
import argparse
import os

import pong_wars_model
import pong_wars_view


# Constants
WIDTH_EACH_PLAYER, HEIGHT_EACH_PLAYER = 16, 16  # Numbers of squares in width and height for each player
SQUARE_SIZE = 16                                # Size of a square in pixel
BALL_RADIUS = 12                                # Radius of the ball
BALL_SPEED = 15                                 # Speed of the ball in pixel, better not bigger than SQUARE_SIZE

OVERWRITE_AREA_MOVE_SPEED = SQUARE_SIZE / 4.0
OVERWRITE_SIZE = 8 * SQUARE_SIZE

TEXT_PANEL_HEIGHT = 20
TUTORIAL_PANEL_HEIGHT = 100

PLAYER_NUM_LIST = [2, 4]                        # Numbers of players supported

PLAYER_COLORS = [(255, 153, 153), (153, 153, 255), (255, 153, 255), (153, 255, 153)]
BALL_COLORS = [(255, 0, 0), (0, 0, 255), (255, 0, 255), (0, 255, 0)]    # Ball colors for each player, contrast is important

PANEL_COLOR = (50, 50, 50)  # Dark gray background for panel
TEXT_COLOR = (255, 255, 255)
        
GAME_TIME = 2 * 60              # In seconds
OVERWRITE_COOLDOWN_TIME = 20    # In seconds


def main(args):
    player_num = 4

    if args.seed:
        random.seed(args.seed)
    if args.record_frames:
        frame_dir = "frames"
        os.makedirs(frame_dir, exist_ok=True)
        frame_num = 0
    if args.player_num:
        if args.player_num in PLAYER_NUM_LIST:
            player_num = args.player_num

    width_square_num = WIDTH_EACH_PLAYER * 2
    height_square_num = HEIGHT_EACH_PLAYER * 2 if player_num == 4 else HEIGHT_EACH_PLAYER
    width_pixel, height_pixel = width_square_num * SQUARE_SIZE, height_square_num * SQUARE_SIZE

    pygame.init()
    pygame.font.init()  # Initialize the font module

    font = pygame.font.SysFont('Consolas', 18)  # Or any other preferred font

    # Set up the display
    screen = pygame.display.set_mode((width_pixel, height_pixel + TEXT_PANEL_HEIGHT * 3 + TUTORIAL_PANEL_HEIGHT))
    pygame.display.set_caption("Pong Wars Strategy")

    clock = pygame.time.Clock()
    squares = pong_wars_model.create_squares(width_square_num, width_square_num, player_num)

    ball_positions = [numpy.array([width_pixel / 4, height_pixel / 2], dtype=float),
                      numpy.array([3 * width_pixel / 4, height_pixel / 2], dtype=float)]
    if player_num == 4:
        ball_positions = [numpy.array([width_pixel / 4, height_pixel / 4], dtype=float), 
                          numpy.array([3 * width_pixel / 4, height_pixel / 4], dtype=float), 
                          numpy.array([width_pixel / 4, 3 * height_pixel / 4], dtype=float), 
                          numpy.array([3 * width_pixel / 4, 3 * height_pixel / 4], dtype=float)]
    desired_angles = [numpy.pi * i / 4 for i in [1, 3, 7, 5][:player_num]]
    angle_variation = numpy.pi / 16  # +/- 11.25 degrees variation
    start_angles = desired_angles + numpy.random.uniform(-angle_variation, angle_variation, player_num)
    ball_directions = numpy.vstack((numpy.cos(start_angles), numpy.sin(start_angles))).T
    ball_directions /= numpy.linalg.norm(ball_directions, axis=1)[:, numpy.newaxis]

    running = True
    paused = False
    gameover = False

    game_timer = GAME_TIME

    overwrite_player_index = 1
    overwrite_position = numpy.array([width_pixel // 2, height_pixel // 2], dtype=float)
    overwrite_size = numpy.array([OVERWRITE_SIZE, OVERWRITE_SIZE], dtype=float)
    overwrite_cooldown_timers = numpy.zeros(player_num, dtype=float)
    
    while running:
        enter_pushed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not gameover:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
                    if pygame.K_1 <= event.key <= pygame.K_0 + player_num:
                        overwrite_player_index = event.key - pygame.K_0
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        enter_pushed = True

        if gameover:    # Display winner
            max_score = max(scores.values())
            winners = [key for key, value in scores.items() if value == max_score]
            if (len(winners) > 1):
                gameover = False    # Only one winner is needed, so game continues
            else:
                winner = int(winners[0])
                winner_text = "Winner: Player " + str(winner)
                pong_wars_view.draw_centered_text_panel(screen, winner_text, font, width_pixel, height_pixel, TEXT_PANEL_HEIGHT, PANEL_COLOR, PLAYER_COLORS[winner-1])
        else:           # Display game timer
            game_timer_text = "Time left: " + f"{game_timer:.1f}"
            pong_wars_view.draw_centered_text_panel(screen, game_timer_text, font, width_pixel, height_pixel, TEXT_PANEL_HEIGHT, PANEL_COLOR, TEXT_COLOR)

        if not paused and not gameover:
            for i in range(player_num):
                ball_directions[i] = pong_wars_model.update_square_and_bounce(ball_positions[i], ball_directions[i], i+1, squares, SQUARE_SIZE, BALL_RADIUS)    # Player index in "squares" starts from "1" rather than "0"
                ball_directions[i] = pong_wars_model.check_boundary_collision(ball_positions[i], ball_directions[i], width_pixel, height_pixel, BALL_RADIUS, BALL_SPEED)
                ball_positions[i] += ball_directions[i] * BALL_SPEED

        pong_wars_view.draw_squares(squares, screen, SQUARE_SIZE, PLAYER_COLORS)

        if paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                overwrite_position[0] -= OVERWRITE_AREA_MOVE_SPEED
            if keys[pygame.K_RIGHT]:
                overwrite_position[0] += OVERWRITE_AREA_MOVE_SPEED
            if keys[pygame.K_UP]:
                overwrite_position[1] -= OVERWRITE_AREA_MOVE_SPEED
            if keys[pygame.K_DOWN]:
                overwrite_position[1] += OVERWRITE_AREA_MOVE_SPEED

            real_overwrite_position, real_overwrite_size = pong_wars_model.calculate_overwrite_area(overwrite_position, overwrite_size, width_pixel, height_pixel)
            pong_wars_view.draw_overwrite_area_cover(screen, real_overwrite_position, real_overwrite_size, PLAYER_COLORS[overwrite_player_index-1], 0.5)

            if enter_pushed:
                if overwrite_cooldown_timers[overwrite_player_index-1] <= 0:
                    pong_wars_model.overwrite_squares(overwrite_player_index, real_overwrite_position, real_overwrite_size, squares, SQUARE_SIZE)
                    overwrite_cooldown_timers[overwrite_player_index-1] = OVERWRITE_COOLDOWN_TIME
                else:
                    pass    #TODO: Let the player now it is in cooldown

        for i in range(player_num):
            pong_wars_view.draw_ball(ball_positions[i], BALL_COLORS[i], screen, SQUARE_SIZE)
        
        # Display scores
        scores = pong_wars_model.calculate_scores(squares)
        scores_texts = [str(scores[i+1]) for i in range(player_num)]    # "scores" is a dictionary, and the key (player index) starts from 1 rather than 0 
        pong_wars_view.draw_centered_text_each_player_panel(screen, scores_texts, font, width_pixel, height_pixel + TEXT_PANEL_HEIGHT, TEXT_PANEL_HEIGHT, PANEL_COLOR, player_num, PLAYER_COLORS)
        # Display overwrite cooldown timer
        cooldown_texts = [("CD: " + f"{overwrite_cooldown_timers[i]:.1f}" if overwrite_cooldown_timers[i] > 0 else "READY") for i in range(player_num)] 
        pong_wars_view.draw_centered_text_each_player_panel(screen, cooldown_texts, font, width_pixel, height_pixel + TEXT_PANEL_HEIGHT * 2, TEXT_PANEL_HEIGHT, PANEL_COLOR, player_num, PLAYER_COLORS)

        # Display tutorial
        pong_wars_view.draw_tutorial_panel(paused, screen, font, width_pixel, height_pixel + TEXT_PANEL_HEIGHT * 3, TUTORIAL_PANEL_HEIGHT, PANEL_COLOR, TEXT_COLOR, player_num)

        if args.record_frames:
            if frame_num%3 == 0:
                pygame.image.save(screen, os.path.join(frame_dir, f"frame_{frame_num}.png"))
            frame_num += 1
      
        pygame.display.flip()
        dt = clock.tick(60)

        if not paused and not gameover:
            game_timer -= dt * 0.001    # dt is millisecond
            overwrite_cooldown_timers = numpy.where(overwrite_cooldown_timers > 0, overwrite_cooldown_timers - dt * 0.001, overwrite_cooldown_timers)

        if game_timer <= 0:
            gameover = True
    
    pygame.quit()
    if args.record_frames:
        pong_wars_view.make_gif(player_num, frame_dir)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--record_frames", action="store_true", help="Record frames for making a movie", default=False)
    args.add_argument("--seed", type=int, help="Seed for random number generator", default=0)
    args.add_argument("--player_num", type=int, help="Number of Players. Currently only '2' and '4' are supported", default=4)
    args = args.parse_args()
    main(args)
