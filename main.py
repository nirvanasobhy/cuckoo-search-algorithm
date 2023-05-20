
import numpy as np
import random

# Function to calculate the total distance of a TSP route
def calculate_distance(route, distance_matrix):
    total_distance = 0
    num_cities = len(route)
    for i in range(num_cities - 1):
        city_a = route[i]
        city_b = route[i + 1]
        total_distance += distance_matrix[city_a][city_b]
    # Add distance from last city back to the starting city
    total_distance += distance_matrix[route[-1]][route[0]]
    return total_distance

# Generate a random solution (TSP route)
def generate_solution(num_cities):
    return random.sample(range(num_cities), num_cities)

# Generate a random solution with a fraction of elements shuffled
def generate_new_solution(solution, alpha):
    num_cities = len(solution)
    num_shuffle = int(alpha * num_cities)
    new_solution = solution.copy()
    indices = random.sample(range(num_cities), num_shuffle)
    for index in indices:
        swap_index = random.randint(0, num_cities - 1)
        new_solution[index], new_solution[swap_index] = new_solution[swap_index], new_solution[index]
    return new_solution

# Cuckoo Search Algorithm
def cuckoo_search_tsp(distance_matrix, num_cuckoos, max_iterations, alpha):
    num_cities = len(distance_matrix)

    # Initialize the population of cuckoos (random solutions)
    population = [generate_solution(num_cities) for _ in range(num_cuckoos)]

    # Main loop
    iteration = 0
    while iteration < max_iterations:
        # Generate new solutions (cuckoos) by shuffling a fraction of elements
        new_population = [generate_new_solution(solution, alpha) for solution in population]

        # Evaluate the fitness (total distance) of the new solutions
        fitness = [calculate_distance(solution, distance_matrix) for solution in new_population]

        # Sort the cuckoos based on fitness (ascending order)
        sorted_indices = np.argsort(fitness)
        population = [new_population[i] for i in sorted_indices]

        # Abandon a fraction of worst solutions and replace them with new ones (random solutions)
        num_abandon = int(alpha * num_cuckoos)
        population[-num_abandon:] = [generate_solution(num_cities) for _ in range(num_abandon)]

        iteration += 1

    # Find the best solution (minimum distance) among the cuckoos
    best_solution = population[0]

    return best_solution

# Example inputs
distance_matrix = [
    [0, 2, 9, 10],
    [1, 0, 6, 4],
    [15, 7, 0, 8],
    [6, 3, 12, 0]
]
num_cuckoos = 10
max_iterations = 100
alpha = 0.3

# Call Cuckoo Search algorithm
best_solution = cuckoo_search_tsp(distance_matrix, num_cuckoos, max_iterations, alpha)

# Print the best solution (TSP route)
print("Best Solution (TSP Route):", best_solution)