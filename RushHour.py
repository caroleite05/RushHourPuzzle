import csv
import os

from RushHourClass import Gameboard, Vehicle, Dimensions
from RushHelpers import backtrace, backtraceV2
from Algorithms import (
    a_star,
    breadth_First_Search,
    depth_First_Search,
)


def upload_board(filepath):
    """
    Load a board from a CSV file.
    """

    vehicles = []

    with open(filepath, newline="") as csv_file:

        reader = csv.reader(csv_file)
        next(reader)

        for vehicle_id, x, y, orientation, length in reader:

            vehicles.append(
                Vehicle(
                    vehicle_id,
                    int(x),
                    int(y),
                    orientation,
                    int(length),
                )
            )

    return vehicles


def choose_board():
    """
    Ask the user to choose a board.
    """

    Dimensions.init()

    boards = {
        "1": ("6x6", 6),
        "2": ("9x9", 9),
        "3": ("12x12", 12),
    }

    print("Choose a board size:")
    print("1 - 6x6")
    print("2 - 9x9")
    print("3 - 12x12")

    choice = input("> ").strip()

    if choice not in boards:
        raise ValueError("Invalid board size.")

    folder, size = boards[choice]

    Dimensions.width = size
    Dimensions.height = size

    board_path = os.path.join("Boards", folder)

    print("\nAvailable boards:\n")

    files = sorted(os.listdir(board_path))

    for file in files:
        print(file)

    board = input("\nBoard: ").strip()

    return os.path.join(board_path, board)


def solve(board_path, algorithm):
    """
    Solve the selected board using the chosen algorithm.
    """

    board = Gameboard(upload_board(board_path))

    if algorithm == "1":
        return a_star(board)

    elif algorithm == "2":
        return breadth_First_Search(board)

    elif algorithm == "3":
        return depth_First_Search(board)

    else:
        raise ValueError("Invalid algorithm.")


def print_results(results, algorithm):
    """
    Print algorithm results.
    """

    if results is None:
        print("\nNo solution found.")
        return

    print("\n========== RESULTS ==========\n")

    print(f"Time: {results['solvetime']:.6f} s")

    if algorithm == "3":
        print(f"Nodes explored: {results['nodes']}")
    else:
        print(f"Nodes explored: {results['nodes_popped']}")

    path = backtrace(
        results["archive"],
        results["solution"],
    )

    print(f"Solution length: {len(path)}")

    print()
    print(backtraceV2(path))


def rush():
    """
    Main entry point.
    """

    board_path = choose_board()

    print("\nChoose an algorithm:")
    print("1 - A*")
    print("2 - Breadth-First Search")
    print("3 - Depth-First Search")

    algorithm = input("> ").strip()

    results = solve(board_path, algorithm)

    print_results(results, algorithm)


def main():
    rush()


if __name__ == "__main__":
    main()