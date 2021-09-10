digits = []
qty = 10

res = ''.join(format(ord(i), 'b') for i in input())
for i in res:
    digits.append(i)


def message(colorA, colorB):
    global digits
    global qty
    print(digits)
    for i in range(qty):
        if int(digits[i]) == 0:
            print(colorA)
        if int(digits[i]) == 1:
            print(colorB)
    digits = digits[1:] + digits[:1]
    print(digits)

while True:
    message("blue", "purple")