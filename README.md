# Flappy Bird Game

This is a Python implementation of the popular Flappy Bird game using the Pygame library. The game features basic mechanics like flapping the bird, avoiding pipes, collecting power-ups, and saving scores.

## Table of Contents

1. [Running the Game](#running-the-game)
2. [Gameplay Instructions](#gameplay-instructions)
3. [Game Design](#game-design)
4. [Code Explanation](#code-explanation)
5. [Screenshots](#screenshots)
6. [Acknowledgments](#acknowledgments)
7. [License](#license)
8. [Contribution](#contribution)




## Running the Game
After installing Pygame and ensuring the directory structure is correct, run the game by executing:
python flappy_bird.py


This will launch the game in a window.

## Gameplay Instructions

### Start the Game:
Press Spacebar or the Up Arrow key to start the game from the welcome screen.

### Flap the Bird:
Press Spacebar or the Up Arrow key to make the bird flap its wings and rise. The bird falls due to gravity.

### Avoid Collisions:
Navigate the bird through the pipes without hitting them. You earn one point for every pipe passed.

### Power-Ups:
Occasionally, a power-up will appear. Collect it to temporarily boost your speed.

### Game Over:
The game ends when the bird crashes into a pipe or hits the ground. Your score will be saved with a timestamp in `scores.txt`.

## Game Design

### Power-Up Class
The power-up appears randomly in the game and provides the player with a temporary speed boost.

#### Attributes:
- `x, y`: Position of the power-up.
- `width, height`: Size of the power-up.
- `image`: The image representing the power-up.

#### Methods:
- `move()`: Moves the power-up leftward across the screen.
- `draw(screen)`: Draws the power-up on the screen.
- `is_collected(playerx, playery, player_width, player_height)`: Checks if the player has collected the power-up.

## Code Explanation

### Game Loop
The `mainGame()` function runs the primary game loop, where events like player input (flapping) are handled, pipes are generated and moved, and collisions are checked.

### Collision Detection
The `isCollide()` function checks whether the bird collides with pipes or the ground.

### Score Handling
The score is tracked and displayed at the top of the screen. Every time the bird successfully passes a pipe, the score increases.

### Power-Up Logic
The `PowerUp` class is responsible for creating, moving, and respawning power-ups. When the player collects a power-up, their speed is temporarily increased.

### Game Over
The game ends when a collision is detected, and the player's score is saved with a timestamp.

## Screenshots
(Insert screenshots of the game here if applicable)

## Acknowledgments
The Pygame library was used for creating the game. This project is inspired by the Flappy Bird game.

## License
This project is open-source and available under the MIT License. See the LICENSE file for more information.

## Contribution
Feel free to fork this repository, submit issues, and contribute to the improvement of this project. If you find bugs or have ideas for features, please submit a pull request.




