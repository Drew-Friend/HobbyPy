# Maze generator -- Randomized Prim Algorithm

## Imports
from audioop import findmax
import random
import time
from colorama import init
from colorama import Fore, Back, Style


class Environment:
    def __init__(self, w, h):
        # Init variables
        self.wal = "||"
        self.path = "  "
        self.unvisited = "u"
        self.head = "<>"
        self.height = h
        self.width = w
        self.maze = []

    ## Functions
    def printMaze(self):
        walk = []
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.maze[i][j] == self.path:
                    print(Fore.GREEN + Back.BLACK + str(self.maze[i][j]), end="")
                    walk.append((i, j))
                elif self.maze[i][j] == self.head:
                    print(Fore.BLUE + Back.BLACK + str(self.maze[i][j]), end="")
                    walk.append((i, j))
                else:
                    print(Fore.WHITE + Back.WHITE + str(self.maze[i][j]), end="")

            print(Fore.BLUE + Back.BLACK + "")
        return walk

    # Find number of surrounding cells
    def surroundingCells(self, rand_wall):
        s_cells = 0
        if self.maze[rand_wall[0] - 1][rand_wall[1]] == self.path:
            s_cells += 1
        if self.maze[rand_wall[0] + 1][rand_wall[1]] == self.path:
            s_cells += 1
        if self.maze[rand_wall[0]][rand_wall[1] - 1] == self.path:
            s_cells += 1
        if self.maze[rand_wall[0]][rand_wall[1] + 1] == self.path:
            s_cells += 1

        return s_cells

    # Initialize colorama
    def create(self):
        init()

        # Denote all cells as unvisited
        for i in range(0, self.height):
            line = []
            for j in range(0, self.width):
                line.append(self.unvisited)
            self.maze.append(line)

        # Randomize starting point and set it a cell
        starting_height = int(random.random() * self.height)
        starting_width = int(random.random() * self.width)
        if starting_height == 0:
            starting_height += 1
        if starting_height == self.height - 1:
            starting_height -= 1
        if starting_width == 0:
            starting_width += 1
        if starting_width == self.width - 1:
            starting_width -= 1

        # Mark it as cell and add surrounding walls to the list
        self.maze[starting_height][starting_width] = self.path
        walls = []
        walls.append([starting_height - 1, starting_width])
        walls.append([starting_height, starting_width - 1])
        walls.append([starting_height, starting_width + 1])
        walls.append([starting_height + 1, starting_width])

        # Denote walls in maze
        self.maze[starting_height - 1][starting_width] = self.wal
        self.maze[starting_height][starting_width - 1] = self.wal
        self.maze[starting_height][starting_width + 1] = self.wal
        self.maze[starting_height + 1][starting_width] = self.wal

        while walls:
            # Pick a random wall
            rand_wall = walls[int(random.random() * len(walls)) - 1]

            # Check if it is a left wall
            if rand_wall[1] != 0:
                if (
                    self.maze[rand_wall[0]][rand_wall[1] - 1] == "u"
                    and self.maze[rand_wall[0]][rand_wall[1] + 1] == self.path
                ):
                    # Find the number of surrounding cells
                    s_cells = self.surroundingCells(rand_wall)

                    if s_cells < 2:
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = self.path

                        # Mark the new walls
                        # Upper cell
                        if rand_wall[0] != 0:
                            if self.maze[rand_wall[0] - 1][rand_wall[1]] != self.path:
                                self.maze[rand_wall[0] - 1][rand_wall[1]] = self.wal
                            if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                                walls.append([rand_wall[0] - 1, rand_wall[1]])

                        # Bottom cell
                        if rand_wall[0] != self.height - 1:
                            if self.maze[rand_wall[0] + 1][rand_wall[1]] != self.path:
                                self.maze[rand_wall[0] + 1][rand_wall[1]] = self.wal
                            if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                                walls.append([rand_wall[0] + 1, rand_wall[1]])

                        # Leftmost cell
                        if rand_wall[1] != 0:
                            if self.maze[rand_wall[0]][rand_wall[1] - 1] != self.path:
                                self.maze[rand_wall[0]][rand_wall[1] - 1] = self.wal
                            if [rand_wall[0], rand_wall[1] - 1] not in walls:
                                walls.append([rand_wall[0], rand_wall[1] - 1])

                    # Delete wall
                    for wall in walls:
                        if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                            walls.remove(wall)

                    continue

            # Check if it is an upper wall
            if rand_wall[0] != 0:
                if (
                    self.maze[rand_wall[0] - 1][rand_wall[1]] == "u"
                    and self.maze[rand_wall[0] + 1][rand_wall[1]] == self.path
                ):

                    s_cells = self.surroundingCells(rand_wall)
                    if s_cells < 2:
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = self.path

                        # Mark the new walls
                        # Upper cell
                        if rand_wall[0] != 0:
                            if self.maze[rand_wall[0] - 1][rand_wall[1]] != self.path:
                                self.maze[rand_wall[0] - 1][rand_wall[1]] = self.wal
                            if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                                walls.append([rand_wall[0] - 1, rand_wall[1]])

                        # Leftmost cell
                        if rand_wall[1] != 0:
                            if self.maze[rand_wall[0]][rand_wall[1] - 1] != self.path:
                                self.maze[rand_wall[0]][rand_wall[1] - 1] = self.wal
                            if [rand_wall[0], rand_wall[1] - 1] not in walls:
                                walls.append([rand_wall[0], rand_wall[1] - 1])

                        # Rightmost cell
                        if rand_wall[1] != self.width - 1:
                            if self.maze[rand_wall[0]][rand_wall[1] + 1] != self.path:
                                self.maze[rand_wall[0]][rand_wall[1] + 1] = self.wal
                            if [rand_wall[0], rand_wall[1] + 1] not in walls:
                                walls.append([rand_wall[0], rand_wall[1] + 1])

                    # Delete wall
                    for wall in walls:
                        if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                            walls.remove(wall)

                    continue

            # Check the bottom wall
            if rand_wall[0] != self.height - 1:
                if (
                    self.maze[rand_wall[0] + 1][rand_wall[1]] == "u"
                    and self.maze[rand_wall[0] - 1][rand_wall[1]] == self.path
                ):

                    s_cells = self.surroundingCells(rand_wall)
                    if s_cells < 2:
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = self.path

                        # Mark the new walls
                        if rand_wall[0] != self.height - 1:
                            if self.maze[rand_wall[0] + 1][rand_wall[1]] != self.path:
                                self.maze[rand_wall[0] + 1][rand_wall[1]] = self.wal
                            if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                                walls.append([rand_wall[0] + 1, rand_wall[1]])
                        if rand_wall[1] != 0:
                            if self.maze[rand_wall[0]][rand_wall[1] - 1] != self.path:
                                self.maze[rand_wall[0]][rand_wall[1] - 1] = self.wal
                            if [rand_wall[0], rand_wall[1] - 1] not in walls:
                                walls.append([rand_wall[0], rand_wall[1] - 1])
                        if rand_wall[1] != self.width - 1:
                            if self.maze[rand_wall[0]][rand_wall[1] + 1] != self.path:
                                self.maze[rand_wall[0]][rand_wall[1] + 1] = self.wal
                            if [rand_wall[0], rand_wall[1] + 1] not in walls:
                                walls.append([rand_wall[0], rand_wall[1] + 1])

                    # Delete wall
                    for wall in walls:
                        if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                            walls.remove(wall)

                    continue

            # Check the right wall
            if rand_wall[1] != self.width - 1:
                if (
                    self.maze[rand_wall[0]][rand_wall[1] + 1] == "u"
                    and self.maze[rand_wall[0]][rand_wall[1] - 1] == self.path
                ):

                    s_cells = self.surroundingCells(rand_wall)
                    if s_cells < 2:
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = self.path

                        # Mark the new walls
                        if rand_wall[1] != self.width - 1:
                            if self.maze[rand_wall[0]][rand_wall[1] + 1] != self.path:
                                self.maze[rand_wall[0]][rand_wall[1] + 1] = self.wal
                            if [rand_wall[0], rand_wall[1] + 1] not in walls:
                                walls.append([rand_wall[0], rand_wall[1] + 1])
                        if rand_wall[0] != self.height - 1:
                            if self.maze[rand_wall[0] + 1][rand_wall[1]] != self.path:
                                self.maze[rand_wall[0] + 1][rand_wall[1]] = self.wal
                            if [rand_wall[0] + 1, rand_wall[1]] not in walls:
                                walls.append([rand_wall[0] + 1, rand_wall[1]])
                        if rand_wall[0] != 0:
                            if self.maze[rand_wall[0] - 1][rand_wall[1]] != self.path:
                                self.maze[rand_wall[0] - 1][rand_wall[1]] = self.wal
                            if [rand_wall[0] - 1, rand_wall[1]] not in walls:
                                walls.append([rand_wall[0] - 1, rand_wall[1]])

                    # Delete wall
                    for wall in walls:
                        if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                            walls.remove(wall)

                    continue

            # Delete the wall from the list anyway
            for wall in walls:
                if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                    walls.remove(wall)

        # Mark the remaining unvisited cells as walls
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.maze[i][j] == "u":
                    self.maze[i][j] = self.wal

        # Set exit and entrance
        for i in range(self.width - 1, 0, -1):
            if self.maze[self.height - 2][i] == self.path:
                self.maze[self.height - 1][i] = self.path
                break

        for i in range(0, self.width):
            if self.maze[1][i] == self.path:
                self.maze[0][i] = self.path
                return (0, i)

    def populate(self, path, map):
        # For each action, see if the resulting coordinate pair is found in path. If so, set the S/A value to the path index of the pair
        for index in range(len(map)):
            # path[index] gives the coordinate pair of the state
            try:
                map[index][0] = path.index((path[index][0], path[index][1] - 1))
            except:
                map[index][0] = -1
            try:
                map[index][1] = path.index((path[index][0] + 1, path[index][1]))
            except:
                map[index][1] = -1
            try:
                map[index][2] = path.index((path[index][0], path[index][1] + 1))
            except:
                map[index][2] = -1
            try:
                map[index][3] = path.index((path[index][0] - 1, path[index][1]))
            except:
                map[index][3] = -1


