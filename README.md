# CENG 3511: Artificial Intelligence Midterm Project
## AI "Catch Game" (Gridworld Chase)

### Project Summary
This project was created for the CENG 3511: Artificial Intelligence midterm. [cite_start]It fulfills the course requirement to "Design and Implement an AI Agent for a Game Environment"[cite: 2].

[cite_start]The game is a 2-player, turn-based "chase" game played on a 7x7 grid (Gridworld)[cite: 7]:
* **Player (Human 🏃):** The "Runner." The goal is to reach the "EXIT" square at (6,6) from the starting position (0,0) without being caught.
* **AI (Opponent 🤖):** The "Chaser." [cite_start]The goal is to catch the Runner by landing on the same square[cite: 4].

---

## [cite_start]1. AI Design and Methodology [cite: 18]

[cite_start]From the project options, **"Option 1: Reinforcement Learning Agent"** [cite: 6] was selected.

[cite_start]To meet this requirement, the **Q-Learning** algorithm [cite: 8] [cite_start]was used to "train the AI" [cite: 22] [cite_start]and "understand decision-making in games"[cite: 32].

[cite_start]This 7x7 "Catch Game" [cite: 7] was chosen because its number of "States" (49 AI positions * 49 Human positions = 2401 Total States) is manageable. [cite_start]This allowed the AI's memory (the Q-Table) to be represented with a simple Python dictionary, avoiding the need for more complex methods[cite: 19].

### How the AI's "Brain" (Q-Table) Works

The AI's learning is stored in a Q-Table (a dictionary) defined in `cache_game.py`.

* **State:** This is what the AI looks at to make a decision. It's represented as a tuple: `(ai_position, human_position)`.
* **Actions:** The 5 moves the AI can choose from in any state: `['UP', 'DOWN', 'LEFT', 'RIGHT', 'STAY']`.
* **Reward System:** This is the motivation system that teaches the AI the difference between a "good" and "bad" move. The AI's only goal is to maximize its total score:
    * **Win:** +200 Points (for catching the human)
    * **Lose:** -200 Points (if the human reaches the exit)
    * **Get Closer:** +10 Points (for any move that reduces the distance)
    * **Get Farther:** -10 Points (for any move that increases the distance)
    * **Move Cost:** -1 Point (a small penalty for every move, encouraging the AI to win efficiently)

---

## [cite_start]2. Project Task: Train/Test the AI [cite: 22]

[cite_start]The AI's "training" [cite: 22] is handled by the `train_ai()` function in `cache_game.py`. This function acts as the AI's "school."

* **Training:** The AI runs **500,000 (EPISODES)** simulated games against an opponent that moves randomly.
* **Learning:** After every move, the AI receives a "Reward" or "Penalty." It then uses the Q-Learning formula (the Bellman Equation) to update the "quality" score of that move in its Q-Table (brain).
* **Testing/Evaluation:** After training, this "trained brain" is saved to the `ai_brain_7x7.json` file. [cite_start]In the real game (`main_pygame.py`), the AI stops "exploring" (epsilon=0) and plays only by choosing the best possible move it learned from its Q-Table[cite: 23, 34].

---

## [cite_start]3. Project Task: Development [cite: 20]

[cite_start]This project was developed using **Python** and **Pygame** as recommended in the project PDF[cite: 27]. The project is split into two main files based on the "Separation of Concerns" principle:

* `cache_game.py`: **(The Backend / AI Brain)**. Contains all game rules, the Q-Learning algorithm, and the `train_ai()` function.
* `main_pygame.py`: **(The Frontend / Visual Interface)**. Contains all the Pygame code, handles user input (keyboard/mouse), and loads the trained AI brain from `cache_game.py` to run the game.
* `ai_png.png` / `player_png.png`: The character sprite images.
* `.gitignore`: Prevents unnecessary or auto-generated files (like `__pycache__` and `ai_brain_7x7.json`) from being uploaded to GitHub.

---

## 4. Setup and Run Instructions 

Per the submission guidelines , here are the setup instructions:

**Requirements:**
* Python 3.x
* Pygame library

**Steps:**

1.  Install the required library (Pygame):
    ```bash
    pip install pygame
    ```

2.  (If you downloaded the project as a ZIP, unzip the folder first. If you used `git clone`, skip this step.)

3.  Run the main game file from your terminal:
    ```bash
    python main_pygame.py
    ```

4.  **IMPORTANT (First-Time Run):** When you run the program for the first time, `ai_brain_7x7.json` will not exist. The console will show `"[TRAINING STARTED]..."`. Please wait 1-2 minutes while the program trains the AI to create this "brain" file.

5.  **Subsequent Runs:** Once the "brain" file is created, the program will load it on startup, and the game will begin **instantly**.