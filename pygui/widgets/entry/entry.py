import pyglet as pg
from pyglet.graphics import Group

from ...widget import Widget



class TextEntry(Widget):
    def __init__(self,
                 text,
                 background,
                 x=0,
                 y=0,
                 z=0,
                 anchor_x='left',
                 anchor_y='bottom',
                 text_color=(0,0,0,255),
                 caret_color=(0,0,0),):

        super(TextEntry, self).__init__(x, y, z, background.width, background.height)

        fgroup = Group(1, parent=self.group)
        self._document = pg.text.document.UnformattedDocument(text)
        self._layout = pg.text.layout.IncrementalTextLayout(self._document, background.width, background.height, group=fgroup)

        self._caret = pg.text.caret.Caret(self._layout, color=caret_color)
        self._caret.visible = True
        self._focus = False

        self._background = background
        self._background.set_group(self.group)

    def _init_layout(self):
        if hasattr(self, '_layout'): self._layout.delete()
        if hasattr(self, '_caret'): self._caret.delete()

    def _update_position(self):
        self._layout.x = self._background.x = self.x + self.__anchor_x_offset__()
        self._layout.y = self._background.y = self.y + self.__anchor_y_offset__()

    def set_group(self, value):
        self._group = Group(self.z, parent=value)
        fgroup = Group(1, parent=self.group)
        self._group.visible = self._visible

        self._layout.group = fgroup
        self._background.set_group(self.group)

    def set_batch(self, value):
        self._batch = value
        self._layout.batch = value
        self._background.set_batch(value)

    def _set_focus(self, value):
        self._focus = value
        self._caret.visible = value
        self._caret.layout = self._layout
        
    def set_style(self, attributes, start=None, end=None):
        self._document.set_style(start, end, attributes)


    """
    Events
    """
    def on_mouse_press(self, x, y, button, modifiers):
        if self._check_hit(x, y):
            self._set_focus(True)
            self._caret.on_mouse_press(x, y, button, modifiers)
        else: self._set_focus(False)

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if not self._focus: return
        self._caret.on_mouse_drag(x, y, dx, dy, button, modifiers)
        
        
    def on_text(self, text):
        if not self._focus: return
        self._caret.on_text(text)

    def on_text_motion(self, motion):
        if not self._focus: return
        self._caret.on_text_motion(motion)

    def __repr__(self):
        return 'TextEntry(id={})'.format(self.id)
