import random


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


playerInput = input("Please enter 3 number: ")

ans = []

for i in range(3):
    ans.append(str(random.randint(0, 9)))


end = False

while end != True:
    for x in range(3):
        if playerInput[x] == ans[x]:
            print(f"{bcolors.FAIL}RED{bcolors.ENDC}", end=" ")
        elif playerInput[x] in ans:
            print(f"{bcolors.WARNING}YELLOW{bcolors.ENDC}", end=" ")
        else:
            print("WHITE", end=" ")

    # print(''.join(ans))

    if playerInput == ''.join(ans):
        print("\nCongratz! You have won the game!")
        end = True
    else:
        print("\nSorry you are not correct, try again.\n")
        playerInput = input("Please enter 3 number: ")
