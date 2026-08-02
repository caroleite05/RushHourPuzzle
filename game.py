from math import ceil


class Vehicle:
    """
    Represents a vehicle on the Rush Hour board.
    """

    def __init__(self, vehicle_id, x, y, orientation, length):
        self.id = vehicle_id
        self.x = x
        self.y = y
        self.orientation = orientation
        self.length = int(length)

    def __repr__(self):
        return (
            f"Vehicle('{self.id}', {self.x}, {self.y}, "
            f"'{self.orientation}', {self.length})"
        )

    def __eq__(self, other):
        if not isinstance(other, Vehicle):
            return False

        return (
            self.id == other.id
            and self.x == other.x
            and self.y == other.y
            and self.orientation == other.orientation
            and self.length == other.length
        )

    def __hash__(self):
        return hash((
            self.id,
            self.x,
            self.y,
            self.orientation,
            self.length
        ))


class BoardDimensions:
    """
    Stores the dimensions of the game board.
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height


class Board:
    """
    Represents the Rush Hour game board.
    """

    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.board = [
            [None for _ in range(dimensions.width)]
            for _ in range(dimensions.height)
        ]
        self.vehicles = []

    def print_board(self):
        """
        Print the current board.
        """
        for row in self.board:
            print(" ".join(cell.id if cell else "." for cell in row))

    def add_vehicle(self, vehicle):
        """
        Add a vehicle to the board.
        """
        if not self.is_valid_position(vehicle):
            raise ValueError(
                f"Invalid position for vehicle '{vehicle.id}'."
            )

        self.vehicles.append(vehicle)
        self.update_board()

    def is_valid_position(self, vehicle):
        """
        Check whether a vehicle can be placed on the board.
        """

        if vehicle.orientation == "H":

            if vehicle.x + vehicle.length > self.dimensions.width:
                return False

            for i in range(vehicle.length):
                if self.board[vehicle.y][vehicle.x + i] is not None:
                    return False

        elif vehicle.orientation == "V":

            if vehicle.y + vehicle.length > self.dimensions.height:
                return False

            for i in range(vehicle.length):
                if self.board[vehicle.y + i][vehicle.x] is not None:
                    return False

        return True

    def move_horizontal_left(self, vehicle):

        if (
            vehicle.orientation == "H"
            and vehicle.x > 0
            and self.board[vehicle.y][vehicle.x - 1] is None
        ):
            vehicle.x -= 1

        self.update_board()

    def move_horizontal_right(self, vehicle):

        if (
            vehicle.orientation == "H"
            and vehicle.x + vehicle.length < self.dimensions.width
            and self.board[vehicle.y][vehicle.x + vehicle.length] is None
        ):
            vehicle.x += 1

        self.update_board()

    def move_vertical_up(self, vehicle):

        if (
            vehicle.orientation == "V"
            and vehicle.y > 0
            and self.board[vehicle.y - 1][vehicle.x] is None
        ):
            vehicle.y -= 1

        self.update_board()

    def move_vertical_down(self, vehicle):

        if (
            vehicle.orientation == "V"
            and vehicle.y + vehicle.length < self.dimensions.height
            and self.board[vehicle.y + vehicle.length][vehicle.x] is None
        ):
            vehicle.y += 1

        self.update_board()

    def update_board(self):
        """
        Update the board after moving vehicles.
        """

        self.board = [
            [None for _ in range(self.dimensions.width)]
            for _ in range(self.dimensions.height)
        ]

        for vehicle in self.vehicles:

            if vehicle.orientation == "H":

                for i in range(vehicle.length):
                    self.board[vehicle.y][vehicle.x + i] = vehicle

            else:

                for i in range(vehicle.length):
                    self.board[vehicle.y + i][vehicle.x] = vehicle

    def is_game_won(self):
        """
        Check whether the red car has reached the exit.
        """

        exit_row = ceil(self.dimensions.height / 2) - 1

        for vehicle in self.vehicles:

            if (
                vehicle.id == "R"
                and vehicle.y == exit_row
                and vehicle.x + vehicle.length == self.dimensions.width
            ):
                return True

        return False


class Game:
    """
    Main game loop.
    """

    def __init__(self, board):
        self.board = board

    def play(self):

        while not self.board.is_game_won():

            print()
            self.board.print_board()
            print()

            move = input(
                "Enter your move (e.g. 'R L'): "
            ).split()

            if len(move) != 2:
                print("Invalid input.")
                continue

            vehicle_id, direction = move
            direction = direction.upper()

            vehicle = next(
                (v for v in self.board.vehicles if v.id == vehicle_id),
                None,
            )

            if vehicle is None:
                print("Invalid vehicle.")
                continue

            if direction == "L":
                self.board.move_horizontal_left(vehicle)

            elif direction == "R":
                self.board.move_horizontal_right(vehicle)

            elif direction == "U":
                self.board.move_vertical_up(vehicle)

            elif direction == "D":
                self.board.move_vertical_down(vehicle)

            else:
                print("Direction must be L, R, U or D.")

        print()
        self.board.print_board()
        print("\nCongratulations! You solved the puzzle!")