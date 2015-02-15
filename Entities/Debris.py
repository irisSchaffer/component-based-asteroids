'''
Created on 14.02.2015

@author: Iris
'''
from Component.Component import Component
import random, math
from Component.Container import container
from Util.Vector import Vector2
from Physics.Body import Body
from Component.LifeCycle import LifeCycle
from Component.PoseTransmitter import PoseTransmitter
from Entities import Helper
from Component.Autodestruct import Autodestruct
from Component.Tag import Tag

class Debris(Component):
    '''
    self-destructing Debris
    '''

    def __init__(self, pos, timeLineId = 'default_time_line', uid = None):
        Component.__init__(self, uid)
        self.uid = 'debris' + self.uid
        self._pos = pos
        self._timeLineId = timeLineId

    def activate(self):
        Component.activate(self)
        self._parameters = container.get('parameters')
        
        for _ in range(int(round(self._getSpreadConfig('number_debris', 'effects')))):
            self.add(self._createDebris())
            
        self.add(Tag('debris'))
        self.add(Autodestruct(self._getSpreadConfig('lifetime'), self._timeLineId))
                        
    def deactivate(self):
        container.get('messenger').send('destroyed_debris', {'uid': self.uid, 'tags': list(self.tags)})          
        Component.deactivate(self)
          
    def _createDebris(self):
        radius = self._getSpreadConfig('radius')
        speed = self._getSpreadConfig('speed')
        
        angularSpeed = self._getSpreadConfig('angular_speed')
        angularSpeed *= random.choice([-1.0, 1.0])
        
        velocity = Vector2(speed, 0.0)
        velocity.rotate(random.uniform(0, math.pi * 2))
    
        debris = Component()
        debris.add(Helper.createRectangle(radius * 2, radius * 2))
        debris.add(Body(
            pos = Vector2(self._pos),
            velocity = velocity,
            angularVelocity = angularSpeed,
            timeLineId = self._timeLineId
        ))
        debris.add(LifeCycle())
        debris.add(PoseTransmitter())
                
        return debris
    
    def _getSpreadConfig(self, name, section = 'debris'):
        return Helper.spreadValue(self._parameters.getFloat(section, name), self._parameters.getFloat(section, name + '_spread'))