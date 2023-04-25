import numpy as np
import random

IMAGE_SIZE_RANGE = [150, 200, 224, 250, 300]
BATCH_SIZE_RANGE = [16, 32, 50, 64, 128]
NUM_EPOCHS_RANGE = [10, 20, 30, 40, 50]
LEARNING_RATE_RANGE = [0.0001, 0.0005, 0.001, 0.005, 0.01]
POPULATION_SIZE = 50
MAX_GENERATIONS = 100
CROSSOVER_RATE = 0.5

def calculate_fitness(individual, labels):
    """
    Calculates the fitness of a population of individuals using categorical cross-entropy.
    
    Args:
    - individual: a list of gene arrays, where each gene array represents an individual in the population
    - labels: a numpy array of shape (num_samples,), where each element is an integer label
    
    Returns:
    - a numpy array of shape (num_individuals,) containing the fitness scores for each individual
    """
    num_individuals = len(individual)
    num_classes = len(np.unique(labels))
    fitness = np.zeros(num_individuals)
    
    for i in range(num_individuals):
        predictions = individual[i]
        targets = np.zeros((len(predictions), num_classes))
        targets[np.arange(len(predictions)), labels] = 1
        loss = -np.sum(targets * np.log(predictions)) / len(predictions)
        fitness[i] = 1 / (1 + loss)
        
    return fitness

def tournament_selection(population, num_selected, tournament_size = 3):
    selected = []
    while len(selected) < num_selected: #num_selected is the number of inds to select from pop/2
        tournament = random.sample(population, tournament_size)
        winner = max(tournament, key=lambda ind: ind.fitness)
        selected.append(winner)
    return selected

def crossover(parent1, parent2, crossover_rate):
    if random.random() < crossover_rate:
        crossover_point = random.randint(0, len(parent1))
        child = parent1[:crossover_point] + parent2[crossover_point:]
    else:
        child = parent1[:]
    return child

def mutation(individual, mutation_rate):
    mutated_ind = individual[:]
    for i in range(len(mutated_ind)):
        if random.random() < mutation_rate:
            mutated_ind[i] = 1 - mutated_ind[i]

population = []

for i in range(POPULATION_SIZE):
    individual = {
        'image_size': random.choice(IMAGE_SIZE_RANGE),
        'batch_size': random.choice(BATCH_SIZE_RANGE),
        'num_epochs': random.choice(NUM_EPOCHS_RANGE),
        'learning_rate': random.choice(LEARNING_RATE_RANGE)
    }
    population.append(individual)
    
for individual in population:
    individual["fitness"] = calculate_fitness(individual)


# def GA(fitness, num_bits, num_iter, num_pop, cross_rate, mut_rate):
#     population = [npr.randint(MIN, MAX, num_bits).tolist() for _ in range(num_pop)]
#     #keep track of best solution
#     best, best_eval = 0, objective(population[0])
#     #enum gens
#     for gen in range(num_iter):
#         #eval candidates in the pop
#         fitness = [objective(c) for c in population]
#         #check for new best solution
#         for i in range(num_pop):
#             if fitness[i] < best_eval:
#                 best, best_eval = population[i], fitness[i]
#                 print(">%d, new best f(%s) = %.3f" % (gen,  population[i], fitness[i]))
#         #select parents
#         selected = [selection(population, fitness) for _ in range(num_pop)]
#         #create next gen
#         children = list()
#         for i in range(0, num_pop, 2):
#             #get selected parents in pairs
#             parent_1, parent_2 = selected[i], selected[i+1]
#             #crossover & mutation
#             for c in crossover(parent_1, parent_2, cross_rate):
#                 #mutation
#                 mutation(c, mut_rate)
#                 #store for next gen
#                 children.append(c)
#         #replace population
#         population = children
#     return [best, best_eval]

# best, score = GA(objective, num_bits, num_iter, num_pop, cross_rate, mut_rate)
# # print("Done!")
# # plt.plot(best)
# # plt.plot(score)
# # plt.show()
# print(f"f({best}) =  {score}")