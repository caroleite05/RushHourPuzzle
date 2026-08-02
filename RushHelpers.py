def backtrace(parents, solution):
    """
    Reconstruct the path from the initial board to the solution.

    Args:
        parents (dict): Dictionary mapping each board to its parent.
        solution (Gameboard): Final board.

    Returns:
        list: Ordered list of boards from the initial state to the solution.
    """

    path = []
    current = solution

    while current != 0:

        if current not in parents:
            print("Error: Parent state not found.")
            return None

        path.append(current)
        current = parents[current]

    path.reverse()
    return path


def backtraceV2(path):
    """
    Convert a sequence of board states into a list of moves.

    Args:
        path (list): List of Gameboard objects.

    Returns:
        list: Human-readable moves.
    """

    if not path:
        return []

    moves = []

    for current_board, next_board in zip(path, path[1:]):

        original = next(
            iter(set(current_board.vehicles) - set(next_board.vehicles))
        )

        moved = next(
            iter(set(next_board.vehicles) - set(current_board.vehicles))
        )

        if original.x < moved.x:
            moves.append(f"{original.id} to the right")

        elif original.x > moved.x:
            moves.append(f"{original.id} to the left")

        elif original.y < moved.y:
            moves.append(f"{original.id} down")

        elif original.y > moved.y:
            moves.append(f"{original.id} up")

    return moves