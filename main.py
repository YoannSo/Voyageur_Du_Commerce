import numpy as np
import matplotlib.pyplot as plt
import random
import math

longevite = 5
popInitial = 20
croisementParCycle = 6
cycleMax=10000
nbMutation = 3

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
    noeuds=[]
    cout=0
    long = longevite
    
    def createTest(self,graphe):
        for noeud in graphe.noeuds:
            self.noeuds.append(graphe.noeuds[1])


    def genererCircuit(self,graphe):
        self.noeuds = graphe.noeuds
        random.shuffle(self.noeuds)

    def swapDoublon(self,graphe):
        myNewCircuit=[]
        needToUpdate=False
        for noeud in self.noeuds:
            if noeud not in myNewCircuit:
                myNewCircuit.append(noeud)
            else:
                noeudsNeeded=graphe.getAllNoeudNotInCircuit(myNewCircuit)
                random_index = random.randint(0,len(noeudsNeeded)-1)
                myNewCircuit.append(noeudsNeeded[random_index])
                needToUpdate=True
        self.noeuds=myNewCircuit
        if needToUpdate:
            self.updateCout()
    def muter(self):
        pos1 = random.randint(0,len(self.noeuds)-1)
        pos2 = random.randint(0,len(self.noeuds)-1)

        noeud1 = self.noeuds[pos1]
        noeud2 = self.noeuds[pos2]
        self.noeuds[pos1] = noeud2
        self.noeuds[pos2] = noeud1
        self.updateCout()

    def estHamiltonien(self,graphe):
        if (len(self.noeuds)!=len(graphe.noeuds)):
            return False
        
        for i in range (0,len(graphe.noeuds)):
            test = False
            for j in range (0,len(self.noeuds)):
                if(graphe.noeuds[i].name == self.noeuds[j].name):
                    test = True
            if test==False :
                return False
        return True
    
    def updateCout(self):
        newCout=0
        for i in range(len(self.noeuds)-1):
             newCout+=math.dist(self.noeuds[i].coor,self.noeuds[i+1].coor)
        self.cout=newCout
    
    def print(self):
        string=""
        for i in range(len(self.noeuds)-1):
                string+=str(self.noeuds[i].name)+"->"
        string+=str(self.noeuds[-1].name)
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




listNoeuds=[]

for i in range(20):
    randX=random.randint(1,1000)
    randY=random.randint(1,1000)
    noeud=Noeud([randX,randY],i)
    listNoeuds.append(noeud)



firstGraphe=Graphe(listNoeuds)



population = []
for i in range (20):
    individu = Circuit()
    individu.genererCircuit(firstGraphe)
    individu.updateCout()
    population.append(individu)

firstGraphe.plot()

mutation(population)


