import pygame
import numpy as np
import pygame.draw
import random
from nn_Sigmoid import NeuralNet as agent

# Game shit
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
# Game shit


class Exp_Buffer:
    def __init__(self):
        self.maxLength = 10000
        self.replay_list = []

    def add_experience(self, pCoord, gCoord, rCoord, choice, reward, nCoord, done):
        pState = [pCoord, gCoord, rCoord]
        nState = [nCoord, gCoord, rCoord]
        self.replay_list.append([pState, choice, reward, nState, done])
        if len(self.replay_list) > self.maxLength:
            self.replay_list.pop(0)

    def get_experience(self, index):
        return self.replay_list[index]


class Player:
    def __init__(self, goal, enemy, coord):
        self.box_size = 100
        self.coord = coord
        self.goal = goal
        self.enemy = enemy
        self.q_network = agent(layers=[6, 10, 4])
        self.target = agent(layers=[6, 10, 4])
        self.q_network.init_weights()
        self.target.params = self.q_network.params

    def new_game(self, coord, goal, enemy):
        self.coord = coord
        self.goal = goal
        self.enemy = enemy

    def draw(self, display):
        pygame.draw.rect(
            display,
            (0, 0, 255),
            (self.coord[0], self.coord[1], self.box_size, self.box_size),
        )
        pygame.draw.rect(
            display,
            (0, 255, 0),
            (self.goal[0], self.goal[1], self.box_size, self.box_size),
        )
        pygame.draw.rect(
            display,
            (255, 0, 0),
            (self.enemy[0], self.enemy[1], self.box_size, self.box_size),
        )

    def update(self):
        self.q_network.X = np.array(
            [
                self.coord[0],
                self.coord[1],
                self.goal[0],
                self.goal[1],
                self.enemy[0],
                self.enemy[1],
            ]
        )
        if self.epsilon_greedy():
            choice = np.argmax(self.q_network.predict())
        else:
            choice = random.randint(0, 4)
        if choice == 0:
            self.coord = (self.coord[0] + 100, self.coord[1])
        elif choice == 1:
            self.coord = (self.coord[0] - 100, self.coord[1])
        elif choice == 2:
            self.coord = (self.coord[0], self.coord[1] + 100)
        else:
            self.coord = (self.coord[0], self.coord[1] - 100)
        return choice

    def epsilon_greedy(self):
        p = random.randint(1, 100)
        epsilon = 1 * iter
        # Explore = False, Exploit = True
        return p < epsilon

    def check_death(self):
        if (
            self.coord[0] < 0
            or self.coord[1] < 0
            or self.coord[0] + self.box_size > SCREEN_HEIGHT
            or self.coord[1] + self.box_size > SCREEN_HEIGHT
        ):
            return False
        return True

    def update_target(self):
        self.target.params = self.q_network.params


def spawn(length_num):
    green = (
        random.randrange(0, length_num) * 100,
        random.randrange(0, length_num) * 100,
    )
    rose = (
        random.randrange(0, length_num) * 100,
        random.randrange(0, length_num) * 100,
    )
    while rose == green:
        rose = (
            random.randrange(0, length_num) * 100,
            random.randrange(0, length_num) * 100,
        )
    blue = (
        random.randrange(0, length_num) * 100,
        random.randrange(0, length_num) * 100,
    )
    while blue == rose or blue == green:
        blue = (
            random.randrange(0, length_num) * 100,
            random.randrange(0, length_num) * 100,
        )
    return green, rose, blue


def game_loop():
    running = True
    while running:
        prevCoord = player.coord
        screen.fill((0, 0, 0))
        choice = player.update()
        running = player.check_death()
        player.draw(screen)
        reward = 0
        buffer.add_experience(
            prevCoord,
            player.goal,
            player.enemy,
            choice,
            reward,
            player.coord,
            not running,
        )
        pygame.display.set_caption("header")
        pygame.display.flip()
        print(buffer.replay_list)
        clock.tick(15)


length_num = 6
g, r, b = spawn(length_num)
player = Player(g, r, b)
buffer = Exp_Buffer()
iter = 0
while True:
    iter += 1
    g, r, b = spawn(length_num)
    player.new_game(g, r, b)
    game_loop()
