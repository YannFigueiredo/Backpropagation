# #  Aplicação de algoritmo neuroevolutivo para predição do mercado de ações da petrobras utilizando celulas de memórias
#
#
# ### Aluno:
# #### Jherson Haryson Almeida Pereira
#

# ## Metodologia
# ### Definição e Imports de blibotecas iniciais

# In[28]:


# pip install keras==2.1.5
# pip install --ignore-installed --upgrade \ https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.6.0-cp36-cp36m-linux_x86_64.whl


# In[ ]:


import random
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import math as mt
import threading

GENES = '10'
TARGET = ['NIN1', 'NIN2', 'NIN3', 'PROPB', 'PROB2', 'PROP3', 'OPT', 'EPOCS']

base = pd.read_csv("dataset/petr4-treinamento.csv")
base = base.dropna() #Remove as linhas onde há colunas com valores faltantes
base_treinamento = base.iloc[:, 1:2].values #Atribui a coluna 1 transformada em array a variável
normalizador = MinMaxScaler(feature_range=(0, 1))
base_treinamento_normalizada = normalizador.fit_transform(base_treinamento)

base_teste = pd.read_csv('dataset/petr4-teste.csv')
preco_real_teste = base_teste.iloc[:, 1:2].values

base_completa = pd.concat((base['Open'], base_teste['Open']), axis=0)

entradas = base_completa[len(base_completa) - len(base_teste)-90:].values
entradas = entradas.reshape(-1, 1)
entradas = normalizador.transform(entradas)

X_teste = []
for i in range(90, 112):
    X_teste.append(entradas[i-90:i, 0])

X_teste = np.array(X_teste)
X_teste = np.reshape(X_teste, (X_teste.shape[0], X_teste.shape[1], 1))

previsores = []
preco_real = []

for i in range(90, 1242):
    previsores.append(base_treinamento_normalizada[i-90:i, 0])
    preco_real.append(base_treinamento_normalizada[i, 0])

previsores, preco_real = np.array(previsores), np.array(preco_real)

# padrão (batch_size, timestep, column)

previsores = np.reshape(
    previsores, (previsores.shape[0], previsores.shape[1], 1))


# print(base_treinamento_normalizadda)

print('working...')


# ### Implementação do Individuo

# In[9]:


class Individual(threading.Thread):
    def __init__(self, chromosome):
        threading.Thread.__init__(self)
        self.chromosome = chromosome
        self.model = None
        self.score = None
        self.predict = None
        # if chromosome:
        #     self.fitness = self.fitness()

    def run(self):
        print("Starting " + self.name)
        self.fitness = self.calc_fitness()
        print("Exiting " + self.name)

    @classmethod
    def create_cromossomo(self):
        return [self.mutated_genes(i) for i in range(0, 8)]

    @classmethod
    def mutated_genes(self, index):
        # TARGET = ['NIN1', 'NIN2', 'NIN3', 'PROPB', 'PROB2', 'PROP3', 'OPT', 'EPOCS']
        random.seed()
        if index is 0:
            return 90 + int(random.uniform(0, 1)*20) #return 90 + int(random.uniform(0, 1)*70)
        elif index is 1 or index is 2:
            return 40 + int(random.uniform(0, 1)*20) #return 40 + int(random.uniform(0, 1)*70)
        elif index is 3 or index is 4 or index is 5:
            return random.uniform(2.5, 3.5)
        elif index is 6:
            return random.randint(0, 3)
        else:
            # return random.randint(100, 120)
            return random.randint(2, 4)

    def calc_fitness(self):
        self.score = self.get_fitness()
        return self.score

    def cross_and_mutate(self, par2): 
        child_chromosome = []  

        for gp1, gp2 in zip(self.chromosome, par2.chromosome):
            prob = random.random()  

            if prob < 0.5:
                child_chromosome.append(gp1)

            else:
                child_chromosome.append(gp2)

        if random.random() > .35:
            mutation = random.randint(0, 7)
            child_chromosome[mutation] = self.mutated_genes(mutation)

        return Individual(child_chromosome)

    def getModel(self):
        return self.model

    def get_fitness(self):
        previsoes = self.rna().predict(X_teste)
        previsoes = normalizador.inverse_transform(previsoes)
        mean = mt.fabs(preco_real_teste.mean() - previsoes.mean())
        self.predict = previsoes
        self.score = mean
        tf.keras.backend.clear_session()
        return mean

    def plot(self, generation):

        f = plt.figure()
        ax = f.add_subplot(1, 1, 1)
        ax.plot(preco_real_teste, color='green', label='Preco real')
        ax.plot(self.predict, color='red', label='Preco predito')
        ax.legend()
        # f.plot(preco_real_teste, color='green', label='Preco real')
        # f.plot(previsoes, color='red', label='Preco predito')


        plt.savefig('result/g_'+str(generation)+'_i_'+str(self.score)+'.png', format='png',
                    transparent=True, bbox_inches=None, pad_inches=0.1)
        plt.close(f)
        f.clear(True)

        file = open('result/g_'+str(generation)+'_i_'+str(self.score)+'.txt', 'w')
        file.write('predict\n\n\n'+str(self.predict)+'\n\n\n\n\nreal\n\n\n'+str(preco_real_teste)+'\n\n\n\nscore\n\n\n'+str(self.score))
        file.close()


    def rna(self):
        # [NIN1, NIN2, NIN3, PROPB, PROB2, PROP3, OPT, EPOCS]
        opt_by_chromosome = 'rmsprop' if self.chromosome[6] >= 1.5 else 'adam'

        regressor = Sequential()
        regressor.add(LSTM(units=self.chromosome[0], return_sequences=True, input_shape=(previsores.shape[1], 1)))
        regressor.add(Dropout(self.chromosome[3]))
        regressor.add(LSTM(units=self.chromosome[1], return_sequences=True))
        regressor.add(Dropout(self.chromosome[4]))
        regressor.add(LSTM(units=self.chromosome[2]))
        regressor.add(Dropout(self.chromosome[5]))
        regressor.add(Dense(units=1, activation='linear'))
        regressor.compile(optimizer=opt_by_chromosome, loss='mean_squared_error', metrics=['mean_absolute_error'])
        regressor.fit(previsores, preco_real, epochs=self.chromosome[7], batch_size=100, verbose=2)
        self.model = regressor
        return regressor



