# Pong Wars Strategy
A variation of [Pong Wars](https://github.com/vnglst/pong-wars). In this variation, players can affect the war actively by overwriting others' areas rather than just watch whatever happens. And the game has a time limit now, so there will be an end and a winner.

The current version of the game supports two modes: 2 players and 4 players.

## Description
After the war starts, players can PAUSE the game at any time and OVERWRITE an area with their own color if not in cooldown. The war is time limited, so when it ends the one holding the largest area will be the winner.

## Dependencies
The project requires Python (3.6 or later) along with the following libraries:
```bash
pip install numpy pygame moviepy natsort
```
## Usage
```bash
python --player_num 2
python --player_num 4
```
#### Options
```bash
args:
-- record_frames: record frames for video and makes a gif
-- seed: seed for random number generator
```

## Credits
This code is inspired by vocdex's Pygame implementation of [pong-wars-python](https://github.com/vocdex/pong-wars-python)

## What's next?
1. The game balance is under adjustment, more tests needed.
2. Maybe no overwrite during the last part of the game would be better.
3. Code Refactoring.
4. Complete game flow including choosing player num at the start and being able to restart without closing the game.
5. Better UI.
