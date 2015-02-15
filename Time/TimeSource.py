
'''
Created on 03.01.2015

@author: Iris
'''
from Component.Component import Component
import time

class TimeSource(Component):
    '''
    Time Source used throughout the application
    '''

    def activate(self):
        Component.activate(self)
        self._startTime = time.time()
    
    def getTime(self):
        return time.time()