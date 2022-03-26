import random


# Parâmetros do problema

GENES = 36

# Parâmetros do AG

MAX_GERACOES = 60

# Gera um indivíduo aleatório
def geraIndividuo ():
    genes = []

    for i in range(GENES):
        genes.append(random.randint(0,1) )

    return { 'genes': genes, 'fitness':  0}

# Gera um vetor de indivíduos aleatórios
def geraPopulacao(tam_populacao):
    pop = []
    for i in range(tam_populacao):
        pop.insert(i, geraIndividuo())
    
    return pop

# Calcula a fitness de todos os indivíduos de uma população
def avaliacao (pop):
    for i in range(len(pop)):
        
        pop[i]['fitness'] = (9
            + pop[i]['genes'][1]
            *pop[i]['genes'][4]  - pop[i]['genes'][22]*pop[i]['genes'][13] + pop[i]['genes'][23]*pop[i]['genes'][3]  - pop[i]['genes'][20]*pop[i]['genes'][9]
            + pop[i]['genes'][35]*pop[i]['genes'][14] - pop[i]['genes'][10]*pop[i]['genes'][25] + pop[i]['genes'][15]*pop[i]['genes'][16] + pop[i]['genes'][2]*pop[i]['genes'][32]
            + pop[i]['genes'][27]*pop[i]['genes'][18] + pop[i]['genes'][11]*pop[i]['genes'][33] - pop[i]['genes'][30]*pop[i]['genes'][31] - pop[i]['genes'][21]*pop[i]['genes'][24]
            + pop[i]['genes'][34]*pop[i]['genes'][26] - pop[i]['genes'][28]*pop[i]['genes'][6]  + pop[i]['genes'][7]*pop[i]['genes'][12]  - pop[i]['genes'][5]*pop[i]['genes'][8]
            + pop[i]['genes'][17]*pop[i]['genes'][19] - pop[i]['genes'][0]*pop[i]['genes'][29]  + pop[i]['genes'][22]*pop[i]['genes'][3]  + pop[i]['genes'][20]*pop[i]['genes'][14]
            + pop[i]['genes'][25]*pop[i]['genes'][15] + pop[i]['genes'][30]*pop[i]['genes'][11] + pop[i]['genes'][24]*pop[i]['genes'][18] + pop[i]['genes'][6]*pop[i]['genes'][7]
            + pop[i]['genes'][8]*pop[i]['genes'][17]  + pop[i]['genes'][0]*pop[i]['genes'][32])



# Seleciona os indíviduos com o método de roleta 
def selecaoRoleta(pop):
    pares = []
    prob = []
    fitnessSoma = 0.0
    for i in range(len(pop)):
        fitnessSoma = pop[i]['fitness'] + fitnessSoma

    for i in range(len(pop)):
        prob.append(pop[i]['fitness'] / fitnessSoma)

    numeroAleatorio = random.random(0,1)

    return {'soma': fitnessSoma, 'prob': prob, 'num': numeroAleatorio}
    

def teste():
    pop = geraPopulacao(2)
    avaliacao(pop)
    sel = selecaoRoleta(pop)
    numeroAleatorio = random.random(0,1)
    return numeroAleatorio

print(teste())