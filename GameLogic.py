#!/usr/bin/env python3
from blessed import Terminal
import random 
import sys
sys.path.append('/path/to/directory')
from AIPlayers import AIPlayer
from player import Player, UserPlayer

# Define constants for card ranks and suits
NUMBER = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
term = Terminal()
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def display_card(rank, suit):
        # Visual for more attractive inerface
        suit_symbols = {'Hearts': '\u2665', 'Diamonds': '\u2666', 'Clubs': '\u2663', 'Spades': '\u2660'}
        card = f"""
        ┌─────────┐
        │ {rank:<2}      │
        │         │
        │  {suit} │
        │         │                       
        │      {rank:>2} │
        └─────────┘
        """
        return card


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

    def make_ai_bets(self, current_bet, choice):
        players_in_round = self.players.copy()
        for player in players_in_round:
            if isinstance(player, AIPlayer) and not player.folded:
                bet_decision = player.make_bet_decision(current_bet, player.hand)
                
                if bet_decision == "fold":
                    player.folded = True
                elif bet_decision == "call":
                    amount_to_call = current_bet - player.pot
                    player.make_bet("call", amount_to_call)
                elif bet_decision == "raise":
                    raise_amount = player.get_raise_amount()
                    current_bet += raise_amount
                    player.make_bet("raise", current_bet)

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
        with term.location(0, term.height - 10):  # Adjust vertical position as needed
            print("Your Hole Cards:")
            for card in user_player.hand:
                rank = card.rank
                suit = card.suit
                print(Card.display_card(rank, suit))

        # Move the cursor to the next line after displaying the hole cards
        with term.location(0, term.height - 4):  # Adjust vertical position as needed
            pass
    
    def reset_round(self):
        # Clear the community cards at the beginning of each round
        self.clear_community_cards()
        for player in self.players:
                player.folded = False

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
        with term.location(0, term.height - 10):  # Adjust vertical position as needed
            print("Community Cards:")
            for card in user_player.hand:
                rank = card.rank
                suit = card.suit
                print(Card.display_card(rank, suit))

        # Move the cursor to the next line after displaying the hole cards
        with term.location(0, term.height - 4):  # Adjust vertical position as needed
            pass


    def get_game_info(self, player):
        return (f"Pot: {self.pot}, Hand: {player.hand}, Community Cards: {self.community_cards}")


    
    def all_in_players(self):
        for player in self.players:
            if (player.balance == 0 and player.make_bet_decision != "fold"):
                print (f"{player} is all in")

    def insufficient_funds(self, player, current_bet):
        if (player.balance < current_bet):
            print(f"{player.name} doesn't have enough chips, going all in")
            self.pot += player.balance
            player.pot += player.balance
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

        for player in active_players:
            self.pot  = self.pot + player.pot

        # If only one player is left or all others are all-in, they automatically win
        if len(active_players) == 1:
            winner = active_players[0]
            winner.balance += self.pot
            print(f"{winner.name} wins { self.pot} chips, with no showdown!")
            return

        # Evaluate hands and determine the best hand ranking for each active player
        player_rankings = {}
        for player in active_players:
            player_hand = player.hand + self.community_cards
            best_ranking = player.get_best_hand_ranking()
            player_rankings[player] = best_ranking
            print(f"{player.name} best hand ranking: {best_ranking}")
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
        
        if not self.players:
            print("No players in the round.")
            return
        while (len(players_in_round) > 1):
            current_player = players_in_round[self.current_player_index]
            if(current_player == last_raiser):
                break
            if isinstance(current_player, AIPlayer) and not current_player.folded:
                bet_choice = current_player.make_bet_decision(current_bet, current_player.hand)
                self.make_ai_bets(current_bet, bet_choice) 
            elif isinstance(current_player, UserPlayer):
                print(f"Current Bet to call: {current_bet} chips \nYour Current Balance {current_player.balance}")
                bet_choice = current_player.make_bet_decision()
                current_player.make_bet(bet_choice, current_bet) 
                if bet_choice == "f":
                    # Handle the player's fold action
                    self.players_in_round.remove(current_player)
                elif bet_choice == "c":
                    # Handle the player's call action
                    amount_to_call = current_bet - current_player.pot
                    self.insufficient_funds(current_player, amount_to_call)
                elif bet_choice == "r":
                    # Allow players to reset the community cards (optional)
                    self.reset_community_cards()   
            print(f"{current_player.name} {bet_choice}")
            if(self.current_player_index != (len(players_in_round)-1)):
                self.current_player_index = (self.current_player_index + 1) 
            else:
                break   

         

        # Handle players who are all-in
        
        self.all_in_players()
        print("End of Round!")
        self.showdown()
        self.next_turn()

        
    def next_turn(self):
        num_players = len(self.players)
        self.current_player_index = 0
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


    print(term.bold('Welcome to Texas Hold\'em Poker!'))
    # Start the game
    while len(game.players) > 1:
        game.start_new_round()
        game.players = [player for player in game.players if player.balance > 0] # removes players who ae all out of chips
    # At this point, the game has ended, and there is a winner.