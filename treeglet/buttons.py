import pyglet
from pyglet.graphics import OrderedGroup, Batch
from .widget import WidgetBase


class PushButton(WidgetBase):

    def __init__(self, x, y, depressed, pressed, hover, anchor_x="left", anchor_y="bottom", group=None, batch=None):

        super().__init__(x, y, depressed.width, depressed.height, anchor_x=anchor_x, anchor_y=anchor_y)

        self._batch = batch or Batch()
        self._group = OrderedGroup(0, parent=group)
        bgroup      = OrderedGroup(0, parent=self._group)

        #Images
        self._himage = hover
        self._pimage = pressed
        self._dimage = depressed

        self._sprite = pyglet.sprite.Sprite(
            depressed,
            x,
            y,
            group=bgroup,
            batch=self._batch
        )

        self.pressed = False

    """
    Properties
    """

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        xO, yO  = self.anchor_offset
        self._sprite.x = value - xO
        self._x = value


    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        xO, yO = self.anchor_offset
        self._sprite.y = value - yO
        self._y = value

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._group = OrderedGroup(value, parent=self._group.parent)
        bgroup = OrderedGroup(0, parent=self._group)
        self._sprite.group = bgroup
        self._z = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._sprite.scale_x *= value/self._width
        self._width = value
        
    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._sprite.scale_y *= value/self._height
        self._height = value

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value


    @property
    def group(self):
        return self._group.parent

    @group.setter
    def group(self, value):
        self._group = OrderedGroup(self.z, parent=value)
        bgroup = OrderedGroup(0, parent=self._group)
        self._sprite.group = bgroup

    @property
    def batch(self):
        return self._batch

    @batch.setter
    def batch(self, value):
        self._batch = value
        self._sprite.batch = value

    def _check_hit(self, x, y):
        xO, yO = self.anchor_offset
        return self._x < x+xO < self._x + self._width and self._y < y+yO < self._y + self._height

    """
    Custom function
    """
    def _rel_resize(self, pp_width, pp_height):
        """
        Relative resize
        Function to resize widget based on parent's changes.

        Properties
        `pp_width`  : Parent Previous Width
        `pp_height` : Parent Previous Height
        """
        new_width  = self.width*self.parent.width/pp_width
        new_height = self.height*self.parent.height/pp_height

        if self.styler.stretch_resolution == True:
            self.width  = new_width if self.styler.stretch_x else self.width
            self.height = new_height if self.styler.stretch_y else self.height
        elif self.styler.fixed_resolution == True:
            self.width, self.height = self.styler.aspect_ratio_size(new_width, new_height)
        
    
    """
    Window Events
    """

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.enabled or not self.visible or not self._check_hit(x,y):
            return
        self.pressed = True
        self._sprite.image = self._pimage

    def on_mouse_release(self, x, y, button, modifiers):
        if not self.enabled or not self.visible or not self.pressed:
            return
        self.pressed = False
        if self._check_hit(x, y): self.dispatch_event("on_click")
        self._sprite.image = self._himage if self._check_hit(x, y) else self._dimage

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.enabled or self.pressed:
            return
        self._sprite.image = self._himage if self._check_hit(x, y) else self._dimage

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if not self.enabled or self.pressed:
            return
        self._sprite.image = self._himage if self._check_hit(x, y) else self._dimage

PushButton.register_event_type("on_click")


class TextButton(PushButton):
    """
    Extension class of PushButton to support text. Can be used as a reference
    to create cusom PushButtons
    """

    def __init__(self, text, x, y, depressed, pressed, hover, anchor_x="left", anchor_y="bottom", group=None, batch=None):

        super().__init__(x, y, depressed, pressed, hover, anchor_x=anchor_x, anchor_y=anchor_y, group=group, batch=batch)
        #Setting up label and group
        self._text_x    = 0 #X positions an be in %
        self._text_y    = 0 #Y positons can be in %

        fgroup = OrderedGroup(1, parent=self._group)
        self._label = pyglet.text.Label(text=text, x=x, y=y, group=fgroup, batch=batch)

    """
    Overwritting Properties
    """

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        xO, yO  = self.anchor_offset
        delta_x = value - self._x

        self._sprite.x = value - xO
        self._label.x += delta_x
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        xO, yO = self.anchor_offset
        delta_y = value - self._y

        self._sprite.y = value - yO
        self._label.y += delta_y
        self._y = value

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._group = OrderedGroup(value, parent=self._group.parent)
        bgroup = OrderedGroup(0, parent=self._group)
        fgroup = OrderedGroup(1, parent=self._group)

        self._label._init_groups(fgroup)
        self._label._update()

        self._sprite.group = bgroup
        self._z = value

    @property
    def group(self):
        return self._group.parent

    @group.setter
    def group(self, value):
        self._group = OrderedGroup(self.z, parent=value)
        bgroup = OrderedGroup(0, parent=self._group)
        fgroup = OrderedGroup(1, parent=self._group)

        self._label._init_groups(fgroup)
        self._label._update()
        self._sprite.group = bgroup

    @property
    def batch(self):
        return self._batch

    @batch.setter
    def batch(self, value):
        self._batch = value
        self._sprite.batch = value
        self._label.batch = value


    """
    Custom function
    """
    def _rel_resize(self, pp_width, pp_height):
        """
        Relative resize
        Function to resize widget based on parent's changes.

        Properties
        `pp_width`  : Parent Previous Width
        `pp_height` : Parent Previous Height
        """
        new_width  = self.width*self.parent.width/pp_width
        new_height = self.height*self.parent.height/pp_height

        if self.styler.stretch_resolution == True:
            self.width  = new_width if self.styler.stretch_x else self.width
            self.height = new_height if self.styler.stretch_y else self.height
        elif self.styler.fixed_resolution == True:
            self.width, self.height = self.styler.aspect_ratio_size(new_width, new_height)
               
        #Refreshing text
        self.text_x = self.text_x
        self.text_y = self.text_y

    """
    Label Setup
    """
    @property
    def text_x(self):
        return self._text_x

    @text_x.setter
    def text_x(self, value):
        self._text_x = value

        if type(value) == str:
            if value.endswith("%"): value = self.width * (int(value[:-1]) / 100)
            else: raise Exception("x value must be a string ending with % or a number")

        xO, yO = self.anchor_offset
        self._label.x = self.x - xO + value

    @property
    def text_y(self):
        return self._text_y

    @text_y.setter
    def text_y(self, value):
        self._text_y = value
        
        if type(value) == str:
            if value.endswith("%"): value = self.height * (int(value[:-1]) / 100)
            else: raise Exception("y value must be a string ending with % or a number")

        xO, yO = self.anchor_offset
        self._label.y = self.y - yO + value

    def style_text(self, **kwargs):
        for var, value in kwargs.items():
            setattr(self._label, var, value)


