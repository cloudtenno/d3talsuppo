# This script is modified from https://github.com/chengxi600/RLStuff/blob/master/Genetic%20Algorithms/8Queens_GA.ipynb
# Modification made in initialization population generation and mutation to avoid duplicating queens
# Improvement made in user interface where user can set the number of queen, population size, mutation rate and maximum epoch
# Error Control also implemented
# Result will be log in text file named Final_Result.txt and should be found under the same directory
# Also added feature to refresh the population to prevent GA getting stuck at local point
# If stuck at local point, try increasing the population size or increasing the mutation rate
# Change the refresh_rate if the program refresh the population too fast

import random
from scipy import special as sc
import itertools

log = open('Lu_Xinpei_EE6227_Assignment_3_Result.txt','w')

print('\nProgram Written by Lu Xinpei')
print('\nProgram Started, to stop press Ctrl+C\n')

generation = 1

MIXING_NUMBER = 2

def get_number_queen():
    try:
        NUM_QUEENS = int(input('Enter Number of Queens: '))
        assert NUM_QUEENS > 0, 'Population size must be greater than 0'
        return int(NUM_QUEENS)
    except KeyboardInterrupt:
        print('\nProgram Stopped')
        exit()
    except:
        print('Please Enter integral above 0')
        retry_queen = get_number_queen()
        return retry_queen

def get_population_size():
    try:
        POPULATION_SIZE = int(input('Enter Population Size: '))
        assert POPULATION_SIZE > 3, 'Population size must be greater than 3'
        return int(POPULATION_SIZE)
    except KeyboardInterrupt:
        print('\nProgram Stopped')
        exit()
    except:
        print('Please Enter integral above 3')
        retry_pop_size = get_population_size()
        return retry_pop_size

def get_mutation_rate():
    try:
        MUTATION_RATE = float(input('Enter Mutation Rate: '))
        assert MUTATION_RATE > 0 and MUTATION_RATE < 1, 'Mutation Rate must be between 0 and 1'
        return float(MUTATION_RATE)
    except KeyboardInterrupt:
        print('\nProgram Stopped')
        exit()
    except:
        print('Please Enter decimal between 0 and 1')
        retry_mut_rate = get_mutation_rate()
        return retry_mut_rate

def get_run_limit():
    try:
        run_limits = int(input('Enter Maximum Epoch: '))
        assert run_limits > 10000, 'Must have more than 10,000 Epoch'
        return int(run_limits)
    except KeyboardInterrupt:
        print('\nProgram Stopped')
        exit()
    except:
        print('Please Enter integral above 10,000')
        retry_run_limits = get_run_limit()
        return retry_run_limits

def get_refresh_rate():
    try:
        refresh_rate = int(input('Define the number of epoch before population refreshes: '))
        assert refresh_rate >= 1000, 'refresh rate must be greater than 1,000'
        return int(refresh_rate)
    except KeyboardInterrupt:
        print('\nProgram Stopped')
        exit()
    except:
        print('Please Enter integral above 0')
        retry_refresh_rate = get_refresh_rate()
        return retry_refresh_rate

def fitness_score(seq):
    score = 0
    for row in range(NUM_QUEENS):
        col = seq[row]
        for other_row in range(NUM_QUEENS):
            #queens cannot pair with itself
            if other_row == row:
                continue
            if seq[other_row] == col:
                continue
            if other_row + seq[other_row] == row + col:
                continue
            if other_row - seq[other_row] == row - col:
                continue
            score += 1
    #divide by 2 as pairs of queens are commutative
    return score/2


def selection(population):
    parents = []
    for ind in population:
        #select parents with probability proportional to their fitness score
        if random.randrange(sc.comb(NUM_QUEENS, 2)*2) < fitness_score(ind):
            parents.append(ind)
    return parents


