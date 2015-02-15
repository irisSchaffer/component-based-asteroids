'''
Created on 10.12.2014

@author: Iris
'''

from Component import Component

class Container(Component):
    '''
    Container for Components
    '''

    def __init__(self, children = []):
        Component.__init__(self)
        self.children = children
        self.children = []
        self.tags = {}
        self._scopes = []
        
    def add(self, child):
        Component.add(self, child)
        
        if len(self._scopes) > 0:
            curScope = self._scopes.pop()
            curScope.append(child)
            self._scopes.append(curScope)
    
    def remove(self, child):
        Component.remove(self, child)
        
        if (len(self._scopes) > 0):
            curScope = self._scopes.pop()
            curScope.remove(child)
            self._scopes.append(curScope)
            
    def has(self, child):
        return self.children.count(child) > 0
        
    def get(self, uid):
        for component in self.children:
            if component.uid == uid:
                return component
        
    def registerTag(self, tag, component):
        if self.tags.get(tag) is None:
            self.tags[tag] = []
            
        components = self.tags[tag]
        components.append(component)
        
    def deregisterTag(self, tag, component):
        if self.tags.get(tag) is not None:
            self.tags[tag].remove(component)
        
    def getByTag(self, tag):
        if self.tags.get(tag) is None:
            return []
        
        return list(self.tags[tag])
    
    def push_scope(self):
        self._scopes.append([])
        
        
    def pop_scope(self):
        components = self._scopes.pop()
        components.reverse()
        for component in components:
            self.remove(component)
            component.deactivate()
        
container = Container()
        