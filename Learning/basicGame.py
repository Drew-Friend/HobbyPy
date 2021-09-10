import pygame
import random
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore")  # suppress warnings
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 300


class NeuralNet:
    """
    A two layer neural network
    """

    def __init__(self, layers=[13, 8, 1], learning_rate=0.001, iterations=100):
        self.params = {}
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.loss = []
        self.sample_size = None
        self.layers = layers
        self.X = None
        self.y = None

    def init_weights(self):
        """
        Randomize Weights
        """
        np.random.seed(1)  # Seed the random number generator
        self.params["W1"] = np.random.randn(self.layers[0], self.layers[1])
        self.params["b1"] = np.random.randn(
            self.layers[1],
        )
        self.params["W2"] = np.random.randn(self.layers[1], self.layers[2])
        self.params["b2"] = np.random.randn(
            self.layers[2],
        )

    def relu(self, Z):
        """
        Turns negative numbers into 0
        """
        return np.maximum(0, Z)

    def dRelu(self, x):
        """
        Derivative of reLU
        """
        x[x <= 0] = 0
        x[x > 0] = 1
        return x

    def eta(self, x):
        ETA = 0.0000000001
        return np.maximum(x, ETA)

    def sigmoid(self, Z):
        """
        The sigmoid function takes in real numbers in any range and
        squashes it to a real-valued output between 0 and 1.
        """
        return 1 / (1 + np.exp(-Z))

    def entropy_loss(self, y, yhat):
        """
        Loss Function
        """
        nsample = len(y)
        yhat_inv = 1.0 - yhat
        y_inv = 1.0 - y
        yhat = self.eta(yhat)  ## clips value to avoid NaNs in log
        yhat_inv = self.eta(yhat_inv)
        loss = (
            -1
            / nsample
            * (
                np.sum(
                    np.multiply(np.log(yhat), y)
                    + np.multiply((y_inv), np.log(yhat_inv))
                )
            )
        )
        return loss

    def forward_propagation(self):
        """
        Performs the forward propagation
        """

        Z1 = self.X.dot(self.params["W1"]) + self.params["b1"]
        A1 = self.relu(Z1)
        Z2 = A1.dot(self.params["W2"]) + self.params["b2"]
        yhat = self.sigmoid(Z2)
        loss = self.entropy_loss(self.y, yhat)

        # save calculated parameters
        self.params["Z1"] = Z1
        self.params["Z2"] = Z2
        self.params["A1"] = A1

        return yhat, loss

    def back_propagation(self, yhat):
        """
        Computes the derivatives and update weights and bias according.
        """
        y_inv = 1 - self.y
        yhat_inv = 1 - yhat

        dl_wrt_yhat = np.divide(y_inv, self.eta(yhat_inv)) - np.divide(
            self.y, self.eta(yhat)
        )
        dl_wrt_sig = yhat * (yhat_inv)
        dl_wrt_z2 = dl_wrt_yhat * dl_wrt_sig

        dl_wrt_A1 = dl_wrt_z2.dot(self.params["W2"].T)
        dl_wrt_w2 = self.params["A1"].T.dot(dl_wrt_z2)
        dl_wrt_b2 = np.sum(dl_wrt_z2, axis=0, keepdims=True)

        dl_wrt_z1 = dl_wrt_A1 * self.dRelu(self.params["Z1"])
        dl_wrt_w1 = self.X.T.dot(dl_wrt_z1)
        dl_wrt_b1 = np.sum(dl_wrt_z1, axis=0, keepdims=True)

        # update the weights and bias
        self.params["W1"] = self.params["W1"] - self.learning_rate * dl_wrt_w1
        self.params["W2"] = self.params["W2"] - self.learning_rate * dl_wrt_w2
        self.params["b1"] = self.params["b1"] - self.learning_rate * dl_wrt_b1
        self.params["b2"] = self.params["b2"] - self.learning_rate * dl_wrt_b2

    def fit(self, X, y):
        """
        Trains the neural network using the specified data and labels
        """
        self.X = X
        self.y = y
        self.init_weights()  # initialize weights and bias

        for i in range(self.iterations):
            yhat, loss = self.forward_propagation()
            self.back_propagation(yhat)
            self.loss.append(loss)

    def predict(self, X):
        """
        Predicts on a test data
        """
        Z1 = X.dot(self.params["W1"]) + self.params["b1"]
        A1 = self.relu(Z1)
        Z2 = A1.dot(self.params["W2"]) + self.params["b2"]
        pred = self.sigmoid(Z2)
        return np.round(pred)

    def acc(self, y, yhat):
        """
        Calculates the accutacy between the predicted valuea and the truth labels
        """
        acc = int(sum(y == yhat) / len(y) * 100)
        return acc

    def plot_loss(self):
        """
        Plots the loss curve
        """
        plt.plot(self.loss)
        plt.xlabel("Iteration")
        plt.ylabel("logloss")
        plt.title("Loss curve for training")
        plt.show()


# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a custom events
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDPOINT = pygame.USEREVENT + 2
pygame.time.set_timer(ADDPOINT, 300)


player = Player()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Setup the clock for a decent framerate
clock = pygame.time.Clock()
score = 0

running = True
# Main loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False

        elif event.type == ADDPOINT:
            score += 1

        # Add a new enemy?
        elif event.type == ADDENEMY:
            if len(enemies) < 15:
                # Create the new enemy and add it to sprite groups
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)

    # Update enemy position
    enemies.update()

    # Fill the screen with black
    pygame.display.set_caption(str(score))
    screen.fill((0, 0, 0))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        player.kill()
        running = False

    # Update the display
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)
    print(len(enemies))
