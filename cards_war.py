from collections import deque
import datetime as dt
import random

import polars as pl


class Card:
    """
    Represents a single card in a deck, with a number (rank) and color (suit).

    Attributes:
        number (int): The rank of the card (1-13).
        color (str): The suit of the card ("BC", "BS", "RD", or "RH").
    """

    def __init__(self, number=0, color="0"):
        self.number = number
        self.color = color

    def __gt__(self, other):
        return self.number > other.number

    def __eq__(self, other):
        return self.number == other.number

    def __repr__(self) -> str:
        return f"{self.number} {self.color}"


class Player:
    """
    Represents a player in the game, with a name, hand of cards, and won cards.

    Attributes:
        name (str): The name of the player.
        hand (collections.deque[Card]): The player's current hand of cards.
        won_cards (list[Card]): The cards the player has won during the game.
    """

    def __init__(self, name: str):
        self.name = name
        self.hand: deque[Card] = deque(maxlen=56)
        self.won_cards: list[Card] = list()

    def __repr__(self) -> str:
        return self.name

    @property
    def score(self):
        """
        Returns the player's total score, which is the sum of cards in their hand and won cards.

        Returns:
            int: The player's score.
        """
        return len(self.hand) + len(self.won_cards)

    def refill_hand(self):
        """
        Refills the player's hand from their won cards if it's empty, after shuffling the won cards.
        """
        random.shuffle(self.won_cards)
        self.hand = deque(self.won_cards[:], maxlen=56)
        self.won_cards = list()

    def isEmptyHand(self):
        """
        Checks if the player's hand is empty.

        Returns:
            bool: True if the hand is empty, False otherwise.
        """
        return len(self.hand) == 0

    def playCard(self):
        """
        Plays a card from the player's hand. If the hand is empty, refills from won cards.

        Returns:
            Card: The card played from the hand.
        """
        if self.score == 0:
            return Card()
        if self.isEmptyHand():
            self.refill_hand()
        return self.hand.popleft()


class cardsWar:
    """
    Represents a game of Cards War with multiple players.

    Attributes:
        players (list[Player]): The list of players in the game.
        round (int): The current round number.
        scoreSchema (plars.Schema): The schema for the score DataFrame.
        score (plars.DataFrame): The DataFrame containing game score data.
        latestResults (dict): A dictionary storing the results of the latest round.
    """

    def __init__(self, playersCount=2):
        """
        Initializes a game of Cards War with the specified number of players.

        Args:
            playersCount (int, optional): The number of players in the game. Defaults to 2.

        Raises:
            AssertionError: If the number of players is less than 2 or not a divisor of 52.
        """
        assert playersCount >= 2 and 56 % playersCount == 0
        self.players = [Player(f"Player {i + 1}") for i in range(playersCount)]
        self.round = 0
        self.scoreSchema = (
            {"Round": pl.Int16}
            | {player.name: pl.Int16 for player in self.players}
            | {"Total": pl.Int16}
        )
        self.score = pl.DataFrame(schema=self.scoreSchema)
        self.latestResults = {}

    def CreateShuffleDeck(self):
        """
        Creates a shuffled deck of cards with 13 ranks ("BC", "BS", "RD", "RH" suits).

        Returns:
            list[Card]: A list of shuffled cards.
        """
        deck = list()
        deck = [
            Card(num + 1, color)
            for num in range(13)
            for color in ["BC", "BS", "RD", "RH"]
        ]
        random.shuffle(deck)
        return deck

    def distributeCards(self):
        """
        Distributes cards from the shuffled deck equally to each player.
        """
        deck = self.CreateShuffleDeck()
        cardsPerPlayer = len(deck) // len(self.players)
        for i, player in enumerate(self.players):
            player.hand.extend(deck[i * cardsPerPlayer : (i + 1) * cardsPerPlayer])
        return

    def get_played_cards(self, players: list[Player]):
        """
        Gets the cards played by each player in the round.

        Args:
            players (list[Player]): The list of players participating in the round.

        Returns:
            list[Card]: A list of cards played by the players.
        """
        return [player.playCard() for player in players]

    def find_winning_players(self, players: list[Player], playedCards: list[Card]):
        """
        Finds the players with the highest card played in the round.

        Args:
            played_cards (list[Card]): A list of cards played by the players.

        Returns:
            tuple: A tuple containing a list of winning players and the highest card played.
        """
        winingPlayers: list[Player] = []
        highestCard = Card()
        for i, card in enumerate(playedCards):
            if card.number == 0:  # Ignore losers
                continue
            elif card > highestCard:
                winingPlayers = [players[i]]
                highestCard = card
            elif card == highestCard:
                winingPlayers.append(players[i])
        return winingPlayers

    def update_scoreboard(self):
        """
        Updates the scoreboard with the current round and player scores.

        Args:
            winner (Player): The winning player.
        """
        self.latestResults = (
            {"Round": self.round}
            | {player.name: player.score for player in self.players}
            | {"Total": sum([player.score for player in self.players])}
        )
        self.score.extend(pl.DataFrame(self.latestResults, schema=self.scoreSchema))
        return

    def award_cards(self, winner: Player, playedCards: list[Card], field: list[Card]):
        """
        Awards the played cards to the winning player.

        Args:
            winner (Player): The winning player.
            played_cards (list[Card]): A list of cards played by all players in the round.
            field (list[Card]): A list of cards played in previous rounds during a war.
        """
        winner.won_cards.extend([card for card in playedCards if card.number != 0])
        winner.won_cards.extend([card for card in field if card.number != 0])
        return

    def playRound(self, players: list[Player], field: list[Card] = []):
        """
        Plays a single round of Cards War. Handles cases where multiple players play the highest card.

        Args:
            players (list[Player]): The list of players participating in the round.
            field (list[Card], optional): A list of cards played in previous rounds during a war. Defaults to [].
        """
        self.round += 1
        playedCards = self.get_played_cards(players)
        winingPlayers = self.find_winning_players(players, playedCards)
        if len(winingPlayers) > 1:
            self.breakDraw(field, playedCards, winingPlayers)
            return
        self.award_cards(winingPlayers[0], playedCards, field)
        self.update_scoreboard()
        return

    def breakDraw(self, field, playedCards, winingPlayers):
        field.extend(playedCards + [player.playCard() for player in winingPlayers])
        self.playRound(winingPlayers, field)

    def isWinner(self):
        """
        Checks if a player has won the game by having all 52 cards.

        Returns:
            bool: True if a player has won, False otherwise.
        """
        for player in self.players:
            if player.score >= 52:
                print(f"{player.name} won the game!!!")
                return True
        return False

    def playGame(self):
        start_time = dt.datetime.now().strftime("%Y-%m-%d %H_%M_%S")
        self.distributeCards()
        self.update_scoreboard()
        while not self.isWinner():
            self.playRound(self.players, [])
            print(self.latestResults)
        self.score.write_csv(f"Results/{start_time} Score.csv")


if __name__ == "__main__":
    cardsWar(2).playGame()
