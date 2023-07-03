import random

import pygame

# Initialize pygame
pygame.init()

WINDOW_WIDTH = 500
FRAMERATE = 10
CAPTION = "Snake"
GRID_LENGTH = 20

# Colors
GRID_LINE_COLOR = (0, 0, 0)  # black
SNAKE_COLOR = (0, 200, 0)  # green
SNAKE_EYE_COLOR = (0, 0, 0)  # black
FOOD_COLOR = (0, 0, 200)  # blue

# Create window/surface
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_WIDTH))
pygame.display.set_caption("Snake")

# Clock instance to manage fps
clock = pygame.time.Clock()

box_width = WINDOW_WIDTH / GRID_LENGTH


class Box:
    def __init__(
        self, pos: tuple[int, int], color: tuple[int, int, int], eyes: bool = False
    ) -> None:
        self.pos = list(pos)  # 0-based positioning
        self.dir = [1, 0]
        self.eyes = eyes
        self.color = color

    def draw(self) -> None:
        x, y = self.pos[0] * box_width, self.pos[1] * box_width
        pygame.draw.rect(window, self.color, pygame.Rect(x, y, box_width, box_width))
        if self.eyes:
            dx = box_width / 3
            dy = box_width / 2
            pygame.draw.circle(window, SNAKE_EYE_COLOR, (x + dx, y + dy), box_width / 6)
            pygame.draw.circle(
                window, SNAKE_EYE_COLOR, (x + 2 * dx, y + dy), box_width / 6
            )

    def move(self) -> None:
        self.pos[0] = (self.pos[0] + self.dir[0] + GRID_LENGTH) % GRID_LENGTH
        self.pos[1] = (self.pos[1] + self.dir[1] + GRID_LENGTH) % GRID_LENGTH

    def set_direction(self, x_dir: int, y_dir: int) -> None:
        self.dir = [x_dir, y_dir]


class Snake:
    def __init__(self, pos: tuple[int, int]) -> None:
        self.pos = pos
        self.head = Box(pos, color=SNAKE_COLOR, eyes=True)
        self.body = [self.head]  # contains boxes that make up the snake
        self.turns = dict()  # contains positions where the snake changes direction
        self.dir = [1, 0]

    def add_turn(self, x_dir: int, y_dir: int) -> None:
        self.dir = [x_dir, y_dir]
        self.head.dir = self.dir
        self.turns[tuple(self.head.pos)] = self.dir

    def move(self) -> None:
        for index, box in enumerate(self.body):
            pos = tuple(box.pos)
            if pos in self.turns:
                box.set_direction(*self.turns[pos])
                if index == len(self.body) - 1:
                    del self.turns[pos]
            box.move()

    def draw(self) -> None:
        for box in self.body:
            box.draw()

    def add_tail(self) -> None:
        curr_tail = self.body[-1]
        new_tail = Box(curr_tail.pos, color=SNAKE_COLOR)
        new_tail.pos = [
            curr_tail.pos[0] - curr_tail.dir[0],
            curr_tail.pos[1] - curr_tail.dir[1],
        ]
        new_tail.dir = curr_tail.dir.copy()
        self.body.append(new_tail)

    def reset(self) -> None:
        self.__init__((3, 3))


def draw_grid() -> None:
    for line_num in range(1, GRID_LENGTH):
        pygame.draw.line(
            window,
            GRID_LINE_COLOR,
            (line_num * box_width, 0),
            (line_num * box_width, WINDOW_WIDTH),
        )
        pygame.draw.line(
            window,
            GRID_LINE_COLOR,
            (0, line_num * box_width),
            (WINDOW_WIDTH, line_num * box_width),
        )


def update_window() -> None:
    window.fill((0, 0, 0))
    draw_grid()
    snake.draw()
    food.draw()
    pygame.display.update()


def get_food_pos() -> tuple[int, int]:
    x = random.randint(0, GRID_LENGTH - 1)
    y = random.randint(0, GRID_LENGTH - 1)
    # ensure it does not coincide with the snake's body
    while (x, y) in {tuple(box.pos) for box in snake.body}:
        x = random.randint(0, GRID_LENGTH - 1)
        y = random.randint(0, GRID_LENGTH - 1)
    return (x, y)


snake = Snake((3, 3))
food = Box(get_food_pos(), color=FOOD_COLOR)
run = True

while run:
    clock.tick(FRAMERATE)

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_LEFT] and snake.dir != [1, 0]:
        snake.add_turn(-1, 0)
    elif key_pressed[pygame.K_RIGHT] and snake.dir != [-1, 0]:
        snake.add_turn(1, 0)
    elif key_pressed[pygame.K_UP] and snake.dir != [0, 1]:
        snake.add_turn(0, -1)
    elif key_pressed[pygame.K_DOWN] and snake.dir != [0, -1]:
        snake.add_turn(0, 1)

    snake.move()

    # snake eats food
    if snake.head.pos == food.pos:
        snake.add_tail()
        food = Box(get_food_pos(), color=FOOD_COLOR)

    # snake crashes with itself
    for box in snake.body[1:]:
        if snake.head.pos == box.pos:
            snake.reset()

    update_window()

pygame.quit()
