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
        self.pot = 0

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
        valid_options = ["fold", "call", "raise"]
        # Check the player's decision and act accordingly
        if (decision == "fold"):
            return "fold"
        elif (decision == "call"):
            return "call"
        elif (decision == "raise"):
            raise_amount = get_raise_amount()
            return "raise", raise_amount
        else:
            print("Invalid input. Please enter 'fold', 'call', or 'raise'.")

    def current_bet(self):
        while True:
            bet_input = input("Enter your bet: ")
            try:
                curr_bet = float(bet_input)
                if curr_bet <= 0:
                    print("Invalid bet amount. Please enter a positive value.")
                else:
                    return curr_bet
            except ValueError:
                print("Invalid input. Please enter a valid number.")


    def make_bet(self, decision, amount):
        if (decision == "fold"):
            self.clear_hand
        elif (decision == "call"):
            self.pot += amount
        elif (decision == "raise"):
            raise_amount = get_raise_amount(self)
            self.pot += amount + raise_amount 


    def get_raise_amount(self):
         while True:
            try:
                raise_amt = float(input("Enter the amount you would like to raise: "))
                if raise_amt <= 0:
                    print("Invalid amount. Please enter a positive value.")
                else:
                    return raise_amt
            except ValueError:
                print("Invalid input. Please enter a valid number.")

   """ def get_best_hand_ranking(self):
        for (player in self.players):
            if (player.hand == A, K, Q, J, 10 & self.suit = self.suit)
                print("{winner.name} got a Royal Flush")
                if ((player.hand[0] == player.hand[0]) == ):"""








class TexasHoldemGame:
    def __init__(self):
        self.deck = Deck()
        self.players = []
        self.community_cards = []
        self.pot = 0
        self.big_blind = 0

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
    
    def all_in_players(self)
        for(players in self.players):
            if (player.balance = 0 & player.make_bet_decision != "fold")
                print (f"{player} is all in")

    def insufficient_funds(self, player, current_bet):
        if (player.balance < current_bet):
            print(f"{player.name} doesn't have enough chips, going all in")
            self.pot += player.balance
            player.pot += balance
            player.balance = 0


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

    def showdown(self):
        active_players = [player for player in self.players if not player.folded]

        # If only one player is left or all others are all-in, they automatically win
        if len(active_players) == 1:
            winner = active_players[0]
            winner.balance += self.pot
            print(f"{winner.name} wins the pot with no showdown!")
            return

        # Evaluate hands and determine the best hand ranking for each active player
        player_rankings = {}
        for player in active_players:
            player_hand = player.hand + self.community_cards
            best_ranking = get_best_hand_ranking(player_hand)
            player_rankings[player] = best_ranking

        # Find the highest hand ranking among the active players
        highest_ranking = max(player_rankings.values())

        # Find the players with the highest ranking (potential ties)
        winners = [player for player, ranking in player_rankings.items() if ranking == highest_ranking]

        # Distribute the pot among the winners
        pot_per_winner = self.pot // len(winners)
        remaining_chips = self.pot % len(winners)

        for winner in winners:
            winner.balance += pot_per_winner
            if remaining_chips > 0:
                winner.balance += 1
                remaining_chips -= 1

        print("Showdown results:")
        for winner in winners:
            print(f"{winner.name} wins {pot_per_winner} chips.")
        if remaining_chips > 0:
            print(f"Remaining {remaining_chips} chips in the pot are not evenly divisible and go to a random winner.")

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
        # Check if players have enough chips to call or raise
        for player in players_in_round:
            if (player.make_bet_decision != "fold"):
                amount_to_call = current_bet - player.pot
                self.handle_insufficient_chips(player, amount_to_call)

        # Handle players who are all-in
        self.handle_all_in_players()




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
