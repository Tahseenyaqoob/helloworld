# Python Snake Game

A classic retro Snake game built with Python using the native `turtle` graphics framework. This project requires zero external dependencies and runs right out of the box on Windows, macOS, and Linux.

---

## Features

- **Zero External Dependencies:** Built using Python's standard library (`turtle`, `time`, `random`).
- **Score & High Score Tracking:** Keeps track of your current score and updates your high score dynamically during gameplay.
- **Classic Arcade Mechanics:** Grid-aligned movement, collision detection (walls and self-collision), and snake growth.
- **Cross-Platform Compatibility:** Runs seamlessly on macOS, Windows, and Linux.

---

## System Requirements

- **Python:** 3.6 or higher.

---

## Getting Started

### 1. Clone or Download

Clone this repository or download the source files directly to your local machine:

```bash
git clone https://github.com/your-username/snake-game.git
cd snake-game
```

### 2. Run the Game

No `pip install` required! Simply execute the script with Python:

#### macOS / Linux
```bash
python3 snake.py
```

#### Windows
```bash
python snake.py
```

---

## Controls

| Key | Action |
| :--- | :--- |
| **Up Arrow** ($\uparrow$) | Move Up |
| **Down Arrow** ($\downarrow$) | Move Down |
| **Left Arrow** ($\leftarrow$) | Move Left |
| **Right Arrow** ($\rightarrow$) | Move Right |

> **Note:** The snake cannot reverse directly into itself (e.g., pressing Down while moving Up will be ignored to prevent self-collision).

---

## Game Rules

1. **Objective:** Eat the red food targets to grow your snake and increase your score.
2. **Scoring:** Each piece of food grants **10 points**.
3. **Game Over Conditions:**
   - Hitting any of the four outer boundaries (walls).
   - Running into your own body.
4. **Reset:** Upon a game over, your score resets to zero, your high score is retained, and the snake returns to the center.

---

## Customization Options

You can easily customize game variables at the top of `snake.py`:

```python
# Speed control: Lower values make the game faster
DELAY = 0.1

# Window dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
```