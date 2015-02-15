'''
Created on 25.01.2015

@author: Iris
'''
from Component.Component import Component
from Aabb import Aabb
from Component.Container import container

class AabbCollider(Component):
    '''
    Axis Aligned Bounding Box Collider
    '''

    def __init__(self, collider = None):
        Component.__init__(self)
        self._collider = collider
        
    def activate(self):
        Component.activate(self)
        if (self._collider is None):
            self._collider = self._calculateBoundingBox()
        self.parent.collider = self._collider
        self.parent.getCollider = self.getBoundingBox;
        container.get('collision_system').register(self.parent)
        
    def deactivate(self):
        container.get('collision_system').deregister(self.parent)
        del self.parent.collider

        Component.deactivate(self)
        
    def getBoundingBox(self):
        boundingBox = self.parent.collider
        minimum = (boundingBox.minimum[0] + self.parent.pos[0], boundingBox.minimum[1] + self.parent.pos[1])
        maximum = (boundingBox.maximum[0] + self.parent.pos[0], boundingBox.maximum[1] + self.parent.pos[1])
        
        return Aabb(minimum, maximum)  
        
    def _calculateBoundingBox(self):
        minimum = self.parent.vertices[0]
        maximum = minimum
        
        for vertix in self.parent.vertices:
            minimum = (min(minimum[0], vertix[0]), min(minimum[1], vertix[1]))
            maximum = (max(maximum[0], vertix[0]), max(maximum[1], vertix[1]))
            
        return Aabb(minimum, maximum)
        