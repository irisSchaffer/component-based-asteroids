'''
Created on 02.12.2014

@author: Iris
'''

from Component.Component import Component
from Network import xprotocol
from Component.Container import container

class NetworkWrapper(Component):
    def __init__(self, numClients, port, updateRate, uid = None):
        self.numClients = numClients
        self.port = port
        self._updateRate = updateRate
        
        Component.__init__(self, uid)
    
    def update(self):
        xprotocol.update()
        
    def activate(self):
        Component.activate(self)
        
        xprotocol.startup(
            num_clients = self.numClients,
            port = self.port
        )
        container.get('rate_updater').register(self.update, self._updateRate)
        
    def deactivate(self):
        xprotocol.shutdown()
        container.get('rate_updater').deregister(self.update)
        Component.deactivate(self)