import pyglet
from pyglet.graphics import Group
from pyglet.text.layout import TextLayout

from ..widget import Widget

class Label(Widget):
    def __init__(self, text, x=0, y=0, z=0, group=None, batch=None):
    
        super().__init__(x=x, y=y, z=z)
        
        self._document = pyglet.text.document.UnformattedDocument(text)
        
        self._group = Group(z, parent=group)
        self._batch = batch
        self._init_layout()
        self._width  = self._layout.width or self._layout.content_width
        self._height = self._layout.height or self._layout.content_height
        
    @property
    def x(self):
        return self._x
        
    @property
    def y(self):
        return self._y
        
    @property
    def z(self):
        return self._z
        
    @property
    def width(self):
        return self._layout.width or self._layout.content_width
        
    @property
    def height(self):
        return self._layout.height or self._layout.content_height
        
    @x.setter
    def x(self, value):
        self._x = value
        self._layout.x = int(value + self.__anchor_x_offset__())
        
    @y.setter
    def y(self, value):
        self._y = value
        self._layout.y = int(value + self.__anchor_y_offset__())
        
    @z.setter
    def z(self, value):
        self._z = value
        self.set_group(self._group.parent)
        
    def _init_layout(self):
        if hasattr(self, '_layout'): 
            self._layout.delete()
        
        self._layout = TextLayout(
            self._document,
            group = self._group,
            batch = self._batch,
        )
        
        self._layout.x = self._x
        self._layout.y = self._y
        
    def set_style(self, attributes, start=None, end=None):
        start = start or 0
        end = end or len(self._document.text)
        
        
        self._document.set_style(start, end, attributes)
        
        self._width  = self._layout.content_width
        self._height = self._layout.content_height
        
        
    def set_group(self, value):
        self._group = Group(self._z, parent=value)
        self._init_layout()
        
    def set_batch(self, value):
        self._batch = value
        self._layout.batch = value
