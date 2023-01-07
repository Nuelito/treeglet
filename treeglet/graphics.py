import pyglet
from pyglet.gl import*
from pyglet.math import*

"""
Custom group for Custom Widgets
"""


class ScissorGroup(pyglet.graphics.Group):
    def __init__(self, x, y, width, height, order=0, parent=None):
        super().__init__(order, parent)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.offset_x = 0
        self.offset_y = 0

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

class ScrollingGroup(ScissorGroup):
    scroll_x = 0
    scroll_y = 0
    window = None #You should probably set this up when using the group

    def set_state(self):
        glEnable(GL_SCISSOR_TEST)
        glScissor(
            int(self.x),
            int(self.y),
            int(self.width),
            int(self.height)
        )
        self.window.view = Mat4.from_translation(Vec3(0,self.scroll_y,0))

    def unset_state(self):
        self.window.view = Mat4.from_translation(Vec3(0,0,0))
        glDisable(GL_SCISSOR_TEST)


