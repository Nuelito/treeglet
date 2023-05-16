import pyglet
from treeglet.styler import Styler
from treeglet.helpers import Rectangle

class EventDispatcher(pyglet.event.EventDispatcher):
    pass


class Widget(EventDispatcher):

    def __init__(self, x=None, y=None, z=0, width=None, height=None, group=None, batch=None):

        EventDispatcher.__init__(self)

        self._x = x
        self._y = y
        self._z = z

        self._width     = width
        self._height    = height

        self._anchor_x  = 'left'
        self._anchor_y  = 'bottom'

        self._root   = None 
        self._group  = group
        self._batch  = batch
        self._parent = None

        self.styler = Styler()
        self._visible = True
        self.styler._target = self
        self._clip_rect = Rectangle()

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        """
        This property defines the order in which the widget is displayed on the
        window.
        """
        return self._z

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def anchor_x(self):
        return self._anchor_x

    @property
    def anchor_y(self):
        return self._anchor_y

    @x.setter
    def x(self, value):
        pass

    @y.setter
    def y(self, value):
        pass

    @z.setter
    def z(self, value):
        pass

    @width.setter
    def width(self, value):
        pass

    @height.setter
    def height(self, value):
        pass

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        pass

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

    @property
    def center(self):
        return self.left + self.width/2, self.bottom + self.height/2

    """
    Custom functions
    """

    def set_batch(self, value):
        pass

    def set_group(self, value):
        pass

    def set_parent(self, value):
        self._parent = value

    def _check_hit(self, x, y):
        return self.left < x < self.right and self.bottom < y < self.top

    def center_anchor(self):
        self.anchor_x = 'center'
        self.anchor_y = 'center'


    def _resize_(self, prev_width, prev_height, curr_width, curr_height):
        """
        Core function used to resize the widget depending on the style set
        on the styler
        """
        if self.width and self.width:
            self.styler.update_size(
                prev_width,
                prev_height,
                curr_width,
                curr_height
            )
        if self.x and self.y:
            self.styler.update_position(
                prev_width,
                prev_height,
                curr_width,
                curr_height,
            )

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
