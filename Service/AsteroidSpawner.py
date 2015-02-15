'''
Created on 14.02.2015

@author: Iris
'''
from Component.Component import Component
from Component.Container import container
from Entities.Asteroid.Asteroid import Asteroid
import random, math
from Util.Vector import Vector2
from Entities import Helper

class AsteroidSpawner(Component):
    '''
    Spawns asteroids
    '''


    def __init__(self, uid):
        Component.__init__(self, uid)
        
    def activate(self):
        Component.activate(self)
        self._parameters = container.get('parameters')
        self._setParams()
        container.get('rate_updater').register(self._update, 1 / self._parameters.getFloat('asteroid', 'spawner_update_rate'))

    def deactivate(self):
        container.get('rate_updater').deregister(self._update)
        Component.deactivate(self)

    def _setParams(self):
        self._numAsteroids = self._parameters.getInt('asteroid', 'number')
        self._vertices = self._parameters.getInt('asteroid', 'vertices')
        
        self._radius = self._parameters.getFloat('asteroid', 'radius')
        self._radiusSpread = self._parameters.getFloat('asteroid', 'radius_spread')
        self._verticesPositionSpread = self._parameters.getFloat('asteroid', 'vertices_position_spread')
                
        self._speed = self._parameters.getInt('asteroid', 'speed')
        self._speedSpread = self._parameters.getFloat('asteroid', 'speed_spread')
        
        self._torque = self._parameters.getInt('asteroid', 'torque')
        self._torqueSpread = self._parameters.getFloat('asteroid', 'torque_spread')
        
        self._halfWorldWidth = self._parameters.getInt('game', 'world_width') * 0.5
        self._halfWorldHeight = self._parameters.getInt('game', 'world_height') * 0.5

    def createAsteroids(self, number):
        for _ in range(number):
            self._createAsteroid()

    def _update(self):
        curNumAsteroids = len(container.getByTag('asteroid_division1'))
                
        if curNumAsteroids < self._numAsteroids - 1:
            self._createAsteroid()

    def _createAsteroid(self):
        angle = random.uniform(0, 2 * math.pi)
        position = Vector2(0, self._halfWorldWidth - self._radius)
        position.rotate(angle)
        
        if abs(position.y) > self._halfWorldHeight:
            position.y = (self._halfWorldHeight - self._radius) * (-1 if position.x < 0 else 1)

        velocity = Vector2(0, 1)
        velocity.rotate(random.uniform(0, math.pi))
        velocity *= Helper.spreadValue(self._speed, self._speedSpread)

        container.add(
            Asteroid(
                pos = position,
                angle = 0,
                velocity = velocity,
                angularVelocity = Helper.spreadValue(self._torque, self._torqueSpread),
                radius = Helper.spreadValue(self._radius, self._radiusSpread),
                vertices = self._vertices,
                verticesPositionSpread = self._verticesPositionSpread
            )
        )
