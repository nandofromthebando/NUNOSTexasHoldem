#!/usr/bin/env python3
import random

class AIPlayer():
    NUMBER = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.hand = []
        self.pot = 0
        self.folded = False
        self.community_cards = []
    
    def clear_hand(self):
        self.hand = []

    def receive_card(self, card):
        self.hand.append(card)

    def get_best_hand_ranking(self):
            hand = self.hand + self.community_cards

            # Check for hand rankings from highest to lowest
            if self.has_royal_flush(hand):
                return "Royal Flush"
            elif self.has_straight_flush(hand):
                return "Straight Flush"
            elif self.has_four_of_a_kind(hand):
                return "Four of a Kind"
            elif self.has_full_house(hand):
                return "Full House"
            elif self.has_flush(hand):
                return "Flush"
            elif self.has_straight(hand):
                return "Straight"
            elif self.has_three_of_a_kind(hand):
                return "Three of a Kind"
            elif self.has_two_pair(hand):
                return "Two Pair"
            elif self.has_pair(hand):
                return "One Pair"
            else:
                return "High Card"

    def has_pair(self, hand):
            ranks_count = {}

            for card in hand:
                rank = card.rank
                ranks_count[rank] = ranks_count.get(rank, 0) + 1

            for rank, count in ranks_count.items():
                if count == 2:
                    return True
            return False

    def has_royal_flush(self, hand):
            sorted_hand = sorted(hand, key=lambda card: AIPlayer.NUMBER.index(card.rank) if card.rank in AIPlayer.NUMBER else -1)
            consecutive_count = 1
            for i in range(1, len(sorted_hand)):
                prev_rank = AIPlayer.NUMBER.index(sorted_hand[i-1].rank)
                current_rank = AIPlayer.NUMBER.index(sorted_hand[i].rank)
                if (current_rank == prev_rank +1):
                    consecutive_count +=1 
                else:
                    consecutive_count =1 
                if consecutive_count ==5:
                    return True
            if (len(sorted_hand) >=2):
                if (sorted_hand[-1].rank == "A" and sorted_hand[0].rank == "2"):
                    if (sorted_hand[1].rank == "3" and sorted_hand[2].rank == "4" and sorted_hand[3].rank == "5"):
                        return True

            return False
        
    def has_straight_flush(self, hand):
        # First, we check if the hand has a flush
            suits_count = {}
            for card in hand:
                suit = card.suit
                suits_count[suit] = suits_count.get(suit, 0) + 1

            flush_suit = None
            for suit, count in suits_count.items():
                if count >= 5:
                    flush_suit = suit
                    break

            if not flush_suit:
                return False

            # Then, we check if the flush has a straight
            sorted_hand = sorted(hand, key=lambda card: AIPlayer.NUMBER.index(card.rank) if card.rank in AIPlayer.NUMBER else -1)
            consecutive_count = 1
            for i in range(1, len(sorted_hand)):
                prev_rank = AIPlayer.NUMBER.index(sorted_hand[i - 1].rank)
                current_rank = AIPlayer.NUMBER.index(sorted_hand[i].rank)

                # If the current card has the same suit as the flush suit and has a consecutive rank
                if sorted_hand[i].suit == flush_suit and current_rank == prev_rank + 1:
                    consecutive_count += 1
                else:
                    consecutive_count = 1

                if consecutive_count == 5:
                    return True

            # Check for the special case of a "Wheel" Straight Flush (A, 2, 3, 4, 5 of the same suit)
            if sorted_hand[-1].rank == "A" and sorted_hand[0].rank == "2" and sorted_hand[1].rank == "3" \
            and sorted_hand[2].rank == "4" and sorted_hand[3].rank == "5" and sorted_hand[-1].suit == flush_suit:
                return True

            return False
    def has_four_of_a_kind(self, hand):
            ranks_count = {}
            for card in hand:
                rank = card.rank
                ranks_count[rank] = ranks_count.get(rank, 0) + 1

            for rank, count in ranks_count.items():
                if count == 4:
                    return True

            return False

    def has_full_house(self, hand):
        return self.has_three_of_a_kind(hand) and self.has_two_pair(hand)

    def has_flush(self, hand):
        suits_count = {}
        for card in hand:
            suit = card.suit
            suits_count[suit] = suits_count.get(suit, 0) + 1

        for count in suits_count.values():
            if count >= 5:
                return True

        return False

    def has_straight(self, hand):
        sorted_hand = sorted(hand, key=lambda card: AIPlayer.NUMBER.index(card.rank) if card.rank in AIPlayer.NUMBER else -1)
        consecutive_count = 1
        for i in range(1, len(sorted_hand)):
            prev_rank = AIPlayer.NUMBER.index(sorted_hand[i - 1].rank)
            current_rank = AIPlayer.NUMBER.index(sorted_hand[i].rank)
            if current_rank == prev_rank + 1:
                consecutive_count += 1
            else:
                consecutive_count = 1

            if consecutive_count == 5:
                return True

        # Check for the special case of a "Wheel" Straight (A, 2, 3, 4, 5)
        if (len(sorted_hand) >=2) and sorted_hand[-1].rank == "A" and sorted_hand[0].rank == "2" and sorted_hand[1].rank == "3" and sorted_hand[2].rank == "4" and sorted_hand[3].rank == "5":
                return True


        return False

    def has_three_of_a_kind(self, hand):
        ranks_count = {}
        for card in hand:
            rank = card.rank
            ranks_count[rank] = ranks_count.get(rank, 0) + 1

        for rank, count in ranks_count.items():
            if count == 3:
                return True

        return False

    def has_two_pair(self, hand):
        pairs_count = 0
        ranks_count = {}
        for card in hand:
            rank = card.rank
            ranks_count[rank] = ranks_count.get(rank, 0) + 1
            if ranks_count[rank] == 2:
                pairs_count += 1
        return pairs_count >= 2

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.hand = []
        self.pot = 0
        self.folded = False
        self.community_cards = []

    def recieve_hand(self, cards):
        self.hand = cards

    def make_bet(self, decision, amount):
        if (decision == "fold"):
            self.clear_hand()
        elif (decision == "call"):
            self.pot += amount
            self.balance -= amount
        elif (decision == "raise"):
            raise_amount = self.get_raise_amount()
            self.pot += amount + raise_amount 
            self.balance -= (amount + raise_amount)

    def get_raise_amount(self):
         return (.1*self.balance)
        

    def receive_card(self, card):
        self.hand.append(card)

    def clear_hand(self):
        self.hand = []

    def make_bet_decision(self, current_bet, hand):
        hand_rank = self.get_best_hand_ranking()

        if hand_rank in ["Royal Flush", "Straight Flush", "Four of a Kind", "Full House"]:
            return "raise"
        elif hand_rank in ["Flush", "Straight", "Three of a Kind"]:
            return "call"
        else:
            if random.random() < 0.2:  
                return "fold"
            else:
                return "call"
