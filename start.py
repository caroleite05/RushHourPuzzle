from play_in_terminal import start_terminal
from play_in_pygame import start_pygame
from RushHour import rush


def start():
    while True:
        print("\n===================================")
        print("      RUSH HOUR PUZZLE")
        print("===================================")
        print("1 - Play in Pygame")
        print("2 - Play in Terminal")
        print("3 - AI Solver (Hint)")
        print("4 - Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            start_pygame()

        elif choice == "2":
            start_terminal()

        elif choice == "3":
            rush()

        elif choice == "4":
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid option. Please try again.")


if __name__ == "__main__":
    start()