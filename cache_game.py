# cache_game.py (7x7 "KUSURSUZ GARDİYAN" VERSİYONU)

import random
import json
import os
import time

# --------------------------------------------------------------------------------
# PART 1: GAME ENGINE (7x7 "UNBEATABLE" SETUP)
# --------------------------------------------------------------------------------

# --- 1.1. Game Constants (7x7) ---
GRID_SIZE = 7
BRAIN_FILE = 'ai_brain_7x7_guardian.json' 

HUMAN_PLAYER = 1
AI_PLAYER = 2

ACTIONS = {
    'UP': (-1, 0),
    'DOWN': (1, 0),
    'LEFT': (0, -1),
    'RIGHT': (0, 1),
    'STAY': (0, 0)
}
ACTION_NAMES = list(ACTIONS.keys())

# --- UNBEATABLE STRATEGY (7x7) ---
# AI starts *ON* the Exit square. It will learn that leaving this square
# is the only way to lose, so it will "guard" it by staying put.
START_POS_HUMAN = (0, 0) # Top-left
EXIT_POS = (6, 6) # Exit (Bottom-right)
START_POS_AI = (6, 6) # AI starts ON the Exit 

# --- 1.2. Game Engine Functions ---

def create_game_state():
    return {
        'human_pos': START_POS_HUMAN,
        'ai_pos': START_POS_AI,
        'current_turn': HUMAN_PLAYER
    }

def is_valid_position(r, c):
    return 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE

def get_valid_moves(position):
    r, c = position
    valid_actions = []
    for action_name, (dr, dc) in ACTIONS.items():
        if is_valid_position(r + dr, c + dc):
            valid_actions.append(action_name)
    return valid_actions

def perform_move(state, player, action):
    new_state = state.copy()
    pos_key = 'human_pos' if player == HUMAN_PLAYER else 'ai_pos'
    if action in get_valid_moves(new_state[pos_key]):
        r, c = new_state[pos_key]
        dr, dc = ACTIONS[action]
        new_state[pos_key] = (r + dr, c + dc)
    new_state['current_turn'] = AI_PLAYER if player == HUMAN_PLAYER else HUMAN_PLAYER
    return new_state

def check_winner(state):
    """ 
    CRITICAL: Check for AI win (catch) *before* checking for Human win (exit).
    This ensures if both land on the exit square at the same time, the AI wins.
    """
    if state['ai_pos'] == state['human_pos']:
        return AI_PLAYER # AI caught the Human
    if state['human_pos'] == EXIT_POS:
        return HUMAN_PLAYER # Human reached the exit
    return None # Game is not over

# --------------------------------------------------------------------------------
# PART 2: AI BRAIN & TRAINING (Q-LEARNING ALGORITHM)
# --------------------------------------------------------------------------------
# This is the core "Artificial Intelligence" part of the project.
# --------------------------------------------------------------------------------

# --- 2.1. Q-Learning Hyperparameters ---
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.95
# Increased episodes for the 7x7 grid (2401 states)
EPISODES = 1000000 # 1 Million training games

epsilon = 1.0
MIN_EPSILON = 0.01
EPSILON_DECAY = 0.999995 # Slower decay for more exploration

# --- 2.2. Reward / Penalty System (THE FLAW IS FIXED) ---
# The "get closer" / "get farther" rewards have been REMOVED.
# This was the "kusur" (flaw) in the algorithm.
# The AI's *only* motivation now is to avoid the -200 (Lose) penalty.
REWARD_WIN = 200      # Big reward for catching the human.
REWARD_LOSE = -200    # Big penalty if the human escapes.
REWARD_MOVE = -1      # Small penalty for every move (encourages efficiency).

# --- 2.3. The AI "Brain" (Q-Table) ---
Q_table = {}

# --------------------------------------------------------------------------------
# PART 3: Q-LEARNING HELPER FUNCTIONS
# --------------------------------------------------------------------------------

def get_state(game_state):
    """ Converts the game_state dict into a simple, hashable tuple (Key). """
    return (game_state['ai_pos'], game_state['human_pos'])

def get_or_create_q_values(state):
    """ Looks up the 'state' in the Q_table, or creates it if new. """
    if state not in Q_table:
        Q_table[state] = {action: 0.0 for action in ACTION_NAMES}
    return Q_table[state]

