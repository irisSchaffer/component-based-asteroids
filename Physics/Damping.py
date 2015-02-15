'''
Created on 13.02.2015

@author: Iris
'''
from Component.Component import Component
from Component.Container import container

class Damping(Component):
    '''
    Linear Damping
    '''


    def __init__(self, damping = 0.0, angularDamping = 0.0):
        Component.__init__(self)
        self.damping = damping
        self.angularDamping = angularDamping
        
    def activate(self):
        Component.activate(self)
        container.get('updater').register(self._update)

    def deactivate(self):
        container.get('updater').deregister(self._update)
        Component.deactivate(self)

    def _update(self):
        self.parent.addForce(self.parent.velocity * -self.damping)
        self.parent.addTorque(-self.parent.angularVelocity * self.angularDamping)