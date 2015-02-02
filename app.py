# -*- coding: utf-8 -*-

import settings
import uuid
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.types import PublishOptions
from twisted.internet.defer import inlineCallbacks
from twisted.internet.task import deferLater
from twisted.internet import reactor
from game import Game

def sleep(dt):
    return deferLater(reactor, dt, lambda: None)

class WhistitiGame(ApplicationSession):
    publishToMe = PublishOptions(excludeMe=False)

    def __init__(self, *args, **kwargs):
        ApplicationSession.__init__(self, *args, **kwargs)
        self.clients = {}  # uid -> player name
        self.queue = set() # uids of players waiting for a game
        self.games = {}    # player uid -> game obj
        self.seed = uuid.uuid4() # App UUID

    @inlineCallbacks
    def start_game(self, *args):
        yield sleep(1)
        print "Starting new game"
        players = list(self.queue)
        self.queue = set(players[4:])
        players = players[:4]
        game = Game(players)
        players_names = [self.clients[uid] for uid in players]
        for p in players:
            self.publish(p + '.start_game', {
                "cards": map(int, game.cards[p]),
                "players": players_names
            })
            self.games[p] = game
        print "Started game with", players_names, game.cards

    def hello(self, player_name):
        """Client greet the server and queue for a game"""
        uid = str(uuid.uuid5(self.seed, str(player_name)))
        self.clients[uid] = player_name
        if uid not in self.queue:
            qsize = len(self.queue) + 1
            for client in self.queue:
                self.publish(client + '.queue_growth', {"queue_size": qsize})
            self.queue.add(uid)
            if len(self.queue) == 4:
                print "Trigger start game"
                self.publish('trigger_start_game', [], options=self.publishToMe)
        print "Got hello from", player_name, "given UUID", uid
        return {"queue_size": len(self.queue), "uuid": uid}

    def bid(self, uid, bid_name):
        if uid not in self.games:
            return {"error": "no_game"}
        game = self.games[uid]
        if not game.in_bidding_phase():
            return {"error": "not_bidding_phase"}
        player_name = self.clients[uid]
        if game.current_bidder() != player_name:
            return {"error": "not_your_turn"}
        return {"ok": bid_name}

    @inlineCallbacks
    def onJoin(self, details):
        yield self.register(self.hello, 'hello')
        yield self.subscribe(self.start_game, 'trigger_start_game')
        yield self.register(self.bid, 'bid')
        print "Application", self.seed, "ready"
 

if __name__ == '__main__':
    options = {
        'url': settings.WAMP_ROUTER,
        'realm': settings.WAMP_REALM,
        'debug': settings.DEBUG,
    }
    ApplicationRunner(**options).run(WhistitiGame)