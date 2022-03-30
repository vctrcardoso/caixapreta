import random
import matplotlib.pyplot as plt
from tqdm import tqdm


# Parâmetros do problema

GENES = 36

# Parâmetros do AG

MAX_GERACOES = 60
TAM_POPULACAO = 10
PROB_CRUZAMENTO = 0.93
PROB_MUTACAO = 0.07

# Gera um indivíduo aleatório
def geraIndividuo ():
    genes = []

    for i in range(GENES):
        genes.append(random.randint(0,1) )

    return { 'genes': genes, 'fitness':  0}

# Gera um vetor de indivíduos aleatórios
def geraPopulacao (tam_populacao):
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

# Faz o sorteio de um indice
def giraRoleta(soma, roleta):
    numAleatorio = random.randrange(0, soma)
    for i in range(len(roleta)):
        if(i == 0):
            if(numAleatorio < roleta[i]):
                idxSorteado = i
        else:
            if(numAleatorio >= roleta[i-1] and numAleatorio < roleta[i]):
                idxSorteado = i
    return idxSorteado

# Seleciona os indíviduos com o método de roleta 
def selecaoRoleta (pop):
    pares = []
    roleta = []
    soma = 0

    for i in range(len(pop)):
        if i == 0:
            roleta.insert(i, pop[i]['fitness'])
            soma = pop[i]['fitness']
        else:
            soma = pop[i]['fitness'] + soma
            roleta.insert(i, soma)

    for i in range(len(pop)):
        
        idx_ind1 = giraRoleta(soma, roleta)
        idx_ind2 = giraRoleta(soma, roleta)
        if(idx_ind2 == idx_ind1):
            idx_ind2 = giraRoleta(soma, roleta)
            if(idx_ind2 == idx_ind1):
                idx_ind2 = idx_ind1 + 1
        
        pares.append({'ind1': pop[idx_ind1], 'ind2': pop[idx_ind2]})


    return pares

# Seleciona o indivíduo mais forte entre 2 indivíduos aleatórios
def duelo (pop):
    ind1 = random.randrange(0, len(pop))
    ind2 = random.randrange(0, len(pop))

    if ind1 == ind2:
        ind2 = random.randrange(0, len(pop))

    if pop[ind1]['fitness'] > pop[ind2]['fitness']:
        indVencedor = ind1
    else:
        indVencedor = ind2

    return indVencedor

# Seleciona os indivíduos pelo método de Torneio
def selecaoTorneio(pop):
    pares = []
    for i in range(len(pop)):
        idx_ind1 = duelo(pop)
        idx_ind2 = duelo(pop)
        if idx_ind2 == idx_ind1:
            idx_ind2 = duelo(pop)
            if idx_ind2 == idx_ind1:
                idx_ind2 = idx_ind1 + 1
    
        pares.insert(i, {'ind1': pop[idx_ind1], 'ind2': pop[idx_ind2]})

    return pares

# Cruzamento entre 2 indivíduos utilizando 1 ponto de corte
def cruzamentoUmponto(ind1, ind2):
    genes_filho = []
    
    pc = random.randint(0, GENES-1)

    for i in range(GENES):
        if i <= pc:
            genes_filho.append( ind1['genes'][i])
        else:
            genes_filho.append( ind2['genes'][i])

    filho = {
        'genes': genes_filho, 
        'fitness': 0
    }
    return filho

# Cruzamento entre 2 indivíduos utilizando 2 pontos de corte
def cruzamentoDoispontos(ind1, ind2):
    genes_filho = []
    
    pc1 = random.randint(0, GENES-1)
    pc2 = random.randint(pc1, GENES-1)

    for i in range(GENES):
        if i <= pc1:
            genes_filho.append(ind1['genes'][i])
        elif i > pc1 and i <= pc2:
            genes_filho.append(ind2['genes'][i])
        else:
            genes_filho.append(ind1['genes'][i])

    filho = {
        'genes': genes_filho, 
        'fitness': 0
    }
    return filho

# Realiza mutacao por escolha aleatória de um bit
def mutacao(ind):
    geneAleatorio = random.randint(0, GENES-1)
    indMutado = {
        'genes': ind['genes'].copy(),
        'fitness': 0
    }
    if indMutado['genes'][geneAleatorio] == 0:
        indMutado['genes'][geneAleatorio] = 1
    else:
        indMutado['genes'][geneAleatorio] = 0

    return indMutado


 # Aplica os operadores genéticos de cruzamento e mutação utilizando o vetor de pares.

