from numpy.core.fromnumeric import choose
import pygame
import numpy as np
from pygame.constants import QUIT
import pygame.draw
import random
from pygame.locals import K_UP, K_ESCAPE, KEYDOWN, QUIT, K_LEFT, K_RIGHT
from nn_Sigmoid import NeuralNet as agent


class Player:
    init_x = 100
    init_y = 400

    def __init__(self):
        self.x = Player.init_x
        self.y = Player.init_y
        self.dead = False
        self.width = 25
        self.height = 25
        self.ups = 15
        self.speed = 0
        self.grav = 1
        self.network = agent(layers=[6, 10, 1])
        self.network.init_weights()

    def draw_it(self, display):
        pygame.draw.rect(
            display, self.network.color, (self.x, self.y, self.width, self.height)
        )

    def update(self):
        if self.speed < 10:
            self.speed += self.grav
        self.y += self.speed
        self.network.X = np.array(
            [
                self.speed,
                self.y,
                pips[0].bottom_surface,
                pips[0].x,
                pips[1].bottom_surface,
                pips[1].x,
            ]
        )
        for p in pips:
            # Collision with bottom
            if (
                self.y + self.height > p.bottom_surface
                or self.y < p.bottom_surface - 150
            ):
                if self.x + self.width > p.x and self.x < p.x + p.width:
                    return True
        if self.y > SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height
        if self.y < 0:
            self.y = 0
        return False

    def jump(self):
        self.speed -= self.ups


class Pipes:
    def __init__(self, x=600):
        self.x = x
        self.width = 60
        self.bottom_surface = random.randint(200, SCREEN_HEIGHT - 50)

    def draw_it(self, display):
        pygame.draw.rect(
            display,
            (255, 255, 255),
            (
                self.x,
                self.bottom_surface,
                self.width,
                SCREEN_HEIGHT - self.bottom_surface,
            ),
        )
        pygame.draw.rect(
            display,
            (255, 255, 255),
            (
                self.x,
                0,
                self.width,
                self.bottom_surface - 150,
            ),
        )

    def update(self):
        self.x -= 2
        return self.x


class BreedingPool:
    def __init__(self, numParent, popList):
        self.list = popList
        self.size = len(popList)
        self.numParent = numParent
        self.parents = [-1 for i in range(self.numParent)]

    def sort_key(self, e):
        return e[1]

    def chooseParents(self):
        self.list.sort(key=self.sort_key)
        for kk in range(self.numParent):
            self.parents[kk] = self.list[-(kk + 1)][0]

    def combine(self, parent1, parent2, child):
        # What are the genes I need
        # Color, 3 values
        # child.color = [
        #     parent1.network.color[0],
        #     parent2.network.color[1],
        #     parent1.network.color[2],
        # ]
        for h in range(len(child.params["W1"])):
            for w in range(len(child.params["W1"][h])):
                par = random.randint(1, 2)
                if par == 1:
                    child.params["W1"][h][w] = parent1.network.params["W1"][h][w]
                else:
                    child.params["W1"][h][w] = parent2.network.params["W1"][h][w]
        for h in range(len(child.params["W2"])):
            for w in range(len(child.params["W2"][h])):
                par = random.randint(1, 2)
                if par == 1:
                    child.params["W2"][h][w] = parent1.network.params["W2"][h][w]
                else:
                    child.params["W2"][h][w] = parent2.network.params["W2"][h][w]
        for h in range(len(child.params["b1"])):
            par = random.randint(1, 2)
            if par == 1:
                child.params["b1"][h] = parent1.network.params["b1"][h]
            else:
                child.params["b1"][h] = parent2.network.params["b1"][h]
        for h in range(len(child.params["b2"])):
            par = random.randint(1, 2)
            if par == 1:
                child.params["b2"][h] = parent1.network.params["b2"][h]
            else:
                child.params["b2"][h] = parent2.network.params["b2"][h]

    def mutate(self, child, gen):
        mutSize = 400 // (gen / 15)
        mutSize = min(400, mutSize)
        # Leave the parents unmutated
        # child.color = [
        #     child.color[0] + random.randint(-20, +20),
        #     child.color[1] + random.randint(-20, +20),
        #     child.color[2] + random.randint(-20, +20),
        # ]
        # for dff in range(len(child.color)):
        #     if child.color[dff] < 0:
        #         child.color[dff] = 0
        #     if child.color[dff] > 255:
        #         child.color[dff] = 255
        child.params["W1"][random.randrange(0, child.layers[0])][
            random.randrange(0, child.layers[1])
        ] += (random.randint(-1 * mutSize, mutSize) / 500)
        child.params["W2"][random.randrange(0, child.layers[1])][
            random.randrange(0, child.layers[2])
        ] += (random.randint(-1 * mutSize, mutSize) / 500)
        child.params["b1"][random.randrange(0, child.layers[1])] += (
            random.randint(-1 * mutSize, mutSize) / 500
        )
        child.params["b2"][random.randrange(0, child.layers[2])] += (
            random.randint(-1 * mutSize, mutSize) / 500
        )

    def new_gen(self, gen):
        self.chooseParents()
        for c in range(self.size - self.numParent):
            rel = c % self.numParent
            self.combine(
                self.parents[rel], self.parents[rel - 1], self.list[c][0].network
            )
            self.mutate(self.list[c][0].network, gen)


# v Game Shit v#
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
speed = 60
pips = []
ADDPOINT = pygame.USEREVENT + 2
pygame.time.set_timer(ADDPOINT, 100)
# ^ Game Shit ^#

# v AI Shit v#
population = 500
generations = 10000
players = [[Player(), -1] for i in range(population)]
bedroom = BreedingPool(4, players)
# ^ AI Shit ^#

for a in range(generations):
    # v 1 Game Loop v#
    pips = [Pipes(x=450), Pipes(x=780)]
    for b in players:
        b[1] = 0
        b[0].dead = False
        b[0].y = Player.init_y
        b[0].speed = 0
        b[0].update()
    score = 0
    display_score = 0
    running = True
    while running:
        killCount = 0
        running = False

        screen.fill((0, 0, 0))
        for pip in pips:
            pip.update()
            pip.draw_it(screen)
        if pips[0].x < -60:
            del pips[0]
            pips.append(Pipes())
        if pips[0].x == 40:
            display_score += 1

        for player in players:
            if not player[0].dead:
                running = True
                if player[0].network.predict() == 1:
                    player[0].jump()
                player[0].dead = player[0].update()
                if player[0].dead:
                    player[1] = score
                player[0].draw_it(screen)
            else:
                killCount += 1

        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == pygame.KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == pygame.K_LEFT:
                    speed -= 30
                    print(speed)
                if event.key == pygame.K_RIGHT:
                    speed += 30
                    print(speed)
                if event.key == pygame.K_ESCAPE:
                    running = False
                    for player in players:
                        if player[1] == -1:
                            player[1] = score
                # elif event.key == pygame.K_SPACE:
                #     #player.jump()
            elif event.type == pygame.QUIT:
                running = False
                for player in players:
                    if player[1] == -1:
                        player[1] = score
            elif event.type == ADDPOINT:
                score += 1
        header = "Score: {}        Generation: {}        Living: {}".format(
            display_score, a + 1, len(players) - killCount
        )
        pygame.display.set_caption(header)
        pygame.display.flip()
        clock.tick(speed)
        if a == 9999:
            input()
    bedroom.new_gen(a + 1)
    # ^ 1 Game Loop ^ #
