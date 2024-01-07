import random
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

POPULATION_SIZE = 200  # Constants
MUTATION_BLOCK = 3
P_CROSSOVER = 0.9
P_MUTATION = 0.1
MAX_GENERATIONS = 50

RANDOM_SEED = 143
random.seed(RANDOM_SEED)

data = pd.read_csv("data/distances-10.csv", header=None)  # File reading
data = data.loc[:, 1:].values
CHROMOSOME_LENGTH = data.shape[0]


class CIndividual(list):
    def __init__(self, *args):
        super().__init__(*args)
        self.fitness = float('inf')


def fitness_function(individual):
    fitness = 0
    for i in range(CHROMOSOME_LENGTH - 1):
        fitness += data[individual[i], individual[i+1]]
    fitness += data[individual[CHROMOSOME_LENGTH - 1], individual[0]]
    return fitness


def individual_creator():
    return CIndividual(random.sample(range(CHROMOSOME_LENGTH), CHROMOSOME_LENGTH))
    # return CIndividual(np.random.permutation(chromosome_length))


def population_creator():
    return list([individual_creator() for i in range(POPULATION_SIZE)])


def clone(to_clone):
    individual = CIndividual(to_clone[:])
    individual.fitness = to_clone.fitness
    return individual


def tournament_selection(population, pop_length):
    offspring = []
    for i in range(pop_length):
        member1 = member2 = member3 = 0
        while member1 == member2 or member1 == member3 or member2 == member3:
            member1, member2, member3 = random.randint(0, pop_length-1), random.randint(0, pop_length-1), random.randint(0, pop_length-1)
        offspring.append(min([population[member1], population[member2], population[member3]], key=lambda individual: individual.fitness))
    return offspring


def order_crossover(parent1, parent2):
    child1, child2 = clone(parent1), clone(parent2)
    point1 = random.randint(1, CHROMOSOME_LENGTH-3)
    point2 = random.randint(point1 + 1, CHROMOSOME_LENGTH-2)
    child1[point1:point2], child2[point1:point2] = parent2[point1:point2], parent1[point1:point2]

    parent1_ptr, parent2_ptr, child1_ptr, child2_ptr = point2, point2, point2, point2
    for i in range(CHROMOSOME_LENGTH):
        if parent1[parent1_ptr % CHROMOSOME_LENGTH] not in child1[point1:point2]:
            child1[child1_ptr % CHROMOSOME_LENGTH] = parent1[parent1_ptr % CHROMOSOME_LENGTH]
            child1_ptr += 1
        if parent2[parent2_ptr % CHROMOSOME_LENGTH] not in child2[point1:point2]:
            child2[child2_ptr % CHROMOSOME_LENGTH] = parent2[parent2_ptr % CHROMOSOME_LENGTH]
            child2_ptr += 1
        parent1_ptr += 1
        parent2_ptr += 1

    return [child1, child2]


def partially_mapped_crossover(parent1, parent2):
    child1, child2 = clone(parent1), clone(parent2)
    point1 = random.randint(1, CHROMOSOME_LENGTH - 3)
    point2 = random.randint(point1 + 1, CHROMOSOME_LENGTH - 2)
    child1[point1:point2], child2[point1:point2] = parent2[point1:point2], parent1[point1:point2]

    parent2_dict = dict(zip(parent1[point1:point2], parent2[point1:point2]))
    parent1_dict = dict(zip(parent2[point1:point2], parent1[point1:point2]))
    parent1_ptr, parent2_ptr = point2, point2
    for i in range(CHROMOSOME_LENGTH - point2 + point1):
        new_symbol1 = parent1[parent1_ptr % CHROMOSOME_LENGTH]
        new_symbol2 = parent2[parent2_ptr % CHROMOSOME_LENGTH]
        while new_symbol1 in parent1_dict:
            new_symbol1 = parent1_dict[new_symbol1]
        while new_symbol2 in parent2_dict:
            new_symbol2 = parent2_dict[new_symbol2]
        child1[parent1_ptr % CHROMOSOME_LENGTH] = new_symbol1
        child2[parent2_ptr % CHROMOSOME_LENGTH] = new_symbol2
        parent1_ptr += 1
        parent2_ptr += 1

    return child1, child2


