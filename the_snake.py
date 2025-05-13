from random import choice, randint
import pygame as pg

# Размеры поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость змейки
SPEED = 20

# Настройка окна
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для объектов игры."""

    def __init__(self, position=None):
        if position is None:
            position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.position = position
        self.body_color = None

    def draw(self, surface):
        """Абстрактный метод отрисовки."""
        raise NotImplementedError("Draw method must be implemented")


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, snake_positions=None):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_pos=None):
        """Ставит яблоко в случайную позицию."""
        if snake_pos is None:
            snake_pos = []
        valid_pos = []
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                pos = (x * GRID_SIZE, y * GRID_SIZE)
                if pos not in snake_pos:
                    valid_pos.append(pos)
        if valid_pos:
            self.position = choice(valid_pos)
        else:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )

    def draw(self, surface):
        """Отрисовывает яблоко."""
        pos = self.position
        rect = pg.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE)
        pg.draw.rect(surface, self.body_color, rect)
        pg.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_dir = None
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление."""
        if self.next_dir:
            opposite = (self.next_dir[0] * -1, self.next_dir[1] * -1)
            if opposite != self.direction:
                self.direction = self.next_dir
            self.next_dir = None

    def move(self):
        """Перемещает змейку."""
        x, y = self.get_head_position()
        dx, dy = self.direction
        new_x = (x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        if new_head in self.positions[1:]:
            self.positions = [self.get_head_position()]
            self.length = 1
            self.last = None
        else:
            self.last = None
            if len(self.positions) >= self.length:
                self.last = self.positions[-1]
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        """Сбрасывает змейку."""
        self.__init__()

    def draw(self, surface):
        """Отрисовывает змейку."""
        for p in self.positions:
            rect = pg.Rect(p[0], p[1], GRID_SIZE, GRID_SIZE)
            pg.draw.rect(surface, self.body_color, rect)
            pg.draw.rect(surface, BORDER_COLOR, rect, 1)
        if self.last:
            rect = pg.Rect(self.last[0], self.last[1], GRID_SIZE, GRID_SIZE)
            pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect)


def handle_keys(obj):
    """Обрабатывает действия пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and obj.direction != DOWN:
                obj.next_dir = UP
            elif event.key == pg.K_DOWN and obj.direction != UP:
                obj.next_dir = DOWN
            elif event.key == pg.K_LEFT and obj.direction != RIGHT:
                obj.next_dir = LEFT
            elif event.key == pg.K_RIGHT and obj.direction != LEFT:
                obj.next_dir = RIGHT


def main():
    """Запуск"""
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pg.display.update()


if __name__ == '__main__':
    main()
