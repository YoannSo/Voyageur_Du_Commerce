import itertools
from operator import attrgetter
import numpy as np
import matplotlib.pyplot as plt
import random
import math
import copy


longevite = 5
nbVille = 5
population = 5
croisementParCycle = 1
cycleMax=100
nbMutation = 1

def mutation (pop):
    for i in range (nbMutation):
        tmp=random.randint(0,len(pop)-1)
        pop[tmp].muter()

def mortIndividu(pop):
    newPop = []
    for i in range (0,len(pop)):
        if (pop[i].long>0):
            newPop.append(pop[i])
    return newPop

# Arrete de notre probleme
class Noeud:
    def __init__(self, coor,name):
        self.coor = coor
        self.name=name

class Circuit:
    def __init__(self):
        self.noeuds=[]
        self.cout=0
        self.long = longevite

    def genererCircuit(self,graphe):
        self.noeuds = graphe.noeuds
        random.shuffle(self.noeuds)
        self.updateCout()

    def swapDoublon(self,graphe):
        myNewCircuit=[]
        needToUpdate=False
        for noeud in self.noeuds:
            if noeud not in myNewCircuit:
                myNewCircuit.append(noeud)
            else:
                noeudsNeeded=graphe.getAllNoeudNotInCircuit(myNewCircuit)
                if(len(noeudsNeeded)>0):
                    myNewCircuit.append(random.choice(noeudsNeeded))
                needToUpdate=True
        self.noeuds=myNewCircuit
        if needToUpdate:
            self.updateCout()
            
    def createWithNoeuds(self,noeuds):
            self.noeuds=noeuds
            self.updateCout()

    def muter(self):
        pos1 = random.randint(0,len(self.noeuds)-1)
        pos2 = random.randint(0,len(self.noeuds)-1)

        noeud1 = self.noeuds[pos1]
        noeud2 = self.noeuds[pos2]
        self.noeuds[pos1] = noeud2
        self.noeuds[pos2] = noeud1
        self.updateCout()

    
    def updateCout(self):
        newCout=0
        for i in range(len(self.noeuds)-1):
             newCout+=math.dist(self.noeuds[i].coor,self.noeuds[i+1].coor)
        newCout+=math.dist(self.noeuds[0].coor,self.noeuds[-1].coor)
        self.cout=newCout
    
    def croisement(self,circuitUseForCroisement,graphe):
        nbNoeud=len(circuitUseForCroisement.noeuds)
        randomIndex=random.randint(1,nbNoeud-1)
        tempCircuit1=self.noeuds[0:randomIndex]
        newCircuit=tempCircuit1
        for i in range(randomIndex,len(circuitUseForCroisement.noeuds)):
            addedValue=circuitUseForCroisement.noeuds[i]
            if(addedValue in newCircuit):
                addedValue=self.noeuds[i]
            newCircuit.append(circuitUseForCroisement.noeuds[i])
        myCircuitSon=Circuit()
        myCircuitSon.createWithNoeuds(newCircuit)
        myCircuitSon.swapDoublon(graphe)
        myCircuitSon.print()
        return myCircuitSon

    def plotCircuit(self):
        for i in range (len(self.noeuds)-1):
            x=[self.noeuds[i].coor[0],self.noeuds[i+1].coor[0]]
            y=[self.noeuds[i].coor[1],self.noeuds[i+1].coor[1]]
            plt.plot(x,y,marker = 'o')
        x=[self.noeuds[-1].coor[0],self.noeuds[0].coor[0]]
        y=[self.noeuds[-1].coor[1],self.noeuds[0].coor[1]]
        plt.plot(x,y,marker = 'o')
        plt.show()


        
    def print(self):
        string=""
        for i in range(len(self.noeuds)):
                string+=str(self.noeuds[i].name)+"->"
        string+=str(self.noeuds[0].name)
        string+="  cout:"+str(self.cout)
        print(string)
        
# Graphe
class Graphe:
    def __init__(self,noeuds):
        self.noeuds=noeuds
    def plot(self):
        for i in range(len(self.noeuds)):
            for j in range(i,len(self.noeuds)):                
                x=[self.noeuds[i].coor[0],self.noeuds[j].coor[0]]
                y=[self.noeuds[i].coor[1],self.noeuds[j].coor[1]]
                plt.plot(x,y,marker = 'o')                
                cout=math.dist(self.noeuds[i].coor,self.noeuds[j].coor)
        plt.show()

    def getAllNoeudNotInCircuit(self,circuit):
        result = []
        for noeud in self.noeuds:
            if noeud not in circuit:
                result.append(noeud)
        return result
            

def retirerLesPires(circuits):
    if(len(circuits)>population):
        newListCircuit=[]
        for i in range(0,population):
            val = selection_roulette(circuits)
            newListCircuit.append(val)
        return newListCircuit
    else:
        return circuits
        


def ajouterPop(circuits,myGraphe):
    manquant = len(circuits)-population
    while (manquant<0 ):
        myRandomCircuit=Circuit()
        myRandomCircuit.genererCircuit(myGraphe)
        copyOfCircuit=copy.deepcopy(myRandomCircuit)
        copyOfCircuit.updateCout()
        circuits.append(copyOfCircuit)
        manquant+=1

def verification(listCircuit):
    allPermut=list(itertools.permutations(listCircuit))
    min=allPermut[0][0].cout
    chemin=allPermut[0][0]
    for permut in allPermut:
        for circuit in permut:
            circuit.updateCout()
            if(min>circuit.cout):
                min=circuit.cout
                chemin=circuit
    return chemin

def selection_roulette(circuits):
    max = sum(1/circuit.cout for circuit in circuits)
    pick = random.uniform(0, max)
    current = 0
    for circuit in circuits:
        current += 1/circuit.cout
        if current > pick:
            return circuit


def main():
    listNoeuds=[]
    listCircuit=[]
    for i in range(nbVille):
        randX=random.randint(1,100)
        randY=random.randint(1,100)
        noeud=Noeud([randX,randY],i)
        listNoeuds.append(noeud)
    myGraphe=Graphe(listNoeuds)
    myGraphe.plot()

    # Generation des circuits
    for i in range(population):
        myRandomCircuit=Circuit()
        myRandomCircuit.genererCircuit(myGraphe)
        copyOfCircuit=copy.deepcopy(myRandomCircuit)
        copyOfCircuit.updateCout()
        listCircuit.append(copyOfCircuit)
        
    # On Mute, on Croise, On reture pire, on supprime longeivité
    for j in range(cycleMax):
        #Croisement
        """
        for i in range (0):
            parent1 = selection_roulette(listCircuit)
            parent2 = selection_roulette(listCircuit)
            if(parent1!=parent2):
                enfant = parent1.croisement(parent2,myGraphe)
                enfant.print()
                parent1.long -=1
                parent2.long -=1
                #listCircuit.append(copy.deepcopy(enfant))
        """
        mutation(listCircuit)
        listCircuit=mortIndividu(listCircuit)
        listCircuit=retirerLesPires(listCircuit)
        ajouterPop(listCircuit,myGraphe)
        
        print("-----------Epoque "+str(j)+"----------------")
        
        for x in listCircuit:
            print("---------------------------")
            x.print()
            print(x.cout)
    print("Fini")
    best = verification(listCircuit)
    best.print()
    best.plotCircuit()
if __name__ == "__main__":
    main()

