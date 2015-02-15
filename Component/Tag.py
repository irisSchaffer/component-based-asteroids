'''
Created on 06.01.2015

@author: Iris
'''
from Container import container
from Component import Component

class Tag(Component):
    '''
    Tag class for tagging components
    '''

    def __init__(self, tag):
        '''
        Constructor
        '''
        Component.__init__(self)
        self.uid = 'tag_' + tag + self.uid
        self._tag = tag

    def activate(self):
        Component.activate(self)
        container.registerTag(self._tag, self.parent)

        if not hasattr(self.parent, 'tags'):
            self.parent.tags = []
        self.parent.tags.append(self._tag)
        self.parent.hasTag = self._hasTag
        
    def deactivate(self):        
        self.parent.tags.remove(self._tag)
        if len(self.parent.tags) == 0:
            del self.parent.tags
        
        container.deregisterTag(self._tag, self.parent)
        
        Component.deactivate(self)
        
    def _hasTag(self, tag):
        return tag in self.parent.tags