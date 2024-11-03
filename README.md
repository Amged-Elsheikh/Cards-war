# Cards War: A Python Simulation

This Python code simulates the card game "Cards War."

## How to Run:

Install Required Libraries:
Ensure you have the following libraries installed:

Bash

```pip install polars```

###  Run the Script:
Execute the Python script:

Bash

```python cards_war.py```

## Game Rules:

**Dealing**: A standard deck of 52 cards is shuffled and distributed equally among players.

**Playing******: Players simultaneously flip over their top card.

**Winning**: The player with the higher card takes both cards.

**War**: If both cards are equal, a "war" occurs. Each player plays three cards face down, then one face up. The highest face-up card wins the war and all the cards.

## Code Structure:

**Card Class**: Represents a single playing card with a number and color.\\
**Player Class**: Represents a player with a hand of cards and a list of won cards.\\
**CardsWar Class**:
<ul>
<li>Initializes the game with a specified number of players.</li>
<li>Shuffles and distributes cards.</li>
<li>Simulates rounds of play, including war scenarios.</li>
<li>Tracks scores and determines the winner.</li>
</ul>


## Additional Notes:
<ul>
<li>The code utilizes the polars library for efficient data manipulation and analysis.</li>
<li>The playRound method has been broken down into smaller functions for better readability and modularity.</li>
<li>The code includes docstrings to explain the purpose of classes, methods, and functions.</li>
</ul>

## Potential Enhancements:
<ul>
<li>Implement different game variations with varying rules.</li>
<li>Add a graphical user interface (GUI) for a visual experience.</li>
<li>Analyze game statistics and player performance.</li>
</ul>

**Enjoy playing Cards War!**
