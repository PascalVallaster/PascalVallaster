# OpenSource by Thorsten Altenkirch
#   => www.youtube.com/watch?v=G_UYXzGuqvM


from sys import stdout


sudoku = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  #  0
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  #  1
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  #  3
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  #  4
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  #  5  x
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  #  6
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  #  7
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  #  8
    [0, 0, 0, 0, 0, 0, 0, 0, 0]   #  9
]
#    0  1  2  3  4  5  6  7  8
#                y


blocks = [[0, 2], [3, 5], [6, 8]]


def create_sudoku():
    global sudoku

    print("Input the numbers from the sudoku line by line.")
    print("For empty spaces type in 0.")
    # numbers = input("Numbers:")
    # numbers = "200000900003060002001095700000034009020000040400850000008170200100040300007000006"
    numbers = "000000000000000000000000000000000000000000000000000000000000000000000000000000000"

    if not numbers:
        exit(f"\nYour input is empty!\n  Input: ''")

    try:
        int(numbers)
    except ValueError:
        exit(f"\nYour input contains non-numeral characters!\n  Input: {numbers}")

    if len(numbers) != 81:
        exit(f"\nYour input hasn't the correct length of 81 digest!\n  Input: {numbers}")

    num_counter = 0
    for y in range(9):
        for x in range(9):
            sudoku[y][x] = int(numbers[num_counter])
            num_counter += 1

    print()


def print_sudoku():
    global sudoku
    boarder = "+-----------+-----------+-----------+"

    for i in range(3):
        print(boarder)
        for _lines in sudoku[blocks[i][0]:blocks[i][1] + 1]:
            counter = 1
            for element in _lines:
                stdout.write(f"| {element} ")
                stdout.flush()
                counter += 1
            print("|")

    print(boarder)


def possible(y, x, n):
    global sudoku
    block_list = []

    # Get row at position y
    for element in sudoku[y]:
        if element == n:
            return False

    # Get Column at position x
    for line in sudoku:
        if line[x] == n:
            return False

    # Get square of the current position (x|y)

    x_count = 0
    for block_x in blocks:
        if block_x[0] <= x <= block_x[1]:
            break
        x_count += 1

    y_count = 0
    for block_y in blocks:
        if block_y[0] <= y <= block_y[1]:
            break
        y_count += 1

    for i in range(blocks[y_count][0], blocks[y_count][1] + 1):
        block_list += sudoku[i][blocks[x_count][0]:blocks[x_count][1] + 1]

    if n in block_list:
        return False

    # Number is possible, return True
    return True


def solve():
    global sudoku

    for y in range(9):
        for x in range(9):
            if sudoku[y][x] == 0:
                for n in range(1, 10):
                    if possible(y, x, n):
                        sudoku[y][x] = n
                        yield from solve()
                        sudoku[y][x] = 0
                return

    yield print_sudoku()


def main():
    last_sudoku = ""

    create_sudoku()
    for _ in solve():
        if last_sudoku == sudoku:
            break
        last_sudoku = sudoku
        input("\nFor more solutions hit Enter...")

    print("\nThere aren't any other solutions")


if __name__ == '__main__':
    main()
