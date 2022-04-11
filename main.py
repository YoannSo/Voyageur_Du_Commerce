import itertools
from operator import attrgetter
import numpy as np
import matplotlib.pyplot as plt
import random
import math
import copy


longevite = 10
nbVille = 15
population = 100
croisementParCycle = 50
cycleMax=1000
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
        test=0
        for noeud in self.noeuds:
            if checkIfNameInCircuit(myNewCircuit,noeud.name):
                noeudsNeeded=graphe.getAllNoeudNotInCircuit(myNewCircuit)
                if(len(noeudsNeeded)>0):
                    test=random.choice(noeudsNeeded)
                    myNewCircuit.append(test)
                needToUpdate=True
            else:
                myNewCircuit.append(noeud)
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
            if checkIfNameInCircuit(circuit,noeud.name)==False:
                result.append(noeud)
        return result

def checkIfNameInCircuit(circuits,name):
    for noeud in circuits:
        if name == noeud.name:
            return True
    return False          

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

def calculNoeud(noeuds):
    newCout=0
    for i in range(len(noeuds)-1):
            newCout+=math.dist(noeuds[i].coor,noeuds[i+1].coor)
    newCout+=math.dist(noeuds[0].coor,noeuds[-1].coor)
    return newCout
def verification(circuit):
    listNoeud=circuit.noeuds
    allPermut=list(itertools.permutations(listNoeud))
    min=calculNoeud(allPermut[0])
    for permut in allPermut:
        value=calculNoeud(permut)
        if(value<min):
            min=value
    print("Valeur minale code dure: "+str(min))

def selection_roulette(circuits):
    max = sum(1/circuit.cout for circuit in circuits)
    pick = random.uniform(0, max)
    current = 0
    for circuit in circuits:
        current += 1/circuit.cout
        if current > pick:
            return circuit

def moy(listCircuit):
    min=listCircuit[0].cout
    for x in listCircuit:
        if x.cout<min:
            min=x.cout
    return min

def plot_moyenne(moy):
    for i in range(len(moy)-1):
        x=moy[i][0],moy[i+1][0]
        y=moy[i][1],moy[i+1][1]
        plt.plot(x,y)
    plt.show()

def getMin(liste):
    min=liste[0].cout
    minIndex=0
    for i in range (len(liste)):
        if liste[i].cout<min:
            min=liste[i].cout
            minIndex=i
    return liste[minIndex]

def main():
    listNoeuds=[]
    listCircuit=[]
    listVal=[]
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
    minSave=getMin(listCircuit)

    for j in range(cycleMax):
        
        #Croisement
        for i in range (croisementParCycle):
            parent1 = selection_roulette(listCircuit)
            parent2 = selection_roulette(listCircuit)
            if(parent1!=parent2):
                enfant = parent1.croisement(parent2,myGraphe)
                parent1.long -=1
                parent2.long -=1
                listCircuit.append(copy.deepcopy(enfant))
    
        mutation(listCircuit)
        listCircuit=mortIndividu(listCircuit)
        listCircuit=retirerLesPires(listCircuit)
        ajouterPop(listCircuit,myGraphe)
        
        tot=moy(listCircuit)
        listVal.append((j,tot))

        minTemp = getMin(listCircuit)
        if (minSave.cout>minTemp.cout):
            minSave = copy.deepcopy(minTemp)

    print("Fini")
    listCircuit.sort(key=attrgetter('cout'))
    
    print("MinSave:"+str(minSave.cout))
    """
    verification(listCircuit[0])
    plot_moyenne(listVal)
    """
    minSave.print()
    minSave.plotCircuit()
if __name__ == "__main__":
    main()

