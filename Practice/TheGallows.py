import random
import string


def choice_word():
    with open("words.txt", "r") as f:
        words_list = f.readlines()

    random.shuffle(words_list)
    word = random.choice(words_list)
    return word


def game(word):
    access_char = string.ascii_uppercase
    answer = ["_", "_", "_"]
    count = 5
    while True:
        print(f"\nATTEMTS = : {count}")
        print(word)
        print(answer)
        print("Available letters: ")
        for char in access_char:
            print(char + " ", end=" ")
        print("\nEnter letter: ")
        player_char = input()
        if player_char == 0 or player_char == "0":
            break

        if player_char in word and len(player_char) == 1:
            for i in range(len(answer)):
                _xz = word.find(player_char, i)
                if _xz >= 0:
                    answer[_xz] = player_char

            access_char = (
                access_char[: access_char.index(player_char)]
                + access_char[access_char.index(player_char) + 1 : :]
            )
        elif len(player_char) == 1:
            print("This letter is not exist!")
            count -= 1
        if "_" not in answer:
            print("\nCongrutalations YOU WINNNNN!!!!\n")
            break
        elif count <= 0:
            print(f"\nYou LOSE! :(\tRIGHT ANSWER: {word}\n")
            break


while True:
    # access_char = string.ascii_uppercase
    # print(access_char, "\n", access_char.find("D"))
    print("THE GALLOWS GAME!?!:)\n1.Start\t0.Exit")
    mng_count = int(input())
    match mng_count:
        case 1:
            word = choice_word()
            game(word)
        case _:
            if mng_count == 0:
                break
            print("Invalid Choice!")
            break
