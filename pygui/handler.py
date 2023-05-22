class EventHandler:

    def __init__(self):
        self.x = -999
        self.y = -999

        self.ccontainer = None #Current Container
        self.containers = set()

        self.twidgets   = {'pressed': None, 'motion': None}

    def top_container(self):
        return max(self.containers, key=lambda con: con.z)

    def top_widget(self, con):
        try:
            widgets = [child for child in con.children if self.widget_hit(child)]
            return max(widgets, key=lambda widget: widget.z)
        except: return None

    def add_container(self, con):
        self.containers.add(con)

    def con_hit(self, con):
        return con._check_hit(self.x, self.y)

    def widget_hit(self, widget):
        x = self.x - widget.parent.translate_x
        y = self.y - widget.parent.translate_y
        return widget._check_hit(x, y)

    def _update_position(self, x, y):
        self.x = x
        self.y = y

    def rel_pos(self, con):
        return self.x - con.translate_x, self.y - con.translate_y

    """
    Mouse Events
    """
    def on_mouse_press(self, x, y, button, modifiers):
        self._update_position(x, y)

        ccontainer = self.top_container()
        cwidget = self.top_widget(ccontainer)
        pwidget = self.twidgets['pressed']

        if (ccontainer != self.ccontainer or cwidget != pwidget) and pwidget:
            pwidget.on_mouse_press(pwidget.left-1,y,button,modifiers)

        if cwidget:
            if self.con_hit(ccontainer): cwidget.on_mouse_press(*self.rel_pos(cwidget.parent), button, modifiers)
            else: cwidget.on_mouse_press(cwidget.left-1,y,button,modifiers)
        self.twidgets['pressed'] = cwidget
        self.ccontainer = ccontainer

    def on_mouse_release(self, x, y, button, modifiers):
        self._update_position(x, y)
        pwidget = self.twidgets['pressed']
        if not pwidget: return

        if self.con_hit(pwidget.parent): pwidget.on_mouse_release(*self.rel_pos(pwidget.parent), button, modifiers)
        else: pwidget.on_mouse_release(pwidget.left-1, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self._update_position(x, y)

        ccontainer = self.top_container()
        cwidget = self.top_widget(ccontainer)
        mwidget = self.twidgets['motion']

        if (ccontainer != self.ccontainer or cwidget != mwidget) and mwidget:
            mwidget.on_mouse_motion(mwidget.left-1,y, dx, dy)

        if cwidget:
            if self.con_hit(ccontainer): cwidget.on_mouse_motion(*self.rel_pos(cwidget.parent), dx, dy)
            else: cwidget.on_mouse_motion(cwidget.left-1, y, dx, dy)
        self.twidgets['motion'] = cwidget
        self.ccontainer = ccontainer
        
    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        self._update_position(x, y)
        if self.twidgets['pressed']: self.twidgets['pressed'].on_mouse_drag(*self.rel_pos(self.twidgets['pressed'].parent), dx, dy, button, modifiers)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        ccontainer = self.top_container()
        if ccontainer and self.con_hit(ccontainer): ccontainer.scroll(scroll_x, scroll_y)

    """
    Text Events
    """
    def on_text(self, text):
        if self.twidgets['pressed']: self.twidgets['pressed'].on_text(text)

    def on_text_motion(self, motion):
        if self.twidgets['pressed']: self.twidgets['pressed'].on_text_motion(motion)

    def on_text_motion_select(self, motion):
        if self.twidgets['pressed']: self.twidgets['pressed'].on_text_motion_select(motion)

