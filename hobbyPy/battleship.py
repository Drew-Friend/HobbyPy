import random
import os

AIBoard = [[" " for i in range(10)] for j in range(10)]
AIBoardVisible = [[" " for i in range(10)] for j in range(10)]
AIBoats = []
boatID = [0, 1, 2, 3, 4]
playerBoard = [[" " for i in range(10)] for j in range(10)]
playerBoats = []
turnNum = 0
hitList = [0, 0, 0, 0, "X"]  # Active Y, Active X, Y Modifier, X Modifier, direction
activeTarget = False
knownDirection = False
inProgress = True


def printboard(board, player):
    """Print the the board of selected player"""
    Axis = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    print("This is {} current board".format(player))  # Tell who's board
    print("    1 2 3 4 5 6 7 8 9 10")  # Display axis
    for i in range(10):  # Display entire board, including Y axis label
        print(
            "{}:  {} {} {} {} {} {} {} {} {} {}".format(
                Axis[i],
                board[i][0],
                board[i][1],
                board[i][2],
                board[i][3],
                board[i][4],
                board[i][5],
                board[i][6],
                board[i][7],
                board[i][8],
                board[i][9],
            )
        )


def playerSetup(boats, board):
    """Player places their ships"""
    boatNames = ["Carrier", "Battleship", "Cruiser", "Submarine", "Destroyer"]
    boatLengths = [5, 4, 3, 3, 2]
    i = 0
    while i < 5:  # For each boat
        altering = True
        Ycoord = input(  # Choose Y coordinate(A-J)
            "Choose the topmost coordinate for your {}: ".format(boatNames[i])
        )
        Ycoord = ord(Ycoord) - 65  # ASCII translation
        Xcoord = input(  # Choose X coordinate(1-10)
            "Choose the leftmost coordinate for your {}: ".format(boatNames[i])
        )
        Xcoord = int(Xcoord) - 1  # list starts at 0
        orient = input(  # Choose vertical or horizontal
            "Is this boat Horizontal(H) or Vertical(V)? "
        )
        while altering:  # Add boat to board, and error check
            for j in range(10):
                if Ycoord == j:
                    for k in range(10):
                        if Xcoord == k:
                            intersectCheck = 0
                            if orient == "V" or orient == "v":
                                if j + boatLengths[i] <= 10:
                                    altering = False
                                    for l in range(boatLengths[i]):
                                        if board[j + l][k] == " ":
                                            intersectCheck += 1
                                    if intersectCheck == boatLengths[i]:
                                        for l in range(boatLengths[i]):
                                            board[j + l][k] = i
                                        i += 1
                                    else:
                                        print(
                                            "Boats intersected, please place your {} again".format(
                                                boatNames[i]
                                            )
                                        )
                                        altering = False
                                else:
                                    Ycoord = input(
                                        "Please input valid topmost coordinate: "
                                    )
                                    Ycoord = ord(Ycoord) - 65
                            elif orient == "H" or orient == "h":
                                if k + boatLengths[i] <= 10:
                                    altering = False
                                    for l in range(boatLengths[i]):
                                        if board[j][k + l] == " ":
                                            intersectCheck += 1
                                    if intersectCheck == boatLengths[i]:
                                        for l in range(boatLengths[i]):
                                            board[j][k + l] = i
                                        i += 1
                                    else:
                                        print(
                                            "Boats intersected, please place your {} again".format(
                                                boatNames[i]
                                            )
                                        )
                                        altering = False
                                else:
                                    Xcoord = input(
                                        "Please input valid leftmost coordinate: "
                                    )
                                    Xcoord = int(Xcoord) - 1
                            else:
                                input("Please input valid orientation(H or V): ")
                            break
                    else:
                        Xcoord = input("Please input valid leftmost coordinate: ")
                        Xcoord = int(Xcoord) - 1
                    break
            else:
                Ycoord = input("Please input valid topmost coordinate: ")
                Ycoord = ord(Ycoord) - 65
        boats.append((Xcoord, Ycoord, orient))  # add the boat to the list
        printboard(board, "your")


