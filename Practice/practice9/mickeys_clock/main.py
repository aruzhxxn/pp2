import pygame 
import datetime
import os
from clock import rotate_center #rotation function

# Window settings: screen width and height in pixels
WIDTH, HEIGHT = 600, 600
# Frames per second (refresh rate)
FPS = 60

# Initialize all Pygame modules
pygame.init()
# Create game window with specified dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Set window title
pygame.display.set_caption("Mickey's Clock")
# Create Clock object for FPS control
clock = pygame.time.Clock()

# Get absolute path to the directory where the current script is located
BASE_PATH = os.path.dirname(__file__)
# Build path to the images folder (named "images")
IMG_DIR = os.path.join(BASE_PATH, "images")

# Try-except block to handle image loading errors
try:
    # Load Mickey's body image (clock face) and scale to 600x600
    # convert_alpha() optimizes the image with transparency for better performance
    mickey_body = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "main-clock.png")).convert_alpha(), (600, 600))
    
    # Load right hand image (minute hand) and scale to 230x500
    right_hand = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "right-hand.png")).convert_alpha(), (230, 500))
    
    # Load left hand image (second hand) and scale to 230x500
    left_hand = pygame.transform.scale(pygame.image.load(os.path.join(IMG_DIR, "left-hand.png")).convert_alpha(), (230, 500))
    
# If an error occurs while loading any image
except pygame.error as e:
    # Print error message
    print(f"Loading error: {e}")
    # Close Pygame
    pygame.quit()
    # Exit the program
    exit()

# Calculate the center point of the screen (where hands will rotate around)
# Use Mickey's body width and height divided by 2
CENTER = (mickey_body.get_width() // 2, mickey_body.get_height() // 2)

# Flag to control the main game loop
running = True

# MAIN GAME LOOP (executes while running = True)
while running:
    # Process all events in the Pygame event queue
    for event in pygame.event.get():
        # If event is closing the window (clicking the X button)
        if event.type == pygame.QUIT:
            # Change flag to False to exit the loop
            running = False

    # GET CURRENT TIME
    now = datetime.datetime.now()           # Get current date and time
    seconds = now.second                    # Extract current seconds (0-59)
    minutes = now.minute                    # Extract current minutes (0-59)
    micro = now.microsecond / 1_000_000     # Convert microseconds to fraction of a second (0.0-0.999999)

    # CALCULATE ROTATION ANGLES FOR HANDS
    # For seconds: multiply by 6 (360°/60 sec) + account for microseconds for smooth movement
    # Negative angle - because Y-axis points down in Pygame (clockwise rotation)
    sec_angle = -((seconds + micro) * 6)
    
    # For minutes: multiply by 6 + add fraction from seconds (seconds/60) for smooth movement
    min_angle = -((minutes + (seconds / 60)) * 6)

    # FRAME RENDERING
    # Fill screen with white color (RGB: 255,255,255)
    screen.fill((255, 255, 255))

    # Draw Mickey's body (clock face) at coordinates (0,0) - top-left corner
    screen.blit(mickey_body, (0, 0))

    # Rotate right hand (minute hand) by calculated angle around center
    # rotate_center function returns rotated image and its rectangle
    rot_min, min_rect = rotate_center(right_hand, min_angle, CENTER)
    # Draw the rotated minute hand
    screen.blit(rot_min, min_rect)

    # Rotate left hand (second hand) by calculated angle around center
    rot_sec, sec_rect = rotate_center(left_hand, sec_angle, CENTER)
    # Draw the rotated second hand
    screen.blit(rot_sec, sec_rect)

    # Update the screen contents (show everything we've drawn)
    pygame.display.flip()
    
    # Limit frame rate to FPS (60 frames per second)
    # Program will wait here to not exceed the specified frame rate
    clock.tick(FPS)

# Close all Pygame modules and exit the program properly
pygame.quit()