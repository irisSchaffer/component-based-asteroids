'''
Created on 24.01.2015

@author: Iris
'''
class IdleState(object):

    def __init__(self, context):
        self.context = context

    def onConnection(self, peer, connected):
        if connected:
            self.context.peers.add(peer)
            if len(self.context.peers) >= self.context.num_players:
                from PlayState import PlayState
                self.context.state = PlayState(self.context)
        else:
            self.context.peers.discard(peer)