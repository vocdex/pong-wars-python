"""
View part for pong wars.
"""

import pygame
import os


def draw_centered_text_panel(screen, text, font, width, height, panel_height, panel_color, text_color):
    # Draw the background panel at the bottom
    pygame.draw.rect(screen, panel_color, (0, height, width, panel_height))

    surface = font.render(text, True, text_color)
    text_x = (width - surface.get_width()) // 2
    text_y = height + (panel_height - font.get_height()) // 2
    screen.blit(surface, (text_x, text_y))
    text_x += surface.get_width()


def draw_centered_text_each_player_panel(screen, texts, font, width, height, panel_height, panel_color, player_num, player_colors):
    # Draw the background panel at the bottom
    pygame.draw.rect(screen, panel_color, (0, height, width, panel_height))

    # Calculate the total width of the score texts
    total_width = 0
    surfaces = []
    for i in range(player_num):
        text = texts[i]
        surface = font.render(text, True, player_colors[i])
        surfaces.append(surface)
        total_width += surface.get_width() + 30  # Include spacing
    total_width -= 30

    # Start position for the first score text to center the block
    text_x = (width - total_width) // 2
    text_y = height + (panel_height - font.get_height()) // 2

    # Draw each score text
    for surface in surfaces:
        screen.blit(surface, (text_x, text_y))
        text_x += surface.get_width() + 30  # Adjust spacing between scores


def draw_tutorial_panel(isPaused, screen, font, width, height, panel_height, panel_color, text_color, player_num):
    tutorial_texts = [
        "P: Continue",
        ("1,2,3,4" if player_num == 4 else "1,2") + ": Change player", 
        "Arrow Keys: Move overwrite area", 
        "Enter: Overwrite"
    ] if isPaused else [
        "P: Pause"
    ]

    # Draw the background panel at the bottom
    pygame.draw.rect(screen, panel_color, (0, height, width, panel_height))

    text_y = height
    for tutorial_text in tutorial_texts:
        tutorial_surface = font.render(tutorial_text, True, text_color)
        
        # Draw each score text
        screen.blit(tutorial_surface, (30, text_y))

        line_spacing = 5
        text_y += font.get_height() + line_spacing

    


def draw_overwrite_area_cover(screen, top_left_position, size, color, transparency):
    rect_surface = pygame.Surface(size, pygame.SRCALPHA)
    rect_surface.fill((color[0], color[1], color[2], int(255 * transparency)))
    screen.blit(rect_surface, top_left_position)


def draw_squares(squares, screen, square_size, player_colors):
    for i in range(squares.shape[0]):
        for j in range(squares.shape[1]):
            color = player_colors[int(squares[i][j]) - 1]   # The player index in "squares" starts from "1" rather than "0" 
            pygame.draw.rect(screen, color, (i * square_size, j * square_size, square_size, square_size))


def draw_ball(position, color, screen, square_size):
    pygame.draw.circle(screen, color, (int(position[0]), int(position[1])), square_size // 2)


def make_gif(player_num, frames_dir, delete_frames=True):
    from moviepy.editor import ImageSequenceClip
    from natsort import natsorted
    import glob
    frame_files = natsorted(glob.glob(os.path.join(frames_dir, "*.png")))
    
    clip = ImageSequenceClip(frame_files, fps=60)
    pics_dir = "./pics"
    clip.write_gif(os.path.join(pics_dir, str(player_num) + "_players.gif"))
    # delete frames
    if delete_frames:
        # remove frames folder
        import shutil
        shutil.rmtree(frames_dir)