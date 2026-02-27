from random import randint


def create_examples(difficulty):
    count_correct = 0
    count_all = 0
    while True:
        x = randint(1, difficulty)
        y = randint(1, difficulty)
        result = x * y
        answer = input(f"{x} * {y} = ")
        if answer.isdigit():
            answer = int(answer)
            count_all += 1
            if result == answer:
                count_correct += 1
                print("CORRECT!")
            elif answer == 0:
                count_all -= 1
                print(f"\nCorrect solve examples: {count_correct} from {count_all}\n")
                return 0
            else:
                print("WRONG Answer!")


while True:
    print(
        "THE EXAMPLES ON MULTYPLICATION GAME\nChoose Difficulty:\n1.Easy\t\t2.Medium\t3.Hard\t\t0.Exit"
    )
    difficulty = int(input("Enter your choice: "))
    while True:
        match difficulty:
            case "exit":
                break
            case 1:
                if create_examples(10) == 0:
                    break
            case 2:
                if create_examples(100) == 0:
                    break
            case 3:
                if create_examples(1000) == 0:
                    break
            case _:
                if difficulty == 0:
                    break
                print("Invalid choice!")
                break
    if difficulty == 0:
        break
