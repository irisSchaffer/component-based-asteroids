'''
Created on 03.01.2015

@author: Iris
'''
from Component.Component import Component
from Component.Container import container

class TimeLine(Component):
    '''
    Class for handling time lines in the application.
    '''

    def activate(self):
        Component.activate(self)
        container.get('updater').register(self.update)
        self._timeSource = container.get('time_source')
        self._initTime()
        
    def deactivate(self):
        container.get('updater').deregister(self.update)
        Component.deactivate(self)
        
    def scale(self, scale):
        self._scale = scale
        
    def getAbsTime(self):
        return (self._currentTime - self._startTime) * self._scale
    
    def reset(self):
        self._initTime()

    def pause(self):
        self._scale = 0
        
    def resume(self):
        self._scale = 1
        
    def getDeltaTime(self):
        return (self._currentTime - self._lastUpdate) * self._scale

    def update(self):
        self._lastUpdate = self._currentTime
        self._currentTime = self._timeSource.getTime()
        
    def _initTime(self):
        self._startTime = self._timeSource.getTime()
        self._currentTime = self._startTime
        self._lastUpdate = self._startTime
        self._scale = 1