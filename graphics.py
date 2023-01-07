import pyglet
from pyglet.gl import*
from pyglet.math import*

class CustomGroup(pyglet.graphics.Group):
    offset_x = 0
    offset_y = 0

class ScissorGroup(CustomGroup):
    """
    Do I need to explain?
    """

    def __init__(self, x, y, width, height, order=0, window=None, parent=None):
        super().__init__(order, parent)

        #Clipping variables
        self.x      = x
        self.y      = y
        self.width  = width
        self.height = height

        self.window = window


    def set_state(self):

        glEnable(GL_SCISSOR_TEST)
        glScissor(
            int(self.x),
            int(self.y),
            int(self.width),
            int(self.height)
        )
        self.window.view = Mat4.from_translation(Vec3(self.offset_x ,self.offset_y,0))



    def unset_state(self):
        self.window.view = Mat4.from_translation(Vec3(0, 0, 0))
        glDisable(GL_SCISSOR_TEST)