# ### Implementação do Algoritmo Genético

# In[10]:


def GeneticAlgorithm(size=10):
    generation = 1
    interations = 0
    population, fitness, bestfit, mean, std, ngeneration, sup_edge, inf_edge = [], [], [], [], [], [], [], []
    
    for i in range(size): 
        cromo = Individual.create_cromossomo()
        population.append(Individual(cromo))

    for individuo in population:
        individuo.start()

    for individuo in population:
        individuo.join()

    for i in population:
        print(i.score)

    exit()
    while (interations < 10):
        interations = interations+1
        print('Interation '+str(interations)+'...')

        x = 0
        ring_perc = []
        population = sorted(population, key=lambda x: x.score, reverse=False)
        for ind in population:
            ind.plot(interations)

        for cromo in population:
            fitness.append(cromo.score)
            ring_perc.append(x + cromo.score)
            x += cromo.score


        bestfit.append(population[0].score)
        mean.append(np.mean(fitness))
        std.append(np.std(fitness))
        sup_edge.append(mean[len(mean) - 1] + std[len(std) - 1])
        inf_edge.append(mean[len(mean) - 1] - std[len(std) - 1])

        if population[0].score <= 0.01:
            ngeneration.append(generation + 1)
            break

        new_g = [] 

        s = int((10 * size) / 100) 
        new_g.extend(population[:s])

        s = int((90 * size) / 100)

        for i in range(s):
            # prob2 = random.randint(0, 100)/100
            prob = random.randrange(0, int(ring_perc[-1]*100))/100
            apt_sum = 0
            parent1 = None

            for ind in population:
                apt_sum += ind.score
                if apt_sum >= prob:
                    parent1 = ind
                    break

            prob = random.randrange(0, int(ring_perc[-1]*100))/100
            apt_sum = 0
            parent2 = None

            for ind in population:
                apt_sum += ind.score
                if apt_sum >= prob:
                    parent2 = ind
                    break

            child = parent1.cross_and_mutate(parent2)
            new_g.append(child)


        population = new_g
        ngeneration.append(generation)
        generation += 1
        
    return bestfit, ngeneration[len(ngeneration)-1]


# ## Simulações

# In[11]:


