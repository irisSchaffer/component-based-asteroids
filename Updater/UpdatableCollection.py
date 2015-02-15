'''
Created on 06.01.2015

@author: Iris
'''
from Component.Container import container

class UpdatableCollection(object):
    '''
    Collection of Updatables of one update rate
    '''

    def __init__(self, updateRate):
        '''
        Constructor
        '''
        
        self.updateRate = updateRate
        self.updateTime = 1 / self.updateRate
        self.updatables = []

        self._startTime = container.get('time_source').getTime()
        self._lastUpdated = self._startTime
        self._paused = False
        
    def getTimeTillUpdate(self):
        deltaTime = container.get('time_source').getTime() - self._lastUpdated

        return self.updateTime - deltaTime
        
    def append(self, updateMethod):
        self.updatables.append(updateMethod)
    
    def remove(self, updateMethod):
        self.updatables.remove(updateMethod)
        
    def contains(self, updateMethod):
        return self.updatables.count(updateMethod) != 0
    
    def length(self):
        return len(self.updatables)
    
    def update(self):
        self._lastUpdated = container.get('time_source').getTime()
        
        for updatable in self.updatables:
            updatable()