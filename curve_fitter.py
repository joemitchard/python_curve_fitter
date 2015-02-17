# Spawn population of size N
# Optimize pop:
# 	LOOP(for X)
# 		Calculate fitness:
# 			Measure of error from f(x)
# 			Keep two fitest into new population
# 		Select two from population
# 			Do one of the following mutations:
# 				Crossover
# 				Crossover + Mutation
# 				Mutation
# 				Nothing ?
# 	END


# plot 'datfile.dat'
# f(x) = candidate
# eg: f(x) = -0.059329087606217634 + -1.9652779663418278 * x + -817.426010540431 * x * x + 218.6218109979809 * x * x * x + -0.11311162727006474 * x * x * x * x
# plot f(x)


import random
import xs
import ys


MIN_RAND_RANGE = -1000
MAX_RAND_RANGE = 1000

INITIAL_POPULATION_SIZE = 1000
GENERATIONS = 100
TOURNAMENT_SIZE = 4

MUTATE_RATE = 1


class Candidate:
    def __init__(self):
        self.a = random.uniform(MIN_RAND_RANGE, MAX_RAND_RANGE)
        self.b = random.uniform(MIN_RAND_RANGE, MAX_RAND_RANGE)
        self.c = random.uniform(MIN_RAND_RANGE, MAX_RAND_RANGE)
        self.d = random.uniform(MIN_RAND_RANGE, MAX_RAND_RANGE)
        self.e = random.uniform(MIN_RAND_RANGE, MAX_RAND_RANGE)
        self.f = random.uniform(MIN_RAND_RANGE, MAX_RAND_RANGE)
        self.fitness = calculate_fitness(self)
        self.list = [self.fitness, self.a, self.b, self.c, self.d, self.e, self.f]


class MutatedCandidate:
    def __init__(self, a, b, c, d, e, f):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.fitness = calculate_fitness(self)
        self.list = [self.fitness, self.a, self.b, self.c, self.d, self.e, self.f]


# FITNESS
def calculate_fitness(candidate):
    total_error = 0
    i = 0
    for X in xs.x:
        total_error += ys.y[i] - f_of_x(X, candidate.a, candidate.b, candidate.c, candidate.d, candidate.e, candidate.f)
        if not i == len(ys.y) - 1:
            i += 1
    return total_error


def f_of_x(X, a, b, c, d, e, f):
    fx = a + b*X + c*X*X + d*X*X*X + e*X*X*X*X + f*X*X*X*X*X
    return fx


# SETUP
# spawn n amount of candidates
def spawn_initial_population(n):
    while n > 0:
        candidate = Candidate()
        population.append(candidate)
        n -= 1


# candidate selection
def tournament_selection(pop):
    selected = []
    i = 0
    while i <= TOURNAMENT_SIZE:
        candidate = pop[random.randint(0, len(pop)-1)]
        selected.append(candidate)
        i += 1
        # infinite loop

    selected.sort()
    winner = selected[0]
    for candidate in selected:
        if candidate.fitness < winner.fitness:
            winner = candidate

    return winner


# mutation
def random_point_mutate(candidate):
    # picks a number between 1 and 6
    point = random.randint(1, 6)
    if point == 1:
        candidate.a += MUTATE_RATE
        candidate.list[1] += MUTATE_RATE
    elif point == 2:
        candidate.b += MUTATE_RATE
        candidate.list[2] += MUTATE_RATE
    elif point == 3:
        candidate.c += MUTATE_RATE
        candidate.list[3] += MUTATE_RATE
    elif point == 4:
        candidate.d += MUTATE_RATE
        candidate.list[4] += MUTATE_RATE
    elif point == 5:
        candidate.e += MUTATE_RATE
        candidate.list[5] += MUTATE_RATE
    else:
        candidate.f += MUTATE_RATE
        candidate.list[6] += MUTATE_RATE

    return candidate


def crossover(candidate_a, candidate_b):
    # pick crossover point and do this intelligently
    crossovered_candidate = MutatedCandidate(candidate_a.list[1], candidate_a.list[2], candidate_a.list[3],
                                             candidate_b.list[4], candidate_b.list[5], candidate_b.list[6])

    return crossovered_candidate

# MAIN
def main():
    global population
    population = []

    spawn_initial_population(INITIAL_POPULATION_SIZE)

    gen_count = 0
    # Main Loop
    while gen_count <= GENERATIONS:
        new_population = []
        i = 0

        while i <= len(population):
            cand_1 = tournament_selection(population)
            cand_2 = tournament_selection(population)

            # mutate the candidates
            # add them to the new population

            # needs a more intelligent way to draw mutate chance
            mutate_draw = random.randint(1, 2)
            if mutate_draw == 1:
                new_cand_1 = random_point_mutate(cand_1)
                new_cand_2 = random_point_mutate(cand_2)
            elif mutate_draw == 2:
                new_cand_1 = crossover(cand_1, cand_2)
                new_cand_2 = crossover(cand_1, cand_2)

            print 'mutated'

            calculate_fitness(new_cand_1)
            calculate_fitness(new_cand_2)

            new_population.append(new_cand_1)
            new_population.append(new_cand_2)

        new_population.sort()

        population = new_population

        print(str(population[0] + population[1] + population[2]))

        gen_count -= 1


main()


# pick two candidates at using proportional fitness / tournament
# crossover/mutate