import networkx as nx
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy import *
from scipy.optimize import linear_sum_assignment
from scipy.optimize import linprog
from queue import Queue
from scipy.optimize import least_squares
import sympy as sp

def cpm(activities):
    """
    Perform Critical Path Method on a set of activities.
    
    Parameters:
        activities (dict): A dictionary where keys are (start, end) tuples and values are durations.

    Returns:
        results (dict): Contains EST, EFT, LST, LFT, Total Float, Free Float, Independent Float.
        graph (DiGraph): The directed graph with duration attributes.
    """
    G = nx.DiGraph()

    # Add nodes and edges with durations
    for (u, v), duration in activities.items():
        G.add_edge(u, v, duration=duration)

    # Topological sorting
    topo_order = list(nx.topological_sort(G))

    # Initialize times
    EST = {node: 0 for node in G.nodes()}
    EFT = {}
    
    # Forward pass
    for u in topo_order:
        for v in G.successors(u):
            edge_duration = G[u][v]['duration']
            EST[v] = max(EST[v], EST[u] + edge_duration)
            EFT[(u, v)] = EST[u] + edge_duration

    # Compute LFT and LST
    LFT = {node: max(EST.values()) for node in G.nodes()}
    LST = {}

    for u in reversed(topo_order):
        for v in G.successors(u):
            edge_duration = G[u][v]['duration']
            LFT[u] = min(LFT[u], LFT[v] - edge_duration)
            LST[(u, v)] = LFT[v] - edge_duration

    # Calculate floats
    total_float = {}
    free_float = {}
    independent_float = {}

    for (u, v), duration in activities.items():
        total_float[(u, v)] = LST[(u, v)] - EST[u]
        free_float[(u, v)] = EST[v] - (EST[u] + duration)
        independent_float[(u, v)] = max(0, EST[v] - LFT[u] - duration)

    results = {
        'EST': EST,
        'EFT': EFT,
        'LST': LST,
        'LFT': LFT,
        'Total Float': total_float,
        'Free Float': free_float,
        'Independent Float': independent_float
    }

    return results, G


def run_cpm_analysis(activities, cpm_function):
    """
    Runs CPM analysis on a given activity dictionary using a provided CPM function.

    Parameters:
        activities (dict): Dictionary of tasks with durations and dependencies.
        cpm_function (function): A function that accepts processed_activities and returns (results, graph).
    """

    # Preprocess activities
    processed_activities = {}
    task_mapping = {}  # Map task names to numerical IDs

    current_id = 1
    for task in activities:
        task_mapping[task] = current_id
        current_id += 1

    for task, data in activities.items():
        for dep in data['dependencies']:
            processed_activities[(task_mapping[dep], task_mapping[task])] = data['duration']

    # Run CPM function (you must define this elsewhere and pass it in)
    results, graph = cpm_function(processed_activities)

    # Reverse mapping for readability
    inv_task_mapping = {v: k for k, v in task_mapping.items()}

    # Print CPM results
    for activity, duration in processed_activities.items():
        print(f"Activity ({inv_task_mapping[activity[0]]}, {inv_task_mapping[activity[1]]}):")
        print(f" EST: {results['EST'][activity[0]]}")
        print(f" EFT: {results['EFT'][activity]}")
        print(f" LST: {results['LST'][activity]}")
        print(f" LFT: {results['LFT'][activity[1]]}")
        print(f" Total Float: {results['Total Float'][activity]}")
        print(f" Free Float: {results['Free Float'][activity]}")
        print(f" Independent Float: {results['Independent Float'][activity]}")
        print("-" * 20)

    # Draw graph with node labels
    node_labels = {node: inv_task_mapping[node] for node in graph.nodes()}
    nx.relabel_nodes(graph, node_labels, copy=False)

    pos = nx.spring_layout(graph)
    labels = nx.get_edge_attributes(graph, 'duration')

    nx.draw(graph, pos, with_labels=True, node_size=700, node_color="skyblue",
            font_size=10, font_color="black", arrowsize=20)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

    plt.title("Project Network Diagram")
    plt.show()


