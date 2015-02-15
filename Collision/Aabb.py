'''
Created on 25.01.2015

@author: Iris
'''

class Aabb(object):
    '''
    Axis Aligned Bounding Box
    '''

    def __init__(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum