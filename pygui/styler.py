from .tags import*

class Styler:
    def __init__(self, target):
        self.target = target

        self.x_scale_percent = 1
        self.y_scale_percent = 1
        
        self._x_scale_type = STYLER_SCALETYPE_NONE
        self._y_scale_type = STYLER_SCALETYPE_NONE

        self.x_position_type = STYLER_POSITIONTYPE_NONE
        self.y_position_type = STYLER_POSITIONTYPE_NONE

    @property
    def x_scale_type(self):
        return self._x_scale_type

    @property
    def y_scale_type(self):
        return self._y_scale_type

    @x_scale_type.setter
    def x_scale_type(self, value):
        self._y_scale_type = value if value==STYLER_SCALETYPE_FIXED or value!=STYLER_SCALETYPE_FIXED==self._y_scale_type else self._y_scale_type
        self._x_scale_type = value

    @y_scale_type.setter
    def y_scale_type(self, value):
        self._x_scale_type = value if value==STYLER_SCALETYPE_FIXED or value != STYLER_SCALETYPE_FIXED==self._x_scale_type else self._x_scale_type
        self._y_scale_type = value

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

        self.target.width  += delta_x * self.x_scale_percent if self._x_scale_type == STYLER_SCALETYPE_INCREMENT else 0
        self.target.height += delta_y * self.y_scale_percent if self._y_scale_type == STYLER_SCALETYPE_INCREMENT else 0

        self.target.width  = self.target.width * new_width / pre_width if self.x_scale_type == STYLER_SCALETYPE_FIXED else self.target.width
        self.target.height = self.target.height * new_height / pre_height if self.y_scale_type == STYLER_SCALETYPE_FIXED else self.target.height


        
    def update_position(self, pre_width, pre_height, new_width, new_height):
        """
        Repositioning the widget
        """
        #Updating X position
        if self.x_position_type == STYLER_POSITIONTYPE_FIXED:
            x_ratio = new_width/pre_width
            self.target.x *= x_ratio
        elif self.x_position_type == STYLER_POSITIONTYPE_INCREMENT:
            delta_x = new_width - pre_width
            self.target.x += delta_x


        #Updating Y position
        if self.y_position_type == STYLER_POSITIONTYPE_FIXED:
            y_ratio = new_height/pre_height
            self.target.y *= y_ratio
        elif self.y_position_type == STYLER_POSITIONTYPE_INCREMENT:
            delta_y = new_height - pre_height
            self.target.y += delta_y


        #Refreshing positions if set to none
        if self.y_position_type == STYLER_POSITIONTYPE_NONE:
            self.target.y = self.target.y 

        if self.x_position_type == STYLER_POSITIONTYPE_NONE:
            self.target.x = self.target.x

