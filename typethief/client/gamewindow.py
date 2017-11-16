# typethief/client/gamewindow.py

import pygame


class GameWindow(object):
    """
    """
    BG_COLOR = 255, 255, 255
    MODES = ['MENU', 'WAITING', 'PLAYING']

    def __init__(
        self,
        width=960,
        height=480,
        fps=100,
    ):
        pygame.init()

        self._size = width, height
        self._mode = 'PLAYING' # todo: after making menu, switch

        self._time = pygame.time.Clock()
        self._fps = fps

        self._screen = pygame.display.set_mode(self._size)

    @property
    def width(self):
        return self._size[0]

    @property
    def height(self):
        return self._size[1]

    @property
    def screen(self):
        return self._screen

    def clear_screen(self):
        self._screen.fill(GameWindow.BG_COLOR)

    def draw(self):
        self._time.tick(self._fps)
        pygame.display.update()
