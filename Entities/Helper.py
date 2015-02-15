'''
Created on 13.02.2015

@author: Iris
'''
from Component.PolyVisual import PolyVisual
import random

def createRectangle(width, height):
    halfWidth = width * 0.5
    halfHeight = height * 0.5
    vertices = (
        (-halfWidth, halfHeight),
        (-halfWidth, -halfHeight),
        (halfWidth, -halfHeight),
        (halfWidth, halfHeight)
    )
    
    return PolyVisual(vertices)

def spreadValue(value, spread):
    s = spread * value
    return value - s + random.uniform(0, 2) * s