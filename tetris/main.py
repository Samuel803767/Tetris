import pygame
import random

# Inicializando o pygame
pygame.init()

# Definindo cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)

# Tamanho da tela
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Configurações do jogo
BLOCK_SIZE = 30
COLUMN_COUNT = 10
ROW_COUNT = 20

# Formatos das peças (tetrominos)
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[0, 1, 0], [1, 1, 1]]   # T
]

SHAPE_COLORS = [CYAN, YELLOW, GREEN, RED, BLUE, ORANGE, MAGENTA]

# Classe para as peças
class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = COLUMN_COUNT // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

# Função para desenhar a grade
def draw_grid():
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        pygame.draw.line(SCREEN, WHITE, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(SCREEN, WHITE, (0, y), (SCREEN_WIDTH, y))

# Função para desenhar as peças
def draw_tetromino(tetromino):
    for i, row in enumerate(tetromino.shape):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(SCREEN, tetromino.color, (tetromino.x * BLOCK_SIZE + j * BLOCK_SIZE, tetromino.y * BLOCK_SIZE + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Função para verificar colisão
def check_collision(board, tetromino):
    for i, row in enumerate(tetromino.shape):
        for j, cell in enumerate(row):
            if cell:
                x = tetromino.x + j
                y = tetromino.y + i
                if x < 0 or x >= COLUMN_COUNT or y >= ROW_COUNT or board[y][x]:
                    return True
    return False

# Função para adicionar o tetromino à grade
def add_tetromino_to_board(board, tetromino):
    for i, row in enumerate(tetromino.shape):
        for j, cell in enumerate(row):
            if cell:
                board[tetromino.y + i][tetromino.x + j] = tetromino.color

# Função para remover linhas completas e aumentar a pontuação
def remove_lines(board):
    global SCORE
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_removed = ROW_COUNT - len(new_board)
    if lines_removed > 0:
        new_board = [[0] * COLUMN_COUNT for _ in range(lines_removed)] + new_board
        SCORE += lines_removed * 100
    return new_board

# Função para desenhar a pontuação na tela
def draw_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {SCORE}", True, WHITE)
    SCREEN.blit(score_text, (10, 10))

# Função do menu inicial
def menu():
    clock = pygame.time.Clock()
    while True:
        SCREEN.fill(BLACK)
        title_font = pygame.font.Font(None, 74)
        button_font = pygame.font.Font(None, 50)

        # Título
        title_text = title_font.render("TETRIS", True, CYAN)
        SCREEN.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        # Botão
        play_text = button_font.render("Jogar", True, BLACK)
        play_button = pygame.Rect(SCREEN_WIDTH // 2 - 75, 250, 150, 50)
        pygame.draw.rect(SCREEN, WHITE, play_button)
        SCREEN.blit(play_text, (SCREEN_WIDTH // 2 - play_text.get_width() // 2, 260))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and play_button.collidepoint(event.pos):
                return

        clock.tick(30)

# Função de Game Over
def game_over_screen():
    clock = pygame.time.Clock()
    while True:
        SCREEN.fill(BLACK)
        game_over_font = pygame.font.Font(None, 74)
        score_font = pygame.font.Font(None, 50)
        button_font = pygame.font.Font(None, 40)

        game_over_text = game_over_font.render("Game Over", True, RED)
        score_text = score_font.render(f"Pontuação: {SCORE}", True, WHITE)
        restart_text = button_font.render("Reiniciar", True, BLACK)

        restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 75, 300, 150, 50)
        pygame.draw.rect(SCREEN, WHITE, restart_button)
        SCREEN.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 100))
        SCREEN.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 200))
        SCREEN.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 310))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and restart_button.collidepoint(event.pos):
                return  # Volta para o menu

        clock.tick(30)

# Função principal
def main():
    global GAME_OVER, SCORE
    GAME_OVER = False
    SCORE = 0
    board = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]
    clock = pygame.time.Clock()
    current_tetromino = Tetromino(random.choice(SHAPES), random.choice(SHAPE_COLORS))
    fall_speed = 500
    last_fall_time = pygame.time.get_ticks()

    while True:
        SCREEN.fill(BLACK)
        draw_grid()

        if not GAME_OVER:
            if pygame.time.get_ticks() - last_fall_time >= fall_speed:
                current_tetromino.y += 1
                if check_collision(board, current_tetromino):
                    current_tetromino.y -= 1
                    add_tetromino_to_board(board, current_tetromino)
                    board = remove_lines(board)
                    current_tetromino = Tetromino(random.choice(SHAPES), random.choice(SHAPE_COLORS))
                last_fall_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN and not GAME_OVER:
                if event.key == pygame.K_LEFT:
                    current_tetromino.x -= 1
                    if check_collision(board, current_tetromino):
                        current_tetromino.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_tetromino.x += 1
                    if check_collision(board, current_tetromino):
                        current_tetromino.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_tetromino.y += 1
                    if check_collision(board, current_tetromino):
                        current_tetromino.y -= 1
                elif event.key == pygame.K_UP:
                    current_tetromino.rotate()
                    if check_collision(board, current_tetromino):
                        current_tetromino.rotate()
                        current_tetromino.rotate()
                        current_tetromino.rotate()

        for y in range(ROW_COUNT):
            for x in range(COLUMN_COUNT):
                if board[y][x]:
                    pygame.draw.rect(SCREEN, board[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        draw_tetromino(current_tetromino)
        draw_score()

        if current_tetromino.y == 0 and check_collision(board, current_tetromino):
            GAME_OVER = True
            game_over_screen()
            return

        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    while True:
        menu()
        main()
