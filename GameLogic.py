import random

# Define constants for card ranks and suits
NUMBER = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in RANKS for suit in SUITS]
        random.shuffle(self.cards)

    def deal(self):
        if not self.cards:
            return None
        return self.cards.pop()

class Player:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.hand = []

    def receive_card(self, card):
        self.hand.append(card)

    def clear_hand(self):
        self.hand = []

    def get_player_input():
        # Prompt the player for input
        decision = input("Enter your betting decision (fold/call/raise): ").strip().lower()

        # Validate the input (optional)
        valid_options = ["fold", "call", "raise"]
        while decision not in valid_options:
            print("Invalid input. Please enter 'fold', 'call', or 'raise'.")
            decision = input("Enter your betting decision: ").strip().lower()

        return decision

        

    def make_bet_decision(self, current_bet):
        decision = get_player_input()

        # Check the player's decision and act accordingly
        if (decision == "fold"):
            return "fold"
        elif (decision == "call"):
            return "call"
        elif (decision == "raise"):
            raise_amount = get_raise_amount()
            return "raise", raise_amount
        else:
            # Invalid input, prompt the player again or handle the error
            print("Invalid input. Please enter 'fold', 'call', or 'raise'.")

    pass

    def make_bet(self, amount):
        if (decision == "fold"):
            #Player gets removed
        elif (decision == "call"):
            #Add bet to pot
        elif (decision == "raise"):
            #Add raise to bet and pot

    def get_raise_amount(self):
        # Implement the logic for the player to decide how much to raise.
        # Return the raise amount based on user input or a calculated value.
        pass

class TexasHoldemGame:
    def __init__(self):
        self.deck = Deck()
        self.players = []
        self.community_cards = []
        self.pot = 0

    def add_player(self, player):
        self.players.append(player)

    def deal_hole_cards(self):
        for _ in range(2):
            for player in self.players:
                card = self.deck.deal()
                if card:
                    player.receive_card(card)

    def deal_community_cards(self, num_cards):
        for _ in range(num_cards):
            card = self.deck.deal()
            if card:
                self.community_cards.append(card)

    def reset_game(self):
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0
        for player in self.players:
            player.clear_hand()

    def start_new_round(self):
        self.reset_game()
        self.deal_hole_cards()
        self.collect_bets()

        if len(self.players) > 1:
            self.deal_community_cards(3)
            self.collect_bets()

        if len(self.players) > 1:
            self.deal_community_cards(1)
            self.collect_bets()

        if len(self.players) > 1:
            self.deal_community_cards(1)
            self.collect_bets()

        if len(self.players) > 1:
            self.showdown()
class Bets:
    def collect_bets(self):
        current_bet = self.big_blind
        last_raiser = None
        players_in_round = self.players.copy

        while (len(players_in_round) > 1):
            for players in players_in_round:
                if(player == last_raiser):
                    break
                if(players.folded):
                    players_in_round.remove(player)
                continue

                bet_choice = player.make_bet_decision(current_bet)
                
                if(bet_choice == "fold"):
                    players_in_round.remove(player)
                    continue

                if (bet_choice == "call"):
                    amount_to_call = current_bet - player.current_bet
                    player.make_bet(amount_to_call)
                    continue

                if (bet_choice == "raise"):
                    raise_amount = player.get_raise_amount()
                    player.make_bet(current_bet + raise_amount)
                    current_bet += raise_amount
                    last_raiser = player
                    continue




# Example usage:
if __name__ == "__main__":
    game = TexasHoldemGame()
    player1 = Player("Alice", 1000)
    player2 = Player("Bob", 1000)

    game.add_player(player1)
    game.add_player(player2)

    while len(game.players) > 1:
        game.start_new_round()

    # At this point, the game has ended, and there is a winner.
