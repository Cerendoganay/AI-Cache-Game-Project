import pygame
import sys
import time
import cache_game as gl # Import our game logic & AI brain as 'gl'

# --------------------------------------------------------------------------------
# PART 1: PYGAME CONSTANTS AND SETUP
# --------------------------------------------------------------------------------

# --- Sizing Constants (UPDATED TO 7x7) ---
SQUARE_SIZE = 80
GRID_WIDTH = gl.GRID_SIZE  # Now 7 (from cache_game.py)
GRID_HEIGHT = gl.GRID_SIZE # Now 7 (from cache_game.py)

WINDOW_WIDTH = GRID_WIDTH * SQUARE_SIZE   # 7 * 80 = 560 pixels
WINDOW_HEIGHT = GRID_HEIGHT * SQUARE_SIZE + 60 # 560 + 60 = 620 pixels

# --- Color Constants (RGB) ---
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GRID = (150, 150, 150)
COLOR_BACKGROUND = (140, 40, 40) # Dark Red / Maroon
COLOR_EXIT = (100, 200, 100)       # Lighter Green
COLOR_INFO = (170, 60, 60) # A slightly lighter red than the background
COLOR_PLAYER = (50, 150, 255)      # Fallback color for Player
COLOR_AI = (255, 100, 50)          # Fallback color for AI
COLOR_BUTTON = (0, 150, 0)         # "Play Again" button
COLOR_BUTTON_TEXT = (255, 255, 255)

# --- Pygame System Initialization ---
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # Window size is now 560x620
pygame.display.set_caption(f"Cache Game (AI Project) - {GRID_WIDTH}x{GRID_HEIGHT}")
clock = pygame.time.Clock()
font_small = pygame.font.SysFont("Arial", 20)
font_large = pygame.font.SysFont("Arial", 40)
font_message = pygame.font.SysFont("Arial", 22, bold=True)

