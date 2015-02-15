'''
Created on 24.01.2015

@author: Iris
'''
from Component.Component import Component
from Util.Vector import Vector2
from Component.Container import container

class Body(Component):
    '''
    Physical Body
    '''

    def __init__(self, pos, angle = 0, velocity = (0.0, 0.0), angularVelocity = 0.0, timeLineId = 'default_time_line'):
        Component.__init__(self)
        self._timeLine = container.get(timeLineId)
        self._pos = pos
        self._angle = angle
        self._velocity = velocity
        self._angularVelocity = angularVelocity
        
        self.mass = 1.0
        self.moi = self.mass * 0.5
        self._force = Vector2(0.0, 0.0)
        self._torque = 0.0
        
    def activate(self):
        Component.activate(self)
        container.get('updater').register(self._update)

        self.parent.pos = self._pos
        self.parent.angle = self._angle
        self.parent.velocity = self._velocity
        self.parent.angularVelocity = self._angularVelocity
        self.parent.acceleration = Vector2(0.0, 0.0)
        self.parent.angularAcceleration = 0.0
        self._clearForces()

        self.parent.body = self

        self.parent.addForce = self._addForce
        self.parent.addTorque = self._addTorque
                
    def deactivate(self):
        Component.deactivate(self)
        container.get('updater').deregister(self._update)
        
        del self.parent.pos
        del self.parent.angle
        del self.parent.velocity
        del self.parent.angularVelocity
        del self.parent.acceleration
        del self.parent.angularAcceleration
        del self.parent.body

    def _addForce(self, force):
        self._force += force

    def _addTorque(self, torque):
        self._torque += torque

    def _clearForces(self):
        self._force[0] = 0.0
        self._force[1] = 0.0
        self._torque = 0.0

    def _calcAcceleration(self):
        self.parent.acceleration = self._force * (1.0 /  self.mass)
        self.parent.angularAcceleration = self._torque / self.moi

    def _move(self):
        dt = self._timeLine.getDeltaTime()
        
        self.parent.angularVelocity += self.parent.angularAcceleration * dt
        self.parent.angle += self.parent.angularVelocity * dt

        self.parent.velocity += self.parent.acceleration * dt
        self.parent.pos += self.parent.velocity * dt
        
    def _update(self):
        self._calcAcceleration()
        self._move()
        self._clearForces()