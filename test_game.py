import game
import pytest


def create_sorted_game():
    players = game.Card.COLORS
    g = game.Game(players)
    # Distribute cards in a predefined manner
    g.cards = {c: [game.Card(i, c) for i in range(1, 14)] for c in g.players}
    return g


def test_1_game_turn():
    g = create_sorted_game()
    assert g.in_bidding_phase()
    for i in range(4):
        assert g.current_player() == g.players[i]
        g.play_card(g.cards[g.players[i]][0])
    winner = g.terminate_trick()
    assert g.current_player() == winner
    assert winner == g.players[0]
    assert not g.in_bidding_phase()


def test_must_do_more():
    g = create_sorted_game()
    assert g.in_bidding_phase()

    g.bid(g.Solo(g.players[0], "heart"))
    assert g.current_bidder() == g.players[1]
    with pytest.raises(g.BidNotAllowed):
        g.bid(g.Solo(g.players[1], "heart"))


def test_not_his_turn():
    g = create_sorted_game()
    assert g.in_bidding_phase()

    g.bid(g.Solo(g.players[0], "heart"))
    assert g.current_bidder() == g.players[1]
    with pytest.raises(g.NotPlayersTurn):
        g.bid(g.Solo(g.players[2], "heart"))