def solve_assignment_problem(cost_matrix, problem_type="balanced"):
    """
    Solves the balanced or unbalanced assignment problem using the Hungarian algorithm.
    
    Parameters:
    - cost_matrix: 2D NumPy array (workers x tasks)
    - problem_type: "balanced" or "unbalanced"

    This function prints the assignment result and minimum total cost.
    
    Example input:
    cost_matrix = np.array([
        [10, 11, 4, 2, 8],
        [7, 11, 10, 14, 12],
        [5, 6, 9, 12, 14],
        [13, 15, 11, 10, 7]
    ])
    
    solve_assignment_problem(cost_matrix, problem_type="unbalanced")
    """

    if problem_type == "unbalanced":
        print("Unbalanced assignment problem detected.")
        
        # Padding matrix with zeros to make it square
        num_workers, num_tasks = cost_matrix.shape
        max_dim = max(num_workers, num_tasks)
        padded_cost_matrix = np.zeros((max_dim, max_dim))
        padded_cost_matrix[:num_workers, :num_tasks] = cost_matrix
        print("Padded cost matrix (added dummy rows or columns):")
        print(padded_cost_matrix)
        cost_matrix = padded_cost_matrix

    # Apply Hungarian Algorithm
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    if problem_type == "unbalanced":
        valid_assignments = (row_ind < cost_matrix.shape[0]) & (col_ind < cost_matrix.shape[1])
        row_ind = row_ind[valid_assignments]
        col_ind = col_ind[valid_assignments]

    total_cost = cost_matrix[row_ind, col_ind].sum()

    # Print output
    print("\nOptimal Assignment:")
    for i in range(len(row_ind)):
        print(f"Worker {row_ind[i]+1} assigned to Task {col_ind[i]+1}")
    print(f"\nMinimum Total Cost: {total_cost}")

def cpm2(activities):
    # Call your CPM algorithm
    results, graph = cpm(activities)
    # activities = {
    #     (1, 2): 8,
    #     (1, 3): 7,
    #     (1, 5): 12,
    #     (2, 3): 4,
    #     (2, 4): 10,
    #     (3, 4): 3,
    #     (3, 5): 5,
    #     (3, 6): 10,
    #     (4, 6): 7,
    #     (5, 6): 4,
    # }
    # Print activity details
    for activity, duration in activities.items():
        print(f"Activity {activity}:")
        print(f" EST: {results['EST'][activity[0]]}")
        print(f" EFT: {results['EFT'][activity]}")
        print(f" LST: {results['LST'][activity]}")
        print(f" LFT: {results['LFT'][activity[1]]}")
        print(f" Total Float: {results['Total Float'][activity]}")
        print(f" Free Float: {results['Free Float'][activity]}")
        print(f" Independent Float: {results['Independent Float'][activity]}")
        print("-" * 20)

    # Draw the project network graph
    pos = nx.spring_layout(graph)
    labels = nx.get_edge_attributes(graph, 'duration')

    nx.draw(graph, pos, with_labels=True, node_size=700, node_color="skyblue",
            font_size=10, font_color="black", arrowsize=20)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

    plt.title("Project Network Diagram")
    plt.show()

