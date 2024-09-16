import pygame
import sys
import random
import serial

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up Arduino communication (modify port as needed)
try:
    arduino = serial.Serial('COM3', 9600, timeout=1)  # Adjust the COM port accordingly
    arduino_connected = True
except serial.SerialException:
    arduino_connected = False

# Load sound effects
correct_sound = pygame.mixer.Sound('sounds/correct.wav')
wrong_sound = pygame.mixer.Sound('sounds/wrong.wav')
toggle_sound = pygame.mixer.Sound('sounds/toggle.mp3')
bg_music = 'sounds/bg_music.mp3'
pygame.mixer.music.load(bg_music)
pygame.mixer.music.play(-1)  # Play background music in a loop

# Set up the display (Resizable window)
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Sjov Binær Udfordring")

# Colors
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
BLUE = (0, 191, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_RED = (255, 99, 71)
YELLOW = (255, 255, 102)
GREEN = (0, 255, 0)
LIGHT_ON = (0, 255, 0)
GLOW = (255, 255, 200)  # Light glow effect

# Fonts
menu_font = pygame.font.SysFont('Comic Sans MS', 50)
button_font = pygame.font.SysFont('Comic Sans MS', 30)

# Game variables
levels = [
    {"binary_password": "0010", "meaning": "Number 2 in Binary", "type": "number", "attempts": 3, "bits": 4},
    {"binary_password": "0101", "meaning": "Number 5 in Binary", "type": "number", "attempts": 4, "bits": 4},
    {"binary_password": "1001", "meaning": "Number 9 in Binary", "type": "number", "attempts": 5, "bits": 4},
    {"binary_password": "1100", "meaning": "Color: Yellow in Binary", "type": "color", "attempts": 5, "bits": 4},
    {"binary_password": "0110", "meaning": "Shape: Square in Binary", "type": "shape", "attempts": 5, "bits": 4},
]
current_level = 0
user_input = ["0"] * 4  # Always have 4 bulbs
light_states = [0] * 4  # Always initialize 4 lights
attempts = levels[current_level]["attempts"]
game_over = False
correct_value = False  # Track if the correct value is entered
confetti = []
menu_active = True  # Main menu state

# Menu Background - Draw sky gradient and shapes
def draw_background():
    screen.fill(LIGHT_BLUE)
    # Draw stars for a playful effect
    for _ in range(50):
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height // 2)
        pygame.draw.circle(screen, WHITE, (x, y), random.randint(2, 4))

# Create menu buttons with borders/shadows for visibility
def create_button(text, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Add border for visibility
    pygame.draw.rect(screen, BLACK, (x - 5, y - 5, width + 10, height + 10))

    # Detect if the mouse is hovering over the button
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    text_surface = button_font.render(text, True, BLACK)
    screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))

# Define actions for buttons
def start_game():
    game_loop()

def show_instructions():
    instructions_screen()

def quit_game():
    pygame.quit()
    sys.exit()

