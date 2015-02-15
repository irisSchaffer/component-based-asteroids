'''
Created on 12.02.2015

@author: Iris
'''
from Component.Component import Component
from Component.Container import container


class Messenger(Component):

    def __init__(self, uid = 'messenger', timelineId = 'default_timeline'):
        Component.__init__(self, uid)
        self._timelineId = timelineId
        self._subscribers = {}
        self._messageQueue = []
        self._unsubscribed = set()

    def activate(self):
        Component.activate(self)
        container.get('updater').register(self._update)

    def deactivate(self):
        container.get('updater').deregister(self._update)
        Component.deactivate(self)

    def subscribe(self, msgType, subscriber):
        subscriberSet = self._subscribers.get(msgType, None)
        if not subscriberSet:
            subscriberSet = set()
            self._subscribers[msgType] = subscriberSet

        assert subscriber not in subscriberSet, 'subscriber already registered'
        subscriberSet.add(subscriber)

    def unsubscribe(self, subscriber):
        self._unsubscribed.add(subscriber)
        for subscriberSet in self._subscribers.itervalues():
            subscriberSet.discard(subscriber)

    def send(self, msgType, param = None):
        self._messageQueue.append((msgType, param))

    def fire(self, msgType, param = None):
        subSet = self._subscribers.get(msgType, None)

        if not subSet:
            # no subscribers for that message msgType
            return

        # don't operate on orig set, list of subscribers might change
        for subscriber in set(subSet):
            if subscriber not in self._unsubscribed:
                subscriber(msgType, param)

    def _update(self):
        # don't use a for-loop, new message could be added during dispatch
        while self._messageQueue:
            item = self._messageQueue.pop(0)
            self.fire(item[0], item[1])

        # clear set of old subscribers
        self._unsubscribed.clear()