def calculate_pert(tasks, dependencies):
    # Define tasks: (optimistic, most likely, pessimistic)
    # tasks = {
    #     'A': (1, 3, 5),
    #     'B': (2, 4, 6),
    #     'C': (1, 2, 3),
    #     'D': (3, 6, 9),
    #     'E': (2, 3, 4),
    #     'F': (1, 2, 3),
    #     'G': (2, 5, 8)
    # }
    #
    # # Define dependencies
    # dependencies = {
    #     'A': [],
    #     'B': ['A'],
    #     'C': ['A'],
    #     'D': ['B', 'C'],
    #     'E': ['C'],
    #     'F': ['D', 'E'],
    #     'G': ['F']
    # }
    #
    # task_info, critical_path = calculate_pert(tasks, dependencies)
    # print("Critical Path:", " -> ".join(critical_path))
    # visualize_pert(task_info)

    task_info = {}

    # Step 1: Compute durations using PERT formula
    for name, (opt, most, pess) in tasks.items():
        duration = (opt + 4 * most + pess) / 6
        task_info[name] = {
            'name': name,
            'duration': duration,
            'early_start': 0,
            'early_finish': 0,
            'late_start': float('inf'),
            'late_finish': float('inf'),
            'successors': []
        }

    # Step 2: Build graph of successors
    for task, deps in dependencies.items():
        for dep in deps:
            task_info[dep]['successors'].append(task)

    # Step 3: Forward Pass
    for task in task_info:
        if not dependencies[task]:
            task_info[task]['early_start'] = 0
            task_info[task]['early_finish'] = task_info[task]['duration']

    sorted_tasks = list(nx.topological_sort(build_nx_graph(dependencies)))

    for task in sorted_tasks:
        for succ in task_info[task]['successors']:
            succ_task = task_info[succ]
            succ_task['early_start'] = max(succ_task['early_start'], task_info[task]['early_finish'])
            succ_task['early_finish'] = succ_task['early_start'] + succ_task['duration']

    # Step 4: Backward Pass
    max_finish = max(task['early_finish'] for task in task_info.values())

    for task in task_info:
        if not task_info[task]['successors']:
            task_info[task]['late_finish'] = max_finish
            task_info[task]['late_start'] = max_finish - task_info[task]['duration']

    for task in reversed(sorted_tasks):
        for succ in task_info[task]['successors']:
            task_info[task]['late_finish'] = min(task_info[task]['late_finish'], task_info[succ]['late_start'])
            task_info[task]['late_start'] = task_info[task]['late_finish'] - task_info[task]['duration']

    # Step 5: Critical Path
    critical_path = [task['name'] for task in task_info.values() if round(task['early_start'], 2) == round(task['late_start'], 2)]

    return task_info, critical_path


def build_nx_graph(dependencies):
    G = nx.DiGraph()
    for task, deps in dependencies.items():
        for dep in deps:
            G.add_edge(dep, task)
    return G


def visualize_pert(task_info):
    G = nx.DiGraph()
    for task in task_info.values():
        label = f"{task['name']}\nES: {round(task['early_start'], 1)}, EF: {round(task['early_finish'], 1)}\nLS: {round(task['late_start'], 1)}, LF: {round(task['late_finish'], 1)}"
        G.add_node(task['name'], label=label)
        for succ in task['successors']:
            G.add_edge(task['name'], succ)

    pos = nx.spring_layout(G)
    labels = nx.get_node_attributes(G, 'label')
    plt.figure(figsize=(12, 7))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue',
            edge_color='gray', font_size=10)
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8)
    plt.title("PERT Network Diagram")
    plt.show()


