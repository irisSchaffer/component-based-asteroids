'''
Created on 10.12.2014

@author: Iris
'''

from Component import Component

class PolyVisual(Component):
    '''
    Adds vertices to parent
    '''

    def __init__(self, vertices):
        Component.__init__(self)
        self._vertices = vertices
        
    def activate(self):
        Component.activate(self)
        self.parent.vertices = self._vertices
        
    def deactivate(self):
        Component.deactivate(self)
        del self.parent.vertices