# Main menu screen
def main_menu():
    global screen_width, screen_height, screen
    menu = True
    while menu:
        screen.fill(WHITE)
        draw_background()

        # Render Title
        title_surface = menu_font.render("Sjov Binær Udfordring", True, BLACK)
        screen.blit(title_surface, (screen_width // 2 - title_surface.get_width() // 2, 100))

        # Render buttons
        create_button("Start Spil", screen_width // 2 - 100, 250, 200, 50, LIGHT_RED, RED, start_game)
        create_button("Instruktioner", screen_width // 2 - 100, 320, 200, 50, LIGHT_BLUE, BLUE, show_instructions)
        create_button("Afslut", screen_width // 2 - 100, 390, 200, 50, LIGHT_RED, RED, quit_game)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.w, event.h
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

        pygame.display.update()

# Instructions screen (friendly binary explanation)
def instructions_screen():
    running = True
    while running:
        screen.fill(WHITE)
        draw_background()

        # Display instructions
        instructions_surface = menu_font.render("Sådan spiller du", True, BLACK)
        screen.blit(instructions_surface, (screen_width // 2 - instructions_surface.get_width() // 2, 100))

        text1 = button_font.render("Tænd/sluk lysene for at danne binær kode.", True, BLACK)
        text2 = button_font.render("Gæt den rigtige binære værdi for at vinde!", True, BLACK)
        screen.blit(text1, (screen_width // 2 - text1.get_width() // 2, 250))
        screen.blit(text2, (screen_width // 2 - text2.get_width() // 2, 300))

        create_button("Tilbage", screen_width // 2 - 100, 450, 200, 50, LIGHT_RED, RED, main_menu)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

# Function to create confetti for celebration effect
def create_confetti():
    global confetti
    confetti = []
    for _ in range(100):
        confetti.append([random.randint(0, screen_width), random.randint(-100, screen_height), random.choice([RED, GREEN, YELLOW])])

# Function to draw the confetti animation
def draw_confetti():
    for i in range(len(confetti)):
        pygame.draw.circle(screen, confetti[i][2], (confetti[i][0], confetti[i][1]), 5)
        confetti[i][1] += random.randint(1, 3)  # Fall speed
        if confetti[i][1] > screen_height:
            confetti[i][1] = random.randint(-100, -50)
            confetti[i][0] = random.randint(0, screen_width)

# Draw the lights and UI for the game, ensuring they are always centered
def draw_lights():
    global correct_value
    screen.fill(WHITE)
    draw_background()

    # Center the lights (always 4 bulbs)
    total_lights_width = 4 * 100 - 20
    start_x = (screen_width - total_lights_width) // 2

    for i, state in enumerate(light_states):
        if correct_value:
            color = LIGHT_ON
            glow_color = GLOW
        else:
            color = LIGHT_ON if state == 1 else RED
            glow_color = LIGHT_ON if state == 1 else BLACK
        # Draw glowing effect
        pygame.draw.circle(screen, glow_color, (start_x + i * 100, screen_height // 2), 50)
        # Draw light bulb
        pygame.draw.circle(screen, color, (start_x + i * 100, screen_height // 2), 40)

    # Display current binary input
    input_text = button_font.render(f"Binær Input: {''.join(user_input)}", True, BLACK)
    screen.blit(input_text, (screen_width // 2 - input_text.get_width() // 2, screen_height - 100))

    if correct_value:
        value_text = button_font.render(f"Korrekt: {''.join(user_input)} - {levels[current_level]['meaning']}", True, BLACK)
        screen.blit(value_text, (screen_width // 2 - value_text.get_width() // 2, screen_height - 50))

    pygame.display.flip()

# Binary Explanation with Animations
def show_binary_explanation():
    binary_value = ''.join(user_input)
    level_type = levels[current_level]["type"]

    # Draw explanation screen once
    draw_explanation_screen(binary_value, level_type)

    # Wait for key input to proceed
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting_for_input = False

# Draw explanation screen based on level type
def draw_explanation_screen(binary_value, level_type):
    screen.fill(LIGHT_BLUE)
    draw_background()

    if level_type == "number":
        decimal_value = int(binary_value, 2)
        animate_number_explanation(binary_value, decimal_value)
    elif level_type == "color":
        animate_color_explanation(binary_value)
    elif level_type == "shape":
        animate_shape_explanation(binary_value)

    pygame.display.flip()

# Animation for number explanation
def animate_number_explanation(binary_value, decimal_value):
    total_lights_width = 4 * 100 - 20
    start_x = (screen_width - total_lights_width) // 2
    y_pos = 150
    step_delay = 1000

    # Draw and explain each binary bit
    for i, bit in enumerate(binary_value):
        # Highlight current bit
        color = LIGHT_ON if bit == '1' else RED
        pygame.draw.circle(screen, color, (start_x + i * 100, y_pos), 40)

        # Show binary power contribution
        if bit == '1':
            contribution = 2 ** (3 - i)
            contribution_text = f"2^{3-i} = {contribution}"
            text_surface = button_font.render(contribution_text, True, BLACK)
            screen.blit(text_surface, (start_x + i * 100 - 30, y_pos + 50))

    # Show final result
    result_text = f"Total: {decimal_value}"
    result_surface = button_font.render(result_text, True, BLACK)
    screen.blit(result_surface, (screen_width // 2 - result_surface.get_width() // 2, y_pos + 100))

# Animation for color explanation
def animate_color_explanation(binary_value):
    explanation_text = [
        "Binary values can represent colors!",
        "Each bit affects the Red, Green, or Blue component."
    ]
    render_explanation_text(explanation_text)

    # Simulate the effect of binary on colors
    color_components = ['Red', 'Green', 'Blue']
    y_pos = 250
    start_x = screen_width // 2 - 100

    # Display binary influence on color components
    for i, bit in enumerate(binary_value[:3]):  # Only using 3 bits for RGB
        if bit == '1':
            component_color = LIGHT_ON
            color_name = color_components[i]
            component_text = f"{color_name} ON"
        else:
            component_color = RED
            color_name = color_components[i]
            component_text = f"{color_name} OFF"

        pygame.draw.rect(screen, component_color, (start_x + i * 100, y_pos, 80, 80))
        text_surface = button_font.render(component_text, True, BLACK)
        screen.blit(text_surface, (start_x + i * 100 - 30, y_pos + 90))

    # Show final color
    final_color_text = "This combination creates Yellow!"
    text_surface = button_font.render(final_color_text, True, BLACK)
    screen.blit(text_surface, (screen_width // 2 - text_surface.get_width() // 2, y_pos + 150))

# Animation for shape explanation
def animate_shape_explanation(binary_value):
    explanation_text = [
        "Binary can also represent shapes!",
        "Different combinations lead to different shapes."
    ]
    render_explanation_text(explanation_text)

    # Show how binary combination creates a shape
    shape_text = "This combination creates a Square!"
    shape_surface = button_font.render(shape_text, True, BLACK)
    screen.blit(shape_surface, (screen_width // 2 - shape_surface.get_width() // 2, 300))
    pygame.draw.rect(screen, LIGHT_ON, (screen_width // 2 - 50, 350, 100, 100))  # Draw a square

# Render the explanation text
def render_explanation_text(explanation_text):
    y_pos = 50
    for line in explanation_text:
        text_surface = button_font.render(line, True, BLACK)
        screen.blit(text_surface, (screen_width // 2 - text_surface.get_width() // 2, y_pos))
        y_pos += 50

# Update lights based on Arduino input
def update_lights_from_arduino():
    if arduino_connected:
        try:
            binary_string = arduino.readline().decode().strip()
            if len(binary_string) == 4 and all(char in '01' for char in binary_string):
                for i, bit in enumerate(binary_string):
                    light_states[i] = int(bit)
                    user_input[i] = bit
        except serial.SerialException:
            pass

# Main game loop
def game_loop():
    global current_level, user_input, light_states, attempts, game_over, correct_value
    running = True

    while running:
        update_lights_from_arduino()
        draw_lights()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    idx = int(event.unicode) - 1
                    if idx < 4 and not correct_value:
                        light_states[idx] = 1 - light_states[idx]
                        user_input[idx] = "1" if light_states[idx] == 1 else "0"
                        pygame.mixer.Sound.play(toggle_sound)

                elif event.key == pygame.K_RETURN and not correct_value:
                    if ''.join(user_input) == levels[current_level]["binary_password"]:
                        pygame.mixer.Sound.play(correct_sound)
                        correct_value = True
                        create_confetti()

                        # Draw confetti for 1 second
                        start_time = pygame.time.get_ticks()
                        while pygame.time.get_ticks() - start_time < 1000:
                            draw_lights()  # Redraw lights to maintain the level screen
                            draw_confetti()
                            pygame.display.update()

                        show_binary_explanation()
                        current_level += 1
                        if current_level >= len(levels):
                            game_over = True
                            running = False
                        else:
                            user_input = ["0"] * 4
                            light_states = [0] * 4
                            correct_value = False
                            attempts = levels[current_level]["attempts"]
                    else:
                        pygame.mixer.Sound.play(wrong_sound)
                        # Turn off the incorrect lights
                        for i in range(4):
                            if user_input[i] != levels[current_level]["binary_password"][i]:
                                light_states[i] = 0
                                user_input[i] = "0"
                        attempts -= 1
                        if attempts == 0:
                            attempts = levels[current_level]["attempts"]

        pygame.display.update()

# Start the game at the main menu
main_menu()
