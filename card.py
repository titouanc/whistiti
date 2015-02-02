import re

class Card(object):
    """
    Card objects have a value (1..13),
    and a color (spade, club, diamond or heart),
    along with methods for comparing them
    """
    # Allowed card colors
    COLORS = ('spade', 'club', 'diamond', 'heart')
    # Allowed card values
    VALUES = [i for i in range(2, 14)] + [1]
    # {value: name} for named cards
    NAMES = {1: 'ace', 11: 'jack', 12: 'queen', 13: 'king'}
    # {name: value} for named cards
    REVERSE_NAMES = {v: k for k, v in NAMES.iteritems()}
    # Parser for texts like "ace of spade"
    PARSE_REGEXP = re.compile(
        r'(1?\d|' + '|'.join(NAMES.values()) +
        ') of (' + '|'.join(COLORS) + ')'
    )

    def __init__(self, value, color=None):
        if color is None:
            # parse compact representation
            if isinstance(value, int):
                colorid, value = (value >> 4) & 0xf, value & 0xf
                color = self.COLORS[colorid]
            # copy color and value from another card
            elif isinstance(value, Card):
                color, value = value.color, value.value
        assert value in self.VALUES
        assert color in self.COLORS
        self.color, self.value = color, value

    def __str__(self):
        name = self.NAMES.get(self.value, str(self.value))
        return "{{%s of %s #%02x}}" % (name, self.color, int(self))
    __repr__ = __str__

    def __gt__(self, other):
        """Return True if this card has a greater value than other"""
        assert isinstance(other, Card)
        if self.value == 1 and other.value != 1:
            return True
        elif self.value > other.value and other.value != 1:
            return True
        return False

    def __eq__(self, other):
        """Return true if other has the same value as self"""
        return self.value == other.value

    def __ne__(self, other):
        """Return true if other has a different value of self"""
        return not self == other

    def same_as(self, other):
        """Return True if other is identical to this card"""
        return (self == other) and (self.color == other.color)

    def __int__(self):
        """Return the compact form (int)  of this card"""
        upper, lower = self.COLORS.index(self.color), self.value
        return (upper << 4) | lower

    @classmethod
    def parse(klass, text):
        match = klass.PARSE_REGEXP.search(text)
        assert match
        value, color = match.group(1), match.group(2)
        if value in klass.REVERSE_NAMES:
            return Card(klass.REVERSE_NAMES[value], color)
        return Card(int(value), color)

    @classmethod
    def deck52(klass):
        """Return a list containing the std 52 cards deck, not randomized"""
        return [klass(v, c) for c in klass.COLORS for v in klass.VALUES]
