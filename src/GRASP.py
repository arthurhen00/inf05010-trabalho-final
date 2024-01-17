from copy import deepcopy
from typing import List
from math import ceil
from random import randint, seed
import time


file_name = 'Hard28_BPP645'
file_path = f'selected_bpp_instances/{file_name}.txt'


class Solution():
    def __init__(self, problem_instance: (int,int,List[int]), assignment:List[List[int]]):
        self.assignment = assignment
        self.problem_instance = problem_instance
        
    def __hash__(self):
        return hash(str(self.assignment))

        
    def __eq__(self, other):
        if not isinstance(other, Solution):
            return False

        return (
            self.assignment == other.assignment
        )
        
    def __lt__(self,other:'Solution'):
        return  self.get_bin_amount() < other.get_bin_amount()
    
    def __le__(self,other:'Solution'):
        return self.get_bin_amount() <= other.get_bin_amount()
    
    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result
    def __str__(self):
        return f'{self.assignment}'
    
    def get_empty_space(self) -> int:
        _, bin_capacity, weights = self.problem_instance
        empty_space = 0
        for bin in self.assignment:
            empty_space += bin_capacity - sum([weights[x] for x in bin])
        return empty_space
    
    def get_bin_amount(self) -> int:
        return len(self.assignment)
    
    def print_space_remaining(self) -> None:
        _, bin_capacity, weights = self.problem_instance
        for bin in self.assignment:
            print(bin_capacity-sum([weights[x] for x in bin]))
        return None
    
    
def read_file(file_path: str) -> None:
    weights = []
    with open(file_path,'r') as f:
        number_of_items = int(f.readline())
        bin_capacity = int(f.readline())
        for i in range(number_of_items):
            weights.append(int(f.readline()))
            
    return number_of_items, bin_capacity, weights


def find_initial_solution(problem_instance: (int,int,List[int])) -> Solution:
    number_of_items, bin_capacity, weights = problem_instance
    assignment = [[]]
    for i in range(number_of_items):
        for bin in assignment:
            if sum([weights[x] for x in bin]) + weights[i] < bin_capacity:
                bin.append(i)
            else:
                assignment.append([i])
            break
            
    return Solution(problem_instance, assignment)

def rand_greedy(solutions: List[Solution],alpha: int) -> Solution:
    sorted(solutions)
    chosen_index = randint(0,ceil(len(solutions)/(100/alpha)-1))
    if solutions[0] < solutions[chosen_index]:
        return solutions[0]
    return solutions[chosen_index]

def local_search(solution: Solution) -> List[Solution]:
    _, bin_capacity , weights = solution.problem_instance
    neighbors = []
    for bin_index, bin in enumerate(solution.assignment):
        for other_bin_index, other_bin in enumerate(solution.assignment):
            if bin == other_bin:
                continue
            other_bin_weight = sum([weights[x] for x in other_bin])
            for item in bin:
                if other_bin_weight + weights[item] <= bin_capacity:
                    new_solution = deepcopy(solution)
                    new_solution.assignment[other_bin_index].append(item)
                    new_solution.assignment[bin_index].remove(item)
                    if new_solution.assignment[bin_index] == []:
                        new_solution.assignment.remove([])
                    neighbors.append(new_solution)
    
    return neighbors

def grasp(alpha: int, prob_instance: (int,int,List[int]), max_iter:int = 100) -> Solution:
    if alpha > 100 or alpha <= 0:
        raise Exception('alpha inválido! (0 <= alpha < 100)') from ValueError
    
    i = 0
    best_s = find_initial_solution(prob_instance)
    while i < max_iter:
        s = local_search(best_s)
        if not s:
            break
        s = rand_greedy(s, alpha)
        
        if s <= best_s:
            best_s = s
        
        i = i+1
        
        
    return best_s

instance = read_file(file_path)
num_items, bin_capacity, weights = instance
print(f'Número de itens: {num_items}')
print(f'Capacidade dos cestos: {bin_capacity}')
print(f'Peso dos itens: {weights}\n')

start_time = time.time()
s = grasp(10,instance, 300)

print("--- Resolvido em %s segundos ---" % (time.time() - start_time))
print(f'Solução: {s}')
print(f'Quantidade de cestos: {s.get_bin_amount()}')
for index,bin in enumerate(s.assignment):
    print(f'Cesto {index}: {', '.join(map(str, bin))}  - Peso total: {sum([weights[x] for x in bin])}')