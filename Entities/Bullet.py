'''
Created on 14.02.2015

@author: Iris
'''
from Component.Component import Component
from Entities import Helper
from Component.Container import container
from Physics.Body import Body
from Component.LifeCycle import LifeCycle
from Component.PoseTransmitter import PoseTransmitter
from Component.Autodestruct import Autodestruct
from Component.Tag import Tag
from Collision.AabbCollider import AabbCollider
from Util.Vector import Vector2
from Component.OutOfBoundsPosInverter import OutOfBoundsPosInverter

class Bullet(Component):
    '''
    Bullet
    '''

    def __init__(self, pos, angle, width, height, spaceship, uid = None):
        Component.__init__(self, uid)
        self.uid = 'bullet' + self.uid
        self._pos = pos
        self._angle = angle
        self._width = width
        self._height = height
        self._spaceship = spaceship
        
    def activate(self):
        Component.activate(self)
        self.spaceship = self._spaceship

        parameters = container.get('parameters')
        
        self.add(Helper.createRectangle(self._width, self._height))
        self.add(Body(
            pos = self._pos,
            angle = self._angle,
            velocity = Vector2(0.0, parameters.getFloat('bullet', 'speed')).rotated(self._angle)
        ))
        self.add(OutOfBoundsPosInverter())
        self.add(AabbCollider())
        self.add(LifeCycle())
        self.add(PoseTransmitter())
        self.add(Autodestruct(parameters.getFloat('bullet', 'lifetime')))
        self.add(Tag('bullet'))
        
    def onCollision(self, collider):
        if self.spaceship == collider:
            return
        
        self.add(Autodestruct(0))
