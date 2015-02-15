'''
Created on 01.12.2014

@author: Iris
'''

from Network.NetworkWrapper import NetworkWrapper
from Component.Container import container
from Updater.RateUpdater import RateUpdater
from State.SessionHandler import SessionHandler
from Service.ConfigReader import ConfigReader
from Time.TimeSource import TimeSource
from Updater.Updater import Updater
from Service.Messenger import Messenger

configReader = ConfigReader(filename = 'config.cfg', uid = 'parameters')
timeSource = TimeSource('time_source')
updater = Updater('updater')
rateUpdater = RateUpdater('rate_updater')

network = NetworkWrapper(
    numClients = configReader.getInt('server', 'num_players'),
    port = configReader.getInt('server', 'port'),
    updateRate = configReader.getInt('server', 'network_update_rate'),
    uid = 'network_wrapper'
)

sessionHandler = SessionHandler()
messenger = Messenger('messenger')

container.add(configReader)
container.add(timeSource)
container.add(updater)
container.add(rateUpdater)
container.add(network)
container.add(sessionHandler)
container.add(messenger)
container.activate()

while(True):
    updater.update()
