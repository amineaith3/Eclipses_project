import pygame
import sys
import os
import time
import webbrowser
import subprocess

# Initialize pygame
pygame.init()

# Constants for the window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
DARK_BLUE = (0, 0, 50)  # Dark Blue background
YELLOW = (255, 255, 0)  # Yellow button color

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Eclipse Q/A Game")

# Define fonts
font = pygame.font.Font(None, 36)

# Define text and buttons
button_width = 400
button_height = 50

# Calculate the center of the screen
center_x = SCREEN_WIDTH // 2
center_y = SCREEN_HEIGHT // 2

# Button coordinates
video_button_rect = pygame.Rect(center_x - button_width // 2, center_y - 150, button_width, button_height)
quiz_button_rect = pygame.Rect(center_x - button_width // 2, center_y , button_width, button_height)
contact_button_rect = pygame.Rect(center_x - button_width // 2, center_y + 150, button_width, button_height)

# Flags to track whether the video has finished
video_finished = False

# Function to simulate video playback
def simulate_video_playback():
    global video_finished
    # Simulate video playback for 3 minutes (180 seconds)
    time.sleep(2)
    video_finished = True
import subprocess

# Function to handle the "Check the Quiz" button
def check_quiz():
    global quiz_started
    if video_finished:
        quiz_started = True
        try:
            # Launch the quiz interface as a separate process
            subprocess.Popen(["python", "quiz_interface.py"])
        except Exception as e:
            print("Error:", e)


# Function to handle the "Contact the Creators" button
def contact_creators():
    # Implement your code for contacting the creators here
    email_adresses = ["amineaithamma2004@gmail.com", "amineaihamma@gmail.com"]
    email_subject = "Raise a technical request"
    recipients = " , ".join(email_adresses)
    # Open the default email client with a pre-filled email
    webbrowser.open(f"mailto:{recipients}?subject={email_subject}")

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
            # Check if buttons are clicked
            if video_button_rect.collidepoint(event.pos) and not video_finished:
                # Handle the "Check the Video" button
                video_file = "educative_eclipse.mp4"
                if os.path.isfile(video_file):
                    os.system(f"start {video_file}")
                    # Simulate video playback
                    simulate_video_playback()
                else:
                    print("Video file not found.")
            elif quiz_button_rect.collidepoint(event.pos):
                # Handle the "Check the Quiz" button
                check_quiz()
            elif contact_button_rect.collidepoint(event.pos):
                # Handle the "Contact the Creators" button
                contact_creators()

    # Clear the screen with dark blue background
    screen.fill(DARK_BLUE)

    # Display buttons with yellow color
    pygame.draw.rect(screen, YELLOW, video_button_rect)
    pygame.draw.rect(screen, YELLOW, quiz_button_rect)
    pygame.draw.rect(screen, YELLOW, contact_button_rect)

    # Text for buttons
    video_text = font.render("Check the Video", True, DARK_BLUE)  # Text color matches the background
    quiz_text = font.render("Check the Quiz", True, DARK_BLUE if video_finished else (150, 150, 150))  # Gray out if video not finished
    contact_text = font.render("Contact the Creators", True, DARK_BLUE)

    # Blit text on buttons
    screen.blit(video_text, (video_button_rect.centerx - video_text.get_width() // 2, video_button_rect.centery - video_text.get_height() // 2))
    screen.blit(quiz_text, (quiz_button_rect.centerx - quiz_text.get_width() // 2, quiz_button_rect.centery - quiz_text.get_height() // 2))
    screen.blit(contact_text, (contact_button_rect.centerx - contact_text.get_width() // 2, contact_button_rect.centery - contact_text.get_height() // 2))

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