def crossover(parents):
    #random indexes to to cross states with
    cross_points = random.sample(range(NUM_QUEENS), MIXING_NUMBER - 1)
    offsprings = []
    #all permutations of parents
    permutations = list(itertools.permutations(parents, MIXING_NUMBER))
    for perm in permutations:
        offspring = []
        #track starting index of sublist
        start_pt = 0
        for parent_idx, cross_point in enumerate(cross_points): #doesn't account for last parent
            #sublist of parent to be crossed
            parent_part = perm[parent_idx][start_pt:cross_point]
            offspring.append(parent_part)
            #update index pointer
            start_pt = cross_point
        #last parent
        last_parent = perm[-1]
        parent_part = last_parent[cross_point:]
        offspring.append(parent_part)
        #flatten the list since append works kinda differently
        offsprings.append(list(itertools.chain(*offspring)))

    return offsprings

def mutate(seq):
    for row in range(len(seq)):
        if random.random() < MUTATION_RATE:
            swap_seq = random.sample(range(NUM_QUEENS), 2)
            place_holder = seq[swap_seq[1]]
            seq[swap_seq[1]] = seq[swap_seq[0]]
            seq[swap_seq[0]] = place_holder
    return seq

def print_found_goal(population, generation, to_print=True):
    for ind in population:
        score = fitness_score(ind)
        if to_print:
            print(f'Current Generation: {generation}, Fitness Score: {score}/{sc.comb(NUM_QUEENS, 2)}', end='\r')
            #print(f'{ind}. Score: {score}')
        if score == sc.comb(NUM_QUEENS, 2):
            return True
    return False

def evolution(population):
    #select individuals to become parents
    parents = selection(population)
    #recombination. Create new offsprings
    offsprings = crossover(parents)
    #mutation
    offsprings = list(map(mutate, offsprings))
    #introduce top-scoring individuals from previous generation and keep top fitness individuals
    new_gen = offsprings
    for ind in population:
        new_gen.append(ind)
    new_gen = sorted(new_gen, key=lambda ind: fitness_score(ind), reverse=True)[:POPULATION_SIZE]
    return new_gen

def generate_population():
    population = []

    for individual in range(POPULATION_SIZE):
        new = [random.sample(range(NUM_QUEENS), NUM_QUEENS) for idx in range(NUM_QUEENS)] #Generate Non Duplicate Sequence
        population.append(new[0])
    
    return population

def print_board(board):
    for row in board:
        print (' '.join(row))
        log.writelines('\n')
        log.writelines(str(row))


if __name__ == "__main__":
    NUM_QUEENS = get_number_queen()
    POPULATION_SIZE = get_population_size()
    MUTATION_RATE = get_mutation_rate()
    run_limits = get_run_limit()
    refresh_rate = get_refresh_rate()

    print(f'\nNumber of Queens: {NUM_QUEENS}, Population Size: {POPULATION_SIZE}, Mutation Rate: {MUTATION_RATE}')
    print('\n')

    population = generate_population()
        
    while not print_found_goal(population, generation):
        population = evolution(population)
        generation += 1
        if int(generation % refresh_rate)==1:
            population = generate_population()
            print('\nRefreshing the population')
        if generation > run_limits:
            print('\n')
            print('Thought Unlikely, but it seems that the GA is stuck at some local point. Please try restart the program or change the run limits')
            break
    
    result = population[0] #Pulling out result
    human_output =  [x+1 for x in result] #Since Python counts from 0, This line of code add 1 to make it easier for human to understand
    to_output_file = f'The Final solution is {human_output}'
    print('\n')
    print(to_output_file)
    print('\n')

    board = [] #Building Visualize Board

    for x in range(NUM_QUEENS):
        board.append(["X"] * NUM_QUEENS)

    for i in range(NUM_QUEENS):
        for j in range(NUM_QUEENS):
            if result[i] == j:
                board[i][j] = "Q"
    
    log.writelines(str(to_output_file))
    log.writelines('\n\nBoard Configuration is Visualized Below \n')
    print_board(board)
    print('\n')
    log.close()

input('Press Enter to Exit')