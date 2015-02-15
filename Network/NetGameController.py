'''
Created on 24.01.2015

@author: Iris
'''
from Component.Component import Component
from Network import xprotocol

class NetGameController(Component):

    def __init__(self, source, n_axis = 4, n_buttons = 6):
        Component.__init__(self)
        self._source = source
        self._n_axis = n_axis
        self._n_buttons = n_buttons

    def activate(self):
        Component.activate(self)
        xprotocol.add_axis_listener(self._on_axis)
        xprotocol.add_button_listener(self._on_button)
        self.parent.axis = [0.0 for i in range(self._n_axis)]
        self.parent.buttons = [False for i in range(self._n_buttons)]

    def deactivate(self):
        del self.parent.buttons
        del self.parent.axis
        xprotocol.remove_button_listener(self._on_button)
        xprotocol.remove_axis_listener(self._on_axis)
        Component.deactivate(self)

    def _on_axis(self, peer, axis, value):
        if peer != self._source:
            return
        
        self.parent.axis[axis] = value

    def _on_button(self, peer, button, value):
        if peer != self._source:
            return

        self.parent.buttons[button] = value