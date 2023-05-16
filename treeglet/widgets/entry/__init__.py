from .custom import*

import pyglet
from pyglet.gl import*
from pyglet.text.caret import Caret
from pyglet.graphics import OrderedGroup, Group

from treeglet.widget import Widget
from treeglet.helpers import Rectangle
from treeglet.group import ScissorGroup
from treeglet.widgets.image import Image

class TextEntry(Widget):

    """
    Setting the z value to `0` will break it so it's important to set it to something else (1 or above)
    """

    _multiline = False

    def __init__(self, text, background, x, y, z=1, color=(0,0,0,255), caret_color=(0,0,0), 
                 group=None, batch=None):

        super().__init__(x=x, y=y, z=z, width=background.width, height=background.height)

        #Entry properties
        self._text          = text
        self._color         = color
        self._caret_color   = caret_color
        self._focus         = False
        self._style         = dict()

        #Groups and background setup
        self._clip_rect     = Rectangle(x, y, self.width, self.height)
        self._background    = background
        self._background.x  = x
        self._background.y  = y

        self._batch  = batch
        self._group  = OrderedGroup(self._z, parent=group)
        self._bgroup = OrderedGroup(0, parent=self._group)
        self._fgroup = OrderedGroup(1, parent=self._group)
        self._background.set_group(self._bgroup)
        
        self._document = pyglet.text.document.UnformattedDocument(self._text)
        self._document.set_style(0, len(self._document.text), dict(color=self._color))

        self._init_layout_()

    def _init_layout_(self):

        if hasattr(self, '_caret'): self._caret.delete()
        if hasattr(self, '_layout'): self._layout.delete()

        self._layout = CustomLayout(
                self._document,
                self.width,
                self.height,
                group=self._fgroup,
                batch=self._batch
        )
        self._layout.top_group.widget = self
        self._layout.x = int(self.x + self.__anchor_x_offset__() + 1)
        self._layout.y = int(self.y + self.__anchor_y_offset__())

        self._caret = Caret(self._layout, color=self._caret_color)
        self._caret.visible = self._focus


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
        self._background.x = value + self.__anchor_x_offset__()
        self._layout.x = value + self.__anchor_x_offset__() + 1

    @y.setter
    def y(self, value):
        self._y = value
        self._background.y = value + self.__anchor_y_offset__()
        self._layout.y = value + self.__anchor_y_offset__()
        
    @z.setter
    def z(self, value):
        self._z = value
        self.set_group(self._group.parent)

    @width.setter
    def width(self, value):
        self._width = value
        self._layout.width = value
        self._background.width = value

    @height.setter
    def height(self, value):
        self._height = value
        self._layout.height = value
        self._background.height = value

    def set_group(self ,value):
        self._group  = OrderedGroup(self._z, parent=value)
        self._bgroup = OrderedGroup(0, parent=self._group)
        self._fgroup = OrderedGroup(1, parent=self._group)
        self._background.set_group(self._group)
        self._init_layout_()

    def set_batch(self, value):
        self._batch = value
        self._background.set_batch(value)
        self._layout.batch = value

    def set_parent(self, value):
        self._parent = value
        self._background.set_group(self._bgroup)
        self._update_clip_rect()

    """
    Entry functions
    """
    def _update_clip_rect(self):
        if self._parent != None:
            translate_x, translate_y = self._parent.translate_x, self._parent.translate_y
            self._clip_rect.x = max(self._parent._clip_rect.x, self.x+self.__anchor_x_offset__()+translate_x)
            self._clip_rect.y = max(self._parent._clip_rect.y, self.y+self.__anchor_y_offset__()+translate_y)
            self._clip_rect.width = min((self._parent._clip_rect.right - self._clip_rect.x), ((self.x + self.__anchor_x_offset__() + translate_x + self.width) - self._clip_rect.x))
            self._clip_rect.height = min((self._parent._clip_rect.top - self._clip_rect.y), ((self.y + self.__anchor_y_offset__() + translate_y + self.height) - self._clip_rect.y))
            return

        self._clip_rect.x = self.x + self.__anchor_x_offset__()
        self._clip_rect.y = self.y + self.__anchor_y_offset__()
        self._clip_rect.width = self.width
        self._clip_rect.height = self.height


    def _set_focus(self, value):
        self._focus = value
        self._caret.visible = value
        
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