def solve_linear_programming(c, A, b, bounds):
    """
        c = [3, 2]  # Maximize: 3x1 + 2x2
    A = [[2, 1], [4, -5]]
    b = [20, 10]
    bounds = [(0, None), (0, None)]  # x1 >= 0, x2 >= 0

    result = solve_linear_programming(c, A, b, bounds)
    print(result)


    //call Like Above
    Solves a linear programming problem of the form:
    Maximize:    c^T * x
    Subject to:  A * x <= b
                 bounds[i][0] <= x[i] <= bounds[i][1]

    Args:
        c (list): Coefficients of the objective function (for maximization).
        A (list of lists): Coefficients for inequality constraints (A_ub).
        b (list): Right-hand side values for inequality constraints (b_ub).
        bounds (list of tuple): Bounds for each variable, e.g., [(0, None), (0, None)]

    Returns:
        dict: Contains optimal value and variable assignments.
    """

    # Convert maximization to minimization by negating c
    c_neg = [-i for i in c]

    result = linprog(c_neg, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    if result.success:
        return {
            'Optimal Value': -result.fun,  # Negate to show max value
            'Variable Values': result.x
        }
    else:
        return {
            'Message': 'Optimization failed',
            'Details': result.message
        }

        
def run_linear_programming(c, A, b, bounds):
    def solve_lp(c, A, b, bounds):
        return linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    def branch_and_bound(c, A, b, bounds):
        Q = Queue()
        Q.put((c, A, b, bounds))
        best_solution = None
        best_value = float('-inf')

        while not Q.empty():
            current_problem = Q.get()
            res = solve_lp(*current_problem)

            if res.success and -res.fun > best_value:
                solution = res.x
                if all(np.isclose(solution, np.round(solution))):
                    value = -res.fun
                    if value > best_value:
                        best_value = value
                        best_solution = solution
                else:
                    for i in range(len(solution)):
                        if not np.isclose(solution[i], np.round(solution[i])):
                            lower_bounds = current_problem[3].copy()
                            upper_bounds = current_problem[3].copy()
                            lower_bounds[i] = (lower_bounds[i][0], np.floor(solution[i]))
                            upper_bounds[i] = (np.ceil(solution[i]), upper_bounds[i][1])
                            Q.put((current_problem[0], current_problem[1], current_problem[2], lower_bounds))
                            Q.put((current_problem[0], current_problem[1], current_problem[2], upper_bounds))
                            break
        return best_solution, best_value

    # Input: Example coefficients and constraints
    # c = [-4, -3]  # Maximize 4x + 3y
    # A = [[2, 1], [1, 2]]
    # b = [8, 6]
    # bounds = [(0, None), (0, None)]

    # Solve and print
    solution, value = branch_and_bound(c, A, b, bounds)
    print(f"Optimal solution: {solution}")
    print(f"Optimal value: {value}")

# Call the function

def solve_dp_problems():
    # Problem 1: Knapsack Problem (0/1 Knapsack)
    def knapsack(weights, values, W):
        n = len(weights)
        dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]
        for i in range(n + 1):
            for w in range(W + 1):
                if i == 0 or w == 0:
                    dp[i][w] = 0
                elif weights[i-1] <= w:
                    dp[i][w] = max(values[i-1] + dp[i-1][w-weights[i-1]], dp[i-1][w])
                else:
                    dp[i][w] = dp[i-1][w]
        return dp[n][W]

    # Problem 2: Subset Sum Problem
    def subset_sum(arr, sum):
        n = len(arr)
        dp = [[False for _ in range(sum + 1)] for _ in range(n + 1)]
        for i in range(n + 1):
            dp[i][0] = True
        for i in range(1, n + 1):
            for s in range(1, sum + 1):
                if arr[i-1] <= s:
                    dp[i][s] = dp[i-1][s] or dp[i-1][s-arr[i-1]]
                else:
                    dp[i][s] = dp[i-1][s]
        return dp[n][sum]

    # Problem 3: Longest Common Subsequence (LCS)
    def lcs(X, Y):
        m = len(X)
        n = len(Y)
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0 or j == 0:
                    dp[i][j] = 0
                elif X[i-1] == Y[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        return dp[m][n]

    # Example usage for each problem:

    # Knapsack Problem
    # weights_1 = [1, 3, 4, 5]
    # values_1 = [1, 4, 5, 7]
    # W_1 = 7
    # print("Knapsack Problem Solution:", knapsack(weights_1, values_1, W_1))  # OUTPUT: 9
    # 
    # # Subset Sum Problem
    # arr_1 = [3, 34, 4, 12, 5, 2]
    # sum_1 = 9
    # print("Subset Sum Problem Solution:", subset_sum(arr_1, sum_1))  # OUTPUT: True
    # 
    # # Longest Common Subsequence Problem
    # X_1 = "AGGTAB"
    # Y_1 = "GXTXAYB"
    # print("Longest Common Subsequence Problem Solution:", lcs(X_1, Y_1))  # OUTPUT: 4
    

def stochastic_gradient_descent(learning_rate=0.01, epochs=1000):
    """
    Perform Stochastic Gradient Descent to learn the weights for linear regression.

    Parameters:
    learning_rate : float
        The learning rate.
    epochs : int
        Number of iterations over the training data.

    Returns:
    weights : numpy array, shape (n_features,)
        The learned weights.
    """
    # Generating some example data
    np.random.seed(0)
    X = 2 * np.random.rand(100, 1)
    y = 4 + 3 * X + np.random.randn(100, 1)

    X_b = np.c_[np.ones((100, 1)), X]  # Add x0 = 1 to each instance

    # Reshape y
    y = y.ravel()

    # Initialize weights
    n_samples, n_features = X_b.shape
    weights = np.zeros(n_features)

    # Running SGD
    for epoch in range(epochs):
        for i in range(n_samples):
            gradient = (np.dot(X_b[i], weights) - y[i]) * X_b[i]
            weights -= learning_rate * gradient

    print(f"Weights: {weights}")
    return weights
def minimize_quadratic_function(learning_rate=0.1, epochs=50):
    """
    Minimizes the quadratic function f(x) = x^2 + 2x + 1 using gradient descent.

    Parameters:
    learning_rate : float
        The learning rate for gradient descent.
    epochs : int
        Number of iterations for optimization.

    Returns:
    x : float
        The minimized value of x.
    """
    def quadratic_loss(x):
        return x ** 2 + 2 * x + 1  # Simple quadratic function

    def quadratic_gradient(x):
        return 2 * x + 2  # Gradient of the function

    # Random initial point
    x = np.random.randn()

    # Gradient descent loop
    for _ in range(epochs):
        x -= learning_rate * quadratic_gradient(x)

    print("Minimum of quadratic function:", x)
    return x
#9 Experiments
def fit_model(model_type, t, y):
    """
    # Example usage:
np.random.seed(123)

# Generate data for exponential model
t_exp = np.linspace(0, 1, 50)
y_exp_true = [2.0, 0.5]
y_exp = 2.0 * np.exp(-0.5 * t_exp) + 0.1 * np.random.randn(50)

# Fit the exponential model
print("Exponential Model Optimized Parameters:", fit_model('exponential', t_exp, y_exp))

# Generate data for logistic growth model
t_log = np.linspace(0, 5, 100)
y_log_true = [5.0, 0.8, 3.0]
y_log = 5.0 / (1 + np.exp(-0.8 * (t_log - 3.0))) + 0.1 * np.random.randn(100)

# Fit the logistic growth model
print("Logistic Model Optimized Parameters:", fit_model('logistic', t_log, y_log))

# Generate data for sum of sine waves model
t_sine = np.linspace(0, 10, 200)
y_sine_true = [2.0, 0.5, 1.0, 1.0, 2.0, 2.5]
y_sine = 2.0 * np.sin(0.5 * t_sine + 1.0) + 1.0 * np.sin(2.0 * t_sine + 2.5) + 0.1 * np.random.randn(200)

# Fit the sum of sine waves model
print("Sine Sum Model Optimized Parameters:", fit_model('sine_sum', t_sine, y_sine))

    Fits a model to the data using nonlinear least squares.

    Parameters:
    model_type : str
        The type of model to fit ('exponential', 'logistic', 'sine_sum').
    t : array-like
        The time or independent variable.
    y : array-like
        The observed data or dependent variable.

    Returns:
    result.x : array
        The optimized parameters of the model.
    """
    def exponential_model(x, t):
        # Exponential decay model
        return x[0] * np.exp(-x[1] * t)

    def logistic_model(x, t):
        # Logistic growth model
        return x[0] / (1 + np.exp(-x[1] * (t - x[2])))

    def sine_sum_model(x, t):
        # Sum of sine waves model
        return x[0] * np.sin(x[1] * t + x[2]) + x[3] * np.sin(x[4] * t + x[5])

    def residual(x, t, y, model_func):
        # Residual function (squared error)
        return model_func(x, t) - y

    # Initial guess for parameters based on model type
    if model_type == 'exponential':
        model_func = exponential_model
        x0 = [1.0, 1.0]  # Initial guess for exponential model parameters
    elif model_type == 'logistic':
        model_func = logistic_model
        x0 = [1.0, 1.0, 1.0]  # Initial guess for logistic model parameters
    elif model_type == 'sine_sum':
        model_func = sine_sum_model
        x0 = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]  # Initial guess for sine sum model parameters
    else:
        raise ValueError("Unknown model type")

    # Fit the model to the data using nonlinear least squares
    result = least_squares(residual, x0, args=(t, y, model_func))

    # Return the optimized parameters
    return result.x