# --- IMAGE LOADING ---
try:
    player_image = pygame.image.load('player_png.png') 
    player_image = pygame.transform.scale(player_image, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
    
    ai_image = pygame.image.load('ai_png.png') 
    ai_image = pygame.transform.scale(ai_image, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
    
    use_images = True
    print("Visual assets (images) loaded successfully.")
except pygame.error as e:
    print(f"WARNING: Could not load images: {e}. Using fallback letters.")
    use_images = False
    player_surface = font_large.render("R", True, COLOR_PLAYER) # R = Runner
    ai_surface = font_large.render("C", True, COLOR_AI)       # C = Chaser

# --------------------------------------------------------------------------------
# PART 2: PYGAME DRAWING FUNCTIONS
# --------------------------------------------------------------------------------

def draw_grid():
    """ Clears the screen and draws the background and grid lines. """
    screen.fill(COLOR_BACKGROUND)
    pygame.draw.rect(screen, COLOR_INFO, (0, WINDOW_HEIGHT - 60, WINDOW_WIDTH, 60))

    for r in range(GRID_HEIGHT):
        for c in range(GRID_WIDTH):
            rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, COLOR_GRID, rect, 1)

def draw_pieces(game_state):
    """ Draws the Exit, AI, and Player pieces on the grid. """
    
    # 1. Draw Exit
    exit_r, exit_c = gl.EXIT_POS
    exit_rect = pygame.Rect(exit_c * SQUARE_SIZE, exit_r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    pygame.draw.rect(screen, COLOR_EXIT, exit_rect)
    exit_text = font_small.render("EXIT", True, COLOR_WHITE)
    screen.blit(exit_text, exit_rect.move(20, 30))

    # 2. Draw AI
    ai_r, ai_c = game_state['ai_pos']
    if use_images:
        ai_draw_pos = (ai_c * SQUARE_SIZE + 10, ai_r * SQUARE_SIZE + 10)
        screen.blit(ai_image, ai_draw_pos)
    else:
        ai_rect = ai_surface.get_rect(center=(ai_c * SQUARE_SIZE + SQUARE_SIZE // 2, ai_r * SQUARE_SIZE + SQUARE_SIZE // 2))
        screen.blit(ai_surface, ai_rect)

    # 3. Draw Human Player
    human_r, human_c = game_state['human_pos']
    if use_images:
        human_draw_pos = (human_c * SQUARE_SIZE + 10, human_r * SQUARE_SIZE + 10)
        screen.blit(player_image, human_draw_pos)
    else:
        human_rect = player_surface.get_rect(center=(human_c * SQUARE_SIZE + SQUARE_SIZE // 2, human_r * SQUARE_SIZE + SQUARE_SIZE // 2))
        screen.blit(player_surface, human_rect)

def draw_message(message, color=COLOR_WHITE):
    """ Writes messages to the info panel at the bottom. """
    text = font_message.render(message, True, color)
    screen.blit(text, (10, WINDOW_HEIGHT - 45))

def draw_winner(message):
    """ Draws the end-game message ("YOU WON!") over a transparent overlay. """
    s = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT - 60))
    s.set_alpha(180)
    s.fill(COLOR_BLACK)
    screen.blit(s, (0,0))
    
    text = font_large.render(message, True, COLOR_WHITE)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, (WINDOW_HEIGHT - 60) // 2))
    screen.blit(text, text_rect)

# --------------------------------------------------------------------------------
# PART 3: MAIN PYGAME GAME LOOP
# --------------------------------------------------------------------------------

def pygame_main_loop():
    
    # --- PLAY AGAIN BUTTON SETUP ---
    play_again_button_rect = pygame.Rect(
        (WINDOW_WIDTH // 2) - 100,
        (WINDOW_HEIGHT - 60) // 2 + 50,
        200, 50
    )
    play_again_text = font_message.render("PLAY AGAIN", True, COLOR_BUTTON_TEXT)
    play_again_text_rect = play_again_text.get_rect(center=play_again_button_rect.center)
    
    
    # --- LOAD OR TRAIN AI BRAIN ---
    # We now check for the 7x7 "guardian" brain file
    if not gl.load_brain():
        # If no brain file is found, show a "Training..." message
        screen.fill(COLOR_BACKGROUND)
        draw_message("AI brain (7x7) not found. Training AI... (This may take 2-3 min)", (255, 100, 0))
        pygame.display.update()
        
        # Run the training and save the new brain
        gl.train_ai()
        gl.save_brain()
    
    
    # --- RESET GAME VARIABLES ---
    game_state = gl.create_game_state()
    winner = None 
    message = "YOUR TURN (Runner). Use Arrow keys (or W,A,S,D)."
    
    # --- MAIN LOOP ---
    running = True
    while running:
        
        # --- 1. HANDLE INPUT ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
                
            # A. INPUTS DURING THE GAME (Key presses)
            if winner is None and game_state['current_turn'] == gl.HUMAN_PLAYER and event.type == pygame.KEYDOWN:
                
                human_action = None
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    human_action = 'UP'
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    human_action = 'DOWN'
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    human_action = 'LEFT'
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    human_action = 'RIGHT'
                
                if human_action and human_action in gl.get_valid_moves(game_state['human_pos']):
                    game_state = gl.perform_move(game_state, gl.HUMAN_PLAYER, human_action)
                    message = "AI's TURN (Chaser)... Thinking..."
                elif human_action:
                    message = "Invalid move! (Hit a wall or wrong key). Try again."
            
            # B. INPUTS AFTER THE GAME (Mouse clicks)
            if winner is not None and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if play_again_button_rect.collidepoint(pos):
                    # Reset the game!
                    game_state = gl.create_game_state()
                    winner = None
                    message = "YOUR TURN (Runner). Use Arrow keys (or W,A,S,D)."

        
        # --- 2. UPDATE LOGIC (AI's Turn) ---
        if winner is None and game_state['current_turn'] == gl.AI_PLAYER:
            
            current_state_key = gl.get_state(game_state)
            
            # Ask the trained AI brain for the *best* move (epsilon=0.0 means "no random moves")
            ai_action = gl.choose_action_for_ai(current_state_key, 0.0) 
            
            game_state = gl.perform_move(game_state, gl.AI_PLAYER, ai_action)
            message = "YOUR TURN (Runner). Use Arrow keys (or W,A,S,D)."
            
            winner = gl.check_winner(game_state)
            if winner == gl.AI_PLAYER:
                message = "GAME OVER! The AI caught you!"
        
        # --- 2. UPDATE LOGIC (Check for Human win) ---
        if winner is None:
             winner = gl.check_winner(game_state)
             if winner == gl.HUMAN_PLAYER:
                 message = "GAME OVER! You reached the exit!"

        
        # --- 3. DRAW ---
        draw_grid()
        draw_pieces(game_state)
        draw_message(message)
        
        # If the game is over, draw the winner message and the "Play Again" button
        if winner is not None:
            if winner == gl.HUMAN_PLAYER:
                draw_winner("YOU WON!")
            else:
                draw_winner("YOU LOST!")
            
            pygame.draw.rect(screen, COLOR_BUTTON, play_again_button_rect, border_radius=10)
            screen.blit(play_again_text, play_again_text_rect)
        
        
        # --- 4. REFRESH SCREEN ---
        pygame.display.update()
        clock.tick(60) # Limit to 60 FPS
        
        if winner is None and game_state['current_turn'] == gl.AI_PLAYER:
            time.sleep(0.3) 

# --------------------------------------------------------------------------------
# PART 4: START THE GAME
# --------------------------------------------------------------------------------
if __name__ == "__main__":
    pygame_main_loop()