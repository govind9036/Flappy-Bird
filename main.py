import random  # For generating random numbers
import sys  # We will use sys.exit to exit the program
import pygame
from pygame.locals import *  # Basic pygame imports
from datetime import datetime  # Import datetime module for timestamp
SCORE_FILE = 'scores.txt'  # File to store scores
  

# Global Variables for the game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/bg_3.jpg'
PIPE = 'gallery/sprites/pipe.png'
SCORE_FILE = 'scores.txt'  # File to store scores

class PowerUp:  
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50  # Power-up width
        self.height = 50  # Power-up height
        self.image = pygame.image.load('gallery/sprites/powerup.png')  # Load your power-up image

    def move(self):
        self.x -= 4  # Power-up moves towards the left at the same speed as pipes

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def is_collected(self, playerx, playery, player_width, player_height):
        # Check if the player collects the power-up
        if (self.x < playerx + player_width) and (self.x + self.width > playerx) and \
           (self.y < playery + player_height) and (self.y + self.height > playery):
            return True
        return False


def welcomeScreen():
    """ 
    Shows welcome images on the screen
    """

    playerx = int(SCREENWIDTH / 5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    background_index = 0  # Index to keep track of current background image
    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREENWIDTH / 2)
    basex = 0
    player_width = GAME_SPRITES['player'].get_width()
    player_height = GAME_SPRITES['player'].get_height()

    # Create initial power-up
    power_up = PowerUp(SCREENWIDTH + 300, random.randint(100, SCREENHEIGHT - 100))
    power_up_active = False
    power_up_timer = 0  # Timer for power-up effect duration

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8  # velocity while flapping
    playerFlapped = False  # It is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        # Check for power-up collection
        # Create a new power-up after it's collected
        if power_up.is_collected(playerx, playery, player_width, player_height):
            playerVelY -= 2  # Boost player speed temporarily
            power_up_active = True
            power_up_timer = pygame.time.get_ticks()  # Start the timer for power-up effect
            power_up = PowerUp(SCREENWIDTH + 300, random.randint(100, SCREENHEIGHT - 100))  # Respawn new power-up


        # Move and draw power-up if active
        if not power_up_active:
            power_up.move()
            power_up.draw(SCREEN)

        # Check if the power-up effect has expired
        if power_up_active and pygame.time.get_ticks() - power_up_timer > 5000:  # 5 seconds duration
            playerVelY += 2  # Reset player speed to normal
            power_up_active = False
            # Respawn a new power-up at a different location
            power_up = PowerUp(SCREENWIDTH + 300, random.randint(100, SCREENHEIGHT - 100))

        # Game logic continues...
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return

        # check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()

                # Change background after every score of 10
                if score % 2 == 0:
                    background_index = (background_index + 1) % 6
                    background_image_path = f'gallery/sprites/bg_{background_index}.jpg'
                    GAME_SPRITES['background'] = pygame.image.load(background_image_path).convert()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width) / 2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            # Game over condition
            gameOver(score)
            return  # Exit the main game loop


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < \
                GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False


def getRandomPipe():
    """
    Generate positions of two pipes (one top and one bottom) for blitting on the screen.
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()  # Height of the pipe
    offset = SCREENHEIGHT / 3  # Offsets to determine where to position pipes vertically
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = SCREENWIDTH + 10  # Set pipe position off-screen initially
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},  # Upper pipe (flipped vertically)
        {'x': pipeX, 'y': y2}  # Lower pipe
    ]
    return pipe




def gameOver(score):
    # Display Game Over text
    font = pygame.font.Font(None, 48)
    game_over_text = font.render('Game Over', True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(SCREENWIDTH / 2, SCREENHEIGHT / 2 - 50))
    
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(SCREENWIDTH / 2, SCREENHEIGHT / 2))
    
    SCREEN.blit(game_over_text, game_over_rect)
    SCREEN.blit(score_text, score_rect)
    pygame.display.update()
    
    # Save score with timestamp
    with open(SCORE_FILE, 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"{timestamp} - Score: {score}\n")
    
    # Wait a little
    pygame.time.wait(1500)
    
    # Wait for a key to be pressed
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                waiting = False

 

def storeScore(score):
    # Open the file in append mode and write the score and timestamp
    with open(SCORE_FILE, 'a') as f:
        f.write(f"Score: {score}, Time: {datetime.now()}\n")


# def storeScore(score):
#     # Open the file in append mode and write the score and timestamp
#     with open(SCORE_FILE, 'a') as f:
#         f.write(f"Score: {score}, Time: {datetime.now()}\n")

if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init()  # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird Game')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
                            pygame.image.load(PIPE).convert_alpha()
                            )

    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen()  # Shows welcome screen to the user until he presses a button
        mainGame()  # This is the main game function
