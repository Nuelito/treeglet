"""
Handlers to handle GUI to prevent weird behaviour by analyzing
`z` variables of each widgets to check priority.
"""
import pyglet

from treeglet.widgets import Button
from treeglet.widgets import TextEntry

class EventHandler:

    fixed_container = False #Decides if EventHandler is being shared
    container   = None
    containers  = [] #For when 
    
    top_widgets = {"pressed": None, "motion": None,}
    
    x: int = 0
    y: int = 0
    
    def update_position(self, x, y):
        self.x, self.y = x, y
        
    def top_widget(self, container, widget=None):
        for child in container._children:
            if child._check_hit(*self.container_adjust_position(container, self.x, self.y)):
                widget = child if widget == None or widget.z < child.z else widget
            else: continue
        return widget
    
    def top_container(self):
        for container in self.containers:
            self.container = None if not self.container or not self.container._check_hit(self.x, self.y) else self.container
            self.container = container if not self.container or (container._check_hit(self.x, self.y) and container.z > self.container.z) else self.container
        return self.container
        
    def container_adjust_position(self, container, x, y):
        return self.x - container.translate_x, self.y - container.translate_y 

    def on_mouse_press(self, x, y, button, modifiers):
        self.update_position(x, y)
        
        widget = self.top_widgets["pressed"]
        if widget and not widget._check_hit(*self.container_adjust_position(widget._parent, x, y)):
            widget.on_mouse_press(widget.left-10, widget.bottom, button, modifiers)
            widget = self.top_widgets["pressed"] = None
            
        if self.fixed_container:
            x, y = self.container_adjust_position(self.container, self.x, self.y)
            self.top_widgets["pressed"] = self.top_widget(self.container)
        else:
            self.container = self.top_container()
            if self.container: 
                x, y = self.container_adjust_position(self.container, x, y)
                self.top_widgets["pressed"] = self.top_widget(self.container)
            
            
        if self.top_widgets["pressed"]: self.top_widgets["pressed"].on_mouse_press(x, y, button, modifiers)
        
    def on_mouse_release(self, x, y, button, modifiers):
        self.update_position(x, y)
        
        if not self.top_widgets["pressed"]: return
        
        if self.fixed_container:
            widget = self.top_widget(self.container)
            x, y =  self.container_adjust_position(self.top_widgets["pressed"]._parent, x, y)
            if widget != self.top_widgets["pressed"] and self.top_widgets["pressed"]:
                self.top_widgets["pressed"].on_mouse_release(self.top_widgets["pressed"].left-10, self.top_widgets["pressed"].bottom, button, modifiers)
                return
            else:
                self.top_widgets["pressed"].on_mouse_release(x, y, button, modifiers)
        else:
            self.container = self.top_container()
            if self.container: 
                x, y = self.container_adjust_position(self.container, x, y)
                widget = self.top_widget(self.container)
                if widget != self.top_widgets["pressed"] and self.top_widgets["pressed"]:
                    self.top_widgets["pressed"].on_mouse_release(self.top_widgets["pressed"].left-10, self.top_widgets["pressed"].bottom, button, modifiers)
                else:
                    self.top_widgets["pressed"].on_mouse_release(x, y, button, modifiers)
        
        
    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        self.update_position(x, y)
        
        if self.fixed_container:
            widget = self.top_widget(self.container)
            x, y = self.container_adjust_position(self.container, x, y)
            if widget: widget.on_mouse_drag(x, y, dx, dy, button, modifiers)
        else:
            """
            self.container = self.top_container()
            if self.container: 
                x, y = self.container_adjust_position(self.container, x, y)
                widget = self.top_widget(self.container)
                if widget: widget.on_mouse_drag(x, y, dx, dy, button, modifiers)
            """
            if self.top_widgets['pressed']:
                self.top_widgets['pressed'].on_mouse_drag(x, y, dx, dy, button, modifiers)
        
    def on_mouse_motion(self, x, y, dx, dy):
        self.update_position(x, y)
        
        widget = self.top_widgets["motion"]
        if widget and not widget._check_hit(*self.container_adjust_position(widget._parent, x, y)):
            widget.on_mouse_motion(widget.left-10, widget.bottom, dx, dy)
            self.top_widgets["motion"] = None
        
        if self.fixed_container:
            widget = self.top_widget(self.container)
            x, y =  self.container_adjust_position(self.container, x, y)
            
            if widget != self.top_widgets["motion"] and self.top_widgets["motion"]:
                self.top_widgets["motion"].on_mouse_motion(self.top_widgets["motion"].left-10, self.top_widgets["motion"].bottom, dx, dy)
            self.top_widgets["motion"] = widget
        else:
            self.container = self.top_container()
            if self.container: 
                x, y = self.container_adjust_position(self.container, x, y)
                widget = self.top_widget(self.container)
                if widget != self.top_widgets["motion"] and self.top_widgets["motion"]: 
                    self.top_widgets["motion"].on_mouse_motion(self.top_widgets["motion"].left-10, self.top_widgets["motion"].bottom, dx, dy)
                self.top_widgets["motion"] = self.top_widget(self.container)
             
        
        if self.top_widgets["motion"]: self.top_widgets["motion"].on_mouse_motion(x, y, dx, dy)
        
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.update_position(x, y)
        
        if self.fixed_container:
            if self.container.scrollable:
                self.container.translate_x += scroll_x * self.container.scroll_speed[0]
                self.container.translate_y += scroll_y * self.container.scroll_speed[1]
        else:
            self.container = self.top_container()
            if self.container and self.container.scrollable and self.container._check_hit(x, y): 
                self.container.translate_x += scroll_x * self.container.scroll_speed[0]
                self.container.translate_y += scroll_y * self.container.scroll_speed[1]
            
                
    #Documents functions
    def on_text(self, text):
        if not self.container: return
        for child in self.container._children: child.on_text(text)
        
    def on_text_motion(self, motion):
        if not self.container: return
        for child in self.container._children: child.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        if not self.container: return
        for child in self.container._children: child.on_text_motion_select(motion)
