from random import randint
from typing import Tuple

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

DIRECTIONS = {
    pygame.K_w: UP,
    pygame.K_s: DOWN,
    pygame.K_a: LEFT,
    pygame.K_d: RIGHT
}

OPPOSITE_DIRECTIONS = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT
}


class GameObject:
    """
    Базовый класс игрового объекта.
    Содержит в себе позицию и цвет объекта.
    """

    position: Tuple[int, int]
    body_color: Tuple[int, int, int]

    def __init__(self):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = BORDER_COLOR

    def draw(self):
        """Заглушка метода отрисовки"""
        pass

    def draw_cell(self, position):
        """Метод отрисовывает клетку в position"""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс яблока"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Задает новое случайное положение яблоку"""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Отрисовывает яблоко"""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс Змеи"""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [(GRID_WIDTH // 2 * GRID_SIZE,
                           GRID_HEIGHT // 2 * GRID_SIZE)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Обновляет направление движения змеи"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет положение змеи"""
        current_head = self.get_head_position()
        self.positions = self.positions[1:]

        x, y = self.direction
        new_head = ((current_head[0] + x * GRID_SIZE) % SCREEN_WIDTH,
                    (current_head[1] + y * GRID_SIZE) % SCREEN_HEIGHT)
        if new_head in self.positions[:-1]:
            raise SystemExit("Game Over!")

        self.positions.append(new_head)

    def reset(self):
        """Откатить змею в начальное положение"""
        current_head = self.get_head_position()
        self.__init__()
        self.positions = [current_head]

    def grow(self):
        """Увеличивает длину змеи на 1"""
        tail = self.positions[0]
        self.move()
        self.positions = [tail] + self.positions

    def draw(self):
        """Отрисовывает змею"""
        for position in self.positions:
            self.draw_cell(position)

    def eats_apple(self, apple: Apple) -> bool:
        """Проверяет, что змея съедает яблоко"""
        return self.positions[-1] == apple.position

    def collides_apple(self, apple: Apple) -> bool:
        """Проверяет, что яблоко пересекается со змеей"""
        return apple.position in self.positions

    def get_head_position(self):
        """Возвращает позицию головы змеи"""
        return self.positions[-1]


def direction_must_be_updated(event, snake):
    """Проверяет, что направление должно быть обновлено"""
    return (event.key in DIRECTIONS
            and snake.direction != OPPOSITE_DIRECTIONS[DIRECTIONS[event.key]])


def handle_keys(snake: Snake):
    """Обрабатывает нажатия клавиш"""
    global SPEED

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            if event.key == pygame.K_q:
                SPEED = min(102, SPEED + 3)
            if event.key == pygame.K_e:
                SPEED = max(3, SPEED - 3)

            if direction_must_be_updated(event, snake):
                snake.next_direction = DIRECTIONS[event.key]


def generate_new_apple_position(snake: Snake, apple: Apple):
    """Генерирует новое положение яблока"""
    while snake.collides_apple(apple):
        apple.randomize_position()


def main():
    """Основная функция"""
    pygame.init()

    snake = Snake()
    apple = Apple()
    generate_new_apple_position(snake, apple)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()

        try:
            snake.move()
        except SystemExit:
            snake.reset()
            generate_new_apple_position(snake, apple)

        if snake.eats_apple(apple):
            snake.grow()
            generate_new_apple_position(snake, apple)

        screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw()
        apple.draw()

        pygame.display.set_caption(f"Змейка. Размер: {len(snake.positions)}."
                                   f" Скорость змейки: {SPEED}")
        pygame.display.update()


if __name__ == '__main__':
    main()
