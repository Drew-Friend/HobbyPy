x = ["x", "y", "z", "a", "b", "c", "d", "e", "f", "g"]
a = []
b = str(120)
tupe = []

# Get all known variables
def ask():
    n = int(input("Number of variables: "))
    for i in range(n):
        aTemp = input("What is coefficient {}? ".format(i + 1))
        if not aTemp.startswith("-"):
            aTemp = "+" + aTemp
        a.append(aTemp)
    bIn = input("What is the constant? ")
    if not bIn.startswith("-"):
        bIn = "+" + bIn
    for i in range(len(a)):
        print(a[i], end="")
        print(x[i], end=" ")
    print("={}".format(bIn))
    return bIn


# solve with t as x1
def solveT():
    for i in range(len(a)):
        #   (-a1 t + B ) / ai
        tupe.append(
            str(-1 * int(a[0]) / int(a[i])) + "t + " + str((int(b)) / int(a[i]))
        )
    tupe[0] = "t"
    print(tupe)


b = ask()
solveT()
input()
