#!/usr/bin/env python3
import random
from AIPlayers import AIPlayer
from player import Player, UserPlayer

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
        self.cards = [Card(rank, suit) for rank in NUMBER for suit in SUITS]
        random.shuffle(self.cards)

    def deal(self):
        if not self.cards:
            return None
        return self.cards.pop()


class TexasHoldemGame:
    def __init__(self):
        self.deck = Deck()
        self.players = []
        self.community_cards = []
        self.pot = 0
        self.big_blind = 10
        self.current_player_index = 0  #for turns
        self.players_in_round = []
        self.last_raiser = None

    def add_player(self, player):
        self.players.append(player)

    def handle_call_action(self, player, amount_to_call):
        if (amount_to_call < player.balance):
            amount_to_call = player.balance
        player.make_bet(amount_to_call)
        self.pot+= amount_to_call
        self.current_player_index = (self.current_player_index + 1) % len(self.players)


    def make_ai_bets(self, current_bet, choice):
        players_in_round = self.players.copy()
        for player in players_in_round:
            if isinstance(player, AIPlayer):
                bet_choice = choice
                raise_amount = player.make_bet_decision(current_bet, player.hand)

                if bet_choice == "fold":
                    players_in_round.remove(player)
                elif bet_choice == "call":
                    amount_to_call = current_bet - player.pot
                    self.handle_call_action(player, amount_to_call)
                elif bet_choice == "raise":
                    self.handle_raise_action(player, current_bet, raise_amount)
                    current_bet += raise_amount
                    last_raiser = player

    def add_ai_player(self, name, initial_balance):
        ai_player = AIPlayer(name, initial_balance)
        self.players.append(ai_player)

    def deal_hole_cards(self):
        for _ in range(2):
            for player in self.players:
                card = self.deck.deal()
                if card:
                    player.receive_card(card)
        # After dealing, display each player's hole cards
        user_player = [player for player in self.players if isinstance(player, UserPlayer)][0]
        print(f"Your Hole Cards: {', '.join(str(card) for card in user_player.hand)}")

    def clear_community_cards(self):
        self.community_cards = []
    
    def reset_round(self):
        # Clear the community cards at the beginning of each round
        self.clear_community_cards()

    def reset_community_cards(self):
        print("Resetting community cards...")
        self.clear_community_cards()
        for player in self.players:
            player.folded = False

    def deal_community_cards(self, num_cards):
        for _ in range(num_cards):
            card = self.deck.deal()
            if card:
                self.community_cards.append(card)
        print(f"Community Cards: {', '.join(str(card) for card in self.community_cards)}")


    def get_game_info(self, player):
        return (f"Pot: {self.pot}, Hand: {player.hand}, Community Cards: {self.community_cards}")

    def handle_raise_action(player, current_bet, raise_amount):
        if (raise_amount > player.balance):
            raise_amount = player.balance
        player.make_bet(raise_amount)
        self.pot+= raise_amount
        current_bet = raise_amount
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    
    def all_in_players(self):
        for player in self.players:
            if (player.balance == 0 and player.make_bet_decision != "fold"):
                print (f"{player} is all in")

    def insufficient_funds(self, player, current_bet):
        if (player.balance < current_bet):
            print(f"{player.name} doesn't have enough chips, going all in")
            self.pot += player.balance
            player.pot += amount_to_call
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
        self.current_player_index = 0

        if len(self.players) > 1:
            self.deal_community_cards(3)
            self.collect_bets()

        if len(self.players) > 1:
            self.deal_community_cards(1)
            self.collect_bets()

        if len(self.players) > 1:
            self.deal_community_cards(1)
            self.collect_bets()

        if len(self.players) >= 1:
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
            best_ranking = player.get_best_hand_ranking()
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

    def collect_bets(self):
        current_bet = self.big_blind
        last_raiser = None
        players_in_round = self.players.copy()
        self.current_player_index = 0
        valid_options = ["fold", "check", "call", "raise"]
        if not self.players:
            print("No players in the round.")
            return
        while (len(players_in_round) > 1):
            current_player = players_in_round[self.current_player_index]
            if(current_player == last_raiser):
                break
            if(current_player.folded):
                players_in_round.remove(player)
                continue
            if isinstance(current_player, AIPlayer):
                bet_choice = current_player.make_bet_decision(current_bet, current_player.hand)
                self.make_ai_bets(current_bet, bet_choice) 
            elif isinstance(current_player, UserPlayer):
                print(self.get_game_info(current_player))
                bet_choice = current_player.make_bet_decision(valid_options)
                current_player.make_bet(bet_choice, current_bet) 
                if bet_choice == "fold":
                    # Handle the player's fold action
                    self.players_in_round.remove(current_player)
                elif bet_choice == "call":
                    # Handle the player's call action
                    amount_to_call = self.current_bet - current_player.pot
                    self.handle_call_action(current_player, amount_to_call)
                elif bet_choice == "reset":
                    # Allow players to reset the community cards (optional)
                    self.reset_community_cards()   
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            print(f"{current_player.name} {bet_choice}")
        # Check if players have enough chips to call or raise
        for player in players_in_round:
            if (player.make_bet_decision != "fold"):
                amount_to_call = current_bet - player.pot
                self.insufficient_funds(player, amount_to_call)

        # Handle players who are all-in
        self.all_in_players()
        print("End of Round!")
        self.showdown()
        self.next_turn()

        
    def next_turn(self):
        num_players = len(self.players)
        while True:
            self.current_player_index = (self.current_player_index + 1) % num_players
            player = self.players[self.current_player_index]
            if not player.folded:
                break


if __name__ == "__main__":
    # Create a new game instance
    game = TexasHoldemGame()

    # Create AI players with desired names and initial balances
    ai_player1 = AIPlayer("AIPlayer1", 1000)
    ai_player2 = AIPlayer("AIPlayer2", 1000)
    ai_player3 = AIPlayer("AIPlayer3", 1000)

    user_player = UserPlayer(f"User", 1000)

    # Add the AI players to the game
    game.add_player(ai_player1)
    game.add_player(ai_player2)
    game.add_player(ai_player3)
    game.add_player(user_player)



    # Start the game
    while len(game.players) > 1:
        game.start_new_round()

    # At this point, the game has ended, and there is a winner.