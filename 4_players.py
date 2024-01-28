import pygame
import random
import math
import argparse
import os


# Constants
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = 25
PLAYER1_COLOR = (255, 153, 153)
PLAYER2_COLOR = (255, 255, 153)
PLAYER3_COLOR = (153, 255, 153)
PLAYER4_COLOR = (153, 153, 255)

# Ball colors for each player, contrast is important
  
BALL_COLOR1 = (255, 0, 0)     # Red
BALL_COLOR2 = (255, 255, 0)     # Yellow
BALL_COLOR3 = (0, 255, 0)     # Green
BALL_COLOR4 = (0, 0, 255)     # Blue

DX = 14
DY = 14


def create_squares():
    squares = []
    for i in range(int(WIDTH / SQUARE_SIZE)):
        row = []
        for j in range(int(HEIGHT / SQUARE_SIZE)):
            if i < WIDTH / SQUARE_SIZE / 2:
                color = PLAYER1_COLOR if j < HEIGHT / SQUARE_SIZE / 2 else PLAYER3_COLOR
            else:
                color = PLAYER2_COLOR if j < HEIGHT / SQUARE_SIZE / 2 else PLAYER4_COLOR
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
    clip.write_gif(os.path.join(pics_dir, "4_players.gif"))
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
    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong Wars")

    clock = pygame.time.Clock()
    squares = create_squares()
    x1, y1 = WIDTH / 4, HEIGHT / 4
    x2, y2 = 3 * WIDTH / 4, HEIGHT / 4
    x3, y3 = WIDTH / 4, 3 * HEIGHT / 4
    x4, y4 = 3 * WIDTH / 4, 3 * HEIGHT / 4

    # Initial directions for four players
    dx1, dy1 = DX, DY
    dx2, dy2 = -DX, DY
    dx3, dy3 = DX, -DY
    dx4, dy4 = -DX, -DY

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        dx1, dy1 = update_square_and_bounce(x1, y1, dx1, dy1, PLAYER1_COLOR, squares)
        dx2, dy2 = update_square_and_bounce(x2, y2, dx2, dy2, PLAYER2_COLOR, squares)
        dx3, dy3 = update_square_and_bounce(x3, y3, dx3, dy3, PLAYER3_COLOR, squares)
        dx4, dy4 = update_square_and_bounce(x4, y4, dx4, dy4, PLAYER4_COLOR, squares)

        # Check boundary collisions for players 3 and 4
        dx1, dy1 = check_boundary_collision(x1, y1, dx1, dy1)
        dx2, dy2 = check_boundary_collision(x2, y2, dx2, dy2)
        dx3, dy3 = check_boundary_collision(x3, y3, dx3, dy3)
        dx4, dy4 = check_boundary_collision(x4, y4, dx4, dy4)

        x1 += dx1
        y1 += dy1
        x2 += dx2
        y2 += dy2
        x3 += dx3
        y3 += dy3
        x4 += dx4
        y4 += dy4


        screen.fill((0, 0, 0))
        draw_squares(squares, screen)
        draw_ball(x1, y1, BALL_COLOR1, screen)
        draw_ball(x2, y2, BALL_COLOR2, screen)
        draw_ball(x3, y3, BALL_COLOR3, screen)
        draw_ball(x4, y4, BALL_COLOR4, screen)
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
