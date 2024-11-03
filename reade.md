Cards War: A Python Simulation

This Python code simulates the card game "Cards War."

How to Run:

Install Required Libraries:
Ensure you have the following libraries installed:

Bash
pip install polars
Use code with caution.

Run the Script:
Execute the Python script:

Bash
python cards_war.py
Use code with caution.

Game Rules:

Dealing: A standard deck of 52 cards is shuffled and distributed equally among players.
Playing: Players simultaneously flip over their top card.
Winning: The player with the higher card takes both cards.
War: If both cards are equal, a "war" occurs. Each player plays three cards face down, then one face up. The highest face-up card wins the war and all the cards.
Code Structure:

Card Class: Represents a single playing card with a number and color.
Player Class: Represents a player with a hand of cards and a list of won cards.
CardsWar Class:
Initializes the game with a specified number of players.
Shuffles and distributes cards.
Simulates rounds of play, including war scenarios.
Tracks scores and determines the winner.
Additional Notes:

The code utilizes the polars library for efficient data manipulation and analysis.
The playRound method has been broken down into smaller functions for better readability and modularity.
The code includes docstrings to explain the purpose of classes, methods, and functions.
Potential Enhancements:

Implement different game variations with varying rules.
Add a graphical user interface (GUI) for a visual experience.
Introduce AI opponents with different playing strategies.
Analyze game statistics and player performance.
Enjoy playing Cards War!