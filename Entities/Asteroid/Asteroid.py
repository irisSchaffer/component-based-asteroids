'''
Created on 13.02.2015

@author: Iris
'''

from Component.Component import Component
from Component.LifeCycle import LifeCycle
from Component.PoseTransmitter import PoseTransmitter
from Component.PolyVisual import PolyVisual
from Collision.AabbCollider import AabbCollider
from Physics.Body import Body
from Component.Tag import Tag
from Component.Container import container
from Component.Autodestruct import Autodestruct
import math
from Util.Vector import Vector2
from Entities import Helper
from Component.OutOfBoundsPosInverter import OutOfBoundsPosInverter
from Entities.Debris import Debris

class Asteroid(Component):
    '''
    Asteroid
    '''

    def __init__(self, pos, angle, velocity, angularVelocity, radius, verticesPositionSpread, vertices, division = 1, uid = None):
        Component.__init__(self, uid)
        self.uid = 'astroid' + self.uid
        parameters = container.get('parameters')
        
        self.radius = radius
        self.division = division
        
        self._verticesPositionSpread = verticesPositionSpread
        self._numVertices = vertices
        self._divisions = parameters.getInt('asteroid', 'divisions')
        self._divisionSpeedFactor = parameters.getFloat('asteroid', 'division_speed_factor')
        self._fragmentsPerDivision = parameters.getInt('asteroid', 'fragments_per_division')
        
        self.add(Tag('asteroid'))
        self.add(Tag('asteroid_division' + str(self.division)))
        
        self.add(PolyVisual(self._createVertices(radius, verticesPositionSpread, vertices)))
        self.add(Body(
            pos = pos,
            angle = angle,
            velocity = velocity,
            angularVelocity = angularVelocity
        ))
        self.add(OutOfBoundsPosInverter())
        self.add(AabbCollider())
        self.add(LifeCycle())
        self.add(PoseTransmitter())
        
    def onCollision(self, collider):
        if hasattr(collider, 'tags') and 'asteroid' in collider.tags:
            return
        
        self.pos.setTo(self.lastValidPos)
        self.add(Autodestruct(0))

        if self.division <= self._divisions:
            self._divide()

        container.add(Debris(Vector2(self.pos), 'animation_time_line'))
        
    def _createVertices(self, radius, verticesPositionSpread, numVertices):
        angle = 2 * math.pi / numVertices;
        vertex = Vector2(0, radius)
        vertices = ()
        
        for _ in range(numVertices):
            vertex.rotate(angle)
            vertices += ((
                Helper.spreadValue(vertex.x, verticesPositionSpread),
                Helper.spreadValue(vertex.y, verticesPositionSpread)
            ),)
        
        return vertices
    
    def _divide(self):
        angle = (math.pi * 7) / 4.0
        angleDiff = (angle * 2) / (self._fragmentsPerDivision - 1)
        for _ in range(self._fragmentsPerDivision):
            velocity = self.velocity.rotated(angle) * self._divisionSpeedFactor
            
            container.add(Asteroid(
                pos = Vector2(self.pos),
                angle = self.angle,
                velocity = velocity,
                angularVelocity = self.angularVelocity,
                radius = self.radius / self._fragmentsPerDivision,
                verticesPositionSpread = self._verticesPositionSpread,
                vertices = self._numVertices,
                division = self.division + 1
            ))
            angle -= angleDiff