import itertools
from operator import attrgetter
from tkinter import * 
import numpy as np
import matplotlib.pyplot as plt
import random
import math
import copy



def mutation (pop,nbMutation):
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
    def __init__(self,longevite):
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
        myCircuitSon=Circuit(self.long)
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

def retirerLesPires(circuits,population):
    if(len(circuits)>population):
        newListCircuit=[]
        for i in range(0,population):
            val = selection_roulette(circuits)
            newListCircuit.append(val)
        return newListCircuit
    else:
        return circuits
        


def ajouterPop(circuits,myGraphe,population,long):
    manquant = len(circuits)-population
    while (manquant<0 ):
        myRandomCircuit=Circuit(long)
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

def lancerJeu():
    longevite = int(longeviteTk.get())
    nbVille = int(nbVilleTk.get())
    population = int(populationTk.get())
    croisementParCycle = int(croisementParCycleTk.get())
    cycleMax=int(cycleMaxTk.get())
    nbMutation = int(nbMutationTk.get())
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
        myRandomCircuit=Circuit(longevite)
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
    
        mutation(listCircuit,nbMutation)
        listCircuit=mortIndividu(listCircuit)
        listCircuit=retirerLesPires(listCircuit,population)
        ajouterPop(listCircuit,myGraphe,population,longevite)
        
        tot=moy(listCircuit)
        listVal.append((j,tot))

        minTemp = getMin(listCircuit)
        if (minSave.cout>minTemp.cout):
            minSave = copy.deepcopy(minTemp)

    print("Fini")
    listCircuit.sort(key=attrgetter('cout'))
    
    print("MinSave:"+str(minSave.cout))

    if(nbVille<10):
        verification(listCircuit[0])
    plot_moyenne(listVal)

    minSave.print()
    minSave.plotCircuit()


window = Tk()
window.geometry(str(200)+"x"+str(300))
window.title("IA Project")



_ = Label(window, text="Longevite: (2 - 10)")
_.pack()
longeviteTk = IntVar(window)
longeviteTk.set(5)
_ = Spinbox(window, from_=2, to=10, textvariable=longeviteTk)
_.pack()

_ = Label(window, text="Nombre de ville: (5-20)")
_.pack()
nbVilleTk = IntVar(window)
nbVilleTk.set(7)
_ = Spinbox(window, from_=5, to=20, textvariable=nbVilleTk)
_.pack()

_ = Label(window, text="Taille de la population: (10-100)")
_.pack()
populationTk = IntVar(window)
populationTk.set(50)
_ = Spinbox(window, from_=10, to=100, textvariable=populationTk)
_.pack()

_ = Label(window, text="Croisement par cycle: (1-10)")
_.pack()
croisementParCycleTk = IntVar(window)
croisementParCycleTk.set(5)
_ = Spinbox(window, from_=1, to=10, textvariable=croisementParCycleTk)
_.pack()

_ = Label(window, text="Nombre de cycles: (10-1000)")
_.pack()
cycleMaxTk = IntVar(window)
cycleMaxTk.set(300)
_ = Spinbox(window, from_=10, to=1000, textvariable=cycleMaxTk)
_.pack()

_ = Label(window, text="Nombre de mutation par cycle: (1-10)")
_.pack()
nbMutationTk = IntVar(window)
nbMutationTk.set(1)
_ = Spinbox(window, from_=1, to=10, textvariable=nbMutationTk)
_.pack()



_ = Button(window, text="Lancer l'algorithme", command=lancerJeu)
_.pack()

window.mainloop()

"""
def main():
   
    
"""

