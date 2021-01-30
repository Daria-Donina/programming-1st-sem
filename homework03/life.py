import pathlib
import random
import json

from typing import List, Optional, Tuple

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(
            self,
            size: Tuple[int, int],
            randomize: bool = True,
            max_generations: Optional[float] = float('inf')
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if not randomize:
            return [[0] * self.cell_width for i in range(self.cell_height)]

        grid = []
        for i in range(self.cell_height):
            line = []
            for j in range(self.cell_width):
                line.append(random.randint(0, 1))
            grid.append(line)

        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        cells = []
        for i in range(max(0, cell[0] - 1), min(self.cell_height, cell[0] + 2)):
            for j in range(max(0, cell[1] - 1), min(self.cell_width, cell[1] + 2)):
                if i != cell[0] or j != cell[1]:
                    cells.append(self.grid[i][j])

        return cells

    def get_next_generation(self) -> Grid:
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

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations > self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename) as file:
            data = json.load(file)

        game = GameOfLife(
            size=(data['rows'], data['cols']),
            randomize=False,
            max_generations=data['max_generations'])

        game.prev_generation = data['prev_generation']
        game.curr_generation = data['curr_generation']
        game.generations = data['generations']

        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        data = {
            'rows': self.rows,
            'cols': self.cols,
            'prev_generation': self.prev_generation,
            'curr_generation': self.curr_generation,
            'max_generations': self.max_generations,
            'generations': self.generations
        }

        with open(filename, 'w') as file:
            json.dump(data, file)
