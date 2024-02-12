"""
View part for pong wars.
"""

import pygame
import os


def draw_score_panel(screen, scores, font, width, height, player_num, player_colors):
    panel_height = 40
    panel_color = (50, 50, 50)  # Dark gray background for score panel

    # Draw the background panel at the bottom
    pygame.draw.rect(screen, panel_color, (0, height - panel_height, width, panel_height))

    # Calculate the total width of the score texts
    total_width = 0
    score_surfaces = []
    for i in range(player_num):
        score_text = str(scores[i+1])   # "scores" is a dictionary, and the key (player index) starts from 1 rather than 0 
        score_surface = font.render(score_text, True, player_colors[i])
        score_surfaces.append(score_surface)
        total_width += score_surface.get_width() + 30  # Include spacing

    # Start position for the first score text to center the block
    text_x = (width - total_width) // 2
    text_y = height - panel_height + (panel_height - font.get_height()) // 2

    # Draw each score text
    for score_surface in score_surfaces:
        screen.blit(score_surface, (text_x, text_y))
        text_x += score_surface.get_width() + 30  # Adjust spacing between scores


def draw_squares(squares, screen, square_size, player_colors):
    for i in range(squares.shape[0]):
        for j in range(squares.shape[1]):
            color = player_colors[int(squares[i][j]) - 1]   # The player index in "squares" starts from "1" rather than "0" 
            pygame.draw.rect(screen, color, (i * square_size, j * square_size, square_size, square_size))


def draw_ball(position, color, screen, square_size):
    pygame.draw.circle(screen, color, (int(position[0]), int(position[1])), square_size // 2)


def make_gif(frames_dir, delete_frames=True):
    from moviepy.editor import ImageSequenceClip
    from natsort import natsorted
    import glob
    frame_files = natsorted(glob.glob(os.path.join(frames_dir, "*.png")))
    
    clip = ImageSequenceClip(frame_files, fps=60)
    pics_dir = "./pics"
    clip.write_gif(os.path.join(pics_dir, "4_players.gif"))
    # delete frames
    if delete_frames:
        # remove frames folder
        import shutil
        shutil.rmtree(frames_dir)