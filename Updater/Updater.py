'''
Created on 15.12.2014

@author: Iris
'''

from Component.Component import Component

class Updater(Component):
    '''
    Updater
    '''

    def __init__(self, uid = None):
        Component.__init__(self, uid)
        
        self.updatables = []

    def register(self, updateMethod):
        self.updatables.append(updateMethod)
        
    def deregister(self, updateMethod):
        self.updatables.remove(updateMethod)
        
    def update(self):
        for updatable in self.updatables:
            updatable()