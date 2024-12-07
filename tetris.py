import pygame
import random

# 初始化 Pygame
pygame.init()

# 设置游戏窗口
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

# 计算游戏区域的位置
PLAY_WIDTH = BLOCK_SIZE * GRID_WIDTH
PLAY_HEIGHT = BLOCK_SIZE * GRID_HEIGHT
TOP_LEFT_X = (WINDOW_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = (WINDOW_HEIGHT - PLAY_HEIGHT) // 2

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),  # 青色 - I
    (255, 255, 0),  # 黄色 - O
    (128, 0, 128),  # 紫色 - T
    (0, 255, 0),    # 绿色 - S
    (255, 0, 0),    # 红色 - Z
    (0, 0, 255),    # 蓝色 - J
    (255, 165, 0)   # 橙色 - L
]

# 定义方块形状
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], 
     [1, 1]],        # O
    [[0, 1, 0],
     [1, 1, 1]],     # T
    [[0, 1, 1],
     [1, 1, 0]],     # S
    [[1, 1, 0],
     [0, 1, 1]],     # Z
    [[1, 0, 0],
     [1, 1, 1]],     # J
    [[0, 0, 1],
     [1, 1, 1]]      # L
]

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = COLORS[SHAPES.index(shape)]
        self.rotation = 0

    def rotate(self):
        # 将形状转换为列表，因为元组不可修改
        self.shape = list(zip(*reversed(self.shape)))

def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            if (j, i) in locked_positions:
                grid[i][j] = locked_positions[(j, i)]
    return grid

def convert_shape_format(piece):
    positions = []
    shape_format = piece.shape

    for i, row in enumerate(shape_format):
        for j, value in enumerate(row):
            if value == 1:
                positions.append((piece.x + j, piece.y + i))

    return positions

def valid_space(piece, grid):
    accepted_pos = [[(j, i) for j in range(GRID_WIDTH) if grid[i][j] == BLACK] for i in range(GRID_HEIGHT)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(piece)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    return Piece(5, 0, random.choice(SHAPES))

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont('comicsans', size)
    label = font.render(text, 1, color)
    
    surface.blit(label, (
        TOP_LEFT_X + PLAY_WIDTH/2 - (label.get_width()/2),
        TOP_LEFT_Y + PLAY_HEIGHT/2 - label.get_height()/2
    ))

def draw_grid(surface, grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                           (TOP_LEFT_X + j*BLOCK_SIZE,
                            TOP_LEFT_Y + i*BLOCK_SIZE,
                            BLOCK_SIZE, BLOCK_SIZE), 0)

    # 画网格线
    for i in range(GRID_HEIGHT):
        pygame.draw.line(surface, GRAY,
                        (TOP_LEFT_X, TOP_LEFT_Y + i*BLOCK_SIZE),
                        (TOP_LEFT_X + PLAY_WIDTH, TOP_LEFT_Y + i*BLOCK_SIZE))
    for j in range(GRID_WIDTH):
        pygame.draw.line(surface, GRAY,
                        (TOP_LEFT_X + j*BLOCK_SIZE, TOP_LEFT_Y),
                        (TOP_LEFT_X + j*BLOCK_SIZE, TOP_LEFT_Y + PLAY_HEIGHT))

def clear_lines(grid, locked):
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc

def draw_window(surface, grid, score=0):
    surface.fill(BLACK)

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, WHITE)

    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH/2 - (label.get_width()/2), 30))

    # 显示当前分数
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render(f'Score: {score}', 1, WHITE)
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH + 50, TOP_LEFT_Y + 150))

    draw_grid(surface, grid)
    pygame.draw.rect(surface, WHITE, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape:', 1, WHITE)
    
    sx = TOP_LEFT_X + PLAY_WIDTH + 50
    sy = TOP_LEFT_Y + 50
    format = shape.shape
    for i, row in enumerate(format):
        for j, column in enumerate(row):
            if column == 1:
                pygame.draw.rect(surface, shape.color,
                               (sx + j*BLOCK_SIZE,
                                sy + i*BLOCK_SIZE,
                                BLOCK_SIZE, BLOCK_SIZE), 0)

def main():
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not valid_space(current_piece, grid):
                        current_piece.rotate()
                        current_piece.rotate()
                        current_piece.rotate()
                if event.key == pygame.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    change_piece = True

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            lines = clear_lines(grid, locked_positions)
            if lines == 1:
                score += 100
            elif lines == 2:
                score += 300
            elif lines == 3:
                score += 500
            elif lines == 4:
                score += 800

        draw_window(screen, grid, score)
        draw_next_shape(next_piece, screen)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(screen, "Game Over!", 80, WHITE)
            pygame.display.update()
            pygame.time.delay(1500)
            run = False

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('俄罗斯方块')

main()
pygame.quit()
