import pyglet

class MouseHandler:
    """
    MouseHandler class made in order for selecting widgets by z-index.
    This prevents clicking two buttons at the same time
    """

    def __init__(self):
        self.x  = 0
        self.y  = 0

        #Pressed Coordinations
        self.px = 0
        self.py = 0

        self.pwidget = None #Pressed widget
        self.hwidget = None #Hovered Widget
        self.dwidget = None #Dragged Widget

    def on_mouse_press(self, x, y, button, modifiers):
        self.x  = x
        self.y  = y
        self.px = x
        self.py = y

    def on_mouse_release(self, x, y, button, modifiers):
        self.x  = x
        self.y  = y

    def on_mouse_motion(self, x, y, dx, dy):
        self.x  = x
        self.y  = y

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        self.x  = x
        self.y  = y