def solve_and_plot_lp(c,A,b):
    # Objective function coefficients (maximize Z = 3x + 2y)
    # c = [-3, -2]  # Negated for minimization
    # 
    # # Coefficients for inequality constraints
    # A = [[1, 1],
    #      [1, 0],
    #      [0, 1]]
    # 
    # # Right-hand side of constraints
    # b = [4, 2, 3]

    # Variable bounds
    x_bounds = (0, None)
    y_bounds = (0, None)

    # Solve the linear programming problem
    res = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method='highs')

    if not res.success:
        print("No solution found:", res.message)
        return

    # Extract results
    x_opt, y_opt = res.x
    z_opt = -res.fun  # Negate for maximization

    print(f"Optimal solution: x = {x_opt}, y = {y_opt}, Z = {z_opt}")

    # Plotting
    x = np.linspace(0, 5, 400)
    y1 = 4 - x  # From x + y ≤ 4
    y2 = 3 * np.ones_like(x)  # y ≤ 3
    y3 = np.full_like(x, np.inf)
    y3[x <= 2] = 100  # x ≤ 2 (cutoff line)

    plt.figure(figsize=(8, 8))

    # Plot constraints
    plt.plot(x, y1, label=r'$x + y \leq 4$')
    plt.plot(x, y2, '--', label=r'$y \leq 3$')
    plt.axvline(x=2, linestyle='--', color='green', label=r'$x \leq 2$')

    # Feasible region (shade intersection)
    y_feasible = np.minimum(np.minimum(y1, y2), y3)
    plt.fill_between(x, 0, y_feasible, where=(x <= 2), color='grey', alpha=0.4)

    # Optimal point
    plt.plot(x_opt, y_opt, 'ro', label=f'Optimal (x={x_opt:.2f}, y={y_opt:.2f})')

    # Labels and formatting
    plt.xlim(0, 5)
    plt.ylim(0, 5)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Graphical Solution of Linear Programming Problem')
    plt.legend()
    plt.grid(True)
    plt.show()
