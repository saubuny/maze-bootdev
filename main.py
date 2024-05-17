from tkinter import Tk, Canvas
from typing import Self
from time import sleep
import random


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1: Point, p2: Point) -> None:
        self.__p1 = p1
        self.__p2 = p2

    def draw(self, canvas: Canvas, fill_color: str) -> None:
        canvas.create_line(
            self.__p1.x, self.__p1.y, self.__p2.x, self.__p2.y, fill=fill_color, width=2
        )


class Window:
    def __init__(self, width: int, height: int) -> None:
        self.__root = Tk(className="Maze")
        self.__root.title("Maze")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__root.attributes("-type", "dialog")  # Floating window
        self.__canvas = Canvas(width=width, height=height, background="white")
        self.__canvas.pack()
        self.__running = False

    def redraw(self) -> None:
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self) -> None:
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self) -> None:
        self.__running = False

    def draw_line(self, line: Line, fill_color: str) -> None:
        line.draw(self.__canvas, fill_color)


class Cell:
    def __init__(self, win: Window | None = None) -> None:
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True

        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0
        self._win = win

        self.visited = False

    def draw(self, top_left: tuple[int, int], bottom_right: tuple[int, int]) -> None:
        self.x1 = top_left[0]
        self.y1 = top_left[1]
        self.x2 = bottom_right[0]
        self.y2 = bottom_right[1]

        if self._win:
            left = Line(Point(self.x1, self.y1), Point(self.x1, self.y2))
            right = Line(Point(self.x2, self.y1), Point(self.x2, self.y2))
            top = Line(Point(self.x1, self.y1), Point(self.x2, self.y1))
            bottom = Line(Point(self.x1, self.y2), Point(self.x2, self.y2))
            self._win.draw_line(left, "black" if self.has_left_wall else "white")
            self._win.draw_line(right, "black" if self.has_right_wall else "white")
            self._win.draw_line(top, "black" if self.has_top_wall else "white")
            self._win.draw_line(bottom, "black" if self.has_bottom_wall else "white")

    def draw_move(self, to_cell: Self, undo: bool = False) -> None:
        color = "gray" if undo else "red"
        self_center = ((self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2)
        other_center = ((to_cell.x1 + to_cell.x2) // 2, (to_cell.y1 + to_cell.y2) // 2)
        line = Line(
            Point(self_center[0], self_center[1]),
            Point(other_center[0], other_center[1]),
        )
        if self._win:
            self._win.draw_line(line, color)


class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        win: Window | None = None,
        seed: int | None = None,
    ) -> None:
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        if seed is not None:
            random.seed(seed)

    def _create_cells(self) -> None:
        self._cells = [
            [Cell(self._win) for _ in range(self._num_rows)]
            for _ in range(self._num_cols)
        ]

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(self._cells, i, j)

    def _draw_cell(self, cells: list[list[Cell]], i: int, j: int) -> None:
        x = i * self._cell_size_x + self._x1
        y = j * self._cell_size_y + self._y1
        if self._win:
            cells[i][j].draw((x, y), (x + self._cell_size_x, y + self._cell_size_y))
        self._animate()

    def _animate(self) -> None:
        if self._win:
            self._win.redraw()
            sleep(0.001)

    def _break_entrance_and_exit(self) -> None:
        self._cells[0][0].has_top_wall = False
        self._draw_cell(self._cells, 0, 0)
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(self._cells, self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i: int, j: int) -> None:
        self._cells[i][j].visited = True
        while True:
            to_visit: list[tuple[int, int]] = []
            # Manually check all neighbors
            if self._can_visit_cell(i - 1, j):
                to_visit.append((i - 1, j))
            if self._can_visit_cell(i + 1, j):
                to_visit.append((i + 1, j))
            if self._can_visit_cell(i, j + 1):
                to_visit.append((i, j + 1))
            if self._can_visit_cell(i, j - 1):
                to_visit.append((i, j - 1))

            if len(to_visit) == 0:
                self._draw_cell(self._cells, i, j)
                return

            direction = random.choice(to_visit)

            if direction[0] == i and direction[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[direction[0]][direction[1]].has_top_wall = False
                self._draw_cell(self._cells, i, j)
                self._draw_cell(self._cells, direction[0], direction[1])
            elif direction[0] == i and direction[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[direction[0]][direction[1]].has_bottom_wall = False
                self._draw_cell(self._cells, i, j)
                self._draw_cell(self._cells, direction[0], direction[1])
            elif direction[0] == i + 1 and direction[1] == j:
                self._cells[i][j].has_right_wall = False
                self._cells[direction[0]][direction[1]].has_left_wall = False
                self._draw_cell(self._cells, i, j)
                self._draw_cell(self._cells, direction[0], direction[1])
            elif direction[0] == i - 1 and direction[1] == j:
                self._cells[i][j].has_left_wall = False
                self._cells[direction[0]][direction[1]].has_right_wall = False
                self._draw_cell(self._cells, i, j)
                self._draw_cell(self._cells, direction[0], direction[1])

            self._break_walls_r(direction[0], direction[1])

    def _reset_cells_visited(self) -> None:
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def solve(self) -> bool:
        return self._solve_r(0, 0)

    def _solve_r(self, i: int, j: int) -> bool:
        self._animate()
        self._cells[i][j].visited = True

        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        if self._can_visit_cell(i - 1, j) and not self._cells[i][j].has_left_wall:
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            self._cells[i][j].draw_move(self._cells[i - 1][j], True)
        if self._can_visit_cell(i + 1, j) and not self._cells[i][j].has_right_wall:
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            self._cells[i][j].draw_move(self._cells[i + 1][j], True)
        if self._can_visit_cell(i, j + 1) and not self._cells[i][j].has_bottom_wall:
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            self._cells[i][j].draw_move(self._cells[i][j + 1], True)
        if self._can_visit_cell(i, j - 1) and not self._cells[i][j].has_top_wall:
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            self._cells[i][j].draw_move(self._cells[i][j - 1], True)
        return False

    # Safe indexing, there is also a better way to do this, i am just lazy and do not care about this guided project
    # I will try harder on the next one, i just have a thing against cell-based projects...
    def _can_visit_cell(self, i: int, j: int) -> bool:
        if i < 0 or j < 0:
            return False
        try:
            return not self._cells[i][j].visited
        except IndexError:
            return False


def main() -> None:
    win = Window(800, 800)
    maze = Maze(8, 8, 20, 20, 39, 39, win, 0)
    maze.solve()
    win.wait_for_close()


main()
