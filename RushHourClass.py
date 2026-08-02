from math import ceil
from copy import deepcopy


class Vehicle:
    """
    Represents a vehicle in the Rush Hour puzzle.
    """

    def __init__(self, vehicle_id, x, y, orientation, length):
        self.id = vehicle_id
        self.x = int(x)
        self.y = int(y)
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
            self.length,
        ))


class Dimensions:
    """
    Stores the board dimensions.
    """

    width = 0
    height = 0

    @staticmethod
    def init():
        pass


class Gameboard:
    """
    Represents a Rush Hour board state.
    """

    def __init__(self, vehicles):

        self.width = Dimensions.width
        self.height = Dimensions.height

        self.vehicles = vehicles

        self.board = [
            ["." for _ in range(self.width)]
            for _ in range(self.height)
        ]

        for vehicle in self.vehicles:

            if vehicle.orientation == "H":

                for i in range(vehicle.length):
                    self.board[vehicle.y][vehicle.x + i] = vehicle.id

            else:

                for i in range(vehicle.length):
                    self.board[vehicle.y + i][vehicle.x] = vehicle.id

    def __repr__(self):
        return "\n".join(
            " ".join(row)
            for row in self.board
        )

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        if not isinstance(other, Gameboard):
            return False

        return self.board == other.board

    def _create_successor(self, vehicle, new_x, new_y):
        """
        Create a new board after moving one vehicle.
        """

        new_vehicles = []

        for current in self.vehicles:

            if current == vehicle:

                new_vehicles.append(
                    Vehicle(
                        current.id,
                        new_x,
                        new_y,
                        current.orientation,
                        current.length,
                    )
                )

            else:

                new_vehicles.append(deepcopy(current))

        return new_vehicles

    def checkformoves(self):
        """
        Generate every valid successor board.
        """

        possible_boards = []

        for vehicle in self.vehicles:

            x = vehicle.x
            y = vehicle.y

            if vehicle.orientation == "H":

                if x > 0 and self.board[y][x - 1] == ".":

                    possible_boards.append(
                        self._create_successor(vehicle, x - 1, y)
                    )

                if (
                    x + vehicle.length < self.width
                    and self.board[y][x + vehicle.length] == "."
                ):

                    possible_boards.append(
                        self._create_successor(vehicle, x + 1, y)
                    )

            else:

                if y > 0 and self.board[y - 1][x] == ".":

                    possible_boards.append(
                        self._create_successor(vehicle, x, y - 1)
                    )

                if (
                    y + vehicle.length < self.height
                    and self.board[y + vehicle.length][x] == "."
                ):

                    possible_boards.append(
                        self._create_successor(vehicle, x, y + 1)
                    )

        return possible_boards

    def hasSolved(self):
        """
        Check whether the red car has reached the exit.
        """

        exit_row = ceil(self.height / 2) - 1

        for vehicle in self.vehicles:

            if (
                vehicle.id == "R"
                and vehicle.orientation == "H"
                and vehicle.y == exit_row
                and vehicle.x == self.width - vehicle.length
            ):
                return True

        return False