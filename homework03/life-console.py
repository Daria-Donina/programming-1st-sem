import curses
import curses.textpad
import time

from life import GameOfLife
from ui import UI


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        curses.textpad.rectangle(screen, 0, 0, self.life.rows + 1, self.life.cols + 1)

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    screen.addch(i + 1, j + 1, '*')
                else:
                    screen.addch(i + 1, j + 1, ' ')
        screen.refresh()

    def run(self) -> None:
        screen = curses.initscr()

        self.draw_borders(screen)

        while not self.life.is_max_generations_exceeded and self.life.is_changing:
            self.draw_grid(screen)
            self.life.step()
            time.sleep(0.2)

        curses.endwin()

game = GameOfLife((10, 10), max_generations=100)
console = Console(game)

console.run()
