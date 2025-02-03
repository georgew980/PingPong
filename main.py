import pygame
import random

# Initialize Pygame and its modules
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600  # Width and height of the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the game window
pygame.display.set_caption('Minimal Pong')  # Set the window title

# Define the Paddle class
class Paddle:
    def __init__(self, x, y):
        """
        Initialize a paddle object.
        :param x: X-coordinate of the paddle's top-left corner
        :param y: Y-coordinate of the paddle's top-left corner
        """
        self.rect = pygame.Rect(x, y, 10, 100)  # Create a rectangular paddle (width: 10, height: 100)
        self.speed = 5  # Speed at which the paddle moves

    def move(self, up=True):
        """
        Move the paddle up or down.
        :param up: Boolean indicating whether to move the paddle up (True) or down (False)
        """
        if up:
            self.rect.y = max(0, self.rect.y - self.speed)  # Move up, ensuring it doesn't go above the screen
        else:
            self.rect.y = min(HEIGHT - self.rect.height, self.rect.y + self.speed)  # Move down, ensuring it doesn't go below the screen

    def draw(self):
        """Draw the paddle on the screen."""
        pygame.draw.rect(screen, (255, 255, 255), self.rect)  # Draw the paddle as a white rectangle

# Define the Ball class
class Ball:
    def __init__(self):
        """Initialize a ball object."""
        self.rect = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)  # Create a square ball (30x30) at the center
        self.dx = random.choice([3, -3])  # Random horizontal speed (left or right)
        self.dy = random.choice([3, -3])  # Random vertical speed (up or down)
        self.max_speed = 15  # Maximum speed the ball can reach

    def move(self):
        """Move the ball and handle collisions with the top and bottom walls."""
        self.rect.x += self.dx  # Move the ball horizontally
        self.rect.y += self.dy  # Move the ball vertically

        # Bounce off the top and bottom edges of the screen
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy = -self.dy  # Reverse the vertical direction

    def reset(self):
        """Reset the ball to the center of the screen with a random direction."""
        self.rect.center = (WIDTH // 2, HEIGHT // 2)  # Move the ball to the center
        self.dx = random.choice([3, -3])  # Random horizontal speed
        self.dy = random.choice([3, -3])  # Random vertical speed

    def draw(self):
        """Draw the ball on the screen."""
        pygame.draw.rect(screen, (255, 255, 255), self.rect)  # Draw the ball as a white square

# Define the Game class
class Game:
    def __init__(self):
        """Initialize the game with paddles, a ball, and a score."""
        self.player = Paddle(50, HEIGHT // 2 - 50)  # Create the player's paddle on the left
        self.opponent = Paddle(WIDTH - 60, HEIGHT // 2 - 50)  # Create the opponent's paddle on the right
        self.ball = Ball()  # Create the ball
        self.score = [0, 0]  # Initialize scores for player and opponent
        self.font = pygame.font.Font(None, 36)  # Font for rendering the score

    def play(self):
        """Main game loop."""
        clock = pygame.time.Clock()  # Create a clock to control the frame rate
        running = True  # Boolean to control the game loop

        while running:
            # Handle events (e.g., quitting the game)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # If the user closes the window
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # If the user presses the ESC key
                        running = False

            # Player movement based on key presses
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:  # Move the player's paddle up
                self.player.move(up=True)
            if keys[pygame.K_DOWN]:  # Move the player's paddle down
                self.player.move(up=False)

            # Simple AI for the opponent's paddle
            if self.ball.rect.centery < self.opponent.rect.centery:  # If the ball is above the opponent's paddle
                self.opponent.move(up=True)  # Move the opponent's paddle up
            else:  # If the ball is below the opponent's paddle
                self.opponent.move(up=False)  # Move the opponent's paddle down

            # Move the ball and handle collisions
            self.ball.move()

            # Check for collisions with the paddles
            if self.ball.rect.colliderect(self.player.rect) or self.ball.rect.colliderect(self.opponent.rect):
                self.ball.dx *= -1  # Reverse the horizontal direction of the ball

            # Check for scoring
            if self.ball.rect.left <= 0:  # If the ball goes past the player's paddle
                self.score[1] += 1  # Increment the opponent's score
                self.ball.reset()  # Reset the ball to the center
            elif self.ball.rect.right >= WIDTH:  # If the ball goes past the opponent's paddle
                self.score[0] += 1  # Increment the player's score
                self.ball.reset()  # Reset the ball to the center

            # Draw everything on the screen
            screen.fill((0, 0, 0))  # Clear the screen with a black background
            self.player.draw()  # Draw the player's paddle
            self.opponent.draw()  # Draw the opponent's paddle
            self.ball.draw()  # Draw the ball

            # Draw the scores
            player_score_text = self.font.render(str(self.score[0]), True, (255, 255, 255))  # Render the player's score
            opponent_score_text = self.font.render(str(self.score[1]), True, (255, 255, 255))  # Render the opponent's score
            screen.blit(player_score_text, (WIDTH // 4, 10))  # Display the player's score on the left
            screen.blit(opponent_score_text, (3 * WIDTH // 4, 10))  # Display the opponent's score on the right

            pygame.display.flip()  # Update the display
            clock.tick(60)  # Limit the frame rate to 60 FPS

        pygame.quit()  # Quit Pygame when the game loop ends

# Entry point of the program
if __name__ == '__main__':
    game = Game()  # Create an instance of the Game class
    game.play()  # Start the game