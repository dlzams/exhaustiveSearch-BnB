import numpy as np
import time
from ortools.sat.python import cp_model

n = 7    # size of the matrix to be created

def assignment_problem(cost_matrix):
    n = len(cost_matrix)
    min_cost = float('inf')
    best_path = []

    def calculate_bound(cost_matrix, path, level):
        bound = 0
        used = [False] * n

        for i in range(level):
            bound += cost_matrix[path[i]][i]
            used[path[i]] = True

        for i in range(level, n):
            min_cost = min(cost_matrix[j][i] for j in range(n) if not used[j])
            bound += min_cost

        return bound

    def branch_and_bound(cost_matrix):
        nonlocal min_cost, best_path

        def backtrack(cost_matrix, path, level):
            nonlocal min_cost, best_path

            if level == n:
                cost = sum(cost_matrix[i][path[i]] for i in range(n))
                if cost < min_cost:
                    min_cost = cost
                    best_path = path.copy()
                return

            bound = calculate_bound(cost_matrix, path, level)
            if bound >= min_cost:
                return

            for i in range(level, n):
                path[level], path[i] = path[i], path[level]
                backtrack(cost_matrix, path, level + 1)
                path[level], path[i] = path[i], path[level]

        path = list(range(n))
        backtrack(cost_matrix, path, 0)

    branch_and_bound(cost_matrix)
    print("Cost:", min_cost)
    print("Solution:", [x+1 for x in best_path])  # Displaying indices starting from 1

def work(costs):
    num_workers = len(costs)
    num_tasks = len(costs[0])

    # Model
    model = cp_model.CpModel()

    # Variables
    x = []
    for i in range(num_workers):
        t = []
        for j in range(num_tasks):
            t.append(model.NewBoolVar(f'x[{i},{j}]'))
        x.append(t)

    # Constraints
    # Each worker is assigned to at most one task.
    for i in range(num_workers):
        model.AddAtMostOne(x[i][j] for j in range(num_tasks))

    # Each task is assigned to exactly one worker.
    for j in range(num_tasks):
        model.AddExactlyOne(x[i][j] for i in range(num_workers))

    # Objective
    objective_terms = []
    for i in range(num_workers):
        for j in range(num_tasks):
            objective_terms.append(costs[i][j] * x[i][j])
    model.Minimize(sum(objective_terms))

    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Print solution.
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for i in range(num_workers):
            for j in range(num_tasks):
                if solver.BooleanValue(x[i][j]):
                    print(
                        f'Worker {i} assigned to task {j} Cost = {costs[i][j]}')
        print(f'Total cost: {solver.ObjectiveValue()}')
    else:
        print('No solution found.')

# Cost matrix for the assignment problem
cost_matrix = np.random.randint(1, 10, size=(n, n))
print("Matrix with size ", n, " x ", n, "formed is: \n")
print(cost_matrix)
print("\n")

# Running the assignment_problem function
print("Result of the branch-and-bound function:")
start_time = time.time()
a = assignment_problem(cost_matrix)
end_time = time.time()
print("Execution time:", end_time - start_time, "seconds")
print("\n")

# Running the work function
print("Result of the exhaustive function:")
start_time = time.time()
b = work(cost_matrix)
end_time = time.time()
print("Execution time:", end_time - start_time, "seconds")
