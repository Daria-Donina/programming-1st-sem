import pygame
import random

from pygame.locals import *
from typing import List, Tuple

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)

            self.draw_grid()
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """

        if not randomize:
            return [[0] * self.cell_width for i in range(self.cell_height)]

        grid = []
        for i in range(self.cell_height):
            line = []
            for j in range(self.cell_width):
                line.append(random.randint(0, 1))
            grid.append(line)

        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """

        x = 0
        y = 0
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                rectangle = pygame.Rect(x + 1, y + 1, self.cell_size - 1, self.cell_size - 1)

                if self.grid[i][j] == 1:
                    color = pygame.Color('green')
                else:
                    color = pygame.Color('white')

                pygame.draw.rect(self.screen, color, rectangle)
                x += self.cell_size

            x = 0
            y += self.cell_size

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        cells = []
        for i in range(max(0, cell[0] - 1), min(self.cell_height, cell[0] + 2)):
            for j in range(max(0, cell[1] - 1), min(self.cell_width, cell[1] + 2)):
                if i != cell[0] or j != cell[1]:
                    cells.append(self.grid[i][j])

        return cells

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """

        grid = []

        for i in range(self.cell_height):
            line = []
            for j in range(self.cell_width):
                creature_count = self.get_neighbours((i, j)).count(1)

                if self.grid[i][j] == 1:
                    if 2 <= creature_count <= 3:
                        line.append(1)
                    else:
                        line.append(0)
                else:
                    if creature_count == 3:
                        line.append(1)
                    else:
                        line.append(0)

            grid.append(line)
        return grid


game = GameOfLife()
game.run()
