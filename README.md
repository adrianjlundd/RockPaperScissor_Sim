# Rock Paper Scissors Simulation (pygame)

This is a simple, self-contained Rock–Paper–Scissors (RPS) world built with `pygame`. Agents (Rock, Paper, Scissors) move around the screen, bounce off edges, and convert each other on collision according to RPS rules. The simulation ends when only one species remains. Press `R` to restart.


## Watch the Simulation on YouTube  
Press the image below to watch or this [link](https://youtu.be/YI2b4zbsgaQ):

[![Watch the simulation on YouTube](data/interface.png)](https://youtu.be/YI2b4zbsgaQ)

## Features
- Object-oriented design with an `Agent` class
- Bouncing, organic movement with gentle random acceleration
- Collision conversion with cooldown
- HUD: species counts, FPS, elapsed time, centered title, and a win banner
- Optional PNG sprites (`rock.png`, `paper.png`, `scissors.png`); otherwise colored circles are used

## Requirements
- Python 3.8+
- `pygame` (see `requirements.txt`)

## Install
```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run
```bash
python main.py
```

If `rock.png`, `paper.png`, and `scissors.png` exist in the same folder, they will be used automatically. Otherwise, the simulation draws colored circles.

## Controls
- `Esc` or `Q`: Quit
- `R`: Restart simulation

## Notes
- The simulation automatically pauses when one species remains and shows “X Wins!”
- Adjust parameters like population size, speeds, and cooldown near the top of `main.py`.


