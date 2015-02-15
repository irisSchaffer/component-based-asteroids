'''
Created on 10.12.2014

@author: Iris
'''

from Component import Component
from Network import xprotocol

class LifeCycle(Component):

    def __init__(self):
        Component.__init__(self)

    def activate(self):
        Component.activate(self)
        xprotocol.spawn_entity(self.parent.uid,
                               self.parent.pos[0],
                               self.parent.pos[1],
                               self.parent.angle,
                               self.parent.vertices)

    def deactivate(self):
        Component.deactivate(self)
        xprotocol.destroy_entity(self.parent.uid)