class Agent_Q:
    def __init__(self, len, actions):
        # Q map is a table of State, Action, and q val/ future state
        # [Q/S`][S][A]
        self.Qmap = [
            [[0 for i in range(actions)] for j in range(len)] for k in range(2)
        ]
        self.epsilon = 0
        self.column = 0

    def epsilonGreedy(self):
        # Insert formula here
        p = random.randint(0, 1)
        while True:
            if p > self.epsilon:
                # Exploit
                choice = self.findMax()
            else:
                # Explore
                choice = random.randint(0, 3)

            # Update coords if move is valid
            if self.Qmap[1][self.column][choice] != -1:
                self.column = self.Qmap[1][self.column][choice]
                return

    def updateValue(self):
        bigBoi = self.findMax()
        # Insert formula here

    def findMax(self):
        # Maximum value of the bottom(q) table, in the current column(state)
        val = max(self.Qmap[0][self.column])
        boop = []
        for check in range(len(self.Qmap[0][self.column])):
            if self.Qmap[0][self.column][check] == val:
                boop.append(check)
        index = random.randrange(0, len(boop))
        return boop[index]


# V Runtime Code V#
width = 18
height = 7
maze = Environment(width, height)
maze.create()
path = maze.printMaze()

actionNum = 4
jimmy = Agent_Q(len(path), actionNum)
maze.populate(path, jimmy.Qmap[1])

complete = False

while not complete:
    # print(jimmy.Qmap[1][jimmy.column])
    # print(jimmy.Qmap[0][jimmy.column])
    prev = path[jimmy.column]
    jimmy.epsilonGreedy()
    head = path[jimmy.column]
    maze.maze[prev[0]][prev[1]] = maze.path
    maze.maze[head[0]][head[1]] = maze.head
    maze.printMaze()
    if head[1] == height - 1:
        complete = True
        jimmy.epsilon += 1
    input()
