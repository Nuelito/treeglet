import pyglet
from pyglet.gl import*
from pyglet.text.layout import*
from pyglet.graphics import Group
from ...helpers import Rectangle

"""
Custom Groups for the text entry
"""

class CustomLayoutGroup(IncrementalTextLayoutGroup):

    def set_state(self):

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glEnable(GL_SCISSOR_TEST)
        
        
        try:
            glScissor(
                int(self.widget._clip_rect.x),
                int(self.widget._clip_rect.y),
                int(self.widget._clip_rect.width),
                int(self.widget._clip_rect.height),
            )
        except: pass #In case entry exceeds frame boundaries. Check `_update_clip_rect` method
        glTranslatef(int(self.translate_x ), int(self.translate_y), 0)

    def unset_state(self):
        glTranslatef(int(-self.translate_x), int(-self.translate_y), 0)
        glDisable(GL_SCISSOR_TEST)
        self.widget._update_clip_rect()

    def __hash__(self):
        return hash((id(self)))

    def __eq__(self, other):
        return (self.__class__ is other.__class__ and
                self._order == other.order and
                self.parent == other.parent and
                self.widget == other.widget)

class CustomLayout(IncrementalTextLayout):
    def _init_groups(self, group):
        
        self.top_group = CustomLayoutGroup(parent=group)
        self.background_group = pyglet.graphics.Group(0, parent=self.top_group)
        self.foreground_group = TextLayoutForegroundGroup(1, parent=self.top_group)
        self.foreground_decoration_group =TextLayoutForegroundDecorationGroup(2, parent=self.top_group)

