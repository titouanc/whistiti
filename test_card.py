from card import Card


def test_card_str():
    assert 'ace of spade' in str(Card(1, 'spade'))
    assert '9 of heart' in str(Card(9, 'heart'))
    assert '10 of diamond' in str(Card(10, 'diamond'))
    assert 'jack of club' in str(Card(11, 'club'))
    assert 'queen of club' in str(Card(12, 'club'))
    assert 'king of club' in str(Card(13, 'club'))


def test_card_parse():
    assert Card(9, 'heart').same_as(Card.parse("9 of heart"))
    assert Card(13, 'club').same_as(Card.parse("king of club"))


def test_parse_all_deck():
    for card in Card.deck52():
        assert card.same_as(Card.parse(str(card)))


def test_deck52():
    all_cards = Card.deck52()
    assert len(all_cards) == 52


def test_different_card_values():
    k, j = Card(13, 'spade'), Card(11, 'heart')
    assert k > j
    assert not j > k
    assert j < k
    assert not j == k
    assert j != k
    assert not j.same_as(k)


def test_ace_is_better():
    k, a = Card(13, 'spade'), Card(1, 'spade')
    assert a > k
    assert not k > a
    assert k < a
    assert not k == a
    assert k != a
    assert not k.same_as(a)


def test_different_card_colors():
    heart, diamond = Card(7, 'heart'), Card(7, 'diamond')
    assert not heart > diamond
    assert not heart < diamond
    assert heart == diamond
    assert not heart != diamond
    assert not heart.same_as(diamond)


def test_compact():
    assert int(Card(1, 'spade')) == 0x01
    assert int(Card(7, 'club')) == 0x17


def test_from_compact():
    for c in Card.COLORS:
        for v in Card.VALUES:
            initial = Card(v, c)
            copy = Card(int(initial))
            assert initial.same_as(copy)
