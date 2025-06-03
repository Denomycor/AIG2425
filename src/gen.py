from typing import OrderedDict
from vec2 import vec2
from car import MLPCar
import math
import torch
from skel import Window, Game
from track import Track
from random import random
from typing import List, Any


def fitness(game):
    track = game.objects[0]


def select_best_organism(fitnesses: List[float], organisms: List[Any]) -> Any:
    if not fitnesses or len(fitnesses) != len(organisms):
        raise ValueError("Lists must be non-empty and of the same length")
    
    best_index = fitnesses.index(max(fitnesses))
    return organisms[best_index]


def run_simulation(random, genes):
    window = Window((1920/2, 1080/2), "Test", (255,255,255))
    game = Game(window, True)
    car = MLPCar(
        game,
        top_speed=100.0,
        acceleration=15.0,
        steering=math.pi*1.5,
        break_strenght=15.0,
        drag_force=10.0,
        color=(255, 0, 0)
    )
    if(random):
        car.set_genes(generate_random_gene(car.wrapper.arch))
    else:
        car.set_genes(genes)

    car.pos = vec2(100, 100)

    track = Track(game, [vec2(100, 100), vec2(100, 400), vec2(400, 400), vec2(600,100), vec2(900, 100), vec2(900, 400), vec2(600, 400), vec2(400,100), vec2(100,100)], (0,0,0), 70, [car])
    car.init_sensors(track)

    game.add_object(track)
    game.add_object(car)


    while(game.running and game.elapsed_time < 30):
        game.run()

    fit = fitness(game)
    return (fit, car.get_genes())



# Cross two different genes to create a new one
def cross_genes(st: OrderedDict, nd: OrderedDict) -> OrderedDict:
    child = OrderedDict()
    for key in st.keys():
        if torch.is_tensor(st[key]) and torch.is_tensor(nd[key]):
            # Perform element-wise crossover for tensors
            mask = torch.rand_like(st[key]) < 0.5
            child[key] = torch.where(mask, st[key], nd[key])
        else:
            # Randomly select gene from either parent
            if torch.rand(1).item() < 0.5:
                child[key] = st[key]
            else:
                child[key] = nd[key]
    return child


# Create a new gene which is a mutation of the parameter gene
def mutate_genes(gene: OrderedDict, mutation_rate: float = 0.1) -> OrderedDict:
    mutated_gene = OrderedDict()
    for key, value in gene.items():
        if "weight" in key or "bias" in key:
            if torch.rand(1).item() < mutation_rate:  # Apply mutation
                mutation = torch.randn_like(value) * 0.1  # Small random perturbation
                mutated_gene[key] = value + mutation
            else:
                mutated_gene[key] = value
        else:
            mutated_gene[key] = value
    return mutated_gene


# From the population and it's fitness select pairs of organisms to generate offspring
def selection_tournament(population: list[OrderedDict], fit: list[int], tournament_size: int, offspring_nr: int) -> list[tuple[OrderedDict, OrderedDict]]:
    selected_pairs = []
    for _ in range(offspring_nr):
        # Select first parent
        candidates = torch.randperm(len(population))[:tournament_size]
        best_candidate = min(candidates, key=lambda idx: fit[idx])
        parent1 = population[best_candidate]

        # Select second parent
        second_best_candidate = min(candidates, key=lambda idx: fit[idx] if fit[idx] > fit[best_candidate] else float('inf'))
        parent2 = population[second_best_candidate]

        selected_pairs.append((parent1, parent2))
    return selected_pairs


# Generate a random set of weights and bias for a given neural network
def generate_random_gene(nn_arch: list[int]) -> OrderedDict:
    out = OrderedDict()
    for i in range(len(nn_arch)-1):
        st = nn_arch[i]
        nd = nn_arch[i+1]
        out["l"+ str(i+1)+".weight"] = torch.rand(nd, st)
        out["l"+ str(i+1)+".bias"] = torch.rand(nd)
    return out


def run_genetic_algorithm():
    generations = 50
    population = 10
    curr_generation = 0

    # run first generation
    results = [run_simulation(True, {}) for _ in range(population)]
    fit1, gene1 = zip(*results)

    fits = list(fit1)
    genes = list(gene1)

    pairs = selection_tournament(genes, fits, 5, 10)
    childs = [cross_genes(g1, g2) for (g1, g2) in pairs]
    for i in range(len(childs)):
        if random() < 0.2:
            childs[i] = mutate_genes(childs[i])

    best_candidate = select_best_organism(fits, genes)

    while curr_generation < generations:
        print(curr_generation)
        results = [run_simulation(False, c) for c in childs]
        fit1, gene1 = zip(*results)

        fits = list(fit1)
        genes = list(gene1)

        pairs = selection_tournament(genes, fits, 5, 10)
        childs = [cross_genes(g1, g2) for (g1, g2) in pairs]
        for i in range(len(childs)):
            if random() < 0.2:
                childs[i] = mutate_genes(childs[i])
        curr_generation += 1
        best_candidate = select_best_organism(fits, genes)

    return best_candidate


import pygame

pygame.init()
print(run_genetic_algorithm())

