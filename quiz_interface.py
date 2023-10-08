import pygame
import sys
import json
import random
import time

# Constants
QUIZ_WIDTH = 1000
QUIZ_HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_BLUE = (0, 0, 128)
LIGHT_YELLOW = (255, 255, 153)
INTRODUCTION_DELAY = 10  # 10 seconds
QUESTION_TIMEOUT = 40  # 40 seconds
FEEDBACK_DISPLAY_TIME = 3  # 3 seconds

def load_quiz_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data['questions']
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: Could not load quiz data.")
        sys.exit(1)

def display_introduction(screen, font, background_image, logo_image):
    # Fill the screen with a white background
    screen.fill(BLACK)
    
    # Calculate the position to center the background image
    bg_x = (QUIZ_WIDTH - background_image.get_width()) // 2
    bg_y = (QUIZ_HEIGHT - background_image.get_height()) // 2
    
    # Center the background image
    screen.blit(background_image, (bg_x, bg_y))
    
    logo_image_small = pygame.transform.scale(logo_image, (40, 40))
    screen.blit(logo_image_small, (20, QUIZ_HEIGHT - 50))
    
    intro_text = font.render("Hello, I hope you are doing well.", True, LIGHT_YELLOW)
    video_text_1 = font.render("I hope you enjoyed the video.", True, LIGHT_YELLOW)
    space_text = font.render("Please click on the spacebar.", True, LIGHT_YELLOW)
    
    # Calculate the horizontal position to center the text
    text_width = max(intro_text.get_width(), video_text_1.get_width(), space_text.get_width())
    horizontal_center = (QUIZ_WIDTH - text_width) // 2

    vertical_spacing = 50  # Vertical spacing between lines of text
    
    screen.blit(intro_text, (horizontal_center, vertical_spacing))
    screen.blit(video_text_1, (horizontal_center, vertical_spacing + intro_text.get_height() * 2))
    screen.blit(space_text, (horizontal_center, vertical_spacing + intro_text.get_height() * 5))

    pygame.display.flip()
    time.sleep(INTRODUCTION_DELAY)

def display_question(screen, font, question, background_image, logo_image, choice_font_size=30):
    # Blit the background image and logo image first
    screen.blit(background_image, (0, 0))
    logo_image_small = pygame.transform.scale(logo_image, (40, 40))
    screen.blit(logo_image_small, (20, QUIZ_HEIGHT - 50))

    # Now render the new question and answer choices
    question_text = font.render(question["question"], True, WHITE)
    question_y = 100  # Adjust the vertical position for the question
    screen.blit(question_text, (50, question_y))

    button_y = 250  # Adjust the starting vertical position for answer choices
    answer_choices = question["choices"][:]
    random.shuffle(answer_choices)

    max_chars_per_line = (QUIZ_WIDTH - 100) // (choice_font_size // 2)  # Adjusted for two lines

    for choice in answer_choices:
        # Split the choice text into two lines if it's too long
        lines = [choice[i:i+max_chars_per_line] for i in range(0, len(choice), max_chars_per_line)]

        choice_font = pygame.font.Font(None, choice_font_size)

        # Render each line of the choice text
        choice_texts = [choice_font.render(line, True, BLACK) for line in lines]

        # Calculate the total height required for the choice button
        button_height = len(choice_texts) * (choice_font_size + 10)  # Adjusted for spacing

        button_rect = pygame.Rect(50, button_y, QUIZ_WIDTH - 100, button_height)
        pygame.draw.rect(screen, LIGHT_YELLOW, button_rect)
        pygame.draw.rect(screen, BLACK, button_rect, 2)

        # Display each line of the choice text on the button
        for i, choice_text in enumerate(choice_texts):
            screen.blit(choice_text, (button_rect.centerx - choice_text.get_width() // 2, button_y + i * (choice_font_size + 10) + 10))

        button_y += button_height + 10  # Adjusted for spacing

    pygame.display.flip()

# Initialize pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((QUIZ_WIDTH, QUIZ_HEIGHT))
pygame.display.set_caption("Quiz Interface")

# Load background image with opacity
background_image = pygame.image.load("eclipse.jpg").convert_alpha()

# Load game logo image
logo_image = pygame.image.load("Astronest.png")

questions = load_quiz_data('eclipse_data.json')
random.shuffle(questions)
selected_questions = questions[:15]
current_question_index = 0
results = {"correct": 0, "wrong": 0}
font = pygame.font.Font(None, 36)

quiz_running = True
game_state = "introduction"  # Initial game state
introduction_displayed = False
question_displayed = False
current_answer_index = 0  # Initialize current_answer_index
question_start_time = 0

while quiz_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quiz_running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if game_state == "introduction" and not introduction_displayed:
                display_introduction(screen, font, background_image, logo_image)
                introduction_displayed = True
                game_state = "question"
            elif game_state == "question" and current_question_index < len(selected_questions):
                display_question(screen, font, selected_questions[current_question_index], background_image, logo_image)
                question_start_time = time.time()
                question_displayed = True
                game_state = "answer"
            elif game_state == "answer" and current_question_index < len(selected_questions):
                current_question_index += 1
                game_state = "question"
            elif game_state == "end":
                # Display answers and explanations here, and allow navigation
                display_answer_or_explanation(screen, font, selected_questions, background_image, current_answer_index)

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and game_state == "end":
            # Move to the previous answer/explanation
            current_answer_index = max(0, current_answer_index - 1)
            display_answer_or_explanation(screen, font, selected_questions, background_image, logo_image, current_answer_index)
            pygame.display.update()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and game_state == "end":
            # Move to the next answer/explanation
            current_answer_index = min(len(selected_questions) - 1, current_answer_index + 1)
            display_answer_or_explanation(screen, font, selected_questions, background_image, logo_image, current_answer_index)
            pygame.display.update()

    if game_state == "question" and question_displayed and time.time() - question_start_time >= QUESTION_TIMEOUT:
        current_question_index += 1
        game_state = "question"  # Reset to question state
        question_displayed = False

    if game_state == "end":
        display_answer_or_explanation(screen, font, selected_questions, background_image, logo_image, current_answer_index)
        pygame.display.update()

# Quit pygame and exit the program
pygame.quit()
sys.exit()