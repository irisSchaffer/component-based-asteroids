'''
Created on 24.01.2015

@author: Iris
'''
from Component import Component
from Container import container
from Network import xprotocol

class PoseTransmitter(Component):

    def __init__(self, rate = 60):
        Component.__init__(self)
        self.rate = rate

    def activate(self):
        Component.activate(self)
        container.get('rate_updater').register(self._update, self.rate)

    def deactivate(self):
        Component.deactivate(self)
        container.get('rate_updater').deregister(self._update)

    def _update(self):
        xprotocol.move_entity(
            self.parent.uid,
            self.parent.pos[0],
            self.parent.pos[1],
            self.parent.angle
        )