# CENG 3511: AI "Catch Game" (Unbeatable Guardian) 

This project is an AI agent developed for the CENG 3511: Artificial Intelligence course. It features a "Guardian" AI that learns, through Reinforcement Learning, to play an "unbeatable" game of "Catch" against a human player.

* **Player (Human ):** The "Runner." Starts at `(0,0)` and tries to reach the "EXIT" at `(6,6)`.
* **AI (Opponent ):** The "Guardian." Starts *on* the Exit at `(6,6)`. Its goal is to intercept the player.

---

##  Methodology

This project implements **"Option 1: Reinforcement Learning Agent"** from the course brief.

### 1. Algorithm Choice: Q-Learning
The AI uses the **Q-Learning** algorithm . This was chosen because it is a powerful, model-free algorithm ideal for a discrete environment like our 7x7 grid. It allows the AI to learn optimal behavior through trial-and-error (training).

### 2. The Q-Table (The AI's Brain)
The AI's "brain" is a Q-Table (`Q_table`), implemented as a Python dictionary. It maps `(state, action)` pairs to expected future rewards.

* **State:** A tuple representing `(ai_position, human_position)`. This results in (49 * 49) = **2401** manageable states, which avoids the need for a complex Deep Q-Network (DQN) .
* **Action:** The 5 possible moves: `['UP', 'DOWN', 'LEFT', 'RIGHT', 'STAY']`.

### 3. The Q-Learning Update Rule
The Q-Table is updated after every move during training using the Bellman Equation:

$Q(s,a) = Q(s,a) + \alpha [r + \gamma \max_{a'} Q(s',a') - Q(s,a)]$

Where the key parameters (defined in `cache_game.py`) are:
* **\( \alpha \)** (Learning Rate): `0.1`
* **\( \gamma \)** (Discount Factor): `0.95`
* **\( r \)** (Reward): The reward received from the `calculate_reward()` function.

### 4. Exploration vs. Exploitation
The AI is trained using an **ε-greedy policy**.
* Epsilon (ε) starts at `1.0` (100% exploration).
* It "decays" (azalır) over 1,000,000 episodes to `0.01` (1% exploration).
* This ensures the AI explores the environment thoroughly before mastering the optimal strategy.

### 5. Implementation Details
* **Language:** Python 
* **Libraries:** Pygame , `json`, `time`, `random`
* **Files:**
    * `cache_game.py`: Contains the AI logic, Q-Learning algorithm, and training loop.
    * `main_pygame.py`: Contains the Pygame visuals, game loop, and user input handling.

---

##  Training and Results

### Training
The AI is trained by simulating **1,000,000 episodes** (games) via the `train_ai()` function. The trained "brain" is then saved to `ai_brain_7x7_guardian.json`.

### Results: The "Unbeatable Guardian" Strategy
The AI's *only* motivation is to maximize its score, which is defined by this simple system:
* **`REWARD_WIN = +200`**
* **`REWARD_LOSE = -200`**
* **`REWARD_MOVE = -1`**

Through training, the AI learns that the *only* way to risk getting the `-200` (Lose) penalty is to move off the `(6,6)` Exit square. Therefore, the optimal (highest Q-value) strategy it learns is to use the **'STAY'** action and "guard" the Exit square.

The `check_winner()` function is sequenced to check for a "catch" (`ai_pos == human_pos` == state['human_pos']:`]) *before* checking for an "exit" (`human_pos == EXIT_POS` == EXIT_POS:`]). This guarantees an **AI win** when the player moves onto the `(6,6)` square. The player can never win.


## How to Run 

**1. Install Pygame:**
```bash
pip install pygame
```

**2. Run the game:**
```bash
python main_pygame.py
```

**3. IMPORTANT (First-Time Run):**
The program will detect that the `ai_brain_7x7_guardian.json` file is missing. The console will show `"[TRAINING STARTED]..."`...")`]. Please wait **2-3 minutes** while the AI is trained.

**4. Subsequent Runs:**
Once the "brain" file is created, the game will load the trained AI and start instantly.

---
📘 Developed by Ceren Doğanay as part of the CENG 3511: Artificial Intelligence course project .