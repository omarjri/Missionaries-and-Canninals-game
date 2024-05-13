import tkinter as tk
from collections import deque

class State:
    def __init__(self, left_missionaries, left_cannibals, boat_position):
        self.left_missionaries = left_missionaries
        self.left_cannibals = left_cannibals
        self.boat_position = boat_position

    def is_valid(self):
        if self.left_missionaries < 0 or self.left_cannibals < 0:
            return False
        if self.left_missionaries > 3 or self.left_cannibals > 3:
            return False
        if (self.left_cannibals > self.left_missionaries > 0) or \
                ((3 - self.left_cannibals) > (3 - self.left_missionaries) > 0):
            return False
        return True

    def is_goal(self):
        return self.left_missionaries == 0 and self.left_cannibals == 0

    def __eq__(self, other):
        return self.left_missionaries == other.left_missionaries and \
               self.left_cannibals == other.left_cannibals and \
               self.boat_position == other.boat_position

    def __hash__(self):
        return hash((self.left_missionaries, self.left_cannibals, self.boat_position))


def successors(state):
    successor_states = []
    if state.boat_position == 'left':
        # Moving 1 or 2 missionaries
        for m in range(3):
            for c in range(3):
                if m + c <= 2 and (m + c) > 0:
                    new_state = State(state.left_missionaries - m, state.left_cannibals - c, 'right')
                    if new_state.is_valid():
                        successor_states.append(new_state)
    else:
        # Moving 1 or 2 missionaries
        for m in range(3):
            for c in range(3):
                if m + c <= 2 and (m + c) > 0:
                    new_state = State(state.left_missionaries + m, state.left_cannibals + c, 'left')
                    if new_state.is_valid():
                        successor_states.append(new_state)
    return successor_states


def heuristic(state):
    # Heuristic function: distance from current state to goal state
    return state.left_missionaries + state.left_cannibals


def astar(initial_state):
    visited = set()
    queue = deque([(initial_state, 0)])
    parent = {}
    while queue:
        state, cost = queue.popleft()
        if state.is_goal():
            path = []
            while state != initial_state:
                path.append(state)
                state = parent[state]
            path.append(initial_state)
            return path[::-1]
        visited.add(state)
        for next_state in successors(state):
            if next_state not in visited:
                parent[next_state] = state
                queue.append((next_state, cost + 1 + heuristic(next_state)))
                queue = deque(sorted(queue, key=lambda x: x[1]))
    return None


class MissionariesCannibalsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Missionaries and Cannibals")
        
        self.canvas = tk.Canvas(self.root, width=400, height=300, bg="lightblue")
        self.canvas.pack()

        self.solve_button = tk.Button(self.root, text="Solve", command=self.solve_astar)
        self.solve_button.pack()

    def solve_astar(self):
        print("Solving with A* Search")
        initial_state = State(3, 3, 'left')
        solution = astar(initial_state)
        self.display_solution(solution)

    def display_solution(self, solution):
        self.canvas.delete("all")
        if solution is None:
            self.canvas.create_text(200, 150, text="No solution found", font=("Arial", 14), fill="black")
        else:
            for i, state in enumerate(solution):
                self.canvas.create_text(200, 50 + i * 30, text=f"Missionaries: {state.left_missionaries}, Cannibals: {state.left_cannibals}, Boat Position: {state.boat_position}", font=("Arial", 12), fill="black")


def main():
    root = tk.Tk()
    game = MissionariesCannibalsGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
