# CENG 3511: Artificial Intelligence Midterm Project
## AI "Catch Game" (Gridworld Chase)

### Project Task 1: Define the Game 

This project fulfills the requirement to "Design and Implement an AI Agent for a Game Environment" .

The game is a 2-player, turn-based "chase" game on a 7x7 grid (Gridworld) .
* **Player (Human):** The "Runner." The goal is to reach the "EXIT" square at (6,6) from the starting position (0,0).
* **AI (Opponent):** The "Guardian." The AI's goal is to **prevent the Runner from reaching the exit,** thereby catching them. The AI starts on the Exit square at (6,6).

---

### Project Tasks 2 & 3: Design and Develop the AI 

The methodology for this project is **"Option 1: Reinforcement Learning Agent"** , using the **Q-Learning** algorithm .

Development was done using **Python** and **Pygame** as recommended . The code is separated into two main files:

* `cache_game.py`: **(The Backend / AI Brain)**
    * Defines all game rules (movement, win conditions).
    * Contains the Q-Learning algorithm, Q-Table, and the Reward/Penalty system.
    * Contains the AI's training simulation function (`train_ai()`).

* `main_pygame.py`: **(The Frontend / Visual Interface)**
    * Contains all Pygame code for drawing and UI.
    * Manages user input (Keyboard/Mouse).
    * Loads the trained AI brain from `cache_game.py` and runs the game.

* `ai_png.png` / `player_png.png`: Character sprites.
* `.gitignore`: Ignores auto-generated files like `__pycache__` and `ai_brain_7x7_guardian.json`.

---

### Project Task 4: Train/Test the AI 

The AI is trained via the `train_ai()` function by simulating **1,000,000 games (EPISODES)**. This training ensures the AI learns the "unbeatable" Guardian strategy.

The trained "brain" is saved to `ai_brain_7x7_guardian.json`.

---

### Submission Guideline: Setup Instructions 

Instructions required to run the project:

**Requirements:**
* Python 3.x
* Pygame library

**Steps:**

1.  Install the required library (Pygame):
    ```bash
    pip install pygame
    ```

2.  Run the game:
    ```bash
    python main_pygame.py
    ```

3.  **IMPORTANT (First-Time Run):** The program will detect that the `ai_brain_7x7_guardian.json` file is missing. The console will show `"[TRAINING STARTED]..."`...")`]. Please wait **2-3 minutes** while the AI is trained.

4.  **Subsequent Runs:** Once the "brain" file is created, the game will start instantly.