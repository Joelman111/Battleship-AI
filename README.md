# Battleship 

A GUI-based implementation of Battleship with an AI that uses the user's past ship placements to inform its future guesses.

## Description

A GUI-based implementation of the classic 2-player board game Battleship using Pygame. The game is single player with a lightweight AI that makes intelligent guesses based on the most likely remaining spots on the board and where the user has placed their ships in the past to inform its future guesses. The AI wins within 6 moves (on average) of the computationally-hard provably optimal algorithm, but is far performant. The game has music, sound effects, and basic graphics. This was a hackathon project completed by 3 college freshmen in under 15 hours, which earned us third place out of ~70 submissions.

## Getting Started

### Installing

```
git clone https://github.com/Joelman111/Battleship-AI.git
pip install -r requirements.txt
```

### Executing program

```
python main.py
```

## Help

In game, you can hit 'i' to toggle the help screen, which will tell you all of the options for the current page. Once the game is over, hit 'm' to go back to the main menu and play again. The game will generate a "battleship.txt" file to persist user ship placements- to reset user ship placements, just delete this file.

## Authors

Joel Miller (joelgmiller11@gmail.com), John Solomon, Sebastian Gamboa

## Demo Video
[![Battleship](https://img.youtube.com/vi/W21yq_cOw68/0.jpg)](https://youtu.be/W21yq_cOw68?si=TBEX-L8NPkrjnUG2)