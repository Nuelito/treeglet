import pyglet
from .widgets import WidgetBase, Behaviour
from .graphics import ScissorGroup, ScrollingGroup


class Frame(WidgetBase):
    def __init__(self, window, x, y, width, height, group=None, batch=None):
        WidgetBase.__init__(self, x, y, width, height)
        window.push_handlers(self)
        self._window = window
        self.behaviour = Behaviour(self, window)

        self._children = set()
        self._root = pyglet.graphics.Group(parent=group)
        self._group = ScissorGroup(x, y, width, height, order=1, parent=self._root)
        self._omx, self._omy = 0, 0 #Offset Mouse XY
        self.batch = batch or pyglet.graphics.Batch()

        bg_group = pyglet.graphics.Group(order=0, parent=self._root)
        self.background = pyglet.shapes.Rectangle(x, y, width, height, color=(50,50,50,235), group=bg_group, batch=batch)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, value):
        self._x = value
        self._group.x = value
        self.background.x = value

    @y.setter
    def y(self, value):
        self._y = value
        self._group.y = value
        self.background.y = value

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @width.setter
    def width(self, value):
        self._width = value
        self._group.width = value
        self.background.width = value

    @height.setter
    def height(self, value):
        self._height = value
        self._group.height = value
        self.background.height = value

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
        self._visible = value
        self._group.visible = value
        self.background._group.visible = value

    def set_group(self, group):
        self._root = pyglet.graphics.Group(order=self.z_index, parent=group)
        self._group = ScissorGroup(self.x, self.y, self.width, self.height, order=1, 
                                   parent=self._root)
        bg_group = pyglet.graphics.Group(order=0, parent=self._root)
        self.background = pyglet.shapes.Rectangle(self.x, self.y, self.width, self.height, 
                                                  color=(*self.background.color, 
                                                         self.background.opacity), 
                                                  group=bg_group, batch=self.batch)
        for child in self._children: 
            print(child)
            child.set_group(self._group)

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

    def on_mouse_press(self, x, y, button, modifiers):

        if not self._check_hit(x, y) or not self.visible: return
        x += self._omx
        y += self._omy


        for widget in self._children:
            if not widget._check_hit(x, y): continue
            if not self.mouse:
                widget.on_mouse_press(x, y, button, modifiers)
                continue
            if not self.mouse: break

            if not self.mouse.pwidget:
                self.mouse.pwidget = widget
                continue
            else:
                if widget == self.mouse.pwidget: continue
                index1 = self.mouse.pwidget.z_index
                index2 = widget.z_index

                if index2 > index1:
                    self.mouse.pwidget = widget
                    continue


        if not self.mouse: return
        if not self.mouse.pwidget: return
        if self.mouse.pwidget not in self._children: return

        if not self.mouse.pwidget._check_hit(x,y):
            y = self.mouse.pwidget.y + self.mouse.pwidget.height+10

        self.mouse.pwidget.on_mouse_press(x, y, button, modifiers)

    def set_group(self, group):
        self._root = pyglet.graphics.Group(order=self.z_index, parent=group)
        self._group = ScissorGroup(self.x, self.y, self.width, self.height, order=1, 
                                   parent=self._root)
        bg_group = pyglet.graphics.Group(order=0, parent=self._root)
        self.background = pyglet.shapes.Rectangle(self.x, self.y, self.width, self.height, 
                                                  color=(*self.background.color, 
                                                         self.background.opacity), 
                                                  group=bg_group, batch=self.batch)
        for child in self._children: child.set_group(self._group)

    def on_mouse_release(self, x, y, button, modifiers):
        #if not self._check_hit(x, y): return
        if self.mouse: self.mouse.pwidget = None

        for widget in self._children:
            widget.on_mouse_release(x+self._omx, y+self._omy, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        #if not self._check_hit(x, y): return
        x += self._omx
        y += self._omy

        for widget in self._children:

            if not self.mouse: 
                widget.on_mouse_motion(x, y, dx, dy)
                continue
            if not self.mouse: return
   
            if not self.mouse.hwidget: 
                self.mouse.hwidget = widget if widget._check_hit(x, y) else self.mouse.hwidget
                continue
            else:                
                if widget == self.mouse.hwidget: continue
                if not widget._check_hit(x, y): continue
                index1 = self.mouse.hwidget.z_index
                index2 = widget.z_index

                if self.mouse.hwidget.parent != widget.parent:
                    if self.mouse.hwidget.parent: index1 = self.mouse.hwidget.parent.z_index
                    if widget.parent: index2 = widget.parent.z_index


                if index2 > index1:
                    self.mouse.hwidget.on_mouse_motion(
                        self.mouse.hwidget.x,
                        self.mouse.hwidget.y+self.mouse.hwidget.height+10,
                        dx,
                        dy
                    )
                    self.mouse.hwidget = widget
                    continue

        if not self.mouse: return
        if not self.mouse.hwidget: return
        if self.mouse.hwidget not in self._children: return

        hitting = True

        if not self.mouse.hwidget._check_hit(x, y) or not self._check_hit(x-self._omx,y-self._omy):
            y = self.mouse.hwidget.y+self.mouse.hwidget.height+10
            hitting = False

        self.mouse.hwidget.on_mouse_motion(x, y, dx, dy)
        if hitting == False: self.mouse.hwidget = None

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        #if not self._check_hit(x, y): return
        if not self.visible: return        
        x += self._omx
        y += self._omy

        for widget in self._children:
            if not self.mouse:
                widget.on_mouse_drag(x, y, dx, dy, button, modifiers)
                continue
            if not self.mouse: return
            if not self.mouse.dwidget:
                self.mouse.dwidget = widget if widget._check_hit(x, y) else self.mouse.dwidget
                continue
            else:
                if self.mouse.dwidget == widget: continue
                if not widget._check_hit(x, y): continue
                index1 = self.mouse.dwidget.z_index
                index2 = widget.z_index

                if self.mouse.dwidget.parent != widget.parent:
                    index1 = self.mouse.dwidget.parent.z_index
                    index2 = widget.parent.z_index

                if index2 > index1:
                    self.mouse.dwidget.on_mouse_drag(
                        self.mouse.dwidget.x,
                        self.mouse.dwidget.y+self.mouse.dwidget.height+10,
                        dx,
                        dy,
                        button, modifiers
                    )
                    self.mouse.dwidget = widget
                    continue

        if not self.mouse: return
        if not self.mouse.dwidget: return
        if self.mouse.dwidget not in self._children: return

        hitting = True

        if not self.mouse.dwidget._check_hit(x,y) or not self._check_hit(x-self._omx,y-self._omy): 
            hitting = False
            y = self.mouse.dwidget.y+self.mouse.dwidget.height+10


        self.mouse.dwidget.on_mouse_drag(x, y, dx, dy, button, modifiers)
        if hitting == False: self.mouse.dwidget = None

    def on_resize(self, width, height):
        if not self.behaviour: return
        self.behaviour.on_resize(width, height)
        """
        dx, dy = width/self.win_width, height/self.win_height
        self.x *= dx
        self.y *= dy
        self.width *=dx
        self.height*=dy
        
        self.win_width, self.win_height = width, height
        """
    def add_widget(self, widget):
        if widget in self._children:
            return

        widget.z_index = len(self._children)
        widget.parent = self
        self._children.add(widget)
        widget.set_group(self._group)
        widget.parent = self

    def add_frame(self, frame):
        """
        Will be worked on in the future as it is not ready yet for
        frames under frames
        """
        pass

    def draw(self):
        if not self.visible: return
        self.batch.draw()

class ScrollFrame(Frame):
    _scroll_x = 0
    _scroll_y = 0

    def __init__(self, window, x, y, width, height, group=None, batch=None):
        super().__init__(window, x, y, width, height, group, batch)
        self._group = ScrollingGroup(x, y, width, height, parent=self._root)
        self._group.window = window

    def set_group(self, group):
        self._root = pyglet.graphics.Group(order=self.z_index, parent=group)
        self._group = ScrollingGroup(self.x, self.y, self.width, self.height, order=1, 
                                   parent=self._root)
        self._group.window = self._window
        bg_group = pyglet.graphics.Group(order=0, parent=self._root)
        self.background = pyglet.shapes.Rectangle(self.x, self.y, self.width, self.height, 
                                                  color=(*self.background.color, 
                                                         self.background.opacity), 
                                                  group=bg_group, batch=self.batch)
        for child in self._children: child.set_group(self._group)

    @property
    def scroll_y(self): return self._scroll_y

    @scroll_y.setter
    def scroll_y(self, value):
        self._scroll_y = value
        self._group.scroll_y = value
        self._omy = -self.scroll_y

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if not self._check_hit(x, y): return
        self.scroll_y -= scroll_y*10

