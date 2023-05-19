import pyglet
from pyglet.graphics import Group

from ..tags import*
from ..styler import*
from ..widget import Widget
from ..widgets import Image
from ..helpers import Rectangle
from ..groups import ScissorGroup
from ..handler import MouseHandler

class Frame(Widget):
    """
    A Container for multiple widgets
    """
    
    def __init__(self, window, x=0, y=0, z=0, width=None, height=None, group=None, batch=None):
        width = width or window.width
        height = height or window.height
        super().__init__(x=x, y=y, z=z, width=width, height=height, group=group, batch=batch)

        
        self._window     = window
        self._children   = set()
        self._background = Image(
            pyglet.image.SolidColorImagePattern((255,255,255,255)).create_image(window.width, window.height), x, y)
        
        
        #Gui management properties
        self._handler = None
        #self._handler.container = self
        #self.handler.fixed_container = True
        self._translate_x = 0
        self._translate_y = 0
        self.scrollable = False
        self.scroll_speed = [1, 1]
        self.z_priority = True
        

        #Display modifiers
        self._clips             = True
        self._clip_rect.x       = x
        self._clip_rect.y       = y
        self._clip_rect.width   = window.width
        self._clip_rect.height  = window.height

        self._bgroup = Group(0, parent=self._group)
        if width and height:
            self._clip_rect.width   = width
            self._clip_rect.height  = height
            self._background.width  = width
            self._background.height = height
        self._fgroup = ScissorGroup(self._clip_rect, 1, parent=self._group)
        self._background.set_group(self._bgroup)
        self._background.set_batch(self._batch)

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
        return self._width or self._window.width

    @property
    def height(self):
        return self._height or self._window.height

    @property
    def clips(self):
        return self._clips

    @x.setter
    def x(self, value):
        self._x = value
        self._clip_rect.x = value + self.__anchor_x_offset__()
        self._background.x = value + self.__anchor_x_offset__()

    @y.setter
    def y(self, value):
        self._y = value
        self._clip_rect.y = value + self.__anchor_y_offset__()
        self._background.y = value + self.__anchor_y_offset__()
        
    @z.setter
    def z(self, value):
        self._z = value
        self.set_group(self._group.parent)

    @width.setter
    def width(self, value):
        self._width = value
        self._clip_rect.width = value
        self._background.width = round(value)

    @height.setter
    def height(self, value):
        self._height = value
        self._clip_rect.height = value
        self._background.height = value

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value
        self._group.visible = value

    @clips.setter
    def clips(self, value):
        self._clips = value
        self._fgroup.clips = value
        
    @property
    def translate_x(self):
        return self._translate_x
        
    @property
    def translate_y(self):
        return self._translate_y
    
    @translate_x.setter
    def translate_x(self, value):
        self._translate_x = value
        self._fgroup.translate_x = value
        
    @translate_y.setter
    def translate_y(self, value):
        self._translate_y = value
        self._fgroup.translate_y = value
        
    @property
    def handler(self):
        return self._handler
        
    @handler.setter
    def handler(self, value):
        self._window.remove_handlers(self)
        if self._handler: self._handler.containers.remove(self)
        value.containers.append(self)

    def set_group(self, value):
        self._group     = Group(self._z, parent=value)
        self._bgroup    = Group(order=0, parent=self._group)
        self._fgroup    = ScissorGroup(self._clip_rect, order=1, parent=self._group)
        self._fgroup.clips = self._clips
        self._fgroup.translate_x = self.translate_x
        self._fgroup.translate_y = self.translate_y
        self._group.visible = self.visible
        
        self._background.set_group(self._bgroup)
        for child in self._children: child.set_group(self._fgroup)

    def set_batch(self, value):
        self._batch = value
        self._background.set_batch(value)
        for child in self._children: child.set_batch(value)

    """
    Frame methods
    """
    @property
    def background(self):
        return self._background.image

    @property
    def background_visible(self):
        return self._background.visible
        
    @background.setter
    def background(self, value):
        self._background.image = value
    
    @background_visible.setter
    def background_visible(self, value):
        self._background.visible = value
    
    def add_widget(self, widget):
        widget.set_group(self._fgroup)
        widget.set_batch(self._batch)
        widget.set_parent(self)
        self._children.add(widget)
        
    """
    Mouse Events
    """
    def on_mouse_press(self, x, y, button, modifiers):
        x, y = x - self.translate_x, y - self.translate_y
        for child in self._children: child.on_mouse_press(x, y, button, modifiers)
        
    def on_mouse_release(self, x, y, button, modifiers):
        x, y = x - self.translate_x, y - self.translate_y
        for child in self._children: child.on_mouse_release(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        for child in self._children: child.on_mouse_drag(x, y, dx, dy, button, modifiers)
        
    def on_mouse_motion(self, x, y, dx, dy):
        x, y = x - self.translate_x, y - self.translate_y
        for child in self._children: child.on_mouse_motion(x, y, dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        x, y = x - self.translate_x, y - self.translate_y
        for child in self._children: child.on_mouse_drag(x, y, dx, dy, button, modifiers)


    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if not self.scrollable: return
        if self._check_hit(x, y):
            self.translate_x += scroll_x * self.scroll_speed[0]
            self.translate_y += scroll_y * self.scroll_speed[1]
        
        x, y = x - self.translate_x, y - self.translate_y
        for child in self._children: child.on_mouse_scroll(x, y, scroll_x, scroll_y)
        
    #Documents functions
    def on_text(self, text):
        for child in self._children: child.on_text(text)
        
    def on_text_motion(self, motion):
        for child in self._children: child.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        for child in self._children: child.on_text_motion_select(motion)

    def _resize(self, prev_width, prev_height, new_width, new_height):
        """
        Overwritting the `_resize_` method as frame has additional properties
        compare to adding to window
        """

        old_x, old_y = self.left, self.bottom
        old_w, old_h = self.width, self.height
        
        bx, by = self.left, self.bottom

        #Updating Frame
        self.styler.update_size(prev_width, prev_height, new_width, new_height)
        self.styler.update_position(prev_width, prev_height, new_width, new_height)
        
        new_x, new_y = self.left, self.bottom
        new_w, new_h = self.width, self.height
        Bx, By = self.left, self.bottom
        
        for child in self._children:
        
            dx = child.x - old_x
            dy = child.y - old_y
            
            child.styler.update_size(old_w, old_h, self.width, self.height)
            
            child.x += (new_x - old_x)
            child.y += (new_y - old_y)
            
            
            
            if child.styler.x_position_type == STYLER_POSITIONTYPE_FIXED: child.x = Bx + (dx*new_w/old_w)
            if child.styler.y_position_type == STYLER_POSITIONTYPE_FIXED: child.y = By + (dy*new_h/old_h)
            
            if child.styler.x_position_type == STYLER_POSITIONTYPE_INCREMENT: child.x += (new_w - old_w)
            if child.styler.y_position_type == STYLER_POSITIONTYPE_INCREMENT: child.y += (new_h - old_h)
            
