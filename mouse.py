from colr import color
from random import randint, choice
import time
import os

# Enviornment
class Board:
    # Initialize class variables
    def __init__(self, numCats, width):
        self.cats = numCats
        self.width = width
        self.board = []
        self.qMap = []

    # Develop a board
    def create(self):
        self.board = [
            ["  " for i in range(self.width + 1)] for j in range(self.width + 1)
        ]
        self.qMap = [[0 for i in range(self.width + 1)] for j in range(self.width + 1)]
        self.catPlace()
        self.board[self.width][self.width] = color("|>", fore="yellow", style="bright")
        self.qMap[self.width][self.width] = 1

    # Place cats randomly
    def catPlace(self):
        tempList = []
        for i in range(self.cats):
            tempList.append([randint(1, self.width - 1), randint(1, self.width - 1)])
        for i in tempList:
            j, k = i[0], i[1]
            self.board[j][k] = color("^^", fore="red", style="bright")
            self.qMap[j][k] = -1

    # Print the board to console
    def display(self, mouse):
        for i in range(len(self.board)):
            print("____", end="")
        print("__\n")
        for i in range(len(self.board)):
            print("|", end="")
            for j in range(len(self.board[0])):
                # print(mouse)
                if mouse == [i, j]:
                    print(color("oo", fore="blue", style="bright"), end="  ")
                else:
                    print(self.board[i][j], end="  ")
            print("|\n")

    # Change Q Values of grid
    def updateQ(self, mouse):
        self.qMap[mouse[0]][mouse[1]] = self.qMap[mouse[0]][mouse[1]] + 0.8 * self.max(
            self.qMap[mouse[0]][mouse[1]]
        )

    # Display current Q Values
    def showQ(self):
        for i in range(len(self.qMap)):
            print("____", end="")
        print("__\n")
        for i in range(len(self.qMap)):
            print("|", end="")
            for j in range(len(self.qMap[0])):
                print(self.qMap[i][j], end="  ")
            print("|\n")

    def max(self, agent):
        options = []
        try:
            if agent[0] == 0:
                options.append(-1000)
            else:
                options.append(self.qMap[agent[0] - 1][agent[1]])
        except:
            options.append(-1000)
        try:
            options.append(self.qMap[agent[0] + 1][agent[1]])
        except:
            options.append(-1000)
        try:
            if agent[1] == 0:
                options.append(-1000)
            else:
                options.append(self.qMap[agent[0]][agent[1] - 1])
        except:
            options.append(-1000)
        try:
            options.append(self.qMap[agent[0]][agent[1] + 1])
        except:
            options.append(-1000)
        if max(options) > -1000:
            return max(options)
        else:
            print(max(options))
            return 0


# Agent
class Mouse:
    # Initialize class variables
    def __init__(self, episode):
        self.actions = ["Up", "Down", "Left", "Right"]
        self.episode = episode
        self.coords = [0, 0]

    # Move the mouse in the area
    def move(self, enviornment):
        epsilon = self.episode - randint(0, 1000)
        if epsilon > 0:
            change = self.exploit(enviornment)
        else:
            change = self.explore(enviornment)
        if change == 0:
            self.coords[0] -= 1
        elif change == 1:
            self.coords[0] += 1
        elif change == 2:
            self.coords[1] -= 1
        else:
            self.coords[1] += 1

    # Determine the best possible location given current information
    def exploit(self, enviornment):
        options = []
        try:
            if self.coords[0] == 0:
                options.append(-99)
            else:
                options.append(enviornment.qMap[self.coords[0] - 1][self.coords[1]])
        except:
            options.append(-100)
        try:
            options.append(enviornment.qMap[self.coords[0] + 1][self.coords[1]])
        except:
            options.append(-99)
        try:
            if self.coords[0] == 0:
                options.append(-100)
            else:
                options.append(enviornment.qMap[self.coords[0]][self.coords[1] - 1])
        except:
            options.append(-100)
        try:
            options.append(enviornment.qMap[self.coords[0]][self.coords[1] + 1])
        except:
            options.append(-100)
        maxQ = max(options)
        if maxQ < 0:
            return self.explore()
        return options.index(maxQ)

    # Choose a random direction
    def explore(self, enviornment):
        options = [0, 1, 2, 3]
        if self.coords[0] == 0:
            options.remove(0)
        if self.coords[1] == 0:
            options.remove(2)
        if self.coords[0] == (len(enviornment) - 1):
            options.remove(1)
        if self.coords[1] == (len(enviornment) - 1):
            options.remove(3)
        temp = choice(options)
        return temp


# Run 1 episode, from spawn until cheese or cat
def episode(epNum):
    maurice = Mouse(epNum)
    running = True
    field.showQ()
    input()
    # Each loop is 1 action
    while running:
        os.system("cls" if os.name == "nt" else "clear")
        maurice.move(field.board)
        field.display(maurice.coords)
        field.updateQ(maurice.coords)
        field.showQ()
        time.sleep(0.5)


field = Board(4, 4)
field.create()

for i in range(1000):
    episode(i)
