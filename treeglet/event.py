import pyglet

class MouseHandler(pyglet.event.EventDispatcher):
    """
    Special class to manage widgets and prevent interactions such as
    clicking two widgets at the same time.
    """
    
    def __init__(self):

        #Mouse Position
        self.x      = 0
        self.y      = 0

        #Widget
        self._frame     = None
        self._pwidget   = None #Press Widget
        self._hwidget   = None #Hover Widget
        self._dwidget   = None #Drag widget

    """
    Custom function
    """
    def _remove_frame(self):
        self._remove_hover()
        self._remove_drag()
        self._frame = None

    def _set_frame(self, value):
        self._remove_frame()
        self._frame = value

    def _set_hover(self, value):
        self._remove_hover()
        self._hover = value

    def _remove_hover(self):
        if self._hwidget == None: return

        bx, by = self._hwidget.bottom_left
        self._hwidget.on_mouse_motion(bx-1, by, 0, 0)
        self._hwidget = None

    def _set_drag(self, value):
        self._remove_drag()
        self._dwidget = value

    def _remove_drag(self):
        if self._dwidget == None: return

        bx, by = self._dwidget.bottom_left
        self._dwidget.on_mouse_drag(bx-1, by-1, 0, 0, 0, 0)
        self._dwidget = None

    """
    Properties
    """
    @property
    def pwidget(self):
        return self._pwidget

    @pwidget.setter
    def pwidget(self, value):
        if value.parent != self._frame: return
        if self._pwidget == None: self._pwidget = value
        else:
            xo = self._pwidget.parent.offset_x if self._pwidget.parent else 0
            yo = self._pwidget.parent.offset_y if self._pwidget.parent else 0

            if self._pwidget._check_hit(self.x-xo, self.y-yo):
                if value.z > self._pwidget.z: self._pwidget = value; return
                return
            else: self._pwidget = value

    @property
    def hwidget(self):
        return self._hwidget

    @hwidget.setter
    def hwidget(self, value):
        if value.parent != self._frame: return
        if self._hwidget == None: self._hwidget = value
        else:
            xo = self._hwidget.parent.offset_x if self._hwidget.parent else 0
            yo = self._hwidget.parent.offset_y if self._hwidget.parent else 0

            if self._hwidget._check_hit(self.x-xo, self.y-yo):
                if value.z > self._frame.z: self._set_hover(value); return
                return
            else: self._set_hover(value)

    @property
    def dwidget(self):
        return self._dwidget

    @dwidget.setter
    def dwidget(self, value):
        if value.parent != self._frame: return
        if self._dwidget == None: self._dwidget = value
        else:
            xo = self._dwidget.parent.offset_x if self._dwidget.parent else 0
            yo = self._dwidget.parent.offset_y if self._dwidget.parent else 0

            if self._dwidget._check_hit(self.x-xo, self.y-yo):
                if value.z > self._frame.z: self._set_drag(value); return
                return
            else: self._set_drag(value)



    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        if self._frame == None: self._frame = value
        else:
            if self._frame._check_hit(self.x, self.y):
                if value.z > self._frame.z: self._set_frame(value); return
                return
            else: self._set_frame(value)

    """
    Mouse Event
    """
    def on_mouse_release(self, x, y, button, modifiers):
        return

    def on_mouse_motion(self, x, y, dx, dy):
        self.x      = x
        self.y      = y


    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        self.x      = x
        self.y      = y
