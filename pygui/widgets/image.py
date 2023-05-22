import pyglet as pg
from pyglet.graphics import Group
from ..widget import Widget

class Image(Widget):

    def __init__(self,
                 image,
                 x=0,
                 y=0,
                 z=0,
                 anchor_x='left',
                 anchor_y='bottom',):

        super(Image, self).__init__(x, y, z, image.width, image.height, anchor_x, anchor_y,)

        self._sprite = pg.sprite.Sprite(image, x, y, group=self.group)
        self.resize_image = False


    """
    Overwritting methods
    """
    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height
        
    @width.setter
    def width(self, value):
        scale_x = value/self._width
        self._sprite.scale_x *= scale_x
        self._width = value

    @height.setter
    def height(self, value):
        scale_y = value/self._height
        self._sprite.scale_y *= scale_y
        self._height = value

    def _update_position(self):
        self._sprite.x = self.x + self.__anchor_x_offset__()
        self._sprite.y = self.y + self.__anchor_y_offset__()

    def set_group(self, value):
        self._group = Group(self.z, parent=value)
        self.group.visible = self.visible
        self._sprite.group = self.group

    def set_batch(self, value):
        self._batch = value
        self._sprite.batch = value or self._sprite.batch #In case no batch exists

    def __repr__(self):
        return 'Image(id={})'.format(self.id)

    @property
    def image(self):
        return self._sprite.image

    @image.setter
    def image(self, value):
        if self.resize_image:
            width, height               = self._width, self._height
            self._width, self._height   = value.width, value.height
            self._sprite.scale_x        = 1
            self._sprite.scale_y        = 1
            self._sprite.image          = value
            self.width, self.height     = value
        else:
            self._sprite.image          = value
            self._width                 = self._sprite.width
            self._height                = self._sprite.height

        self.dispatch_event('on_image_change', value)

Image.register_event_type('on_image_change')
