'''
Created on 13.02.2015

@author: Iris
'''
from Component.Component import Component
import ConfigParser

class ConfigReader(Component):
    '''
    Config Reader
    '''


    def __init__(self, filename , uid = None):
        Component.__init__(self, uid)
        self._parser = ConfigParser.ConfigParser()
        self._parser.read(filename)
        
    def getInt(self, section, configName):
        return self._parser.getint(section, configName)
    
    def getBoolean(self, section, configName):
        return self._parser.getboolean(section, configName)
        
    def getFloat(self, section, configName):
        return self._parser.getfloat(section, configName)
