# 安装必要的库
import pygame
import numpy as np

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


class Player:
    def __init__(self, position, color):
        self.position = position
        self.color = color


# 定义黑色球员和红色球员的位置
black_players = [
    Player((3, 5), BLUE),
    Player((1, 8), BLUE),
    Player((1, 2), BLUE)
]

red_players = [
    Player((2, 5), RED),
    Player((4, 2), RED),
    Player((4, 8), RED)
]

# 合并球员列表
players = black_players + red_players


class Ball:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction


# 定义球的位置和方向
ball = Ball((3.5, 5), (1, 1))  # 球的位置在 (3, 5)，方向为向右


# 绘制棋盘
def draw_board():
    for row in range(BOARD_SIZE_Y):
        for col in range(BOARD_SIZE_X):
            color = GREEN_ONE if (row + col) % 2 == 0 else GREEN_TWO
            pygame.draw.rect(screen, color, pygame.Rect(col * TILE_SIZE_X, row * TILE_SIZE_Y, TILE_SIZE_X, TILE_SIZE_Y))


# 绘制球员
def draw_players():
    for player in players:
        col, row = player.position
        pygame.draw.circle(screen, player.color,
                           (col * TILE_SIZE_X, row * TILE_SIZE_Y),
                           TILE_SIZE_Y // 4)


# 绘制球和箭头
def draw_ball_and_arrow():
    col, row = ball.position
    pygame.draw.circle(screen, WHITE,
                       (col * TILE_SIZE_X, row * TILE_SIZE_Y),
                       TILE_SIZE_Y // 4)

    # 绘制箭头
    arrow_start = (col * TILE_SIZE_X, row * TILE_SIZE_Y)
    arrow_end = (arrow_start[0] + ball.direction[0] * TILE_SIZE_Y / 2,
                 arrow_start[1] + ball.direction[1] * TILE_SIZE_Y / 2)
    pygame.draw.line(screen, WHITE, arrow_start, arrow_end, 5)
    pygame.draw.polygon(screen, WHITE, [
        (arrow_end[0] + ball.direction[0] * 10, arrow_end[1] + ball.direction[1] * 10),
        (arrow_end[0] - ball.direction[1] * 10, arrow_end[1] + ball.direction[0] * 10),
        (arrow_end[0] + ball.direction[1] * 10, arrow_end[1] - ball.direction[0] * 10)
    ])


# 主游戏循环
def handle_click(param):
    pass


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