import sympy as sp


def minimize_kkt(n):
    x = sp.symbols(f'x1:{n+1}', real=True)
    λ = sp.symbols('λ1', real=True)

    f = sum(var**2 for var in x)
    g = sum(x) - 1  # g(x) ≤ 0

    L = f + λ * g
    grad_L = [sp.diff(L, var) for var in x]

    kkt_eqs = grad_L + [λ * g]

    solution = sp.solve(kkt_eqs, list(x) + [λ], dict=True)

    feasible = []
    for sol in solution:
        g_val = g.subs(sol)
        λ_val = sol[λ]
        if g_val <= 0 and λ_val >= 0:
            feasible.append(sol)

    if feasible:
        for i, sol in enumerate(feasible):
            print(f"\n✅ Minimum Solution {i+1}:")
            for var in x:
                print(f"  {var} = {sol[var]}")
            print(f"  λ = {sol[λ]}")
            grad_f = [sp.diff(f, var) for var in x]
            grad_f_val = [g.subs({var: sol[var] for var in x}) for g in grad_f]
            print(f"  Gradient of f at optimal point: {grad_f_val}")
            print(f"  Objective value: {f.subs(sol)}")
    else:
        print("✘ No feasible KKT solution found.")
def maximize_kkt(n):
    x = sp.symbols(f'x1:{n+1}', real=True)
    λ = sp.symbols('λ1', real=True)

    f = -sum(var**2 for var in x)  # maximize f = minimize -f
    g = sum(x) - 1  # g(x) ≤ 0

    L = f + λ * g
    grad_L = [sp.diff(L, var) for var in x]

    kkt_eqs = grad_L + [λ * g]

    solution = sp.solve(kkt_eqs, list(x) + [λ], dict=True)

    feasible = []
    for sol in solution:
        g_val = g.subs(sol)
        λ_val = sol[λ]
        if g_val <= 0 and λ_val >= 0:
            feasible.append(sol)

    if feasible:
        for i, sol in enumerate(feasible):
            print(f"\n✅ Maximum Solution {i+1}:")
            for var in x:
                print(f"  {var} = {sol[var]}")
            print(f"  λ = {sol[λ]}")
            original_f = -f  # flip sign back
            grad_f = [sp.diff(original_f, var) for var in x]
            grad_f_val = [g.subs({var: sol[var] for var in x}) for g in grad_f]
            print(f"  Gradient of f at optimal point: {grad_f_val}")
            print(f"  Objective value: {original_f.subs(sol)}")
    else:
        print("✘ No feasible KKT solution found.")