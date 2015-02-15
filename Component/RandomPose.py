'''
Created on 15.12.2014

@author: Iris
'''

import math, random
from Component import Component
from Network import xprotocol
from Container import container

class RandomPose(Component):

    def __init__(self, worldWidth, worldHeight, rate):
        Component.__init__(self)
        self.width = worldWidth
        self.height = worldHeight
        self.rate = rate

    def _getNewPose(self):
        x = random.uniform(-self.width * 0.5, self.width * 0.5)
        y = random.uniform(-self.height * 0.5, self.height * 0.5)
        angle = random.uniform(0, 2 * math.pi)

        self.parent.pos = (x, y)
        self.parent.angle = angle

    def activate(self):
        Component.activate(self)
        self._getNewPose()
        container.get('rate_updater').register(self.update, self.rate)

    def deactivate(self):
        container.get('rate_updater').deregister(self.update)
        del self.parent.pos
        del self.parent.angle
        Component.deactivate(self)

    def update(self):
        print('updating random pose')
        self._getNewPose()
        xprotocol.move_entity(self.parent.uid,
                              self.parent.pos[0],
                              self.parent.pos[1],
                              self.parent.angle)