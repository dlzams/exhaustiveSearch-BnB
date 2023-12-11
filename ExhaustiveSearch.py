from ortools.sat.python import cp_model
import time

def read_cost_matrix_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        cost_matrix = [[int(num) for num in line.strip().split()] for line in lines]
    return cost_matrix

def read_cost_matrix_from_keyboard():
    print("Enter the matrix size:")
    n = int(input())
    print("Enter the matrix:")
    cost_matrix = []
    for _ in range(n):
        row = list(map(int, input().split()))
        cost_matrix.append(row)
    return cost_matrix

def main():
    # Data
    print("\nBonjour, Welcome!")
    print("\nChoose input option:")
    print("1. Enter the matrix from the keyboard")
    print("2. Read the matrix from a text file")

    choice = input("\nEnter choice (1 or 2): ")

    if choice == '1':
        cost_matrix = read_cost_matrix_from_keyboard()
        start = time.time()
        work(cost_matrix)
        end = time.time()
        print("Execution time:", end - start)
    elif choice == '2':
        filename = input("Enter the text file path: ")
        print("\n")
        cost_matrix = read_cost_matrix_from_file(filename)
        start = time.time()
        work(cost_matrix)
        end = time.time()
        print("Execution time:", end - start)
    else:
        print("Invalid selection. Please try again.")

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
        print(f'Total cost       : {solver.ObjectiveValue()}')
    else:
        print('No solution found.')

if __name__ == '__main__':
    main()
