'''
Created on 13.02.2015

@author: Iris
'''
from Component.Component import Component
from Component.PolyVisual import PolyVisual
from Network.NetGameController import NetGameController
from Component.Tag import Tag
from Entities.Spaceship.SpaceshipLogic import SpaceshipLogic
from Component.Container import container

class Spaceship(Component):
    '''
    player's spaceship
    '''


    def __init__(self, pos, width, height, peerId, uid = None):
        Component.__init__(self, uid)
        parameters = container.get('parameters')
        
        halfWidth = width * 0.5
        halfHeight = height * 0.5
        
        vertices = (
            (-halfWidth,  -halfHeight),
            (         0,   halfHeight),
            ( halfWidth,  -halfHeight),
        )
        
        self.add(PolyVisual(vertices))
        self.add(NetGameController(peerId))
        self.add(SpaceshipLogic(pos, parameters.getInt('spaceship', 'lives')))
        self.add(Tag('spaceship'))
