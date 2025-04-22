
import pygame
import random
import sys

WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)

def draw_grid(surface):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(surface, DARK_GREEN, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, DARK_GREEN, (0, y), (WIDTH, y))

def random_fruit(snake):
    while True:
        pos = [random.randint(0, COLS-1), random.randint(0, ROWS-1)]
        if pos not in snake:
            return pos

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('贪吃蛇 Snake')
    clock = pygame.time.Clock()
    snake = [[COLS//2, ROWS//2]]
    direction = (0, -1)
    fruit = random_fruit(snake)
    score = 0
    running = True

    while running:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w] and direction != (0, 1):
                    direction = (0, -1)
                elif event.key in [pygame.K_DOWN, pygame.K_s] and direction != (0, -1):
                    direction = (0, 1)
                elif event.key in [pygame.K_LEFT, pygame.K_a] and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key in [pygame.K_RIGHT, pygame.K_d] and direction != (-1, 0):
                    direction = (1, 0)
                elif event.key == pygame.K_ESCAPE:
                    running = False

        new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
        if (
            new_head[0] < 0 or new_head[0] >= COLS
            or new_head[1] < 0 or new_head[1] >= ROWS
            or new_head in snake
        ):
            break

        snake.insert(0, new_head)
        if new_head == fruit:
            score += 1
            fruit = random_fruit(snake)
        else:
            snake.pop()

        screen.fill(BLACK)
        draw_grid(screen)
        pygame.draw.rect(
            screen, RED,
            (fruit[0]*CELL_SIZE, fruit[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )
        for s in snake:
            pygame.draw.rect(
                screen, GREEN,
                (s[0]*CELL_SIZE, s[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )

        font = pygame.font.SysFont(None, 30)
        score_surface = font.render(f'分数: {score}', True, WHITE)
        screen.blit(score_surface, (10, 10))

        pygame.display.flip()

    font = pygame.font.SysFont(None, 60)
    text = font.render('游戏结束!', True, RED)
    screen.blit(text, (WIDTH//2-120, HEIGHT//2-30))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
