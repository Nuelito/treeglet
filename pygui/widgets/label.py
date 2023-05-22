import pyglet as pg
from pyglet.graphics import Group

from ..widget import Widget


class Label(Widget):
    def __init__(self,
                 text,
                 x=0,
                 y=0,
                 z=0,
                 anchor_x='left',
                 anchor_y='bottom',):

        super(Label, self).__init__(x, y, z, anchor_x=anchor_x, anchor_y=anchor_y)

        self._document = pg.text.document.UnformattedDocument(text)
        self._layout = pg.text.layout.TextLayout(self._document, group=self.group, batch=self.batch)
        
    @property
    def width(self):
        return self._layout.width or self._layout.content_width

    @property
    def height(self):
        return self._layout.height or self._layout.content_height

    @width.setter
    def width(self, value):
        return

    @height.setter
    def height(self, value):
        return

    def _update_position(self):
        self._layout.x = self.x + self.__anchor_x_offset__()
        self._layout.y = self.y + self.__anchor_y_offset__()

    def set_group(self, value):
        self._group = Group(self.z, parent=value)
        self._layout.group = self.group
        self._group.visible = self._visible

    def set_batch(self, value):
        self._batch = value
        self._layout.batch = value
        
    def __repr__(self):
        return 'Label(id={})'.format(self.id)
