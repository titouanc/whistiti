# -*- coding: utf-8 -*-

import settings
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.internet.defer import inlineCallbacks

class WhistitiGame(ApplicationSession):
    def onJoin(self, details):
        uuids = [self.call("hello", str(i)) for i in range(3)]
        print uuids 
 

if __name__ == '__main__':
    options = {
        'url': settings.WAMP_ROUTER,
        'realm': settings.WAMP_REALM,
        'debug': settings.DEBUG,
    }
    ApplicationRunner(**options).run(WhistitiGame)