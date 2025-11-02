import random
import json
import os
import time

# --------------------------------------------------------------------------------
# PART 1: GAME ENGINE (The Rules)
# --------------------------------------------------------------------------------
# This section defines the "environment" or the rules of the game.
# --------------------------------------------------------------------------------

# --- 1.1. Game Constants ---
GRID_SIZE = 7
BRAIN_FILE = 'ai_brain_7x7.json' # The file where the AI's trained memory is stored.

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

START_POS_HUMAN = (0, 0) # Top-left
START_POS_AI = (6, 6) # Bottom-right
EXIT_POS = (6, 6) # Human's target

# --- 1.2. Game Engine Functions ---

def create_game_state():
    """ Returns a dictionary representing the starting state of the game. """
    return {
        'human_pos': START_POS_HUMAN,
        'ai_pos': START_POS_AI,
        'current_turn': HUMAN_PLAYER
    }

def is_valid_position(r, c):
    """ Checks if a (row, col) coordinate is inside the 7x7 grid. """
    return 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE

def get_valid_moves(position):
    """ Returns a list of valid actions ('UP', 'DOWN'...) from a given position. """
    r, c = position
    valid_actions = []
    for action_name, (dr, dc) in ACTIONS.items():
        if is_valid_position(r + dr, c + dc):
            valid_actions.append(action_name)
    return valid_actions

def perform_move(state, player, action):
    """ Takes the current state and returns a NEW state after the action. """
    new_state = state.copy()
    
    pos_key = 'human_pos' if player == HUMAN_PLAYER else 'ai_pos'
        
    if action in get_valid_moves(new_state[pos_key]):
        r, c = new_state[pos_key]
        dr, dc = ACTIONS[action]
        new_state[pos_key] = (r + dr, c + dc)
    
    new_state['current_turn'] = AI_PLAYER if player == HUMAN_PLAYER else HUMAN_PLAYER
    return new_state

def check_winner(state):
    """ Checks if the game has ended and returns the winner. """
    if state['ai_pos'] == state['human_pos']:
        return AI_PLAYER # AI caught the Human
    if state['human_pos'] == EXIT_POS:
        return HUMAN_PLAYER # Human reached the exit
    return None # Game is not over


# --------------------------------------------------------------------------------
# PART 2: AI BRAIN & TRAINING (Q-LEARNING ALGORITHM)
# --------------------------------------------------------------------------------
# This is the core "Artificial Intelligence" part of the project (CENG 3511).
# We are using the Q-Learning algorithm (a Reinforcement Learning method)
# as specified in "Project Option 1".
# --------------------------------------------------------------------------------

# --- 2.1. Q-Learning Hyperparameters ---
# These are the settings that control how the AI learns.
LEARNING_RATE = 0.1    # (Alpha) How quickly the AI adopts new information.
DISCOUNT_FACTOR = 0.95 # (Gamma) How much the AI values future rewards (vs. immediate rewards).
EPISODES = 500000      # The number of simulated games the AI will play to train itself.

# --- Epsilon-Greedy Strategy (Exploration vs. Exploitation) ---
epsilon = 1.0          # Start at 1.0 (100% random exploration).
MIN_EPSILON = 0.01     # Minimum 1% random exploration.
EPSILON_DECAY = 0.99995 # Slowly decrease epsilon after each game.

# --- 2.2. Reward / Penalty System ---
# This is the AI's "motivation". The AI's goal is to maximize its total reward.
REWARD_WIN = 200      # Big reward for catching the human.
REWARD_LOSE = -200    # Big penalty if the human escapes.
REWARD_MOVE = -1      # Small penalty for every move (encourages efficiency).
REWARD_GET_CLOSER = 10 # Reward for getting closer.
REWARD_GET_FARTHER = -10 # Penalty for moving farther away.

# --- 2.3. The AI "Brain" (Q-Table) ---
# This is the AI's memory, implemented as a simple Python dictionary.
# Key = The "State" -> e.g., ((0,1), (3,4)) -> "AI is at (0,1), Human is at (3,4)"
# Value = A dictionary of "Actions" and their "Quality" (Q) scores -> e.g., {'UP': 10, 'DOWN': -5}
Q_table = {}

# --------------------------------------------------------------------------------
# PART 3: Q-LEARNING HELPER FUNCTIONS
# --------------------------------------------------------------------------------

def get_state(game_state):
    """ 
    Converts the game_state dictionary into a simple, hashable tuple.
    This tuple is used as the "Key" in our Q_table.
    This simple state representation is why we *don't* need a complex Deep Q-Network (DQN).
    """
    return (game_state['ai_pos'], game_state['human_pos'])

def get_or_create_q_values(state):
    """ 
    Looks up the 'state' in the Q_table. 
    If the AI has never seen this state before, it creates a new entry for it with all Q-values at 0.
    """
    if state not in Q_table:
        Q_table[state] = {action: 0.0 for action in ACTION_NAMES}
    return Q_table[state]

