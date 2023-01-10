import pyglet
from treeglet.widget import WidgetBase
from treeglet.graphics import ScissorGroup

class Frame(WidgetBase):
    def __init__(self, window, x, y, width, height, anchor_x="left", anchor_y="bottom", 
                 order=0, group=None, batch=None):
        WidgetBase.__init__(self, x, y, width, height, anchor_x=anchor_x, anchor_y=anchor_y)
        #window.push_handlers(self)

        self.wwidth, self.wheight = window.width, window.height
        self.parent = window
        self.window = window
        self.batch = batch

        #Creating groups
        xOffset, yOffset = self.get_offset()

        self._group  = group
        self._rgroup = pyglet.graphics.Group(order=order, parent=group)
        self._fgroup = ScissorGroup(
                x - xOffset, 
                y - yOffset, 
                width, 
                height, 
                order=1,
                window=window,
                parent=self._rgroup
        )
        self.bgroup = pyglet.graphics.Group(order=0, parent=self._rgroup)

        #Specific Variables
        self.widgets = set()

        #Temporary
        self.background = pyglet.shapes.Rectangle(x, y, width, height, group=self.bgroup,
                                                  batch=batch)
        self.background.opacity = 50

    """
    Frame properties
    """
    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        if value == None:
            self._parent = self.window
        else:
            self._parent = value
        self.wwidth  = value.width
        self.wheight = value.height

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        xOffset, yOffset = self.get_offset() #Alignement offset

        self._x = value
        self._fgroup.x = value - xOffset
        self.background.x = self.x - xOffset

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        xOffset, yOffset = self.get_offset() #Alignement offset

        self._y = value
        self._fgroup.y = value - yOffset
        self.background.y = self.y - yOffset

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        self.background.width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        self.background.height = value

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, value):
        """
        Changing the core groups and every widgets to display properly in
        the window.
        """

        xOffset, yOffset = self.get_offset()
        self._rgroup = pyglet.graphics.Group(order=value, parent=self._group)
        self._fgroup = ScissorGroup(
                self.x - xOffset, 
                self.y - yOffset, 
                self.width, 
                self.height, 
                order=1, 
                window=window,
                parent=self._rgroup
        )
        visible_bg = self.bgroup.visible
        self.bgroup = pyglet.graphics.Group(order=0, parent=self._rgroup)
        self.bgroup.visible = visible_bg
        self.background.group = self.bgroup
        self._order = value

        for widget in self.widgets: widget.group = self._fgroup

    @property
    def group(self):
        return self._root.parent

    @group.setter
    def group(self, value):
        self._group = value
        self.order = self._order

    """
    Background properties
    """
    @property
    def visible_bg(self):
        return self.bgroup.visible

    @visible_bg.setter
    def visible_bg(self, value):
        self.bgroup.visible = value

    """
    Special Functions
    """
    def add_widget(self, widget, x=None, y=None):
        widget.parent = self
        widget.batch  = self.batch
        widget.group  = self._fgroup

        #Repositioning widget if needed
        xOffset, yOffset = self.get_offset()
        x = widget.x if x == None else self.x - xOffset + x
        y = widget.y if y == None else self.y - yOffset + y
        widget.x = x
        widget.y = y

        self.widgets.add(widget)

    def remove(self, widget):
        pass

    def update_group(self):
        xOffset, yOffset    = self.get_offset()

        self._fgroup.x      = self.x - xOffset
        self._fgroup.y      = self.y - yOffset
        self._fgroup.width  = self.width
        self._fgroup.height = self.height


    """
    Events Sections
    """

    def on_mouse_press(self, x, y, button, modifiers):
        for widget in self.widgets:
            widget.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        for widget in self.widgets:
            widget.on_mouse_release(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        for widget in self.widgets:
            widget.on_mouse_motion(x, y, dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        for widget in self.widgets:
            widget.on_mouse_drag(x, y, dx, dy, button, modifiers)

    def on_resize(self, width, height):
        """
        Updating the frame and the rest of it's descendants
        """

        FB_x, FB_y = self.bottom_left
        FT_x, FT_y = self.top_right
        FC_x, FC_y = self.center

        old_x       = self.x
        old_y       = self.y

        old_width   = self.width
        old_height  = self.height
        
        new_width   = self.width *(width/self.wwidth)
        new_height  = self.height*(height/self.wheight)


        if self.styler.stretch_resolution == True:
            """
            Stretch resolution setup
            """
            self.width   = new_width if self.styler.stretch_x else old_width
            self.height  = new_height if self.styler.stretch_y else old_height

        elif self.styler.fixed_resolution == True:
            self.width, self.height = self.styler.aspect_ratio_size(new_width, new_height)
            #self.width, self.height = self.styler.aspect_ratio_size(self.wwidth, self.wheight)

        self.x      = old_x*width/self.wwidth if self.styler.sticky_x else old_x
        self.y      = old_y*height/self.wheight if self.styler.sticky_y else old_y
        
        for widget in self.widgets: 
            """
            Adjusting widgets with dot product innit?
            """

            dx = widget.x - old_x
            dy = widget.y - old_y
            #dx = (widget.x - old_x) - (widget.x - self.x)
            #dy = (widget.y - old_y) - (widget.y - self.y)
            #anchor_x, anchor_y = self.get_offset()
            #wanchor_x, wanchor_y = widget.get_offset()

            #Fx, Fy  = old_x - anchor_x, old_y - anchor_y
            #wx, wy = widget.x - wanchor_x, widget.y - wanchor_y


            """
            When resized there is a new x and y coordinations call the frame resized
            coordinations in order to resize if needed
            """
            
            #Widget Old width and height
            wo_width  = widget.width
            wo_height = widget.height

            #The most beautiful code you've ever seen

            positions = [
                [widget.x - FB_x, widget.y - FB_y],
                [widget.x - FC_x, widget.y - FC_y],
                [widget.x - FT_x, widget.y - FT_y],
            ]

            widget.frame_resized(
                old_x,
                old_y,
                old_width,
                old_height
            )         
            #widget.x = widget.x+dx if widget.styler.sticky_x else widget.x
            #widget.y = widget.y+dy if widget.styler.sticky_y else widget.y

            dw = widget.width - wo_width
            dh = widget.height - wo_height

            widget.x = self.x+dx*self.width/old_width if widget.styler.sticky_x else widget.x
            widget.y = self.y+dy*self.height/old_height if widget.styler.sticky_y else widget.y

            nFB_x, nFB_y = self.bottom_left
            nFC_x, nFC_y = self.center
            nFT_x, nFT_y = self.top_right #NFT???


            #Alignement if not resizing
            if dw == 0 and widget.styler.sticky_x:
                if widget.anchor_x == "left":   widget.x = nFB_x + positions[0][0]
                if widget.anchor_x == "center": widget.x = nFC_x + positions[1][0]
                if widget.anchor_x == "top":    widget.x = nFT_x + positions[1][0]
            if dh == 0 and widget.styler.sticky_y:
                if widget.anchor_y == "bottom": widget.y = nFB_y + positions[0][1]
                if widget.anchor_y == "center": widget.y = nFC_y + positions[1][1]
                if widget.anchor_y == "top":    widget.y = nFT_y + positions[2][1]


            
        self.wwidth = width
        self.wheight= height

        self.update_group()
    
    def frame_resized(self, width, height, owidth, oheight):
        """
        Might be updated in the future for frames under frame
        features
        """
        return

class ScrollFrame(Frame):
    """
    Self explainatory
    """

    def __init__(self, window, x, y, width, height, anchor_x="left", anchor_y="bottom", 
                 order=0, group=None, batch=None):
        Frame.__init__(self, window, x, y, width, height, anchor_x=anchor_x, anchor_y=anchor_y,
                       order=order, group=group, batch=batch)

    @property
    def scroll_x(self):
        return self._fgroup.offset_x

    @scroll_x.setter
    def scroll_x(sellf, value):
        self._fgroup.offset_x = value

    @property
    def scroll_y(self):
        return self._fgroup.offset_y

    @scroll_y.setter
    def scroll_y(self, value):
        self._fgroup.offset_y = value

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if not self._check_hit(x, y): return
        self.scroll_y -= scroll_y*10
        self.on_mouse_motion(x, y, 0, 0)

    def on_mouse_press(self, x, y, button, modifiers):
        y -= self.scroll_y

        for widget in self.widgets:
            widget.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        y -= self.scroll_y

        for widget in self.widgets:
            widget.on_mouse_release(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        y -= self.scroll_y

        for widget in self.widgets:
            widget.on_mouse_motion(x, y, dx, dy)

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        y -= self.scroll_y

        for widget in self.widgets:
            widget.on_mouse_drag(x, y, dx, dy, button, modifiers)


