'''
Created on 14.02.2015

@author: Iris
'''
from Component import Component
from Container import container
from Util.Vector import Vector2

class OutOfBoundsPosInverter(Component):
    '''
    Inverts position of parent if position is out of bounds
    '''

    def __init__(self):
        Component.__init__(self)
        
    def activate(self):
        Component.activate(self)
        parameters = container.get('parameters')
        self._halfWorldWidth = parameters.getInt('game', 'world_width') * 0.5
        self._halfWorldHeight = parameters.getInt('game', 'world_height') * 0.5
        self.parent.lastValidPos = Vector2(self.parent.pos)
        
        container.get('updater').register(self._update)
        
    def deactivate(self):
        del self.parent.lastValidPos
        
        container.get('updater').deregister(self._update)
        Component.deactivate(self)
        
    def _update(self):
        if abs(self.parent.pos.x) > self._halfWorldWidth:
            self.parent.pos.setTo(Vector2(-self.parent.lastValidPos.x, self.parent.lastValidPos.y))
        if abs(self.parent.pos.y) > self._halfWorldHeight:
            self.parent.pos.setTo(Vector2(self.parent.lastValidPos.x, -self.parent.lastValidPos.y))
            
        self.parent.lastValidPos = Vector2(self.parent.pos)
