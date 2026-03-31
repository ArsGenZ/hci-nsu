from random import randint


def guess_number_easy(difficulty):
    number = randint(1, difficulty)
    attempts = 0
    while True:
        guess = input(
            f"Guess a number between 1 and {difficulty} and 0 to return in menu: "
        )
        if guess.isdigit():
            guess = int(guess)
            if guess == 0:
                return 0
            attempts += 1
            if guess == number:
                print(
                    f"\nCongratulations! You guessed the number in {attempts} attempts.\n"
                )
                break
            elif guess < number:
                print("Too low!")
            else:
                print("Too high!")


while True:
    print(
        "THE GUESS NUMBER GAME\nChoose Difficulty:\n1.Easy\t\t2.Medium\t3.Hard\t\t0.Exit"
    )
    difficulty = int(input("Enter your choice: "))
    while True:
        match difficulty:
            case "exit":
                break
            case 1:
                if guess_number_easy(10) == 0:
                    break
            case 2:
                if guess_number_easy(100) == 0:
                    break
            case 3:
                if guess_number_easy(1000) == 0:
                    break
            case _:
                if difficulty == 0:
                    break
                print("Invalid Choice!")
                break
    if difficulty == 0:
        break
