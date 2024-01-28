import pygame
import random
import math


# Constants
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = 25
DAY_COLOR = (51, 255, 255)
NIGHT_COLOR = (255, 153, 255)
DAY_BALL_COLOR = NIGHT_COLOR
NIGHT_BALL_COLOR = DAY_COLOR
DX = 14
DY = 14


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


def main():
    pygame.init()
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

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
