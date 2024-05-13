from tkinter import Tk, Canvas


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
        self.__root.attributes("-type", "dialog")
        self.__canvas = Canvas(width=width, height=height)
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
    def __init__(self, win: Window) -> None:
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True

        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win

    def draw(self, top_left: tuple[int, int], bottom_right: tuple[int, int]) -> None:
        self._x1 = top_left[0]
        self._y1 = top_left[1]
        self._x2 = bottom_right[0]
        self._y2 = bottom_right[1]

        if self.has_left_wall:
            left = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            self._win.draw_line(left, "black")
        if self.has_right_wall:
            right = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
            self._win.draw_line(right, "black")
        if self.has_top_wall:
            top = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            self._win.draw_line(top, "black")
        if self.has_bottom_wall:
            bottom = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            self._win.draw_line(bottom, "black")


def main() -> None:
    win = Window(800, 800)
    c1 = Cell(win)
    c2 = Cell(win)
    c1.has_bottom_wall = False
    c1.draw((400, 400), (500, 500))
    c2.draw((600, 400), (700, 500))
    win.wait_for_close()


main()
