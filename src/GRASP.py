from copy import deepcopy
from typing import List
from math import ceil
from random import randint, seed
import time


file_name = 'teste2'
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
    
    def all_items_assigned(self) -> bool:
        num_items , _, _ = self.problem_instance
        assigned_items = 0
        for bin in self.assignment:
            assigned_items += len(bin)
            
        return num_items == assigned_items
    
    def get_bin_amount(self) -> int:
        return len(self.assignment)
    
    def get_neighbors(self) -> List['Solution']:
        _, bin_capacity , weights = self.problem_instance
        neighbors = []
        for bin_index, bin in enumerate(self.assignment):
            for other_bin_index, other_bin in enumerate(self.assignment):
                if bin == other_bin:
                    continue
                other_bin_weight = sum([weights[x] for x in other_bin])
                for item in bin:
                    if other_bin_weight + weights[item] <= bin_capacity:
                        new_solution = deepcopy(self)
                        new_solution.assignment[other_bin_index].append(item)
                        new_solution.assignment[bin_index].remove(item)
                        if new_solution.assignment[bin_index] == []:
                            new_solution.assignment.remove([])
                        neighbors.append(new_solution)
        
        return neighbors
    

    
    def get_bins_with_enough_space(self, weight: int) -> List['Solution']:
        _ , bin_capacity, weights = self.problem_instance
        bins_with_enough_space = []
        for index, bin in enumerate(self.assignment):
            if sum([weights[x] for x in bin]) + weight <= bin_capacity:
                bins_with_enough_space.append(index)
                
        return bins_with_enough_space
    
def read_file(file_path: str) -> (int,int,List[int]):
    weights = []
    with open(file_path,'r') as f:
        number_of_items = int(f.readline())
        bin_capacity = int(f.readline())
        for i in range(number_of_items):
            weights.append(int(f.readline()))
            
    return number_of_items, bin_capacity, weights

def rand_greedy(instance: (int,int,List[int]),alpha: int) -> Solution:
    _, bin_capacity, weights = instance
    s = Solution(instance,[[]])
    i = 0
    while(not s.all_items_assigned()):
        if s.assignment[0] == []:
            s.assignment[0].append(i)
        else:
            bins_with_enough_space = s.get_bins_with_enough_space(weights[i])
            sorted(bins_with_enough_space, key= lambda x: bin_capacity - sum([weights[y] for y in s.assignment[x]]) + weights[i]) # Escolha gulosa - Poe o item no bin em que o encaixe fica mais justo
            if bins_with_enough_space:
                chosen_index = randint(0,ceil(len(bins_with_enough_space)/(100/alpha)))
                if chosen_index == len(bins_with_enough_space): # Se o indice sorteado for igual ao tamanho da lista dos bins disponiveis ele é inválido, entao criamos outro bin
                    s.assignment.append([i]) 
                else:
                    chosen_bin_index = bins_with_enough_space[chosen_index]
                    s.assignment[chosen_bin_index].append(i) #Senao adiciona o item no bin escolhido
            else:
                s.assignment.append([i])
            
        i = i + 1
    return s

def local_search(solution: Solution) -> Solution:
    
    improved = True
    explored = set()
    while improved:
        improved = False
        neighbors = solution.get_neighbors()
        for neighbor in neighbors:
            if neighbor <= solution and neighbor not in explored:
                explored.add(solution)
                solution = neighbor
                improved = True
                break
            
    return solution
        
   
def grasp(alpha: int, prob_instance: (int,int,List[int]), max_iter:int = 100) -> Solution:
    if alpha > 100 or alpha <= 0:
        raise Exception('alpha inválido! (0 <= alpha < 100)') from ValueError
    
    i = 0
    solutions = []
    while i < max_iter:
        s = rand_greedy(prob_instance, alpha)
        s = local_search(s)
        
        solutions.append(s)
        
        i = i+1
        
       
    return min(solutions), i

instance = read_file(file_path)
num_items, bin_capacity, weights = instance
print(f'Número de itens: {num_items}')
print(f'Capacidade dos cestos: {bin_capacity}')
print(f'Peso dos itens: {weights}\n')

start_time = time.time()
s, iterations = grasp(10,instance, 300)

print(f"--- Resolvido em {time.time() - start_time: .5f} segundos | {iterations} iterações realizadas ---")
print(f'Solução: {s}')
print(f'Quantidade de cestos: {s.get_bin_amount()}')
for index,bin in enumerate(s.assignment):
    print(f'Cesto {index}: {', '.join(map(str, bin))}  - Peso total: {sum([weights[x] for x in bin])}')