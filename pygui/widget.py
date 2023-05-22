import pyglet
from pyglet.graphics import Group
from pyglet.event import EventDispatcher

from uuid import uuid4
from .styler import Styler

_id_bank = set()

def _gen_uid():
    uid = str(uuid4())
    uid = uid if uid not in _id_bank else _gen_uid()
    _id_bank.add(uid)
    return uid

class Widget(EventDispatcher):

    def __init__(self,
                 x=0,
                 y=0,
                 z=0,
                 width=100,
                 height=100,
                 anchor_x='left',
                 anchor_y='bottom',
                 group=None,
                 batch=None):

        EventDispatcher.__init__(self)

        self._x = x
        self._y = y
        self._z = z

        self._width  = width
        self._height = height

        self._anchor_x = anchor_x
        self._anchor_y = anchor_y

        self._group = Group(z, parent=group)
        self._batch = None
        self.parent = None

        self._visible = True

        self._id = _gen_uid()
        self.styler = Styler(self)


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
        self._update_position()

    @y.setter
    def y(self, value):
        self._y = value
        self._update_position()

    @z.setter
    def z(self, value):
        self._z = value
        self.set_group(self.group.parent)

    @width.setter
    def width(self, value):
        self._width = value
        self._update_size()

    @height.setter
    def height(self, value):
        self._height = value
        self._update_size()

    @property
    def batch(self):
        return self._batch

    @property
    def group(self):
        return self._group

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self.group.visible = value
        self._visible = value

    """
    Anchors
    """
    @property
    def anchor_x(self):
        return self._anchor_x

    @property
    def anchor_y(self):
        return self._anchor_y

    @anchor_x.setter
    def anchor_x(self, value):
        c_offset = self.__anchor_x_offset__()
        n_offset = self.__anchor_x_offset__(value)

        self._anchor_x = value
        self.x = self.x

    @anchor_y.setter
    def anchor_y(self, value):
        c_offset = self.__anchor_y_offset__()
        n_offset = self.__anchor_y_offset__(value)

        self._anchor_y = value
        self.y = self.y

    def __anchor_x_offset__(self, value=None):
        value = value or self.anchor_x
        x_off = {'left' : 0, 'center': -self._width/2,'right' : -self._width}
        return x_off[value]

    def __anchor_y_offset__(self, value=None):
        value = value or self.anchor_y
        x_off = {'bottom' : 0, 'center': -self._height/2,'top' : -self._height}
        return x_off[value]

    """
    Boundaries
    """
    @property
    def left(self):
        return self.x + self.__anchor_x_offset__()

    @property
    def bottom(self):
        return self.y + self.__anchor_y_offset__()

    @property
    def right(self):
        return self.left + self.width

    @property
    def top(self):
        return self.bottom + self.height


    def _update_position(self):
        pass

    def _update_size(self):
        pass

    def _check_hit(self, x, y):
        left = self.__anchor_x_offset__() + self.x
        bottom = self.__anchor_y_offset__() + self.y

        right = left + self.width
        top = bottom + self.height
        return left < x < right and bottom < y < top

    def _resize(self, oWidth, oHeight, nWidth, nHeight):
        self.styler.update_size(oWidth, oHeight, nWidth, nHeight)
        self.styler.update_position(oWidth, oHeight, nWidth, nHeight)

    
    def set_batch(self, value):
        pass

    def set_group(self, value):
        pass

    """
    Events
    """

    def on_mouse_press(self, x, y, button, modifier):
        pass

    def on_mouse_release(self, x, y, button, modifier):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        pass
        
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        pass

    def on_text(self, text):
        return

    def on_text_motion(self, motion):
        pass

    def on_text_motion_select(self, motion):
        pass

    @property
    def id(self):
        return self._id

    def __repr__(self):
        return 'Widget(id={})'.format(self._id)

    def __hash__(self):
        return hash(self._id)

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self._id == other._id)