def plotGraphConfidence(meanAgGer, supAgEdge, infAgEdge, maxAgGer, word=""):
    fig, ax = plt.subplots()
    fig.set_size_inches(18.5, 10.5)
    plt.plot(range(maxAgGer), meanAgGer, color='orange', label='Genetic Algoreithm')
    plt.fill_between(range(maxAgGer), supAgEdge, infAgEdge, color='orange', alpha=0.3)
    plt.legend()
    plt.title ('Fitness X Generations -  %s' %word)
    plt.ylabel('Fitness')
    plt.xlabel('Generations')

    plt.show()

def executeWords(WORD=""):
    global TARGET 
    TARGET = WORD
    meanAg, maxAgGer = [], 0
    auxNGenerationAg, auxBestFitnessAg = [], []

    for i in range(0, 1):
        
        bestFitnessAg, bestAgGeneration = GeneticAlgorithm(10)
        meanAg.append(bestFitnessAg)
        
        auxNGenerationAg.append(bestAgGeneration)
        auxBestFitnessAg.append(bestFitnessAg)
        
        if bestAgGeneration > maxAgGer:
            maxAgGer = bestAgGeneration
    
    for currentarray in meanAg:
        if len(currentarray) < maxAgGer:
            for i in range(maxAgGer - len(currentarray)):
                currentarray.append(currentarray[-1])

    meanAg = np.transpose(meanAg)


    stdAgGer ,meanAgGer ,supAgEdge ,infAgEdge = [], [], [], []

    for i in meanAg:
        stdAgGer.append(np.std(i))
        meanAgGer = np.append(meanAgGer, np.mean(i))

        supAgEdge.append(meanAgGer[-1] + stdAgGer[-1])
        infAgEdge.append(meanAgGer[-1] - stdAgGer[-1])

    if len(meanAgGer) < maxAgGer:
        for i in range(maxAgGer - len(meanAgGer)):
            meanAgGer = np.append(meanAgGer, meanAgGer[-1])
            supAgEdge.append(supAgEdge[-1])
            infAgEdge.append(infAgEdge[-1])

    plotGraphConfidence(meanAgGer, supAgEdge, infAgEdge, maxAgGer, word=WORD)
    return auxNGenerationAg, auxBestFitnessAg
    


# ### Intervalo de confiança

# In[12]:


nGenerationAg, bestFitnessAg = [], []

for word in (0, 1):
    print(word)
    auxNGenerationAg, auxBestFitnessAg = executeWords(word)
    nGenerationAg.append(auxNGenerationAg)
    bestFitnessAg.append(auxBestFitnessAg)


# ### Acertos por palavras

# In[5]:


def plotBarChartAcc(agAccuracy):
        fig, ax = plt.subplots()
        fig.set_size_inches(18.5, 10.5)
        plt.bar([0.25, 1.25, 2.25], agAccuracy, width=0.25, label='Genetic Algorithm', color='orange')
        plt.xticks([0.25, 1.25, 2.25],('WORD A', 'WORD B', 'WORD C'))
        plt.legend()
        plt.ylabel('hits')
        plt.title('hit percent per words')
        plt.show()

agAccuracy = []

for index in range(0, 1):
    agHit = 0

    for i in range(10):
        if bestFitnessAg[index][i][0] <= 0.02:
            agHit += 1

    agAccuracy.append(agHit*10)

    
    
plotBarChartAcc(agAccuracy)


# ### Geração por Palavra

# In[6]:


# print(nGenerationAg) 
# print(nGenerationRw) 
# print(bestFitnessAg) 
# print(bestFitnessRw)


def plotBarChart(meanAg, stdAg, ):
        fig, ax = plt.subplots()
        fig.set_size_inches(18.5, 10.5)
        plt.bar([0.25, 1.25, 2.25], meanAg,yerr = stdAg, width=0.25, label='Genetic Algorithm', color='orange')
        plt.xticks([0.25, 1.25, 2.25],('WORD A', 'WORD B', 'WORD C'))
        plt.legend()
        plt.ylabel('Mean of generations')
        plt.title('Mean of generations per words')
        plt.show()
   
# asdasd

meanAg = [np.mean(nGenerationAg[i]) for i in range(3)]
stdAg = [np.std(nGenerationAg[i]) for i in range(3)]


plotBarChart(meanAg, stdAg)



print(' --------------------------------')
print('|----------- ACERTOS ------------|')
print('|--------------------------------|')
print('|-----------|AG = 100 /          |')
print(' --------------------------------')
print('| WORD A    |    '+str(round(agAccuracy[0]))+'%  / ')


