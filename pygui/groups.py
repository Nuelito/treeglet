import pyglet
from pyglet.gl import*

class ScissorGroup(pyglet.graphics.Group):
    def __init__(self, rect=None, order=0, parent=None):
        super().__init__(order=order, parent=parent)
        self.rect = rect
        
        self.translate_x = 0
        self.translate_y = 0
        self.clips = True

    def set_state(self):
        if self.clips:
            glEnable(GL_SCISSOR_TEST)
        
            glScissor(
                int(self.rect.left),
                int(self.rect.bottom),
                int(self.rect.width),
                int(self.rect.height),
            )
        
        glTranslatef(int(self.translate_x), int(self.translate_y), 0)

    def unset_state(self):
        glTranslatef(int(-self.translate_x), int(-self.translate_y), 0)
        if self.clips: glDisable(GL_SCISSOR_TEST)
        
    def __eq__(self, other):
        return (self.__class__ is other.__class__ and
                self.order == other.order and
                self.parent == other.parent and
                self.rect == other.rect)

    def __hash__(self):
        return hash((self.order, self.parent, self.rect))
