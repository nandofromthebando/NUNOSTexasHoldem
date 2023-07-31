# Texas Hold'em Poker Game

Welcome to the Texas Hold'em Poker Game project! This is a simple text-based implementation of the popular Texas Hold'em poker variant with the added feature of user accounts and password storage. The game is written in Python and is in its early stages of development. Feel free to contribute, fix bugs, or collaborate on this project!

## How to Play

1. Clone the repository to your local machine:
git clone https://github.com/yourusername/texas-holdem-poker.git


2. Ensure you have Python installed. The game is compatible with Python 3.

3. Install the required dependencies. You can do this by running the following command:
pip install bcrypt


4. Run the game:
python main.py

5. Follow the on-screen instructions to play the game. The game will guide you through each round of betting and dealing of cards.

## Game Rules

- The game is played with a standard deck of 52 cards.
- Each player starts with a certain amount of chips (balance).
- Players are dealt two private cards (hole cards) at the beginning.
- Subsequently, five community cards are dealt face up on the table over three rounds: the flop (3 cards), the turn (1 card), and the river (1 card).
- Players aim to create the best possible hand using their hole cards and the community cards.
- The player with the best hand at the end of the final betting round wins the pot.

## Classes and Modules

### `Card` Class

Represents a single playing card with a rank and suit.

### `Deck` Class

Represents a deck of cards and handles shuffling and dealing.

### `Player` Class

Represents a player in the game with a name, balance (chips), and hand (cards). Players can receive cards, make betting decisions, and place bets.

### `TexasHoldemGame` Class

The main class that orchestrates the game. It manages the deck, players, community cards, and the betting rounds.

### `Bets` Class

Handles the logic for collecting bets and managing the betting rounds.

## Database

The game now includes a database to store user accounts and passwords securely. The database schema includes a table named `players` with columns for `id`, `name`, `password_hash`, `balance`, and `game_state`.

## Contribution Guidelines

We welcome any contributions to the project. If you'd like to contribute, please follow these guidelines:

1. Fork the repository and create a new branch for your feature or bug fix.
2. Make your changes and ensure the code follows the project's coding style.
3. Write unit tests for new functionalities and ensure all tests pass.
4. Submit a pull request to the main repository.

## Bugs and Issues

If you encounter any bugs or issues while playing the game or using the user accounts feature, please report them on the GitHub issue tracker. Include a detailed description of the problem, steps to reproduce it, and any error messages if applicable.

## Collaborate and Reach Out

We encourage collaboration and welcome any suggestions or feedback you might have. Feel free to reach out!
