'''
Created on 25.01.2015

@author: Iris
'''
from Component.Component import Component
from Component.Container import container

class AabbCollisionSystem(Component):
    '''
    Checks collisions
    '''

    def __init__(self, uid = 'collision_system'):
        Component.__init__(self, uid)
        self.collidables = []
        
    def register(self, collider):
        self.collidables.append(collider)
    
    def deregister(self, collider):
        self.collidables.remove(collider)
        
    def activate(self):
        Component.activate(self)
        container.get('updater').register(self._update)
        
    def deactivate(self):
        container.get('updater').deregister(self._update)
        Component.deactivate(self)
        
    def _update(self):
        collidables = list(self.collidables)
        while len(collidables) > 0:
            a = collidables.pop()
            
            for b in collidables:
                if self.isCollision(a.getCollider(), b.getCollider()):
                    if hasattr(a, 'onCollision'):
                        a.onCollision(b)
                    if hasattr(b, 'onCollision'):
                        b.onCollision(a)            
        
    def isCollision(self, a, b):
        if a.maximum[0] < b.minimum[0] or a.minimum[0] > b.maximum[0]:
            return False;
        
        if a.maximum[1] < b.minimum[1] or a.minimum[1] > b.maximum[1]:
            return False;

        return True;