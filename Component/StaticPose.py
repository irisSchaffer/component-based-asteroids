'''
Created on 10.12.2014

@author: Iris
'''

from Component import Component
from Util.Vector import Vector2

class StaticPose(Component):
    '''
    Adds position and angle
    '''


    def __init__(self, pos = Vector2(0, 0), angle = 0):
        Component.__init__(self)
        self._pos = pos
        self._angle = angle

    def activate(self):
        Component.activate(self)
        self.parent.pos = self._pos
        self.parent.angle = self._angle

    def deactivate(self):
        del self.parent.pos
        del self.parent.angle
        Component.deactivate(self)
        