''' Project by Group VI on Grey Wolf Optimization (GWO)
	Prabhanshu Chauhan (2018BCSE074)
	Nistha Singh (2018BCSE073)
	Raman Kishore Singh (2018BCSE075)
'''


import random
import math


''' <------ Meta-heuristic problem independent high level algorithm ----> '''


def vec(dim):
    return [0.0 for i in range(dim)]

class FitnessModel:
    '''
        model_name    : Target Model Name (unimodal, multimodal, fix_dim_multimodal)
        _range        : Range of fitness function
    '''
    def __init__(self, fitness_function, _range):
        self.eval = fitness_function
        self.xmin = _range[0]
        self.xmax = _range[1]

 
class Wolf:
    '''
        fitness : FitnessModel object function to evaluate fitness
        dim     : dimension of the wolf position vector
    '''
    def __init__(self, fitness, dim, seed):
        self.rnd = random.Random(seed)

        self.position = vec(dim)

        for i in range(dim):
            self.position[i] = ((fitness.xmax - fitness.xmin) * self.rnd.random() + fitness.xmin)

        self.fitness = fitness.eval(self.position) 

class GWO:
    ''' 
        fitness : fitness model
        max_iter: maximum number of iteration
        N       : number of wolves/search agents.
        dim     : dimension of the position vector
    '''
    def __init__(self, fitness, max_iter, N, dim, seed):
        self.fitness = fitness
        self.max_iter = max_iter
        self.num_wolves = N
        self.dim = dim
        self.rnd = random.Random(seed)
        self.X = [ Wolf(fitness, dim, i) for i in range(num_wolves) ]
        self.alpha, self.beta, self.delta, *self.omega = self.sortAgents()
        self.a = 2


    def sortAgents(self):
        self.X = sorted(self.X, key = lambda wolf: wolf.fitness)
        return self.X

    def init_vec_A(self):
        A = vec(3)
        for i in range(3):
            A[i] = self.a * (2 * self.rnd.random() - 1)
        return A

    def init_vec_C(self):
        C = vec(3)
        for i in range(3):
            C[i] = 2 * self.rnd.random()
        return C

    def optimize(self):

        t = 0
        while t < self.max_iter:
            print("Iter = " + str(t) + " alpha fitness = %.3f" % self.alpha.fitness)

            a = 2*(1 - t/self.max_iter)

            for i in range(self.num_wolves):
                A1, A2, A3 = self.init_vec_A()
                C1, C2, C3 = self.init_vec_C()

                D_alpha = vec(self.dim)
                D_beta  = vec(self.dim)
                D_delta = vec(self.dim)
                
                for j in range(self.dim):
                    D_alpha[j] = abs(C1 * self.alpha.position[j] - self.X[i].position[j])
                    D_beta[j]  = abs(C2 * self.beta.position[j] - self.X[i].position[j])
                    D_delta[j] = abs(C3 * self.delta.position[j] - self.X[i].position[j])

                X1 = vec(self.dim)
                X2 = vec(self.dim)
                X3 = vec(self.dim)

                for j in range(self.dim):
                    X1[j] = self.alpha.position[j] - A1 * D_alpha[j]
                    X2[j] = self.beta.position[j] - A2 * D_beta[j] 
                    X3[j] = self.delta.position[j] - A3 * D_delta[j]

                Xnew = vec(self.dim)
                
                for j in range(self.dim):
                    Xnew[j] = (X1[j] + X2[j] + X3[j])/3

                fnew = self.fitness.eval(Xnew)
                if fnew < self.X[i].fitness:
                    self.X[i].position = Xnew
                    self.X[i].fitness  = fnew
                    
            self.alpha, self.beta, self.delta, *self.omega = self.sortAgents()
            
            t += 1
        return self.alpha.position

''' ----------------------------------------------------------------- '''

''' <----- Application/Problems ----->
    Provide a function (fitness) to optimise
'''


# These functions are used from "Grey Wolf Optimizer" paper by Seyedali Mirjalili

# fmin = 0
def f1(x):
    fitness_value = 0.0
    for i in range(len(x)):
        xi = x[i]
        fitness_value += (xi*xi)
    return fitness_value

# fmin = 0
def f9(x):
    fitness_value = 0.0
    for i in range(len(x)):
        xi = x[i]
        fitness_value += (xi*xi - 10 * math.cos(2*math.pi*xi) + 10)
    return fitness_value
    
# fmin = -1.0316
def f16(x):
    x1,x2 = x
    fitness_value = 4*(x1**2) - 2.1*(x1**4) + 1/3 * (x1**6) + x1*x2 - 4*(x2**2) + 4*(x2**4)
    return fitness_value

''' ----------------------------------------------------------- '''

# Driver Code

dim = 2
fitness = FitnessModel(fitness_function = f16, _range = [-5,5])

num_wolves = 50
max_iter = 100

print("num_wolves = " + str(num_wolves))
print("max_iter = " + str(max_iter))
print("\nStarting GWO algorithm\n")

optimiser = GWO(fitness, max_iter, num_wolves, dim, 0)
optimum_position = optimiser.optimize()

print("\nGWO completed\n")
print("\nBest solution found:")
print(["%.6f"%optimum_position[k] for k in range(dim)])
err = fitness.eval(optimum_position)
print("fitness of best solution = %.6f" % err)