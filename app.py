import pygame
import random

# Inicialização do Pygame
pygame.init()

# Configurações do jogo
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
MINE_COUNT = 10
CELL_SIZE = WIDTH // COLS

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (169, 169, 169)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BUTTON_COLOR = (100, 100, 255)
CONFETTI_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Configuração da tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Campo Minado")
font = pygame.font.Font(None, 74)  # Fonte maior para "You Win!" e "Game Over!"
button_font = pygame.font.Font(None, 50)  # Fonte para o botão

# Função para criar o tabuleiro
def create_board(rows, cols, mine_count):
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    mines = set()
    while len(mines) < mine_count:
        r, c = random.randint(0, rows - 1), random.randint(0, cols - 1)
        if (r, c) not in mines:
            mines.add((r, c))
            board[r][c] = -1
    for r, c in mines:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != -1:
                    board[nr][nc] += 1
    return board

# Função para desenhar o tabuleiro
def draw_board(board, revealed, flagged):
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, DARK_GRAY if revealed[r][c] else GRAY, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            if revealed[r][c]:
                if board[r][c] == -1:
                    pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 4)
                elif board[r][c] > 0:
                    text = font.render(str(board[r][c]), True, BLUE)
                    screen.blit(text, text.get_rect(center=rect.center))
            elif flagged[r][c]:
                pygame.draw.circle(screen, GREEN, rect.center, CELL_SIZE // 4)

# Função para revelar células
def reveal(board, revealed, r, c):
    if revealed[r][c]:
        return
    revealed[r][c] = True
    if board[r][c] == 0:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    reveal(board, revealed, nr, nc)

# Função para verificar vitória
def check_victory(board, revealed, flagged):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != -1 and not revealed[r][c] and not flagged[r][c]:
                return False
    return True

# Função para desenhar confetes
def draw_confetti(screen):
    for _ in range(100):  # Desenha 100 confetes
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        color = random.choice(CONFETTI_COLORS)
        pygame.draw.circle(screen, color, (x, y), 5)

# Função principal
def main():
    running = True
    board = create_board(ROWS, COLS, MINE_COUNT)
    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]
    game_over = False
    victory = False

    clock = pygame.time.Clock()
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return  # Sai da função main() imediatamente após encerrar o Pygame

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if game_over or victory:
                    # Verifica se o botão de reiniciar foi clicado
                    if WIDTH // 2 - 100 <= x <= WIDTH // 2 + 100 and HEIGHT // 2 + 50 <= y <= HEIGHT // 2 + 150:
                        # Reinicia o jogo
                        board = create_board(ROWS, COLS, MINE_COUNT)
                        revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
                        flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]
                        game_over = False
                        victory = False
                elif not game_over and not victory:
                    c, r = x // CELL_SIZE, y // CELL_SIZE
                    if event.button == 1:  # Botão esquerdo do mouse
                        if not flagged[r][c]:
                            if board[r][c] == -1:
                                game_over = True
                            reveal(board, revealed, r, c)
                    elif event.button == 3:  # Botão direito do mouse
                        flagged[r][c] = not flagged[r][c]

                    victory = check_victory(board, revealed, flagged)

        draw_board(board, revealed, flagged)

        if game_over:
            # Cria uma superfície semi-transparente para escurecer o fundo
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # Preto com 50% de transparência
            screen.blit(overlay, (0, 0))

            # Exibe a mensagem "Game Over!" em tamanho grande
            text = font.render("Game Over!", True, RED)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 50))

            # Desenha o botão de reiniciar
            button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 100)
            pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
            button_text = button_font.render("Restart", True, WHITE)
            screen.blit(button_text, (WIDTH // 2 - button_text.get_width() // 2, HEIGHT // 2 + 100 - button_text.get_height() // 2))
        elif victory:
            # Exibe a mensagem "You Win!" em tamanho grande
            text = font.render("You Win!", True, GREEN)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 50))

            # Desenha confetes
            draw_confetti(screen)

            # Desenha o botão de reiniciar
            button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 100)
            pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
            button_text = button_font.render("Restart", True, WHITE)
            screen.blit(button_text, (WIDTH // 2 - button_text.get_width() // 2, HEIGHT // 2 + 100 - button_text.get_height() // 2))

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()