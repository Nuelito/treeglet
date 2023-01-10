import pyglet

class MouseHandler:
    def __init__(self):
        """
        A class meant to handle widget interactions. Instances of it's
        abilities is preventing clicking two buttons at the same time.
        """

        #Current position
        self.x      = 0
        self.y      = 0

        #Press position
        self.px     = 0
        self.py     = 0

        #Target widgets
        self.pwidget = None
        self.hwidget = None
        self.dwidget = None

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
