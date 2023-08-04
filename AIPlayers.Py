#!/usr/bin/env python3
from player import Player

class AIPlayer(Player):
    def make_bet_decision(self, current_bet):
        if self.has_royal_flush(self.hand):
            return "raise"
        elif self.has_straight_flush(self.hand):
            return "raise"
        elif self.has_four_of_a_kind(self.hand):
            return "raise"
        elif self.has_full_house(self.hand):
            return "raise"
        elif self.has_flush(self.hand):
            return "call"
        elif self.has_straight(self.hand):
            return "call"
        elif self.has_three_of_a_kind(self.hand):
            return "call"
        elif self.has_two_pair(self.hand):
            return "fold"
        elif self.has_pair(self.hand):
            return "fold"
        else:
            return "fold"