def choose_action_for_ai(state, epsilon_value):
    """ 
    Algorithm: Epsilon-Greedy Strategy
    This function decides the AI's move.
    1. With (epsilon_value) probability: Choose a random valid move (Exploration).
    2. With (1 - epsilon_value) probability: Choose the best-known move from the Q-Table (Exploitation).
    """
    valid_actions = get_valid_moves(state[0]) # state[0] = AI's position
    
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
        
        return random.choice(best_actions) # Choose the best known action

def calculate_reward(old_state, new_state, winner):
    """ Calculates the reward/penalty based on the rules in PART 2.2. """
    if winner == AI_PLAYER:
        return REWARD_WIN
    if winner == HUMAN_PLAYER:
        return REWARD_LOSE

    def get_distance(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    old_distance = get_distance(old_state['ai_pos'], old_state['human_pos'])
    new_distance = get_distance(new_state['ai_pos'], new_state['human_pos'])
    
    reward = REWARD_MOVE 
    if new_distance < old_distance:
        reward += REWARD_GET_CLOSER
    elif new_distance > old_distance:
        reward += REWARD_GET_FARTHER
    return reward

# --------------------------------------------------------------------------------
# PART 4: THE TRAINING LOOP (The AI's "School")
# --------------------------------------------------------------------------------
# This is where the AI "learns". It simulates 'EPISODES' number of games
# against a random-moving opponent to fill the Q-Table.
# [cite_start]This fulfills the "Train/Test the AI" task [cite: 22] from the PDF.
# --------------------------------------------------------------------------------

def train_ai():
    """ 
    The main training function. This will run 'EPISODES' (e.g., 500,000)
    simulated games to fill the Q-Table.
    """
    global epsilon, Q_table
    
    print(f"[TRAINING STARTED]... Playing {EPISODES} games. This may take a moment.")
    start_time = time.time()
    
    for episode in range(EPISODES):
        game_state = create_game_state()
        game_over = False
        
        while not game_over:
            current_state_key = get_state(game_state) 

            if game_state['current_turn'] == AI_PLAYER:
                # 1. Choose action (Epsilon-Greedy)
                ai_action = choose_action_for_ai(current_state_key, epsilon)
                # 2. Perform action
                new_game_state = perform_move(game_state, AI_PLAYER, ai_action)
                winner = check_winner(new_game_state)
                if winner: game_over = True
                
                # 3. Calculate reward
                reward = calculate_reward(game_state, new_game_state, winner)
                
                # 4. === THE Q-LEARNING ALGORITHM ===
                # This is the "learning" moment, based on the Bellman Equation.
                # It updates the AI's "brain" (Q-Table) with what it just learned.
                # Q(s,a) = Q(s,a) + LR * [Reward + (DF * max(Q(s',a'))) - Q(s,a)]
                
                old_q_values = get_or_create_q_values(current_state_key)
                old_q_value = old_q_values[ai_action]
                
                next_state_key = get_state(new_game_state)
                next_q_values = get_or_create_q_values(next_state_key)
                max_next_q_value = 0.0 if game_over else max(next_q_values.values())
                
                # Apply the formula:
                new_q_value = old_q_value + LEARNING_RATE * (reward + DISCOUNT_FACTOR * max_next_q_value - old_q_value)
                
                # Update the brain:
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
                        # If the AI's last move led to the human winning,
                        # update the AI's brain with the big penalty.
                        Q_table[current_state_key][ai_action] = old_q_value + LEARNING_RATE * (REWARD_LOSE - old_q_value)

        # Decay epsilon (AI gets smarter, explores less)
        if epsilon > MIN_EPSILON:
            epsilon *= EPSILON_DECAY
            
        if (episode + 1) % 50000 == 0:
            print(f"  ...Training {episode + 1}/{EPISODES} complete. (Epsilon: {epsilon:.4f})")

    end_time = time.time()
    print(f"[TRAINING COMPLETE!] Total time: {end_time - start_time:.2f} seconds.")

# --------------------------------------------------------------------------------
# PART 5: SAVING & LOADING THE BRAIN
# --------------------------------------------------------------------------------
# Why? Training takes 1-2 minutes. We save the trained Q_table to a file
# so we don't have to re-train it every time we start the game.
# --------------------------------------------------------------------------------

def save_brain(filename=BRAIN_FILE):
    """ Saves the Q-Table (the AI's brain) to a .json file. """
    print(f"Saving AI brain to '{filename}'...")
    try:
        # Convert tuple-keys (e.g., ((0,1), (3,4))) to string-keys to save as JSON.
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
            # Convert string-keys back into tuple-keys (using eval())
            Q_table = {eval(k): v for k, v in string_q_table.items()}
        print("Brain loaded successfully.")
        return True
    except FileNotFoundError:
        print("WARNING: Saved brain file not found.")
        return False
    except Exception as e:
        print(f"ERROR: Could not load brain! {e}")
        return False