class IconButton(PushButton):
    """
    Extension class of the PushButton class to display icons onto the button
    """

    def __init__(self, icon, x, y, depressed, pressed, hover, anchor_x="left", anchor_y="bottom", group=None, batch=None):

        super().__init__(x, y, depressed, pressed, hover, anchor_x=anchor_x, anchor_y=anchor_y, group=group, batch=batch)

        class CustomSprite(pyglet.sprite.Sprite):
            """
            Extension class of the pyglet.sprite.Sprite to allow anchoring
            """

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.anchor_x = "left"
                self.anchor_y = "bottom"

            @property
            def x(self):
                return self._x

            @x.setter
            def x(self, value):
                xO, yO = self.anchor_offset

                self._x = value - xO
                self._update_position()

            @property
            def y(self):
                return self._y

            @y.setter
            def y(self, value):
                xO, yO = self.anchor_offset

                self._y = value - yO
                self._update_position()

            @property
            def anchor_offset(self):
                xO = self.width if self.anchor_x == "right" else 0
                yO = self.height if self.anchor_y == "top" else 0

                xO = self.width//2 if self.anchor_x == "center" else xO
                yO = self.height//2 if self.anchor_y == "center" else yO

                return xO, yO

        #Exclusive Properties
        self._icon = icon
        fgroup = OrderedGroup(1, parent=self._group)
        self._isprite = CustomSprite(
            icon,
            x,
            y,
            group=fgroup,
            batch=self._batch
        )

        self._icon_x = 0
        self._icon_y = 0


    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        iX, iY = self._isprite.anchor_offset
        xO, yO  = self.anchor_offset
        delta_x = value - self._x

        self._sprite.x = value - xO
        self._isprite.x += delta_x + iX
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        iX, iY = self._isprite.anchor_offset
        xO, yO = self.anchor_offset
        delta_y = value - self._y

        self._sprite.y = value - yO
        self._isprite.y += delta_y + iY
        self._y = value       

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._group = OrderedGroup(value, parent=self._group.parent)
        bgroup = OrderedGroup(0, parent=self._group)
        fgroup = OrderedGroup(1, parent=self._group)

        self._sprite.group = bgroup
        self._isprite.group = fgroup
        self._z = value

    @property
    def group(self):
        return self._group.parent

    @group.setter
    def group(self, value):
        self._group = OrderedGroup(self.z, parent=value)
        bgroup = OrderedGroup(0, parent=self._group)
        fgroup = OrderedGroup(1, parent=self._group)

        self._sprite.group = bgroup
        self._isprite.group = fgroup

    @property
    def batch(self):
        return self._batch

    @batch.setter
    def batch(self, value):
        self._batch = value
        self._sprite.batch = value
        self._isprite.batch = value
    """
    Custom function
    """
    def _rel_resize(self, pp_width, pp_height):
        """
        Relative resize
        Function to resize widget based on parent's changes.

        Properties
        `pp_width`  : Parent Previous Width
        `pp_height` : Parent Previous Height
        """
        new_width  = self.width*self.parent.width/pp_width
        new_height = self.height*self.parent.height/pp_height

        if self.styler.stretch_resolution == True:
            self.width  = new_width if self.styler.stretch_x else self.width
            self.height = new_height if self.styler.stretch_y else self.height
        elif self.styler.fixed_resolution == True:
            self.width, self.height = self.styler.aspect_ratio_size(new_width, new_height)
               
        #Refreshing Icon
        self.icon_x = self.icon_x
        self.icon_y = self.icon_y
    """
    Icon setup
    """
    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value
        self._isprite.image = value

    @property
    def icon_x(self):
        return self._icon_x

    @icon_x.setter
    def icon_x(self, value):
        self._icon_x = value

        if type(value) == str:
            if value.endswith("%"): value = self.width * (int(value[:-1]) / 100)
            else: raise Exception("x value must be a string ending with % or a number")

        xO, yO = self.anchor_offset
        self._isprite.x = self.x - xO + value

    @property
    def icon_y(self):
        return self._icon_y

    @icon_y.setter
    def icon_y(self, value):
        self._icon_y = value
        
        if type(value) == str:
            if value.endswith("%"): value = self.height * (int(value[:-1]) / 100)
            else: raise Exception("y value must be a string ending with % or a number")

        xO, yO = self.anchor_offset
        self._isprite.y = self.y - yO + value



    def style_icon(self, **kwargs):
        for var, value in kwargs.items():
            setattr(self._isprite, var, value)


