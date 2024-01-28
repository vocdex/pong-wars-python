import pygame
import random
import math
import argparse
import os


# Constants
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = 25
DAY_COLOR = (51, 255, 255)
NIGHT_COLOR = (255, 153, 255)
DAY_BALL_COLOR = NIGHT_COLOR
NIGHT_BALL_COLOR = DAY_COLOR
DX = 14
DY = 14

def calculate_scores(squares):
    scores = {DAY_COLOR: 0, NIGHT_COLOR: 0}
    for row in squares:
        for color in row:
            if color in scores:
                scores[color] += 1
    return scores


def draw_score_panel(screen, scores, font):
    panel_height = 40
    panel_color = (50, 50, 50)  # Dark gray background for score panel

    # Draw the background panel at the bottom
    pygame.draw.rect(screen, panel_color, (0, HEIGHT - panel_height, WIDTH, panel_height))

    # Calculate the total width of the score texts for 2 players
    player_colors = [DAY_COLOR, NIGHT_COLOR]
    total_width = 0
    score_surfaces = []
    for color in player_colors:
        score_text = str(scores[color])
        score_surface = font.render(score_text, True, color)
        score_surfaces.append(score_surface)
        total_width += score_surface.get_width() + 30  # Include spacing

    # Start position for the first score text to center the block
    text_x = (WIDTH - total_width) // 2
    text_y = HEIGHT - panel_height + (panel_height - font.get_height()) // 2

    # Draw each score text
    for score_surface in score_surfaces:
        screen.blit(score_surface, (text_x, text_y))
        text_x += score_surface.get_width() + 30  # Adjust spacing between scores



def create_squares():
    squares = []
    for i in range(int(WIDTH / SQUARE_SIZE)):
        row = []
        for j in range(int(HEIGHT / SQUARE_SIZE)):
            color = DAY_COLOR if i < WIDTH / SQUARE_SIZE / 2 else NIGHT_COLOR
            row.append(color)
        squares.append(row)
    return squares

def draw_squares(squares, screen):
    for i in range(len(squares)):
        for j in range(len(squares[i])):
            color = squares[i][j]
            pygame.draw.rect(screen, color, (i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_ball(x, y, color, screen):
    pygame.draw.circle(screen, color, (int(x), int(y)), SQUARE_SIZE // 2)


def update_square_and_bounce(x, y, dx, dy, color, squares):
    updated_dx, updated_dy = dx, dy
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        check_x = x + math.cos(rad) * (SQUARE_SIZE // 2)
        check_y = y + math.sin(rad) * (SQUARE_SIZE // 2)
        i, j = int(check_x // SQUARE_SIZE), int(check_y // SQUARE_SIZE)
        if 0 <= i < len(squares) and 0 <= j < len(squares[i]):
            if squares[i][j] != color:
                squares[i][j] = color
                if abs(math.cos(rad)) > abs(math.sin(rad)):
                    updated_dx = -updated_dx
                else:
                    updated_dy = -updated_dy
                updated_dx += random.uniform(-0.01, 0.01)
                updated_dy += random.uniform(-0.01, 0.01)
    return updated_dx, updated_dy


def check_boundary_collision(x, y, dx, dy):
    if x + dx > WIDTH - SQUARE_SIZE // 2 or x + dx < SQUARE_SIZE // 2:
        dx = -dx
    if y + dy > HEIGHT - SQUARE_SIZE // 2 or y + dy < SQUARE_SIZE // 2:
        dy = -dy
    return dx, dy


def make_gif(frames_dir, delete_frames=True):
    from moviepy.editor import ImageSequenceClip
    from natsort import natsorted
    import glob
    frame_files = natsorted(glob.glob(os.path.join(frames_dir, "*.png")))
    
    clip = ImageSequenceClip(frame_files, fps=60)
    pics_dir = "./pics"
    os.makedirs(pics_dir, exist_ok=True)
    clip.write_gif(os.path.join(pics_dir, "2_players.gif"))
    # delete frames
    if delete_frames:
        # remove frames folder
        import shutil
        shutil.rmtree(frames_dir)
        
            

def main(args):
    if args.seed:
        random.seed(args.seed)
    if args.record_frames:
        frame_dir = "frames"
        os.makedirs(frame_dir, exist_ok=True)
        frame_num = 0
    pygame.init()
    pygame.font.init()  # Initialize the font module

    font = pygame.font.SysFont('Consolas', 18)  # Or any other preferred font
    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong Wars")

    clock = pygame.time.Clock()
    squares = create_squares()
    x1, y1 = WIDTH / 4, HEIGHT / 2
    dx1, dy1 = DX, DY
    x2, y2 = WIDTH * 3 / 4, HEIGHT / 2
    dx2, dy2 = -DX, -DY

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        dx1, dy1 = update_square_and_bounce(x1, y1, dx1, dy1, DAY_COLOR, squares)
        dx2, dy2 = update_square_and_bounce(x2, y2, dx2, dy2, NIGHT_COLOR, squares)

        dx1, dy1 = check_boundary_collision(x1, y1, dx1, dy1)
        dx2, dy2 = check_boundary_collision(x2, y2, dx2, dy2)

        x1 += dx1
        y1 += dy1
        x2 += dx2
        y2 += dy2

        screen.fill((0, 0, 0))
        draw_squares(squares, screen)
        draw_ball(x1, y1, DAY_BALL_COLOR, screen)
        draw_ball(x2, y2, NIGHT_BALL_COLOR, screen)

        # Display scores
        scores = calculate_scores(squares)
        draw_score_panel(screen, scores, font)
        if args.record_frames:
            if frame_num%3 == 0:
                pygame.image.save(screen, os.path.join(frame_dir, f"frame_{frame_num}.png"))
            frame_num += 1
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    if args.record_frames:
        make_gif(frame_dir)

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--record_frames", action="store_true", help="Record frames for making a movie", default=False)
    args.add_argument("--seed", type=int, help="Seed for random number generator", default=0)
    args = args.parse_args()
    main(args)
