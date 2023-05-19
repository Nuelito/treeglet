import pyglet
from pyglet.gl import*
from pyglet.graphics import*

from .widget import Widget

class Gui:
    def __init__(self, window):

        #Settings
        self.aa = True

        self._group = Group()
        self._batch = Batch()

        self.window = window
        self._children = set()
        self.win_sizes = window.width, window.height

    """
    Events
    """

    def on_resize(self, width, height):
        [child._resize(*self.win_sizes, width, height) for child in self._children]
        self.win_sizes = width, height

    def on_draw(self):
        glClearColor(0.7, 0.7, 0.7, 1.0)
        self.window.clear()
        if self.aa:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        self._batch.draw()

    """
    Gui specific function
    """
    def add_widget(self, widget, group=None):
        self._children.add(widget)
        widget.set_group(self._group)
        widget.set_batch(self._batch)
        self.window.push_handlers(widget)

    def remove_widget(self, widget):
        if widget not in self._children:
            return
        widget.set_group(None)
        widget.set_batch(None)
        self.window.remove_handlers(widget)