def AISetup(boats, board):
    """AI randomly places it's boats"""
    boatLengths = [5, 4, 3, 3, 2]
    for i in range(len(boatLengths)):
        checking = True
        while checking:
            intersectCheck = 0
            Xcoord = random.randint(0, 9)
            Ycoord = random.randint(0, 9)
            orient = random.randint(0, 1)  # 0 for vertical, 1 for horizontal
            if orient == 0:
                if Xcoord + boatLengths[i] < 10:
                    for j in range(boatLengths[i]):
                        if board[Ycoord][Xcoord + j] == " ":
                            intersectCheck += 1
                    if intersectCheck == boatLengths[i]:
                        for j in range(boatLengths[i]):
                            board[Ycoord][Xcoord + j] = i
                        checking = False
            else:
                if Ycoord + boatLengths[i] < 10:
                    for j in range(boatLengths[i]):
                        if board[Ycoord + j][Xcoord] == " ":
                            intersectCheck += 1
                    if intersectCheck == boatLengths[i]:
                        for j in range(boatLengths[i]):
                            board[Ycoord + j][Xcoord] = i
                        checking = False


def FIREEEEEEEE(hidden, visible):
    """Player chooses where to fire"""
    checking = True
    while checking:
        targetY = ord(input("Choose y coordinate for target: ")) - 65
        targetX = int(input("Choose x coordinate for target: ")) - 1
        if targetX <= 9 and targetX >= 0 and targetY <= 9 and targetY >= 0:
            if visible[targetY][targetX] == " ":
                if hidden[targetY][targetX] != " ":
                    visible[targetY][targetX] = "%"
                    hidden[targetY][targetX] = "%"
                    os.system("cls" if os.name == "nt" else "clear")
                    print("Hit!")
                else:
                    visible[targetY][targetX] = "~"
                    hidden[targetY][targetX] = "~"
                    os.system("cls" if os.name == "nt" else "clear")
                    print("Miss!")
                checking = False
        else:
            print("Please pick a valid target")
    printboard(visible, "The AI's")


def hitCheck(y, x, board):
    """AI checks if it hit or missed"""
    if board[y][x] == " ":
        board[y][x] = "~"
        print("They missed!")
        return False
    else:
        board[y][x] = "%"
        print("They got a hit!")
        return True


def circleCheck(y, x, board):
    """AI checks circle around the last accurate shot"""
    global hitList
    global knownDirection
    knownDirection = True
    if x != 0:  # Left
        if board[y][x - 1] != "~" and board[y][x - 1] != "%":
            if hitCheck(y, x - 1, board):
                hitList[2], hitList[3], hitList[4] = 0, hitList[3] - 1, "L"
                return True
            else:
                knownDirection = False
                return False
    if y != 0:  # Up
        if board[y - 1][x] != "~" and board[y - 1][x] != "%":
            if hitCheck(y - 1, x, board):
                hitList[2], hitList[3], hitList[4] = hitList[2] - 1, 0, "U"
                return True
            else:
                knownDirection = False
                return False
    if x != 9:  # Right
        if board[y][x + 1] != "~" and board[y][x + 1] != "%":
            if hitCheck(y, x + 1, board):
                hitList[2], hitList[3], hitList[4] = 0, hitList[3] + 1, "R"
                return True
            else:
                knownDirection = False
                return False
    if y != 9:  # Down
        if board[y + 1][x] != "~" and board[y + 1][x] != "%":
            if hitCheck(y + 1, x, board):
                hitList[2], hitList[3], hitList[4] = hitList[2] + 1, 0, "D"
                return True
            else:
                knownDirection = False
                return False
    else:  # No Valid Target
        knownDirection = False
        return False


