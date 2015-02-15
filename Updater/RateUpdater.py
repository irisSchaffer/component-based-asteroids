'''
Created on 15.12.2014

@author: Iris
'''

from Component.Container import container
from UpdatableCollection import UpdatableCollection
from Updater import Updater
import time

class RateUpdater(Updater):
    '''
    Updater
    '''

    def __init__(self, uid = None):
        Updater.__init__(self, uid)
    
    def activate(self):
        Updater.activate(self)
        container.get('updater').register(self.update)
        
    def deactivate(self):
        container.get('updater').deregister(self.update)
        Updater.deactivate(self)
        
    def register(self, updateMethod, updateRate):
        for updatableCollection in self.updatables:
            if updateRate == updatableCollection.updateRate:
                updatableCollection.append(updateMethod)
                return
        
        updatableCollection = UpdatableCollection(updateRate)
        updatableCollection.append(updateMethod)
        self.updatables.append(updatableCollection)
        
    def deregister(self, updateMethod):
        for updatableCollection in self.updatables:
            if updatableCollection.contains(updateMethod):
                updatableCollection.remove(updateMethod)
                
                if updatableCollection.length() == 0:
                    self.updatables.remove(updatableCollection)
                
                return
        
    def update(self):
        sleepTime = 500
                
        for updatable in self.updatables:
            timeTillUpdate = updatable.getTimeTillUpdate()
              
            if timeTillUpdate < 0.01:
                updatable.update()           
              
            # adjust sleepTime for this component if necessary
            sleepTime = min(timeTillUpdate, sleepTime)
              
        #if sleepTime > 0:
        #    time.sleep(sleepTime)  # prevent 100% cpu usage by sleeping unused time