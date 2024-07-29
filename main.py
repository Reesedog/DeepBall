import pygame
import numpy as np
import sympy as sp

pygame.init()

BOARD_SIZE_X = 5
BOARD_SIZE_Y = 10
TILE_SIZE_X = 200
TILE_SIZE_Y = 60

WIDTH, HEIGHT = BOARD_SIZE_X * TILE_SIZE_X, BOARD_SIZE_Y * TILE_SIZE_Y
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DeepBalls")

# Colors
GREEN_ONE = (8, 102, 38)
GREEN_TWO = (0, 255, 82)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

board = np.zeros((BOARD_SIZE_X, BOARD_SIZE_Y), dtype=int)

running = True

# Arrow configurations
arrow_offsets = {
    'blue': [(1.7, 0), (1, 1), (1, -1)],
    'red': [(-1.7, 0), (-1, 1), (-1, -1)]
}

arrows = []


class Player:
    def __init__(self, x, y, color):
        self.position = (x * TILE_SIZE_X, y * TILE_SIZE_Y)
        self.color = color


# 定义黑色球员和红色球员的位置
black_players = [
    Player(3, 5, BLUE),
    Player(1, 8, BLUE),
    Player(1, 2, BLUE)
]

red_players = [
    Player(2, 5, RED),
    Player(4, 2, RED),
    Player(4, 8, RED)
]

# 合并球员列表
players = black_players + red_players


class Ball:
    def __init__(self, x, y, direction):
        self.position = (x * TILE_SIZE_X, y * TILE_SIZE_Y)
        self.direction = direction


# 定义球的位置和方向
ball = Ball(3, 5, (1, 1))  # 球的位置在 (3, 5)，方向为向右


# 绘制棋盘
def draw_board():
    for row in range(BOARD_SIZE_Y):
        for col in range(BOARD_SIZE_X):
            color = BLACK
            pygame.draw.rect(screen, color,
                             pygame.Rect(col * TILE_SIZE_X, row * TILE_SIZE_Y, TILE_SIZE_X - 2, TILE_SIZE_Y - 2))


# 绘制球员
def draw_players():
    for player in players:
        col, row = player.position
        pygame.draw.circle(screen, player.color,
                           (col, row),
                           TILE_SIZE_Y // 4)


# 绘制球和箭头
def draw_ball_and_arrow():
    col, row = ball.position
    pygame.draw.circle(screen, WHITE,
                       (int(col), int(row)),
                       TILE_SIZE_Y // 4)

    # 绘制箭头
    arrow_start = (int(col), int(row))
    arrow_end = (int(arrow_start[0] + ball.direction[0] * 20),
                 int(arrow_start[1] + ball.direction[1] * 20))
    pygame.draw.line(screen, WHITE, arrow_start, arrow_end, 5)
    pygame.draw.polygon(screen, WHITE, [
        (int(arrow_end[0] + ball.direction[0] * 10), int(arrow_end[1] + ball.direction[1] * 10)),
        (int(arrow_end[0] - ball.direction[1] * 10), int(arrow_end[1] + ball.direction[0] * 10)),
        (int(arrow_end[0] + ball.direction[1] * 10), int(arrow_end[1] - ball.direction[0] * 10))
    ])

    for arrow in arrows:
        draw_arrow(arrow['start'], arrow['end'], arrow['color'])


def draw_arrow(start, end, color):
    pygame.draw.polygon(screen, color, [
        (int(end[0] + (end[0] - start[0]) * 0.2), int(end[1] + (end[1] - start[1]) * 0.2)),
        (int(end[0] - (end[1] - start[1]) * 0.2), int(end[1] + (end[0] - start[0]) * 0.2)),
        (int(end[0] + (end[1] - start[1]) * 0.2), int(end[1] - (end[0] - start[0]) * 0.2))
    ])


def show_arrows(player):
    global arrows
    x, y = player.position
    color = 'blue' if player.color == BLUE else 'red'
    arrows = []
    for offset in arrow_offsets[color]:
        end_x = x + offset[0] * 20
        end_y = y + offset[1] * 20
        arrows.append({
            'start': (x, y),
            'end': (end_x, end_y),
            'color': player.color,
            'direction': offset
        })


# 处理球的运动逻辑
def move_ball():
    global arrows
    x, y = sp.symbols('x y')
    col, row = ball.position
    direction = ball.direction

    # 定义球的运动方程
    line_eq = sp.Eq((y - row) / direction[1], (x - col) / direction[0])

    # 寻找最近的交点
    intersection_points = []
    for i in range(BOARD_SIZE_X + 1):
        x_val = i * TILE_SIZE_X
        if ball.direction[0] * (x_val - col) > 0:
            y_val = sp.solve(line_eq.subs(x, x_val), y)[0]
            if 0 <= y_val <= HEIGHT:
                intersection_points.append((x_val, y_val))

    for j in {0, 10}:
        if direction[1] != 0:
            y_val = j * TILE_SIZE_Y
            if ball.direction[1] * (y_val - row) > 0:
                x_val = sp.solve(line_eq.subs(y, y_val), x)[0]
                if (0 <= x_val <= WIDTH) & (x_val != col):
                    intersection_points.append((x_val, y_val))

    # 找到最近的交点
    next_position = min(intersection_points, key=lambda p: ((p[0] - col) ** 2 + (p[1] - row) ** 2) ** 0.5)

    # 检查碰撞边框
    if next_position[0] == 0 or next_position[0] == WIDTH:
        direction = (-direction[0], direction[1])
    if next_position[1] == 0 or next_position[1] == HEIGHT:
        direction = (direction[0], -direction[1])

    ball.position = next_position
    ball.direction = direction

    for p in players:
        if ((p.position[0] - ball.position[0]) ** 2 + (p.position[1] - ball.position[1]) ** 2) ** 0.5 < 40:
            print("shoot!!!!!")
            show_arrows(p)
            break


# 处理鼠标点击事件
def handle_click(pos):
    global ball
    x, y = pos

    arrows.clear()

    move_ball()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(pygame.mouse.get_pos())

    screen.fill(GREEN_ONE)
    draw_board()
    draw_players()
    draw_ball_and_arrow()
    pygame.display.flip()

pygame.quit()
