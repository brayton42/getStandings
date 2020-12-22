class Team:
    def __init__(self, name, draftSpot, round, wins, exp):
        self.name = name
        self.draftSpot = draftSpot
        self.round = round
        self.wins = wins
        self.expected = exp

    def setWins(self, wins):
        self.wins = wins
