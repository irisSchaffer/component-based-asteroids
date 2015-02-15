'''
Created on 13.02.2015

@author: Iris
'''
from Component.Component import Component
from Component.Container import container
from Util.Vector import Vector2
from Physics.Body import Body
from Physics.Damping import Damping
from Collision.AabbCollider import AabbCollider
from Component.LifeCycle import LifeCycle
from Component.PoseTransmitter import PoseTransmitter
from Component.OutOfBoundsPosInverter import OutOfBoundsPosInverter
from Entities.Bullet import Bullet

class SpaceshipLogic(Component):
    '''
    Spaceship Logic
    '''

    def __init__(self, pos, numLives = 3):
        Component.__init__(self)
        self._pos = pos
        self._numLives = numLives
            
    def activate(self):
        Component.activate(self)
                
        self._setParameters()
        
        self.parent.lives = self._numLives

        self.parent.onCollision = self._onCollision
        self.parent.loseLife = self._loseLife
        self.parent.shoot = self._shoot
        self.parent.reset = self._reset
        self.parent.destroy = self._destroy
        
        self._initSpaceship()
        container.get('updater').register(self._update)
        
    def deactivate(self):
        Component.deactivate(self)
        container.get('updater').deregister(self._update)
        del self.parent.lives
        
    def _setParameters(self):
        self._parameters = container.get('parameters')
        
        self._spaceshipHeight = self._parameters.getFloat('spaceship', 'height')
        self._spaceshipDamping = self._parameters.getFloat('spaceship', 'damping')
        self._spaceshipAngularDamping = self._parameters.getFloat('spaceship', 'angular_damping')
        self._spaceshipTorque = self._parameters.getFloat('spaceship', 'torque')
        self._spaceshipSpeed = self._parameters.getFloat('spaceship', 'speed')
        
        self._bulletWidth = self._parameters.getFloat('bullet', 'width')
        self._bulletHeight = self._parameters.getFloat('bullet', 'height')
        
    def _initSpaceship(self):
        self._prevButtonState = False
        self._shipComponents = {}
        
        self._shipComponents['body'] = Body(Vector2(self._pos))
        self._shipComponents['damping'] = Damping(
            self._spaceshipDamping,
            self._spaceshipAngularDamping
        )
        self._shipComponents['outOfBoundsPosInverter'] = OutOfBoundsPosInverter()
        self._shipComponents['collider'] = AabbCollider()
        self._shipComponents['lifeCycle'] = LifeCycle()
        self._shipComponents['poseTransmitter'] = PoseTransmitter()

        for _, component in self._shipComponents.iteritems():
            self.parent.add(component)

    def _destroy(self):
        for _, component in self._shipComponents.iteritems():
            self.parent.remove(component)
            
        self._shipComponents = {}
        
    def _reset(self):
        self._destroy()
        self._initSpaceship()
  
    def _onCollision(self, collider):
        if not hasattr(collider, 'tags'):
            return

        if 'spaceship' in collider.tags or 'asteroid' in collider.tags:
            self.parent.pos.setTo(self.parent.lastValidPos)
            self.parent.loseLife()
            
        if 'bullet' in collider.tags:
            if collider.spaceship == self.parent:
                return
            
            self.parent.loseLife()

    def _shoot(self):
        position = Vector2(self.parent.pos.x, self.parent.pos.y)
        tip = Vector2(0, self._spaceshipHeight * 0.5).rotated(self.parent.angle)
        
        bullet = Bullet(
            pos = Vector2(position + tip),
            angle = self.parent.angle,
            width = self._bulletWidth,
            height = self._bulletHeight,
            spaceship = self.parent
        )
        container.add(bullet)

    def _loseLife(self):
        self.parent.lives -= 1
        container.get('messenger').send('lost_life', self.parent)

    def _update(self):
        if not hasattr(self.parent, 'body'):
            return

        self._handleTorque()
        self._handleShooting()
        self._handleVelocity()

    def _handleTorque(self):    
        self.parent.addTorque(-self.parent.axis[0] * self._spaceshipTorque)
    
    def _handleShooting(self):
        if self.parent.buttons[0] is True and self._prevButtonState is False:
            self.parent.shoot()
        
        # only shoot once for every key press
        self._prevButtonState = self.parent.buttons[0]
    
    def _handleVelocity(self):
        # only allow flying forward
        if self.parent.axis[1] < 0:
            self.parent.addForce(
                Vector2(0, -self.parent.axis[1] * self._spaceshipSpeed).rotated(self.parent.angle)
            )