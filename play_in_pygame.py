import pygame
import sys
import random
import csv

from game import Vehicle, BoardDimensions, Board


# ---------------------------------------------------------
# Read board from CSV
# ---------------------------------------------------------

def read_vehicles_from_csv(file_path):
    vehicles = []

    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            vehicles.append(
                Vehicle(
                    row["id"],
                    int(row["x"]),
                    int(row["y"]),
                    row["orientation"],
                    int(row["length"]),
                )
            )

    return vehicles


# ---------------------------------------------------------
# Load board
# ---------------------------------------------------------

def load_board(file_path, width, height):
    board = Board(BoardDimensions(width, height))

    vehicles = read_vehicles_from_csv(file_path)

    for vehicle in vehicles:
        board.add_vehicle(vehicle)

    return board


# ---------------------------------------------------------
# Play game
# ---------------------------------------------------------

def play_game(file_path, width, height):

    pygame.init()

    FPS = 60
    clock = pygame.time.Clock()

    CELL = 80

    BOTTOM_PANEL = 80

    screen = pygame.display.set_mode(
        (width * CELL, height * CELL + BOTTOM_PANEL)
    )

    solve_button = pygame.Rect(
        width * CELL - 170,
        height * CELL + 20,
        200,
        40
    )

    pygame.display.set_caption("Rush Hour")

    WHITE = (255, 255, 255)
    BLACK = (30, 30, 30)
    GRID = (180, 180, 180)
    RED = (220, 70, 70)

    board = load_board(file_path, width, height)

    vehicles = board.vehicles

    colors = {}

    for vehicle in vehicles:

        if vehicle.id == "R":
            colors[vehicle.id] = RED
        else:
            colors[vehicle.id] = (
                random.randint(50, 255),
                random.randint(50, 255),
                random.randint(50, 255),
            )

    selected = None

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:

                # Primeiro verifica se clicou no botão
                if solve_button.collidepoint(event.pos):

                    algorithm = choose_algorithm()

                    if algorithm == "astar":
                        print("A* selected")
                        print("\n========================")
                        print("Future Feature")
                        print("========================")
                        print(f"{algorithm.upper()} selected.")
                        print("Automatic solving with AI")
                        print("will be implemented in a")
                        print("future version.")
                        print("========================\n")

                    elif algorithm == "bfs":
                        print("Breadth First Search selected")
                        print("\n========================")
                        print("Future Feature")
                        print("========================")
                        print(f"{algorithm.upper()} selected.")
                        print("Automatic solving with AI")
                        print("will be implemented in a")
                        print("future version.")
                        print("========================\n")

                    elif algorithm == "dfs":
                        print("Depth First Search selected")
                        print("\n========================")
                        print("Future Feature")
                        print("========================")
                        print(f"{algorithm.upper()} selected.")
                        print("Automatic solving with AI")
                        print("will be implemented in a")
                        print("future version.")
                        print("========================\n")

                    # Não selecionar nenhum veículo
                    continue

                # Caso contrário, verifica se clicou num veículo
                mx, my = event.pos

                gx = mx // CELL
                gy = my // CELL

                selected = None

                for vehicle in vehicles:

                    if vehicle.orientation == "H":

                        if (
                            gy == vehicle.y
                            and vehicle.x <= gx < vehicle.x + vehicle.length
                        ):
                            selected = vehicle
                            break

                    else:

                        if (
                            gx == vehicle.x
                            and vehicle.y <= gy < vehicle.y + vehicle.length
                        ):
                            selected = vehicle
                            break

            elif event.type == pygame.KEYDOWN and selected is not None:

                if selected.orientation == "H":

                    if event.key == pygame.K_LEFT:
                        board.move_horizontal_left(selected)

                    elif event.key == pygame.K_RIGHT:
                        board.move_horizontal_right(selected)

                else:

                    if event.key == pygame.K_UP:
                        board.move_vertical_up(selected)

                    elif event.key == pygame.K_DOWN:
                        board.move_vertical_down(selected)

                if board.is_game_won():

                    print("Puzzle solved!")

                    running = False

        screen.fill(WHITE)

        # Grid

        for y in range(height):

            for x in range(width):

                pygame.draw.rect(
                    screen,
                    GRID,
                    (x * CELL, y * CELL, CELL, CELL),
                    1,
                )

        # Vehicles

        for vehicle in vehicles:

            color = colors[vehicle.id]

            if vehicle == selected:
                pygame.draw.rect(
                    screen,
                    BLACK,
                    (
                        vehicle.x * CELL - 2,
                        vehicle.y * CELL - 2,
                        (vehicle.length if vehicle.orientation == "H" else 1)
                        * CELL
                        + 4,
                        (1 if vehicle.orientation == "H" else vehicle.length)
                        * CELL
                        + 4,
                    ),
                )

            if vehicle.orientation == "H":

                rect = (
                    vehicle.x * CELL,
                    vehicle.y * CELL,
                    vehicle.length * CELL,
                    CELL,
                )

            else:

                rect = (
                    vehicle.x * CELL,
                    vehicle.y * CELL,
                    CELL,
                    vehicle.length * CELL,
                )

            pygame.draw.rect(screen, color, rect)

        pygame.draw.rect(screen, (60,160,255), solve_button)
        pygame.draw.rect(screen, BLACK, solve_button, 2)

        text = pygame.font.SysFont(None,28).render(
            "Solve with AI",
            True,
            WHITE
        )

        screen.blit(
            text,
            (
                solve_button.x + 12,
                solve_button.y + 10
            )
        )

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


# ---------------------------------------------------------
# Menu
# ---------------------------------------------------------

def menu():

    boards = {

        "1": ("Boards/6x6/beginner.csv", 6, 6),
        "2": ("Boards/6x6/intermediate.csv", 6, 6),
        "3": ("Boards/6x6/advanced.csv", 6, 6),
        "4": ("Boards/6x6/expert.csv", 6, 6),
        "5": ("Boards/9x9/game_9x9.csv", 9, 9),
        "6": ("Boards/12x12/game_12x12.csv", 12, 12),

    }

    print("\nChoose a board:\n")

    print("1 - Beginner (6x6)")
    print("2 - Intermediate (6x6)")
    print("3 - Advanced (6x6)")
    print("4 - Expert (6x6)")
    print("5 - 9x9")
    print("6 - 12x12")

    option = input("> ")

    if option in boards:

        file, w, h = boards[option]

        play_game(file, w, h)

    else:

        print("Invalid option.")


def choose_algorithm():

    print()

    print("Choose algorithm")

    print("1 - A*")

    print("2 - Breadth First Search")

    print("3 - Depth First Search")

    option = input("> ")

    if option == "1":
        return "astar"

    if option == "2":
        return "bfs"

    if option == "3":
        return "dfs"

    return None

# ---------------------------------------------------------

def start_pygame():
    menu()


if __name__ == "__main__":
    menu()