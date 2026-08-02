import time
from collections import deque

from RushHourClass import Gameboard, Dimensions


def breadth_First_Search(gameboard):
    """
    Breadth-First Search (BFS).
    """

    start_time = time.time()

    boards_queue = deque()
    archive = {gameboard: 0}
    boards_queue.appendleft(gameboard)

    number = 0

    while boards_queue:

        current_board = boards_queue.pop()
        number += 1

        if current_board.hasSolved():
            return {
                "solvetime": time.time() - start_time,
                "nodes_popped": number,
                "archive": archive,
                "solution": current_board
            }

        for move in current_board.checkformoves():

            new_board = Gameboard(move)

            if new_board not in archive:
                archive[new_board] = current_board
                boards_queue.appendleft(new_board)

    return None


def depth_First_Search(gameboard):
    """
    Depth-First Search (DFS).
    """

    start_time = time.time()

    stack = [gameboard]
    archive = {gameboard: 0}

    number = 0

    while stack:

        current_board = stack.pop()
        number += 1

        if current_board.hasSolved():
            return {
                "solvetime": time.time() - start_time,
                "nodes": number,
                "archive": archive,
                "solution": current_board
            }

        for move in current_board.checkformoves():

            new_board = Gameboard(move)

            if new_board not in archive:
                archive[new_board] = current_board
                stack.append(new_board)

    return None


def heuristic(gameboard):
    """
    Manhattan distance between the red car and the exit.
    """

    red_car = None

    for vehicle in gameboard.vehicles:
        if vehicle.id == "R":
            red_car = vehicle
            break

    if red_car is None:
        return 0

    exit_x = Dimensions.width - 2
    exit_y = Dimensions.height // 2 - 1

    distance_x = abs((red_car.x + red_car.length) - exit_x)
    distance_y = abs(red_car.y - exit_y)

    return distance_x + distance_y


def a_star(gameboard):
    """
    A* Search.
    """

    start_time = time.time()

    open_set = [(heuristic(gameboard), gameboard)]
    closed_set = set()

    archive = {gameboard: 0}

    g_score = {gameboard: 0}
    f_score = {gameboard: heuristic(gameboard)}

    number = 0

    while open_set:

        current_f, current_board = min(open_set, key=lambda x: x[0])
        open_set.remove((current_f, current_board))

        number += 1

        if current_board.hasSolved():

            return {
                "solvetime": time.time() - start_time,
                "nodes_popped": number,
                "archive": archive,
                "solution": current_board
            }

        closed_set.add(current_board)

        for move in current_board.checkformoves():

            neighbor = Gameboard(move)

            if neighbor in closed_set:
                continue

            tentative_g = g_score[current_board] + 1

            if neighbor not in archive or tentative_g < g_score.get(neighbor, float("inf")):

                archive[neighbor] = current_board
                g_score[neighbor] = tentative_g

                f = tentative_g + heuristic(neighbor)
                f_score[neighbor] = f

                if not any(board == neighbor for _, board in open_set):
                    open_set.append((f, neighbor))

    return None