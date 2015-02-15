'''
Created on 14.02.2015

@author: Iris
'''
from Component import Component
from Container import container

class Autodestruct(Component):

    def __init__(self, lifetime = 1.0, timeLineId = 'default_time_line'):
        Component.__init__(self)
        self._lifetime = lifetime
        self._timeLineId = timeLineId

    def activate(self):
        Component.activate(self)
        self._timeLine = container.get(self._timeLineId)
        self._deadline = self._timeLine.getAbsTime() + self._lifetime
        container.get('updater').register(self._update)

    def deactivate(self):
        container.get('updater').deregister(self._update)
        Component.deactivate(self)

    def _update(self):
        if self._timeLine.getAbsTime() >= self._deadline:
            container.remove(self.parent)