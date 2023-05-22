import pyglet as pg
from pyglet.graphics import Group

from ..tags import*
from ..widget import Widget
from ..widgets import Image
from ..group import ScissorGroup
from ..helpers import Rectangle

class Frame(Widget):
    def __init__(self,
                 window,
                 x=0,
                 y=0,
                 z=0,
                 width=250,
                 height=250,
                 anchor_x='left',
                 anchor_y='bottom',):

        super(Frame, self).__init__(x, y, z, width, height, anchor_x, anchor_y)


        self._background = None
        self.children = set()
        self.children_by_id = dict()

        self._handler = None
        self.scrollable = True
        self.scroll_speed = [1.0, 1.0]

        self.window = window
        self._group = Group(z, parent=None)
        self.fgroup = ScissorGroup(window, Rectangle(x, y, width, height), order=self.z, parent=self._group)

    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, value):
        self._background = value
        bgroup = Group(0, parent=self._group)
        self._background.set_group(bgroup)
        self._background.width = self.width
        self._background.height = self.height
        self._background.set_batch(self.batch)
    
    def _update_position(self):
        self.fgroup.area.x = self.x + self.__anchor_x_offset__()
        self.fgroup.area.y = self.y + self.__anchor_y_offset__()
        
        if not self.background: return
        self.background.x = self.fgroup.area.x
        self.background.y = self.fgroup.area.y

    def _update_size(self):
        self._background.width = self.width
        self._background.height = self.height

    def scroll(self, scroll_x, scroll_y):
        self.translate_x += scroll_x * self.scroll_speed[0]
        self.translate_y += scroll_y * self.scroll_speed[1]

    @property
    def translate_x(self):
        return self.fgroup.translate_x

    @property
    def translate_y(self):
        return self.fgroup.translate_y

    @translate_x.setter
    def translate_x(self, value):
        self.fgroup.transalte_x = value

    @translate_y.setter
    def translate_y(self, value):
        self.fgroup.translate_y = value

    @property
    def handler(self):
        return self._handler

    @handler.setter
    def handler(self, value):
        self._handler = value
        value.add_container(self)

    def set_group(self, value):
        self._group = Group(self.z, parent=value)
        self.fgroup = ScissorGroup(self.window, 
                                   Rectangle(self.left, self.bottom, self.width, self.height),
                                   self.fgroup.translate_x,
                                   self.fgroup.translate_y,
                                   order=1, 
                                   parent=self.group)
        self._group.visible = self._visible

        if self.background:
            bgroup = Group(0, parent=self._group)
            self.background.set_group(bgroup)

        [child.set_group(self.fgroup) for child in self.children]


    def set_batch(self, value):
        if self.background: self.background.set_batch(value)
        [child.set_batch(value) for child in self.children]
        self._batch = value

    def add_widget(self, widget):
        if widget.id in self.children_by_id:
            return

        widget.set_group(self.fgroup)
        widget.set_batch(self.batch)
        widget.parent = self

        self.children.add(widget)
        self.children_by_id[widget.id] = widget

    def remove_widget(self, widget):
        if widget.id not in self._children_by_id:
            return
        self.childre.remove(widget)
        del self.children_by_id[widget.id]
    
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
        
        for child in self.children:
        
            dx = child.x - old_x
            dy = child.y - old_y
            
            child.styler.update_size(old_w, old_h, self.width, self.height)
            
            child.x += (new_x - old_x)
            child.y += (new_y - old_y)
            
            
            
            if child.styler.x_position_type == STYLER_POSITIONTYPE_FIXED: child.x = Bx + (dx*new_w/old_w)
            if child.styler.y_position_type == STYLER_POSITIONTYPE_FIXED: child.y = By + (dy*new_h/old_h)
            
            if child.styler.x_position_type == STYLER_POSITIONTYPE_INCREMENT: child.x += (new_w - old_w)
            if child.styler.y_position_type == STYLER_POSITIONTYPE_INCREMENT: child.y += (new_h - old_h)

    def __repr__(self):
        return 'Frame(id={})'.format(self.id)
