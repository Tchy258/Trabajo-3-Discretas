import math

#La clase cola se usa para el algoritmo BFS, encola los nodos a visitar
class cola:
    def __init__(self):
        self.cola=[]
    def estaVacio(self):
        if len(self.cola)==0:
            return True
        else:
            return False
    def encolar(self,nodo):
        self.cola.append(nodo)
    def desencolar(self):
        return self.cola.pop(0)


#La clase grafo, contiene los nodos
class Grafo:
    def __init__(self,n):
        self.nodos=[None]*(n+1)
        for i in range(0,n+1):
            self.nodos[i]=Nodo(i)

#La clase Nodo es un vertice del grafo que representa un estado con "On" interruptores en On
#También tiene la lista de adyacencia de ese nodo que indica cuales son sus vecinos, es decir, a cuales nodos
#puedo llegar aplicando k movimientos
class Nodo:
    def __init__(self,On):
        self.On=On
        self.adyacencia=[]
    def agregarArista(self,nodo,operacion):
        if nodo not in self.adyacencia:
            self.adyacencia.append((nodo,operacion))
            #Operacion es una 2-tupla, que me dice cuantos interruptores hay que prender y cuantos apagar, en ese orden


#Arma el grafo para un valor impar de k
def armarGrafo_K_Impar(n,k):
    grafo=Grafo(n) #Se instancia el grafo, de tamaño n+1
    for cantidadDeOn in range(0,n+1): #Por cada posible estado de interruptores encendidos
        for encendibles in range(math.ceil(k/2),k+1): 
            #Hay una cantidad finita de operaciones que se pueden hacer, que corresponde a prender "encendibles" interruptores
            #y apagar "apagables" interruptores
            #Por ejemplo k=3, permite las siguientes 4 operaciones (3,0) (2,1) (1,2) (0,3)
            apagables=k-encendibles
            if cantidadDeOn>=apagables and cantidadDeOn<=n-encendibles and cantidadDeOn+encendibles<=n:
            #Si es posible realizar esta operacion, de prender "encendibles" interruptores y apagar "apagables"
                grafo.nodos[cantidadDeOn].agregarArista(cantidadDeOn+encendibles-apagables,(encendibles,apagables))
                #Entonces hay una arista del nodo que tiene "cantidadDeOn" interruptores encendidos con el nodo que tiene
                #"cantidadDeOn+encendibles-apagables" interruptores encendidos
                grafo.nodos[cantidadDeOn+encendibles-apagables].agregarArista(cantidadDeOn,(apagables,encendibles))
                #Y viceversa
    return grafo

def armarGrafo_K_Par(n,k):
    grafo=Grafo(n)
    for cantidadDeOn in range(0,n+1,2):
        for encendibles in range(int(k/2)+1,k+1):
            apagables=k-encendibles
            if cantidadDeOn>=apagables and cantidadDeOn<=encendibles and cantidadDeOn+encendibles<=n:
                grafo.nodos[cantidadDeOn].agregarArista(cantidadDeOn+encendibles-apagables,(encendibles,apagables))
                grafo.nodos[cantidadDeOn+encendibles-apagables].agregarArista(cantidadDeOn,(apagables,encendibles))
    return grafo

#BFS aplica el algoritmo bfs hasta llegar al nodo con 0 interruptores y registra por cuales nodos se pasó y cuanta es la distancia
def BFS(cantidadDeOn,grafo,n,distancia,anterior):
    nodosAVisitar=cola()
    #Primero se crea una cola de nodos a visitar para que el algoritmo BFS revise los vecinos de un nodo u
    visitado=[False]*(n+1)
    #En principio no se ha visitado ningún nodo
    distancia[cantidadDeOn]=0
    #La distancia del inicio al mismo inicio es 0
    visitado[cantidadDeOn]=True
    #El inicio siempre ha sido visitado
    nodosAVisitar.encolar(cantidadDeOn)
    #El primer nodo a revisar es el del inicio
    while not nodosAVisitar.estaVacio():
        #Mientras me queden nodos por revisar
        u=nodosAVisitar.desencolar()
        #Ver el nodo u que está al principio de la fila
        for i in range(len(grafo.nodos[u].adyacencia)): #Para la lista de adyacencia de este nodo u
            if not visitado[grafo.nodos[u].adyacencia[i][0]]: #Si no he visitado el siguiente nodo
                visitado[grafo.nodos[u].adyacencia[i][0]]=True #Ahora si
                distancia[grafo.nodos[u].adyacencia[i][0]]=distancia[u]+1 
                #Mi distancia a este vecino, es la que llevaba hasta el nodo u + 1
                anterior[grafo.nodos[u].adyacencia[i][0]]=u
                #Para llegar a este nodo de la lista de adyacencia de u, tuve que pasar por u
                nodosAVisitar.encolar(grafo.nodos[u].adyacencia[i][0])
                #Agrego a la cola de nodos por visitar, el siguiente vecino de u
                if (grafo.nodos[u].adyacencia[i][0]==0):
                    #Si llegue al nodo 0, ya encontré las formas de llegar
                    return