def AIFire(board):
    """AI decides where to shoot"""
    global hitList
    global activeTarget
    global knownDirection
    checking = True
    if activeTarget:  # Hit, and boat hasn't sunk
        if knownDirection:  # Multiple hits, computer knows orientation
            if (
                hitList[4] == "U"
                and board[hitList[0] + hitList[2] - 1][hitList[1] + hitList[3]] != "~"
                and board[hitList[0] + hitList[2] - 1][hitList[1] + hitList[3]] != "%"
            ):
                if hitCheck(hitList[0] + hitList[2] - 1, hitList[1], board):
                    hitList[2] = hitList[2] - 1
            elif (
                hitList[4] == "D"
                and board[hitList[0] + hitList[2] + 1][hitList[1] + hitList[3]] != "~"
                and board[hitList[0] + hitList[2] + 1][hitList[1] + hitList[3]] != "%"
            ):
                if hitCheck(
                    hitList[0] + hitList[2] + 1, hitList[1] + hitList[3], board
                ):
                    hitList[2] = hitList[2] + 1
            elif (
                hitList[4] == "L"
                and board[hitList[0] + hitList[2]][hitList[1] + hitList[3] - 1] != "~"
                and board[hitList[0] + hitList[2]][hitList[1] + hitList[3] - 1] != "%"
            ):
                if hitCheck(hitList[0], hitList[1] + hitList[3] - 1, board):
                    hitList[3] = hitList[3] - 1
            elif (
                hitList[4] == "R"
                and board[hitList[0] + hitList[2]][hitList[1] + hitList[3] + 1] != "~"
                and board[hitList[0] + hitList[2]][hitList[1] + hitList[3] + 1] != "%"
            ):
                if hitCheck(hitList[0], hitList[1] + hitList[3] + 1, board):
                    hitList[3] = hitList[3] + 1
            else:  # Check opposite direction
                if hitList[4] == "L":  # If it's horizontal, check the right
                    if (
                        board[hitList[0]][hitList[1] + 1] != "~"
                        and board[hitList[0]][hitList[1] + 1] != "%"
                    ):
                        if hitCheck(hitList[0], hitList[1] + 1, board):
                            hitList[2], hitList[3], hitList[4] = 0, 1, "R"
                    else:  # In case of 2 boats touching
                        circleCheck(
                            hitList[0] + hitList[2], hitList[1] + hitList[3], board
                        )
                elif hitList[4] == "U":  # If it's vertical, check the bottom
                    if (
                        board[hitList[0] + 1][hitList[1]] != "~"
                        and board[hitList[0] + 1][hitList[1]] != "%"
                    ):
                        if hitCheck(hitList[0] + 1, hitList[1], board):
                            hitList[2], hitList[3], hitList[4] = 1, 0, "D"
                    else:  # In case of 2 boats touching
                        circleCheck(
                            hitList[0] + hitList[2], hitList[1] + hitList[3], board
                        )
                else:
                    print("problem")
        elif not circleCheck(
            hitList[0] + hitList[2], hitList[1] + hitList[3], board
        ):  # Does not know orientation
            hitCheck(random.randint(0, 9), random.randint(0, 9), board)
    else:  # No boat, random guess
        y = random.randint(0, 9)
        x = random.randint(0, 9)
        while board[y][x] == "~" or board[y][x] == "%":
            y = random.randint(0, 9)
            x = random.randint(0, 9)
        if hitCheck(y, x, board):
            hitList[0], hitList[1] = y, x
            activeTarget = True
        else:
            hitList[0], hitList[1] = 0, 0
            activeTarget = False


def sinkCheck(board, who="nope"):
    """Check which boats are sunk"""
    global hitList
    global activeTarget
    global knownDirection
    global boatID
    boatNames = ["Carrier", "Battleship", "Cruiser", "Submarine", "Destroyer"]
    boatsSeen = set()
    for i in range(5):
        for j in range(10):
            for k in range(len(board[j])):
                if board[j][k] == i:
                    boatsSeen.add(i)
    if who == "ai":
        for i in boatID:
            if i not in boatsSeen:
                print("The {} is gone!".format(boatNames[i]))
                boatID.remove(i)
                activeTarget = False
                knownDirection = False
                for i in range(4):
                    hitList[i] = 0
                hitList[4] = "X"
    else:
        for i in range(5):
            if i not in boatsSeen:
                print("The {} is gone!".format(boatNames[i]))
    if boatsSeen == set():
        return False
    else:
        return True


def turn(AIBoard, AIBoardVisible, AIBoats, playerBoard, playerBoats, turnNum):
    """One turn cycle, both players have the chance to shoot"""
    winner = "null"
    turnNum = turnNum + 1
    print("Turn {}, Player can fire:".format(turnNum))
    input("Press enter to continue")
    os.system("cls" if os.name == "nt" else "clear")
    printboard(AIBoardVisible, "The AI's")
    FIREEEEEEEE(AIBoard, AIBoardVisible)
    if not sinkCheck(AIBoard):
        winner = "You"
        return winner
    print("AI can now fire")
    input("Press enter to continue")
    os.system("cls" if os.name == "nt" else "clear")
    AIFire(playerBoard)
    printboard(playerBoard, "your")
    if not sinkCheck(playerBoard, "ai"):
        winner = "the AI"
        return winner
    return winner


# v  The Game   v#
playerSetup(playerBoats, playerBoard)
AISetup(AIBoats, AIBoard)
while inProgress:
    winner = turn(AIBoard, AIBoardVisible, AIBoats, playerBoard, playerBoats, turnNum)
    if winner != "null":
        inProgress = False
        input("Game over, {} won!".format(winner))
