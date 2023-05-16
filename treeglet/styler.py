#Tags
from treeglet.tags import*

class Styler:
    """
    Modifier class to update position and sizes of widgets when
    the window is resized
    """

    _x_scale_type = STYLER_SCALETYPE_NONE
    _y_scale_type = STYLER_SCALETYPE_NONE

    x_position_type = STYLER_POSITIONTYPE_NONE
    y_position_type = STYLER_POSITIONTYPE_NONE

    _target = None #The widget on which changes are applied

    #How much percent you want the widget to increase with the window
    scale_x_percent = 1
    scale_y_percent = 1

    @property
    def x_scale_type(self):
        return self._x_scale_type

    @property
    def y_scale_type(self):
        return self._y_scale_type

    @x_scale_type.setter
    def x_scale_type(self, value):
        if value == STYLER_SCALETYPE_FIXED:
            self._y_scale_type = value
        if value != STYLER_SCALETYPE_FIXED and self._y_scale_type == STYLER_SCALETYPE_FIXED:
            self._y_scale_type = value
        self._x_scale_type = value

    @y_scale_type.setter
    def y_scale_type(self, value):
        if value == STYLER_SCALETYPE_FIXED:
            self._x_scale_type = value
        if value != STYLER_SCALETYPE_FIXED and self._x_scale_type == STYLER_SCALETYPE_FIXED:
            self._x_scale_type = value

        self._y_scale_type = value

    def copy(self, widget):
        """
        Copying the style of another styler to this
        styler.
        """

        styler = widget.styler

        self.x_scale_type = styler.x_scale_type
        self.y_scale_type = styler.y_scale_type

        self.x_position_type = styler.x_position_type
        self.y_position_type = styler.y_position_type

    def set_position_type(self, STYLER_TAG):
        self.x_position_type = STYLER_TAG
        self.y_position_type = STYLER_TAG

    def set_scale_type(self, STYLER_TAG):
        self.x_scale_type = STYLER_TAG
        self.y_scale_type = STYLER_TAG

    def update_size(self, pre_width, pre_height, new_width, new_height):
        """
        Scaling the widget
        """
        delta_x = new_width - pre_width
        delta_y = new_height - pre_height

        if self.x_scale_type == STYLER_SCALETYPE_INCREMENT:
            self._target.width += delta_x * self.scale_x_percent

        if self.y_scale_type == STYLER_SCALETYPE_INCREMENT:
            self._target.height += delta_y * self.scale_y_percent
        

        #Scaling with fixed resolution
        if self.x_scale_type == STYLER_SCALETYPE_FIXED:
            twidth  = self._target.width * new_width / pre_width
            theight = self._target.height* new_width/ pre_width

            self._target.width = twidth
            self._target.height = theight
        
    def update_position(self, pre_width, pre_height, new_width, new_height):
        """
        Repositioning the widget
        """
        #Updating X position
        if self.x_position_type == STYLER_POSITIONTYPE_FIXED:
            x_ratio = new_width/pre_width
            self._target.x *= x_ratio
        elif self.x_position_type == STYLER_POSITIONTYPE_INCREMENT:
            delta_x = new_width - pre_width
            self._target.x += delta_x

        #Updating Y position
        if self.y_position_type == STYLER_POSITIONTYPE_FIXED:
            y_ratio = new_height/pre_height
            self._target.y *= y_ratio
        elif self.y_position_type == STYLER_POSITIONTYPE_INCREMENT:
            delta_y = new_height - pre_height
            self._target.y += delta_y


        #Refreshing positions if set to none
        if self.y_position_type == STYLER_POSITIONTYPE_NONE:
            self._target.y = self._target.y 

        if self.x_position_type == STYLER_POSITIONTYPE_NONE:
            self._target.x = self._target.x

