import pyglet
from pyglet.gl import*
from pyglet.graphics import Batch, Group

class Gui:
    def __init__(self, window):

        self.window = window
        self.children = set()
        self.children_by_id = dict()

        self._batch = Batch()
        self._group = Group()

        self.bgcolor = 0.7, 0.7, 0.8, 1.0
        self.window_dimensions = [window.width, window.height]
        window.push_handlers(on_draw=self.on_draw, on_resize=self.on_resize)

    @property
    def group(self):
        return self._group

    @property
    def batch(self):
        return self._batch

    def add_widget(self, widget):
        if widget.id in self.children_by_id:
            return

        widget.set_group(self.group)
        widget.set_batch(self.batch)
        self.children.add(widget)
        self.window.push_handlers(widget)
        self.children_by_id[widget.id] = widget

    def remove_widget(self, widget):
        if widget.id not in self.children_by_id:
            return
        self.children.remove(widget)
        del self.children_by_id[widget.id]
        self.window.remove_handlers(widget)

    def on_resize(self, width, height):
        [widget._resize(*self.window_dimensions, width, height) for widget in self.children]
        self.window_dimensions = width, height

    def on_draw(self):
        glClearColor(*self.bgcolor)
        self.window.clear()
        self.batch.draw()