def operadoresGeneticos(pares, opCruzamento):
    pop_nova = []

    for par in pares:
        ind1 = par['ind1']
        ind2 = par['ind2']

        probCruzamento = random.random()
        probMutacao = random.random()
        
        if probCruzamento <= PROB_CRUZAMENTO:
            if opCruzamento == 1:
                filho = cruzamentoUmponto(ind1, ind2)
            else:
                filho = cruzamentoDoispontos(ind1, ind2)
        elif probCruzamento < 0.5:
            filho = ind1
        else:
            filho = ind2

        if probMutacao <= PROB_MUTACAO:
            filho = mutacao(filho)
    

        pop_nova.append(filho)

    return pop_nova


# Aplica o elitismo de um elemento.

def elitismo(pop_antiga, pop_nova):
    melhorElemento = 0
    for i in range(len(pop_antiga)):
        if pop_antiga[i]['fitness'] > pop_antiga[melhorElemento]['fitness']:
            melhorElemento = i
    
    pop_nova[0] = pop_antiga[melhorElemento]


# Calcula a media de Fitness de uma populacao
def fitnessMedio(pop):
    soma = 0
    for ind in pop:
        soma = ind['fitness'] + soma

    media = soma / len(pop)

    return media

# Seleciona o melhor elemento da populacao
def melhorElemento(pop):
    melhorElemento = 0
    for i in range(len(pop)):
        if pop[i]['fitness'] > pop[melhorElemento]['fitness']:
            melhorElemento = i

    return pop[i]['fitness']
            

# LOOP principal do AG


def main():

    print ('MENU DE CONFIGURAÇÃO DO SISTEMA \n')
    print ('Defina a quantidade de indivíduos da população: ')
    TAM_POPULACAO = int(input('Resposta: '))
    print ('Escolha o tipo de seleção que deseja utilizar: (1) Roleta (2) Torneio')
    Op_Selecao = int(input('Resposta: '))
    print ('Escolha o tipo de cruzamento que deseja utilizar: (1) 1 ponto de corte (2) 2 pontos de corte')
    Op_Cruzamento = (input('Resposta: '))
    print ('Defina probabilidade de mutação que deseja utilizar: (de 1 a 100)')
    PROB_MUTACAO = float(input('Resposta: '))
    print ('Defina a probabilidade de cruzamento: (de 1 a 100)')
    PROB_CRUZAMENTO = float(input('Resposta: '))
    print ('Deseja utilizar o elitismo no algoritmo: (1) Sim (2) Não')
    Op_Elitismo = int(input('Resposta: '))
    print ('Defina a quantidade de gerações: ')
    MAX_GERACOES = int(input('Resposta: '))

    PROB_MUTACAO = PROB_MUTACAO / 100
    PROB_CRUZAMENTO = PROB_CRUZAMENTO / 100


    Populacao = geraPopulacao(TAM_POPULACAO)
    avaliacao(Populacao)
    geracao = 0
    xMedia = []
    yMedia = []
    xMelhorInd = []
    yMelhorInd = []
    xSolucaoOtima = []
    ySolucaoOtima = []
    with tqdm(total=MAX_GERACOES) as geracoes:
        for geracao in range(MAX_GERACOES):

            geracoes.update(1)

            # print("Geração: ", geracao)

            # print("Melhor elemento >>>", melhorElemento(Populacao))
            # print("Media da populacao >>>", fitnessMedio(Populacao))
            
            if Op_Selecao == 1:
                pares = selecaoRoleta(Populacao)
            else:
                pares = selecaoTorneio(Populacao)
            
            popFilha = operadoresGeneticos(pares, Op_Cruzamento)
            avaliacao(popFilha)

            if Op_Elitismo == 1:
                elitismo(Populacao, popFilha)
                Populacao = popFilha
            else:
                Populacao = popFilha

            avaliacao(Populacao)
            
            x = geracao
            y = float(fitnessMedio(Populacao))
            xInd = geracao
            yInd = float(melhorElemento(Populacao))
            xSolucaoOtima.append(geracao)
            ySolucaoOtima.append(27)

            xMedia.append(x) 
            yMedia.append(y)
            xMelhorInd.append(xInd)
            yMelhorInd.append(yInd)
            
        
            geracao = geracao + 1

    plt.figure(figsize=(5, 2.7), layout='constrained')
    plt.plot(xMedia, yMedia, label='Media das populações') 
    plt.plot(xMelhorInd, yMelhorInd, label='Melhor indivíduo da população') 
    plt.plot(xSolucaoOtima, ySolucaoOtima, label='Solução ótima conhecida')
    plt.xlabel('Gerações')
    plt.ylabel('Fitness')
    plt.title("Evolução do fitness")
    plt.legend()
    plt.show()
    
main()
