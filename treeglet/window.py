import pyglet
from pyglet.gl import*

class Window(pyglet.window.Window):
    """
    Default window that goes with Treeglet
    library
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._prev_res = self.width, self.height
        self._children = set()
        self.can_clear = True

        self._bgcolor = 0.7, 0.7, 0.7, 1.0
        self._group = pyglet.graphics.Group()
        self._batch = pyglet.graphics.Batch()

    def add_widget(self, widget):
        widget.set_batch(self._batch)
        widget.set_group(self._group)
        self._children.add(widget)

    def on_resize(self, width, height):
        #Copied from the repository to not break this event
        self._projection.set(self.width, height, *self.get_framebuffer_size())
        
        for child in self._children: child._resize_(*self._prev_res, width, height)
        self._prev_res = width, height

    def on_draw(self):
        glClearColor(*self._bgcolor)
        self.clear()

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        self._batch.draw()

    def on_key_press(self, symbol, modifiers):
        """
        Overwritting pyglet default escape button
        """
        pass
