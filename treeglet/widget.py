import pyglet
from pyglet.graphics import OrderedGroup, Batch

class WidgetStyler:
    """
    Style class to give some swagger to your widgets
    """

    target = None

    #Position arguments
    sticky_x    = True
    sticky_y    = True

    #Resolutions
    _fixed_resolution   = False
    _stretch_resolution = False

    #Resolution arguments
    stretch_x   = False
    stretch_y   = False


    """
    Position Modifiers
    """
    @property
    def sticky(self):
        return True if self.sticky_x and self.sticky_y else False

    @sticky.setter
    def sticky(self, value):
        self.sticky_x = value
        self.sticky_y = value

    """
    Resolution
    """
    @property
    def aspect_ratio(self):
        from fractions import Fraction
        eq = Fraction(self.target.width/self.target.height).limit_denominator()

        return eq.numerator, eq.denominator

    def aspect_ratio_size(self, size_x, size_y):
        """
        Setting up aspect ratio
        """

        aspect_x, aspect_y = self.aspect_ratio
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
        self.stretch_x = value
        self.stretch_y = value

        self._stretch_resolution = value
        self._fixed_resolution = not value if value==True else self._fixed_resolution

    @property
    def fixed_resolution(self):
        return self._fixed_resolution

    @fixed_resolution.setter
    def fixed_resolution(self, value):
        self._fixed_resolution = value
        self._stretch_resolution = not value if value==True else self._stretch_resolution



class WidgetBase(pyglet.gui.WidgetBase):
    """
    An extenstion to the `pyglet.gui.widget.WidgetBase` class to fit
    the features of treeglet
    """

    def __init__(self, x, y, width, height, anchor_x="left", anchor_y="bottom"):
        super().__init__(x, y, width, height)

        self._parent    = None
        self._visible   = True
        self._z     = 0 #Z index of widget

        self.styler = WidgetStyler()
        self.styler.target = self

        #Alignement
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y

        #Offset
        self._offset_x = 0
        self._offset_y = 0


    @property
    def bottom_left(self):
        xO, yO = self.anchor_offset

        return self._x - xO, self._y - yO

    @property
    def center(self):
        xO, yO = self.anchor_offset

        return self._x - xO+self._width//2, self._y - yO+self._height//2
    
    @property
    def top_left(self):
        xO, yO = self.anchor_offset

        return self._x - xO+self._width, self._y - yO+self._height


    @property
    def anchor_offset(self):
        x = 0 if self.anchor_x=='left' else self._width
        y = 0 if self.anchor_y=='bottom' else self._height

        x = self._width//2 if self.anchor_x=='center' else x
        y = self._height//2 if self.anchor_y=='center' else y
        return x, y

    def style(self, **kwargs):
        for var, value in kwargs.items():
            setattr(self.styler, var, value)


