'''
Created on 10.12.2014

@author: Iris
'''

import uuid

class Component(object):
    '''
    Component
    '''

    def __init__(self, uid = None):
        self.children = []
        self.active = False
        self.uid = uid
        
        if (self.uid == None):
            self.uid = str(uuid.uuid4().int)

    def activate(self):
        print('activating ' + self.uid)
        
        for child in self.children:
            child.activate()

        self.active = True
        
    def deactivate(self):
        print('deactivating ' + self.uid)
        
        for child in self.children:
            child.deactivate()

        self.active = False
        
    def isActive(self):
        return self.active
    
    def add(self, child):
        child.parent = self
        self.children.append(child)
        
        if self.active is True:
            child.activate()
        
    def remove(self, child):
        child.deactivate()
        self.children.remove(child)
