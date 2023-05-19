import pyglet
from pyglet.graphics import Group

from .image import Image
from ..widget import Widget


class Button(Widget):
    def __init__(self, depressed, pressed, hover=None, x=0, y=0, z=0, group=None, batch=None):
        super().__init__(x=x, y=y, z=z, width=depressed.width, height=depressed.height)
        
        self._dimage = depressed
        self._pimage = pressed
        self._himage = hover or depressed
        
        self._group  = Group(z, parent=group)
        self._button = Image(depressed, x, y, 0, self._group, batch)
        
        self._pressed = False
        self._button._resize_image = False
        
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
        return self._width
        
    @property
    def height(self):
        return self._height
        
    @x.setter
    def x(self, value):
        self._x = value
        self._button.x = value + self.__anchor_x_offset__()
        
    @y.setter
    def y(self, value):
        self._y = value
        self._button.y = value + self.__anchor_y_offset__()
        
    @z.setter
    def z(self, value):
        self._z = value
        self.set_group(self._group.parent)
        
    @width.setter
    def width(self, value):
        self._width = value
        self._button.width = value
    
    @height.setter
    def height(self, value):
        self._height = value
        self._button.height = value
        
    def set_group(self, value):
        self._group = Group(self._z, parent=value)
        self._button.set_group(self._group)
        
    def set_batch(self, value):
        self._batch = value
        self._button.set_batch(value)
        
    """
    Events
    """
    def on_mouse_press(self, x, y, button, modifiers):
        if self._check_hit(x, y):
            self._pressed = True
            self._button.image = self._pimage
            
    def on_mouse_release(self, x, y, button, modifiers):
        self._button.image = self._dimage if not self._check_hit(x, y) else self._himage
        self._pressed = False
        
    def on_mouse_motion(self, x, y, dx, dy):
        self._button.image = self._himage if self._check_hit(x, y) else self._dimage
