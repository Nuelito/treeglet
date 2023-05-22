import pyglet as pg
from pyglet.gl import*
import pyglet.math as math
from pyglet.graphics import Group

class ScissorGroup(Group):
    def __init__(self, window, area, translate_x=0, translate_y=0, order=0, parent=None):
        super(ScissorGroup, self).__init__(order, parent)

        self.area = area
        self.window = window

        self.translate_x = translate_x
        self.translate_y = translate_y

    def set_state(self):
        glEnable(GL_SCISSOR_TEST)
        glScissor(int(self.area.left),
                  int(self.area.bottom),
                  int(self.area.width),
                  int(self.area.height),)
        self.window.view = math.Mat4.from_translation(math.Vec3(self.translate_x, self.translate_y, 0))

    def unset_state(self):
        self.window.view = math.Mat4()
        glDisable(GL_SCISSOR_TEST)