#Distancia minima con pasos, encuentra la distancia minima según lo hecho en el algoritmo BFS y
#guiandose por cuales operaciones hay que hacer de encendido y apagado, elige los interruptores pertinentes a encender y apagar
def distanciaMinimaConPasos(grafo,cantidadDeOn,n,estadoInicial):
    #Al principio la distancia a cualquier nodo es infinita (n+2 porque es mayor que cualquier distancia posible)
    distancia=[n+2]*(n+1)
    #No se de cual nodo llegué para llegar al nodo i
    anterior=[-1]*(n+1)
    BFS(cantidadDeOn,grafo,n,distancia,anterior)
    #Se aplica el algoritmo BFS que encuentra las distancias, y por cuales nodos tuve que pasar
    camino=[]
    #Lista que contendrá el camino inverso, desde el nodo 0 hasta el inicial
    movimiento=0
    #Mi primer movimiento es desde el nodo 0
    camino.append(movimiento)
    listaDeOperaciones=[]
    #Lista de operaciones contiene en el orden desde el 0 al inicial, de que interruptores hay que encender y apagar
    #por lo que después se haran las operaciones opuestas para llegar del inicial al 0
    while anterior[movimiento] != -1: 
        #Mientras el nodo que estoy viendo está conectado a otro anterior (es decir, no es el inicial)
        camino.append(anterior[movimiento]) #Agrego el nodo desde el que vine para llegar al que estoy viendo
        for i in range(0,len(grafo.nodos[movimiento].adyacencia)): 
            #Buscar en la lista de adyacencia del nodo actual que operacion me lleva al nodo desde el que vine
            if grafo.nodos[movimiento].adyacencia[i][0]==anterior[movimiento]: #Cuando la encuentro
                operaciones=grafo.nodos[movimiento].adyacencia[i][1] #La guardo
                break #Dejo de buscar
        movimiento=anterior[movimiento] #El siguiente nodo que voy a ver va a ser el nodo desde el que vine
        listaDeOperaciones.append(operaciones) #Agrego la operacion que tuve que hacer para llegar a este
    #Partiendo desde el estado inicial
    estadoActual=estadoInicial
    print('La distancia más corta es: '+str(distancia[0]))
    #La distancia más corta se encontró con el algoritmo BFS
    print('El camino y los pasos son los siguientes: ')
    for i in range(len(camino)-2,-1,-1):
        print('Cantidad de interruptores encendidos: '+str(camino[i+1]))
        #camino es la lista que tiene los nodos por los que se tuvo que pasar para llegar desde 0 al inicial y este for
        #parte en el ultimo indice de este camino (es decir, desde el nodo inicial), hasta llegar al final (el nodo 0)
        print('Estado Actual: ')
        print(estadoActual)
        print('Interruptores a mover: ')
        #La listaDeOperaciones, contiene los interruptores que hay que prender y apagar para ir yendo desde el 0 al inicial
        #Por lo que si desde un nodo u tuve que apagar "a" interruptores y prender "p" interruptores para llegar
        #a un nodo v, entonces para el inverso, tengo que prender "a" y apagar "p"
        apagar=listaDeOperaciones[i][0]
        encender=listaDeOperaciones[i][1]
        print('(',end='')
        for interruptor in range(0,len(estadoActual)): #Por cada interruptor del estado actual
            if estadoActual[interruptor]=='0' and encender>0: #Si me quedan interruptores por prender y estoy viendo uno apagado
                estadoActual[interruptor]='1' #Lo prendo
                encender-=1 #Tengo uno menos que prender
                print(interruptor+1,end=' ') #Digo cual fue el que prendí
            elif estadoActual[interruptor]=='1' and apagar>0: #Si me quedan interruptores por apagar y estoy viendo uno prendido
                estadoActual[interruptor]='0' #Lo apago
                apagar-=1 #Tengo uno menos que apagar
                print(interruptor+1,end=' ') #Digo cual fue el que apagué
            if apagar==0 and encender==0: break #Si no tengo nada más que prender o apagar, dejo de revisar los interruptores
        print(')')
    print('Estado Actual:')
    print(estadoActual)


n=int(input('n? ')) #Prgunto por el n
k=int(input('k? ')) #Pregunto por el k
estados=input('estados iniciales?: ') #Pregunto los estados iniciales, donde 1 es on y 0 es off
estados=estados.split() #Convierto el string de estados a una lista
sePuedeApagar=True #En principio, es posible apagarlos todos
cantidadDeOn=0 #No se cuantos hay encendidos
for i in range(0,len(estados)): #Reviso los interruptores
    if estados[i]=='1': #Veo cuales estan encendidos
        cantidadDeOn+=1 #Y lo añado a la cuenta de interruptores encendidos
if k%2==0: #Si k es par
    if cantidadDeOn%2!=0: #Si hay una cantidad impar de interruptores encendidos
        sePuedeApagar=False #Entonces no se puede apagar
        print("No es posible apagar todos los interruptores, siempre quedará al menos 1")
    if sePuedeApagar: #Si se puede apagar, entonces hay una cantidad de par de interruptores encendidos
        grafo=armarGrafo_K_Par(n,k) #Y se arma el grafo
elif k%2!=0: #Si k impar
    grafo=armarGrafo_K_Impar(n,k) #Se arma su grafo
if sePuedeApagar: #Si puedo apagar todos los interruptores
    distanciaMinimaConPasos(grafo,cantidadDeOn,n,estados) #Busco la cantidad minima de pasos y cuales son