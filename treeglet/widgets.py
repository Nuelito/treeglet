import pyglet
import pyglet.gl as gl
import pyglet.gui as gui

class Behaviour:
    """
    `Behaviours` class is a container for variable that defines the way
    Widgets change with the window.
    """

    #Position setup
    sticky_x = False
    sticky_y = False

    def __init__(self, widget, parent):
        self.widget = widget
        self.parent = parent

        self.w_x = self.widget.x
        self.w_y = self.widget.y

        self.p_width  = parent.width
        self.p_height = parent.height

    def on_resize(self, width, height):
        dx = (self.widget.x)/self.p_width

        self.widget.x = width*dx


        self.p_width  = width
        self.p_height = height

class WidgetBase(gui.WidgetBase):
    name = "widget"
    _z_index    = 0
    _visible    = True
    parent      = None
    _mouse      = None
    behaviour   = None

    @property
    def mouse(self):
        return self._mouse

    def set_mouse_handler(self, mouse):
        self._mouse = mouse

    @property
    def global_z_index(self):
        if self.parent:
            return self.z_index + self.parent.global_z_index
        return self.z_index  
    def hide(self): 
        pass
    def show(self): 
        pass
    def set_group(self, group): 
        pass
    def on_resize(self, width, height):
        pass


class PushButton(WidgetBase):
    def __init__(self, x, y, pressed, depressed, hover=None, group=None, batch=None):
        WidgetBase.__init__(self, x, y, depressed.width, depressed.height)

        self._pimage = pressed
        self._dimage = depressed
        self._himage = hover or depressed

        self._group = pyglet.graphics.Group(0, parent=group) #`Base` group
        bg_group = pyglet.graphics.Group(order=0, parent=self._group)
        self._batch = batch or pyglet.graphics.Batch()
        self._sprite = pyglet.sprite.Sprite(depressed, x, y, group=bg_group, batch=self._batch)

        self._pressed = False



    @property
    def z_index(self):
        return self._z_index

    @z_index.setter
    def z_index(self, value):
        self._z_index = value
        self.set_group(self._group.parent)

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._sprite._visible = value
        self._visible = value

    def set_group(self, group):
        self._group = pyglet.graphics.Group(0, parent=group)
        bg_group = pyglet.graphics.Group(parent=self._group)
        self._sprite.group = bg_group

    def hide(self):
        self.visible = False 
        self.on_mouse_motion(0,0,0,0) #To update sprite

    def show(self):
        self.visible = True
        self.on_mouse_motion(0,0,0,0) #To update sprite

    def on_mouse_press(self, x, y, button, modifiers):
        if not self._check_hit(x, y) or not self.visible: return

        self._pressed = True
        self._sprite.image = self._pimage
        self.dispatch_event("on_press")

    def on_mouse_release(self, x, y, button, modifiers):
        if not self._pressed: return

        self._pressed = False
        self._sprite.image = self._dimage
        if self._check_hit(x, y): self.dispatch_event("on_click")

    def on_mouse_motion(self, x, y, dx, dy):
        if self._pressed: return

        self._sprite.image = self._himage if self._check_hit(x, y) else self._dimage

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if self._pressed: return
        self._sprite.image = self._himage if self._check_hit(x, y) else self._dimage

    def on_resize(self, width, height):
        print(width, height)

PushButton.register_event_type("on_press")
PushButton.register_event_type("on_click")

class TextButton(PushButton):
    def __init__(self, text, x, y, pressed, depressed, hover=None, group=None, batch=None):
        PushButton.__init__(self, x, y, pressed, depressed, hover, group, batch)
        fg_group = pyglet.graphics.Group(1, parent=group)
        self._label = pyglet.text.Label(text=text, x=x, y=y, group=fg_group, batch=batch)

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._sprite._visible = value
        self._label.visible = value
        self._visible = value

    def set_group(self, group):
        self._group = pyglet.graphics.Group(self.z_index, parent=group)
        bg_group = pyglet.graphics.Group(order=0, parent=self._group)
        fg_group = pyglet.graphics.Group(order=1, parent=self._group)
        self._sprite.group= bg_group
        self._label.group = fg_group
   

    def style(self, **kwargs):
        for var, value in kwargs.items():
            setattr(self._label, var, value)

    def center_text(self):
        self.style(
            x = self.x + self._width//2,
            y = self.y + self._height//2,
            anchor_x = "center",
            anchor_y = "center",
        )
