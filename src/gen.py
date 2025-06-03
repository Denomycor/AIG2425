from functools import reduce
from typing import OrderedDict
from vec2 import vec2
from car import MLPCar
import math
import torch


def make_car(game):
    return MLPCar(
        game,
        top_speed=100.0,
        acceleration=15.0,
        steering=math.pi*1.5,
        break_strenght=15.0,
        drag_force=10.0,
        color=(255, 0, 0)
    )


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
def selection_tournament(population: list[MLPCar], fit: list[int], tournament_size: int, offspring_nr: int) -> list[tuple[MLPCar, MLPCar]]:
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

