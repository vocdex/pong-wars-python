# Pong Wars
<div align="center">
    <img src="./pics/4_players.gif" width="400" alt="Pong Wars" />
    <img src="./pics/2_players.gif" width="400" alt="Pong Wars" /> 
</div>

## Description
Pong Wars is a colorful and dynamic variation of the classic Pong game implemented in Python using Pygame. In this game, two balls compete to fill the game area with their respective colors.

The current version of the game supports two modes: 2 players and 4 players.
## Dependencies
The project requires Python along with the following libraries:
```bash
pip install pygame moviepy natsort
```
## Usage
```bash
python 2_players.py
python 4_players.py
```
#### Options
```bash
args:
-- record_frames: record frames for video and makes a gif
-- seed: seed for random number generator
```

## Credits
1. This code is inspired by Koen van Gilst's JavaScript implementation of [Pong Wars](https://github.com/vnglst/pong-wars)
2. Relevant Hacker News discussion: [Show HN: Pong Wars – A colorful and dynamic variation of the classic Pong game](https://news.ycombinator.com/item?id=39159418)

## What's next?
1. Build Gymnasium environment for Pong Wars to train RL agents