def choose_action_for_ai(state, epsilon_value):
    """ Algorithm: Epsilon-Greedy Strategy """
    valid_actions = get_valid_moves(state[0])
    
    if random.uniform(0, 1) < epsilon_value:
        return random.choice(valid_actions) # Explore
    else:
        # Exploit
        q_values = get_or_create_q_values(state)
        best_q_value = -float('inf')
        best_actions = []
        
        for action in valid_actions:
            if q_values[action] > best_q_value:
                best_q_value = q_values[action]
                best_actions = [action]
            elif q_values[action] == best_q_value:
                best_actions.append(action)
        
        return random.choice(best_actions)

def calculate_reward(old_state, new_state, winner):
    """ Calculates the reward based on the SIMPLIFIED rules in PART 2.2. """
    if winner == AI_PLAYER:
        return REWARD_WIN
    if winner == HUMAN_PLAYER:
        return REWARD_LOSE
    
    # "Get closer/farther" rewards are REMOVED to fix the flaw.
    return REWARD_MOVE 

# --------------------------------------------------------------------------------
# PART 4: THE TRAINING LOOP
# --------------------------------------------------------------------------------
# This fulfills the "Train/Test the AI" task from the PDF.
# --------------------------------------------------------------------------------

def train_ai():
    """ 
    The main training function. This will run 'EPISODES' (e.g., 1,000,000)
    simulated games to fill the Q-Table.
    """
    global epsilon, Q_table
    
    print(f"[TRAINING STARTED]... Playing {EPISODES} games (7x7 Guardian). This will take a few minutes.")
    start_time = time.time()
    
    for episode in range(EPISODES):
        game_state = create_game_state()
        game_over = False
        
        while not game_over:
            current_state_key = get_state(game_state) 

            if game_state['current_turn'] == AI_PLAYER:
                ai_action = choose_action_for_ai(current_state_key, epsilon)
                new_game_state = perform_move(game_state, AI_PLAYER, ai_action)
                winner = check_winner(new_game_state)
                if winner: game_over = True
                
                reward = calculate_reward(game_state, new_game_state, winner)
                
                # === THE Q-LEARNING ALGORITHM (Bellman Equation) ===
                old_q_values = get_or_create_q_values(current_state_key)
                old_q_value = old_q_values[ai_action]
                
                next_state_key = get_state(new_game_state)
                next_q_values = get_or_create_q_values(next_state_key)
                max_next_q_value = 0.0 if game_over else max(next_q_values.values())
                
                new_q_value = old_q_value + LEARNING_RATE * (reward + DISCOUNT_FACTOR * max_next_q_value - old_q_value)
                
                Q_table[current_state_key][ai_action] = new_q_value
                
                game_state = new_game_state
                
            else: # During training, the 'Human' opponent plays randomly.
                human_valid_moves = get_valid_moves(game_state['human_pos'])
                human_action = random.choice(human_valid_moves)
                game_state = perform_move(game_state, HUMAN_PLAYER, human_action)
                
                winner = check_winner(game_state)
                if winner:
                    game_over = True
                    if winner == HUMAN_PLAYER:
                        Q_table[current_state_key][ai_action] = old_q_value + LEARNING_RATE * (REWARD_LOSE - old_q_value)

        if epsilon > MIN_EPSILON:
            epsilon *= EPSILON_DECAY
            
        if (episode + 1) % 100000 == 0: # Her 100,000'de bir rapor ver
            print(f"  ...Training {episode + 1}/{EPISODES} complete. (Epsilon: {epsilon:.4f})")

    end_time = time.time()
    print(f"[TRAINING COMPLETE!] Total time: {end_time - start_time:.2f} seconds.")

# --------------------------------------------------------------------------------
# PART 5: SAVING & LOADING THE BRAIN
# --------------------------------------------------------------------------------

def save_brain(filename=BRAIN_FILE):
    """ Saves the Q-Table (the AI's brain) to a .json file. """
    print(f"Saving AI brain to '{filename}'...")
    try:
        string_q_table = {str(k): v for k, v in Q_table.items()}
        with open(filename, 'w') as f:
            json.dump(string_q_table, f)
        print("Save successful.")
    except Exception as e:
        print(f"ERROR: Could not save brain! {e}")

def load_brain(filename=BRAIN_FILE):
    """ Loads the pre-trained Q-Table from a .json file. """
    global Q_table
    print(f"Loading trained AI brain from '{filename}'...")
    try:
        with open(filename, 'r') as f:
            string_q_table = json.load(f)
            Q_table = {eval(k): v for k, v in string_q_table.items()}
        print("Brain loaded successfully.")
        return True
    except FileNotFoundError:
        print(f"WARNING: Saved brain file '{filename}' not found.")
        return False
    except Exception as e:
        print(f"ERROR: Could not load brain! {e}")
        return False