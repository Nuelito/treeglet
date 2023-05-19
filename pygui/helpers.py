class Rectangle:
    """
    This class is used to ease construction of other class such
    as ScissorGroup
    """
    def __init__(self, x=None, y=None, width=None, height=None):

        self.x = x
        self.y = y

        self.width  = width
        self.height = height

    @property
    def left(self):
        return self.x

    @property
    def bottom(self):
        return self.y

    @property
    def right(self):
        return self.x + self.width

    @property
    def top(self):
        return self.y + self.height

    @left.setter
    def left(self, value):
        self.x = value

    @bottom.setter
    def bottom(self, value):
        self.y = value

    @right.setter
    def right(self, value):
        self.width = value - self.x
        
    def __repr__(self):
        return f"Rectangle(x={self.x}, y={self.y}, width={self.width}, height={self.height})"

    @top.setter
    def top(self, value):
        self.height = value - self.y
        
    def __eq__(self, other):
        return (self.__class__ is other.__class__ and
                self.x == other.x and
                self.y == other.y and
                self.width == other.width and
                self.height == other.height)
                
    def __hash__(self):
        return id(self)
