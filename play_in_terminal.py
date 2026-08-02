from game import Board, BoardDimensions, Game, Vehicle
import csv


def read_vehicles_from_csv(file_path):
    """
    Read a Rush Hour board from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        list[Vehicle]: List of vehicles defined in the board.
    """

    vehicles = []

    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            vehicle = Vehicle(
                row["id"],
                int(row["x"]),
                int(row["y"]),
                row["orientation"],
                int(row["length"])
            )
            vehicles.append(vehicle)

    return vehicles


def load_level(file_path, width, height, level_name):
    """
    Load a level and start the game.

    Args:
        file_path (str): Path to the board CSV.
        width (int): Board width.
        height (int): Board height.
        level_name (str): Name displayed to the player.
    """

    vehicles = read_vehicles_from_csv(file_path)

    board = Board(BoardDimensions(width, height))

    for vehicle in vehicles:
        board.add_vehicle(vehicle)

    print(f"\n{level_name}")
    Game(board).play()


def start_terminal():
    print("\nHello! Welcome to our version of the 'Rush Hour Puzzle' in Terminal!")
    print("Whenever you want to quit the game, type 'quit'.")
    print("If you want to return to the menu, type 'menu'.")
    print("If you want to restart the level, type 'r'.")

    start = input("\nReady to start? (y/n): ")

    while start.lower() not in ["y", "n", "quit"]:
        print("Invalid input. Please try again.")
        start = input("Ready to start? (y/n): ")

    if start.lower() in ["n", "quit"]:
        print("\nGoodbye!")
        quit()

    menu()


def menu():
    print("\nBoard Sizes")
    print("  6x6")
    print("  9x9")
    print(" 12x12")

    difficulty = input("\nChoose the board size (e.g. 6x6): ")

    while difficulty not in ["6x6", "9x9", "12x12", "quit"]:
        print("Invalid input.")
        difficulty = input("Choose the board size (e.g. 6x6): ")

    if difficulty == "quit":
        print("\nGoodbye!")
        quit()

    if difficulty == "6x6":
        size_6x6()
    elif difficulty == "9x9":
        size_9x9()
    elif difficulty == "12x12":
        size_12x12()


def size_6x6():
    print("\nBOARD - 6x6")
    print(" 1 - Beginner")
    print(" 2 - Intermediate")
    print(" 3 - Advanced")
    print(" 4 - Expert")

    level = input("\nChoose the level: ")

    while level not in ["1", "2", "3", "4", "menu", "Menu", "quit"]:
        print("Invalid input.")
        level = input("Choose the level: ")

    if level == "quit":
        print("\nGoodbye!")
        quit()

    if level.lower() == "menu":
        menu()
        return

    if level == "1":
        beginner()
    elif level == "2":
        intermediate()
    elif level == "3":
        advanced()
    elif level == "4":
        expert()


def size_9x9():
    print("\nBOARD - 9x9")
    print(" 1 - Game 9x9")

    level = input("\nChoose the level: ")

    while level not in ["1", "menu", "Menu", "quit"]:
        print("Invalid input.")
        level = input("Choose the level: ")

    if level == "quit":
        print("\nGoodbye!")
        quit()

    if level.lower() == "menu":
        menu()
        return

    game_9x9()


def size_12x12():
    print("\nBOARD - 12x12")
    print(" 1 - Game 12x12")

    level = input("\nChoose the level: ")

    while level not in ["1", "menu", "Menu", "quit"]:
        print("Invalid input.")
        level = input("Choose the level: ")

    if level == "quit":
        print("\nGoodbye!")
        quit()

    if level.lower() == "menu":
        menu()
        return

    game_12x12()


def beginner():
    load_level(
        "Boards/6x6/beginner.csv",
        6,
        6,
        "Beginner"
    )


def intermediate():
    load_level(
        "Boards/6x6/intermediate.csv",
        6,
        6,
        "Intermediate"
    )


def advanced():
    load_level(
        "Boards/6x6/advanced.csv",
        6,
        6,
        "Advanced"
    )


def expert():
    load_level(
        "Boards/6x6/expert.csv",
        6,
        6,
        "Expert"
    )


def game_9x9():
    load_level(
        "Boards/9x9/game_9x9.csv",
        9,
        9,
        "Game 9x9"
    )


def game_12x12():
    load_level(
        "Boards/12x12/game_12x12.csv",
        12,
        12,
        "Game 12x12"
    )