def shuffle_mutation(mutant, probability):
    for idx in range(CHROMOSOME_LENGTH):
        if random.random() < probability:
            indexes = list(range(idx, idx+MUTATION_BLOCK))
            indexes = [x % CHROMOSOME_LENGTH for x in indexes]
            values = [mutant[x] for x in indexes]

            random.shuffle(values)
            for i, index in enumerate(indexes):
                mutant[index] = values[i]


def main():
    population = population_creator()
    fitness_population = list(map(fitness_function, population))
    for individual, fitness_value in zip(population, fitness_population):
        individual.fitness = fitness_value

    min_fitness_values = []
    mean_fitness_values = []
    fitness_values = [individual.fitness for individual in population]
    max_value = np.max(fitness_values) + 100

    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot(fitness_values, ' o', markersize=1)
    ax.set_ylim(0, max_value)
    ax.set_title("Visualization of evolution")
    ax.set_ylabel("Overall distance (fitness value)")
    ax.set_xlabel("Phenotype's id")

    generation_counter = 0
    while generation_counter < MAX_GENERATIONS:
        offspring = tournament_selection(population, len(population))
        offspring = list(map(clone, offspring))

        for i in range(0, len(offspring) - 1, 2):
            if random.random() < P_CROSSOVER:
                offspring[i], offspring[i+1] = order_crossover(offspring[i], offspring[i+1])
                # offspring[i], offspring[i+1] = partially_mapped_crossover(offspring[i], offspring[i+1])

        for mutant in offspring:
            if random.random() < P_MUTATION:
                shuffle_mutation(mutant, 1.0/CHROMOSOME_LENGTH)

        fitness_population = list(map(fitness_function, offspring))
        for individual, fitness_value in zip(offspring, fitness_population):
            individual.fitness = fitness_value
        population[:] = offspring
        fitness_values = [individual.fitness for individual in population]

        min_fitness_value = np.min(fitness_values)
        min_fitness_values.append(min_fitness_value)
        mean_fitness_value = np.mean(fitness_values)
        mean_fitness_values.append(mean_fitness_value)
        best_index = fitness_values.index(min_fitness_value)
        generation_counter += 1

        print(f"Generation {generation_counter}: Minimal distance = {min_fitness_value}, Average distance = {mean_fitness_value}")
        print("The best route:", *population[best_index], population[best_index][0], "\n")

        line.set_ydata(fitness_values)
        plt.draw()
        plt.gcf().canvas.flush_events()
        time.sleep(0.3)

    plt.ioff()
    plt.show()

    plt.plot(min_fitness_values, label="Minimal value")
    plt.plot(mean_fitness_values, label="Average value")
    plt.xlabel("Generation")
    plt.ylabel("Min/Average distance")
    plt.title("Dependence of minimal and average distance on generation")
    plt.legend()
    plt.show()

    if CHROMOSOME_LENGTH == 10:
        cities = pd.read_csv("data/distances-10.csv", header=None)  # File reading
        cities = cities.values
        best_route = population[fitness_values.index(np.min(fitness_values))]

        graph = nx.Graph()
        graph.add_nodes_from(cities[:, 0])
        cities_pos = {}
        for city in cities:
            cities_pos[city[0]] = np.array([city[1], city[2]])
        for i in range(CHROMOSOME_LENGTH - 1):
            graph.add_edge(cities[best_route[i], 0], cities[best_route[i + 1], 0])
        graph.add_edge(cities[best_route[0], 0], cities[best_route[CHROMOSOME_LENGTH - 1], 0])

        for src, dest, edge_attrs in graph.edges(data=True):
            edge_attrs["distance"] = f"{data[np.where(cities[:, 0] == src)[0], np.where(cities[:, 0] == dest)[0]][0]}km"
        labels = {edge: graph.edges[edge]["distance"] for edge in graph.edges}

        fig, ax = plt.subplots(figsize=(12, 12))
        ax.set_title("TSP problem solution")
        nx.draw_networkx_nodes(graph, pos=cities_pos, nodelist=cities[:, 0], node_size=20, node_color="aqua")
        nx.draw_networkx_edges(graph, pos=cities_pos, style="dashed", edgelist=graph.edges, edge_color="black")
        nx.draw_networkx_labels(graph, pos=cities_pos, font_color='black', font_size=7, verticalalignment="bottom", horizontalalignment="right")
        nx.draw_networkx_edge_labels(graph, pos=cities_pos, edge_labels=labels, font_color='black', font_size=7, verticalalignment="top")
        plt.show()


if __name__ == "__main__":
    main()
