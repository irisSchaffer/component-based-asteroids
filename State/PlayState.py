'''
Created on 24.01.2015

@author: Iris
'''
from Component.Container import container
from IdleState import IdleState
from Network import xprotocol
from Time.TimeLine import TimeLine
from Util.Vector import Vector2
from Collision.AabbCollisionSystem import AabbCollisionSystem
from Entities.Spaceship.Spaceship import Spaceship
from Entities.Debris import Debris
from Component.Tag import Tag
from Component.Component import Component
from Component.StaticPose import StaticPose
from Component.LifeCycle import LifeCycle
from Entities import Helper
from Service.AsteroidSpawner import AsteroidSpawner

class PlayState(object):

    def __init__(self, context):
        self.context = context

        container.push_scope()
        xprotocol.set_world_width(800)
        
        self._parameters = container.get('parameters')
        self._asteroidSpawner = AsteroidSpawner('asteroid_spawner')
        
        container.add(TimeLine('default_time_line'))
        container.add(TimeLine('animation_time_line'))
        container.add(AabbCollisionSystem('collision_system'))
        container.add(self._asteroidSpawner)

        container.get('messenger').subscribe('lost_life', self._onLostLife)
        container.get('messenger').subscribe('destroyed_debris', self._onAutodestructed)

        self._addSpaceships()
        self._addHud()
        self._asteroidSpawner.createAsteroids(self._parameters.getInt('asteroid', 'number'))

    def _addSpaceships(self):
        invert = 1
        count = 1
                
        for peer in self.context.peers:
            spaceship = Spaceship(
                uid ='spaceship' + str(count),
                pos = Vector2(self._parameters.getInt('spaceship', 'pos_x') * invert, self._parameters.getInt('spaceship', 'pos_y')),
                width = self._parameters.getInt('spaceship', 'width'),
                height = self._parameters.getInt('spaceship', 'height'),
                peerId = peer
            )
            
            container.add(spaceship)
            
            invert *= -1
            count += 1
            
    def _addHud(self):
        posY = self._parameters.getInt('hud', 'pos_y')
        padding = self._parameters.getInt('hud', 'point_padding')
        radius = self._parameters.getInt('hud', 'point_radius')
        inverse = 1
        
        for spaceship in container.getByTag('spaceship'):
            posX = self._parameters.getInt('hud', 'pos_x')
            
            for i in range(0, spaceship.lives):
                point = Component(self._getHudPointUid(spaceship, i))
                point.add(Helper.createRectangle(radius, radius))
                point.add(StaticPose(Vector2(posX * inverse, posY)))
                point.add(LifeCycle())
                point.add(Tag('hud_life'))
                
                container.add(point)
                
                posX -= padding
            
            inverse *= -1
                
    def _getHudPointUid(self, spaceship, i):
        return spaceship.uid + '_life' + str(i)

    def _onLostLife(self, msgType, spaceship):
        container.get('default_time_line').pause()
        print str(spaceship.uid) + ' lost life!'
        self._gameOver = spaceship.lives <= 0
        
        debris = Debris(spaceship.pos, 'animation_time_line')
        debris.add(Tag('lost_debris'))
        container.add(debris)
        container.remove(container.get(self._getHudPointUid(spaceship, spaceship.lives)))
        
        for debris in container.getByTag('bullet'):
            container.remove(debris)
        
        spaceship.destroy()

        if self._gameOver:
            for asteroid in container.getByTag('asteroid'):
                container.add(Debris(asteroid.pos, 'animation_time_line'))
                container.remove(asteroid)
                
            container.remove(self._asteroidSpawner)

    def _onAutodestructed(self, msgType, details):
        if not 'lost_debris' in details['tags']:
            return
        
        for debris in container.getByTag('lost_debris'):
            container.remove(debris)

        if not self._gameOver:    
            for asteroid in container.getByTag('asteroid'):
                container.remove(asteroid)
                
            self._asteroidSpawner.createAsteroids(self._parameters.getInt('asteroid', 'number'))

            for ship in container.getByTag('spaceship'):
                ship.reset()
            
            container.get('default_time_line').resume()            

    def onConnection(self, peer, connected):
        if connected:
            # should never happen
            pass
        else:
            self.context.peers.discard(peer)

            if len(self.context.peers) < self.context.num_players:
                container.pop_scope()

                self.context.state = IdleState(self.context)