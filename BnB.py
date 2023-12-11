import time

# Main function
def assignment_problem(cost_matrix):
    # Save the size of the matrix
    n = len(cost_matrix)
    # Save the best solution/cost
    min_cost = float('inf')

    # Function to calculate the bound on unselected nodes
    def calculate_bound(cost_matrix, path, level):
        bound = 0
        used = [False] * n

        for i in range(level):
            bound += cost_matrix[path[i]][i]
            used[path[i]] = True    

        for i in range(level, n):
            min_cost = float('inf')
            for j in range(n):
                if not used[j] and cost_matrix[j][i] < min_cost:
                    min_cost = cost_matrix[j][i]
            bound += min_cost

        return bound

    def branch_and_bound(cost_matrix):
        nonlocal min_cost
        path = list(range(n))
        best_path = None

        # Function for exploration in the search
        def backtrack(cost_matrix, path, level):
            nonlocal min_cost, best_path

            # Check the current level against the variable n (matrix size)
            if level == n:
                cost = sum(cost_matrix[i][path[i]] for i in range(n))
                if cost < min_cost:
                    min_cost = cost
                    best_path = path.copy()
                return

            # Exploration constraint if it exceeds the minimum/optimal value
            bound = calculate_bound(cost_matrix, path, level)
            if bound >= min_cost:
                return

            for i in range(level, n):
                path[level], path[i] = path[i], path[level]
                backtrack(cost_matrix, path, level + 1)
                path[level], path[i] = path[i], path[level]

        backtrack(cost_matrix, path, 0)
        return min_cost, best_path

    # Solve the problem
    min_cost, best_path = branch_and_bound(cost_matrix)

    # Display the results
    print("Cost (Expense):", min_cost)
    print("Solution       :", [x+1 for x in best_path])  # Displaying indices starting from 1

# Function to read the cost matrix from a file
def read_cost_matrix_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        cost_matrix = [[int(num) for num in line.strip().split()] for line in lines]
    return cost_matrix

# Function to read the cost matrix from the keyboard
def read_cost_matrix_from_keyboard():
    print("Enter the matrix size:")
    n = int(input())
    print("Enter the matrix:")
    cost_matrix = []
    for _ in range(n):
        row = list(map(int, input().split()))
        cost_matrix.append(row)
    return cost_matrix

# Main program
print("\nBonjour, Welcome!")
print("\nChoose input option:")
print("1. Enter the matrix from the keyboard")
print("2. Read the matrix from a text file")

print(" ")
option = input("Enter choice (1 or 2): ")

if option == "1":
    cost_matrix = read_cost_matrix_from_keyboard()
    start = time.time()
    assignment_problem(cost_matrix)
    end = time.time()
    print("Execution Time:", end - start)
elif option == "2":
    file_path = input("Enter the text file path: ")
    cost_matrix = read_cost_matrix_from_file(file_path)
    start = time.time()
    assignment_problem(cost_matrix)
    end = time.time()
    print("Execution Time:", end - start)
else:
    print("Invalid choice. Program terminated.\n")
