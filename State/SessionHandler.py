'''
Created on 24.01.2015

@author: Iris
'''
from Component.Component import Component
from Network import xprotocol
from IdleState import IdleState

class SessionHandler(Component):

    def __init__(self):
        Component.__init__(self)
        self.state = None
        self.peers = set()
        self.num_players = 2

    def activate(self):
        Component.activate(self)
        xprotocol.add_connection_listener(self._onConnection)
        self.state = IdleState(self)

    def deactivate(self):
        xprotocol.remove_connection_listener(self._onConnection)
        Component.deactivate(self)

    def _onConnection(self, peer, connected):
        self.state.onConnection(peer, connected)