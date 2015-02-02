from card import Card
from random import shuffle


class Game(object):
    class Bid(object):
        def __init__(self, name, players):
            self.name, self.players = name, players

        def won_tricks(self, game):
            return filter(lambda t: t['winner'] in self.players, game.tricks)

        def get_trump(self):
            return self.__dict__.get('trump', None)

        def greater_than(self, other):
            return False

        def __gt__(self, other):
            if isinstance(other, type(self)):
                return self.greater_than(other)
            else:
                return BID_RANK.index(type(self)) > BID_RANK.index(type(other))

    class Solo(Bid):
        def __init__(self, player, trump, bonus=0):
            super(Game.Solo, self).__init__("Solo", [player])
            self.required_tricks = 6 + bonus
            self.trump = trump

        def greater_than(self, other):
            return self.required_tricks > other.required_tricks

        def validate(self, game):
            self.won_tricks(game) >= self.required_tricks

    class RuleViolation(Exception):
        pass

    class NotPlayersCard(RuleViolation):
        def __init__(self, player, card):
            super(NotPlayersCard, self).__init__()
            self.player, self.card = player, card

    class NotPlayersTurn(RuleViolation):
        pass

    class CanFollow(RuleViolation):
        def __init__(self, color):
            self.color = color

    class BidNotAllowed(RuleViolation):
        pass

    BID_RANK = [Solo]

    def __init__(self, players):
        assert len(players) == 4
        self.players = tuple(players)
        self.marker = 0
        self.dealer = 0
        self.scores = {p: 0 for p in self.players}
        self.new_turn()

    def new_turn(self):
        cards = Card.deck52()
        shuffle(cards)
        self.cards = {self.players[i]: cards[13*i:13*(i+1)] for i in range(4)}
        self.tricks = []
        self.trump = None
        self.current_trick = []
        self.bids = []
        self.bidder = 0
        self.can_bid = {p: True for p in self.players}

    def current_player(self):
        return self.players[(self.marker + len(self.current_trick))%4]

    def can_drop_card(self, card):
        player = self.current_player()
        current_player_cards = self.cards[player]
        if card not in current_player_cards:
            raise NotPlayersCard(player, card)
        if len(self.current_trick) > 0:
            follow = lambda card: card.color == self.current_trick[0].color
            has_color = len(filter(follow, self.cards[player])) > 0
            if not follow(card) and has_color:
                raise CanFollow(self.current_trick[0].color)
        return True

    def play_card(self, card):
        if self.can_drop_card(card):
            self.cards[self.current_player()].remove(card)
            self.current_trick.append(card)

    def terminate_trick(self):
        best_card = self.current_trick[0]
        winner = self.players[self.marker]
        color = best_card.color
        for i in range(1, 4):
            card = self.current_trick[i]
            follow = card.color == color
            cut = card.color == self.trump and best_card.color != card.color
            higher = card.value > best_card.value
            if follow and higher or cut:
                best_card, winner = card, self.players[(self.marker+i)%4]
        self.marker = self.players.index(winner)
        return winner

    def in_bidding_phase(self):
        return sum(map(len, self.cards.values())) == 52

    def current_bidder(self):
        return self.players[(self.bidder + self.marker) % 4]

    def bid(self, bid):
        if self.current_bidder() not in bid.players:
            raise self.NotPlayersTurn()

        if bid is None:
            self.can_bid[self.current_bidder()] = False
        elif len(self.bids) == 0 or bid > self.bids[-1]:
            self.bids.append(bid)
        else:
            raise self.BidNotAllowed()

        if not self.bidding_phase_finished():
            self.bidder += 1
            while not self.can_bid[self.current_bidder()]:
                self.bidder += 1

    def bidding_phase_finished(self):
        return sum(map(int, self.can_bid.values())) == 1

