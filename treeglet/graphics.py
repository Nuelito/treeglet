import pyglet
from pyglet.gl import*
from pyglet.math import*

class ScissorGroup(pyglet.graphics.Group):
    """
    Do I need to explain?
    """

    def __init__(self, x, y, width, height, order=0, parent=None):
        super().__init__(order, parent)

        #Clipping variables
        self.x      = x
        self.y      = y
        self.width  = width
        self.height = height


    def set_state(self):
        glEnable(GL_SCISSOR_TEST)
        glScissor(
            int(self.x),
            int(self.y),
            int(self.width),
            int(self.height)
        )


    def unset_state(self):
        glDisable(GL_SCISSOR_TEST)
