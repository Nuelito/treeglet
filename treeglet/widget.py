import pyglet

class WidgetStyle:
    """
    Class made to style widget using different `properties`
        Anchor : Property to allow anchor position


    """
    target = None

    #Position modifiers
    _sticky_x   = True
    _sticky_y   = True
    _sticky     = True


    #Fixed Resolution whatchamacalits
    _fixed_resolution  = False

    #Stretch Resolution whatchamacalits
    _stretch_resolution = False
    stretch_x   = True
    stretch_y   = True
    
    """
    Position modifiers
    """

    @property
    def sticky_x(self):
        return self._sticky_x

    @sticky_x.setter
    def sticky_x(self, value):
        self._sticky_x = value

    @property
    def sticky_y(self):
        return self._sticky_y

    @sticky_y.setter
    def sticky_y(self, value):
        self._sticky_y = value

    @property
    def sticky(self):
        if sticky_x == sticky_y and sticky_x == True:
            return True
        return False

    @sticky.setter
    def sticky(self, value):
        self._sticky    = value
        self._sticky_x  = value
        self._sticky_y  = value

    """
    Fixed resolution manipulation
    """

    def get_aspect_ratio(self):
        from fractions import Fraction
        eq = Fraction(self.target.width/self.target.height).limit_denominator()

        x = eq.numerator
        y = eq.denominator

        return x, y

    def aspect_ratio_size(self, size_x, size_y):
        """
        Setting up aspect ratio
        """

        aspect_x, aspect_y = self.get_aspect_ratio()
        widget  = self.target.parent

        width   = self.target.width
        height  = self.target.height
        

        if aspect_x < aspect_y:
            width   = size_x
            height  = size_x*aspect_y/aspect_x

        else:
            height  = size_y
            width   = size_y*aspect_x/aspect_y

        
        return width, height

    """
    Size modifiers
    """

    @property
    def stretch_resolution(self):
        return self._stretch_resolution

    @stretch_resolution.setter
    def stretch_resolution(self, value):
        self._stretch_resolution = value
        self._fixed_resolution = not value if value == True else self._fixed_resolution

    @property
    def fixed_resolution(self):
        return self._fixed_resolution

    @fixed_resolution.setter
    def fixed_resolution(self, value):
        self._fixed_resolution = value
        self._stretch_resolution = not value if value == True else self._stretch_resolution




class WidgetBase(pyglet.gui.WidgetBase):
    """
    An extension of the widget class that will be the base for
    this module
    """

    def __init__(self, x, y, width, height, order=0, anchor_x="left", anchor_y="bottom"):
        pyglet.gui.WidgetBase.__init__(self, x, y, width, height)

        self._id = "Widget" #Useless variable, for tesing purpose

        self._parent    = None
        self._order     = order
        self.visible    = True

        self.styler = WidgetStyle()
        self.styler.target = self
        self.mouse_handler = None

        #Alignement
        self._anchor_x = anchor_x
        self._anchor_y = anchor_y

    """
    General properties
    """
    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, value):
        self._order = value

    @property
    def anchor_x(self):
        return self._anchor_x

    @property
    def anchor_y(self):
        return self._anchor_y

    """
    Position properties
    """
    @property
    def center(self):
        x_offset, y_offset = self.get_offset()

        return self.x - x_offset + self.width//2, self.y - y_offset + self.height//2


    @property
    def bottom_left(self):
        x_offset, y_offset = self.get_offset()

        return self.x - x_offset,  self.y - y_offset

    @property
    def top_right(self):
        x_offset, y_offset = self.get_offset()
        
        return self.x + x_offset, self.y + y_offset

    def get_offset(self):
        x = self.anchor_x
        y = self.anchor_y

        if      x == "left": x = 0
        elif    x == "right": x = self.width
        elif    x == "center": x = self.width//2

        if      y == "bottom": y = 0
        elif    y == "top": y = self.height
        elif    y == "center": y = self.height//2

        return x, y

    """
    Modified functions
    """
    def _check_hit(self, x, y):
        xo, yo = self.get_offset()
        return self._x < x+xo < self._x + self._width and self._y < y+yo < self._y+self._height


    def style(self, **kwargs):
        for var, value in kwargs.items():
            setattr(self.styler, var, value)


class PushButton(WidgetBase):
    def __init__(self, x, y, depressed, pressed, hover, anchor_x="left", anchor_y="bottom", 
                 order=0, group=None, batch=None):
        
        WidgetBase.__init__(self, x, y, depressed.width, depressed.height, anchor_x=anchor_x,
                            anchor_y=anchor_y, order=order)

        #Graphic variables
        self._batch = batch or pyglet.graphics.Batch()
        self._group = pyglet.graphics.Group(order, parent=group)
        bg_group    = pyglet.graphics.Group(0, parent=self._group)

        #Storing Images and initialising sprite
        self._himage = hover
        self._pimage = pressed
        self._dimage = depressed

        self._sprite = pyglet.sprite.Sprite(
            depressed,
            x,
            y,
            group=bg_group,
            batch=self._batch
        )

        #Specific variables
        self.pressed = False

    """
    Properties
    """
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        xOffset, yOffset = self.get_offset()

        self._x = value
        self._sprite.x = value - xOffset

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        xOffset, yOffset = self.get_offset()

        self._y = value
        self._sprite.y = value - yOffset

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        """
        Resizing image sprite x
        """

        scale_x = value/self._width
        self._width = value
        self._sprite.scale_x *= scale_x

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        """
        Resizing image sprite y
        """

        scale_y = value/self._height
        self._height = value
        self._sprite.scale_y *= scale_y

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, value):
        self._group = pyglet.graphics.Group(value, parent=self._group.parent)
        bg_group    = pyglet.graphics.Group(0, parent=self._group)
        self._sprite.group = bg_group
        self._order = value

    @property
    def group(self):
        """
        The group to which the widget belongs to
        """
        return self._group.parent

    @group.setter
    def group(self, group):
        """
        Setter to change the parent group of the widget
        """

        if self._group.parent == group:
            return
        
        self._group = pyglet.graphics.Group(self.order, parent=group)
        bg_group    = pyglet.graphics.Group(0, parent=self._group)
        self._sprite.group = bg_group

    @property
    def batch(self):
        return self._batch

    @batch.setter
    def batch(self, batch):
        if self._batch == batch:
            return

        self._batch = batch
        self._sprite.batch = batch
        
    """
    Special Functions
    """
    def draw(self):
        self._batch.draw()

    """
    Window events (widget stuff)
    """
    def frame_resized(self, oldx, oldy, owidth, oheight):
        """
        Function to reposition and resize widgets under frames
        """
        if not self.styler.fixed_resolution or not self.styler.stretch_resolution: return
        parent = self.parent
        new_width  = self.width*parent.width/owidth
        new_height = self.height*parent.height/oheight
        
        self.width = new_width
        self.height= new_height


    """
    Window events (mouse interactions)
    """
    def on_mouse_press(self, x, y, button, modifiers):
        if not self._check_hit(x, y) or not self.enabled:
            return
        
        self.pressed = True
        self._sprite.image = self._pimage

    def on_mouse_release(self, x, y, button, modifiers):
        if not self.enabled or not self.pressed:
            return

        self.pressed = False
        self._sprite.image = self._himage if self._check_hit(x, y) else self._dimage

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.enabled or self.pressed:
            return
        self._sprite.image = self._himage if self._check_hit(x, y) else self._dimage

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if not self.enabled or self.pressed:
            return
        self._sprite.image = self._himage if self._check_hit(x, y) else self._dimage

