import pyglet as pg
from pyglet.graphics import Group

from ..widget import Widget
from .image import Image

class Button(Widget):
    def __init__(self,
                 depressed,
                 pressed,
                 hover=None,
                 x=0,
                 y=0,
                 z=0,
                 anchor_x='left',
                 anchor_y='bottom',):

        super(Button, self).__init__(x, y, z, depressed.width, depressed.height, anchor_x, anchor_y)

        self._dimage = depressed
        self._pimage = pressed
        self._himage = hover or depressed

        self._button = Image(depressed, x, y, z=0)
        self._button.set_group(self.group)
        self._button.set_batch(self.batch)

    def _update_position(self):
        self._button.x = self.x + self.__anchor_x_offset__()
        self._button.y = self.y + self.__anchor_y_offset__()

    def _update_size(self):
        self._button.width  = self.width
        self._button.height = self.height

    def set_group(self, value):
        self._group = Group(self._z, parent=value)
        self._button.set_group(self._group)
        self._group.visible = self._visible

    def set_batch(self, value):
        self._batch = value
        self._button.set_batch(value)

    def __repr__(self):
        return 'Button(id={})'.format(self.id)

    """
    Events
    """
    def on_mouse_press(self, x, y, button, modifiers):
        if self._check_hit(x, y):
            self._pressed = True
            self._button.image = self._pimage
            self.dispatch_event('on_press')
            
    def on_mouse_release(self, x, y, button, modifiers):
        self._button.image = self._dimage if not self._check_hit(x, y) else self._himage
        self._pressed = False
        
    def on_mouse_motion(self, x, y, dx, dy):
        self._button.image = self._himage if self._check_hit(x, y) else self._dimage


Button.register_event_type('on_press')
