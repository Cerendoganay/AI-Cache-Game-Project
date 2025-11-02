# CENG 3511: Artificial Intelligence Midterm Project
## AI "Catch Game" (Gridworld Chase)

[cite_start]This project is an implementation of an AI agent for a 2-player "Catch Game" environment, submitted for the CENG 3511: Artificial Intelligence course[cite: 1, 2].

* **Player (Human):** The "Runner" . The goal is to reach the "EXIT" square.
* **Opponent (AI):** The "Chaser" . The goal is to catch the Runner by landing on the same square.

The AI does *not* use a pre-designed algorithm like Minimax. Instead, it is **trained** using Reinforcement Learning to *learn* the optimal strategy to intercept the player.

---

## 1. AI Methodology: Q-Learning

[cite_start]As required by the project brief for a learning agent [cite: 6][cite_start], this AI uses the **Q-Learning** algorithm[cite: 8].

### How it Works
The AI's "brain" is a **Q-Table** (a simple Python dictionary). This table stores the "quality" (Q-value) for every possible action in every possible state.

* **State (`state`):** A tuple representing `(ai_position, human_position)`.
    * *Example:* `((6, 6), (0, 0))`
* **Actions (`action`):** A list of moves: `['UP', 'DOWN', 'LEFT', 'RIGHT', 'STAY']`.
* **Reward/Penalty System:** The AI is trained by receiving rewards/penalties for its actions:
    * **Win:** +200 (for catching the human)
    * **Lose:** -200 (if the human reaches the exit)
    * **Get Closer:** +10 (for reducing the distance to the human)
    * **Get Farther:** -10 (for increasing the distance)
    * **Move:** -1 (a small penalty for every move to encourage efficiency)

### AI Training
The AI is trained by running the `train_ai()` function located in `cache_game.py`. This function simulates **500,000 games** against a random-moving opponent.

During this process, the Q-Table is filled using the Q-Learning formula. This "trained brain" is then saved to `ai_brain_7x7.json`.

**Note:** The `.gitignore` file is configured to *prevent* this large `ai_brain_7x7.json` file from being uploaded to GitHub. The program will **automatically train and create this file** on the user's computer the first time it is run.

---

## 2. Project Files

* `cache_game.py`: **(The AI Brain & Game Logic)**. Contains all game rules, the Q-Learning algorithm, and the `train_ai()` function.
* `main_pygame.py`: **(The Game Frontend)**. Contains all Pygame code for visuals, handles user input (keyboard/mouse), and loads the trained AI brain to play against.
* `ai_png.png` / `player_png.png`: Image assets for the characters.
* `.gitignore`: Ignores `__pycache__` and the `ai_brain_7x7.json` file.

---

## 3. Installation and How to Run

[cite_start]These instructions fulfill the "README file with setup instructions" requirement.

**Prerequisites:**
* Python 3.x
* Pygame library

**Instructions:**

1.  **Clone the repository (or download the ZIP):**
    ```bash
    git clone [YOUR_GITHUB_REPO_URL]
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd [YOUR_PROJECT_FOLDER_NAME]
    ```

3.  **Install the required library (Pygame):**
    ```bash
    pip install pygame
    ```

4.  **Run the game:**
    ```bash
    python main_pygame.py
    ```

5.  **First-Time Run:** The first time you run the program, the console will show **"[TRAINING STARTED]..."**. This process will take 1-2 minutes as the AI trains itself.
6.  **Subsequent Runs:** After training, the AI's "brain" (`ai_brain_7x7.json`) will be saved, and the game will start instantly every time after that.