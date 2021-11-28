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
#se puede llegar aplicando k movimientos
class Nodo:
    def __init__(self,On):
        self.On=On
        self.adyacencia=[]
    def agregarArista(self,nodo,operacion):
        if nodo not in self.adyacencia:
            self.adyacencia.append((nodo,operacion))
            #Operacion es una 2-tupla, que dice cuantos interruptores hay que prender y cuantos apagar, en ese orden


#armarGrafo_K_Impar arma el grafo para un valor impar de k
def armarGrafo_K_Impar(n,k):
    grafo=Grafo(n) #Se instancia el grafo, de tamaño n+1
    for cantidadDeOn in range(0,n+1): #Por cada posible estado de interruptores encendidos
        for encendibles in range(math.ceil(k/2),k+1): 
            #Hay una cantidad finita de operaciones que se pueden hacer, que corresponde a prender "encendibles" interruptores
            #y apagar "apagables" interruptores
            #Por ejemplo k=3, permite las siguientes 4 operaciones (3,0) (2,1) (1,2) (0,3)
            #De las cuales solo se ven las primeras 2 en cada nodo, pues las otras 2 restantes aparecen de añadir 
            #la misma arista en el segundo nodo que va en el sentido contrario
            apagables=k-encendibles
            if cantidadDeOn>=apagables and cantidadDeOn+encendibles<=n:
            #Si es posible realizar esta operacion de prender "encendibles" interruptores y apagar "apagables"
                operacion=encendibles-apagables
                vecino=cantidadDeOn+operacion
                grafo.nodos[cantidadDeOn].agregarArista(vecino,(encendibles,apagables))
                #Entonces hay una arista desde el nodo que tiene "cantidadDeOn" interruptores encendidos con el nodo que tiene
                #"cantidadDeOn+encendibles-apagables" interruptores encendidos
                grafo.nodos[vecino].agregarArista(cantidadDeOn,(apagables,encendibles))
                #Y viceversa
    return grafo

def armarGrafo_K_Par(n,k):
    grafo=Grafo(n)
    #El procedimiento es analogo al caso k impar, pero este grafo tendrá 2 componentes conexas, de las cuales solo interesa
    #la que contiene todos los nodos pares, no se gasta tiempo en conectar los impares, pues no se necesitan para resolver
    #el problema
    for cantidadDeOn in range(0,n+1,2):
        for encendibles in range(int(k/2)+1,k+1):
            #Como k es par, es posible que este grafo tenga lazos, sin embargo, al solo ver las operaciones que parten desde
            #k/2 +1 interruptores a encender, se evita el caso en que encendibles=apagables y se omite el lazo de la
            #construcción del grafo
            #Por ejemplo k=4, permite las siguientes 4 operaciones (4,0) (3,1) (1,3) (0,4)
            #se omite la operacion (2,2) porque es un lazo
            apagables=k-encendibles
            if cantidadDeOn>=apagables and cantidadDeOn+encendibles<=n:
                operacion=encendibles-apagables
                vecino=cantidadDeOn+operacion
                grafo.nodos[cantidadDeOn].agregarArista(vecino,(encendibles,apagables))
                grafo.nodos[vecino].agregarArista(cantidadDeOn,(apagables,encendibles))
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
        #Mientras queden nodos por visitar
        u=nodosAVisitar.desencolar()
        #Ver el nodo "u" que está al principio de la cola
        for i in range(len(grafo.nodos[u].adyacencia)): #Para la lista de adyacencia de este nodo "u"
            if not visitado[grafo.nodos[u].adyacencia[i][0]]: #Si no se ha visitado el siguiente nodo
                visitado[grafo.nodos[u].adyacencia[i][0]]=True #Ahora si se visitó
                distancia[grafo.nodos[u].adyacencia[i][0]]=distancia[u]+1 
                #La distancia a este vecino desde el nodo origen, es la distancia que había desde el origen
                #hasta el nodo "u" más 1
                anterior[grafo.nodos[u].adyacencia[i][0]]=u
                #Para llegar a este nodo de la lista de adyacencia de "u", hay que pasar por "u"
                nodosAVisitar.encolar(grafo.nodos[u].adyacencia[i][0])
                #Se agrega el siguiente vecino de u a la cola de nodos por visitar
                if (grafo.nodos[u].adyacencia[i][0]==0):
                    #Si se llegó al nodo 0, ya se encontró la forma más corta de llegar a él
                    return

#distanciaMinimaConPasos, encuentra la distancia minima según lo hecho en el algoritmo BFS y
#guiandose por cuales operaciones hay que hacer de encendido y apagado, elige los interruptores pertinentes a encender y apagar
def distanciaMinimaConPasos(grafo,cantidadDeOn,n,estadoInicial):
    #Al principio la distancia a cualquier nodo es "infinita" (n+2 porque es mayor que cualquier distancia posible)
    distancia=[n+2]*(n+1)
    #Inicialmente no se sabe por cual nodo "anterior[u]" hay que pasar para llegar al nodo u
    anterior=[-1]*(n+1)
    BFS(cantidadDeOn,grafo,n,distancia,anterior)
    #Se aplica el algoritmo BFS que encuentra las distancias, y por cuales nodos hay que pasar para llegar a 0
    camino=[]
    #Lista que contendrá el camino inverso, desde el nodo 0 hasta el inicial
    movimiento=0
    #El primer movimiento es desde el nodo 0
    camino.append(movimiento)
    #Se agrega el 0 al camino a seguir para llegar al nodo inicial
    listaDeOperaciones=[]
    #Lista de operaciones contiene en el orden de que interruptores hay que encender y apagar para ir desde el 0 al inicial
    #por lo que después se haran las operaciones opuestas para llegar del inicial al 0
    while anterior[movimiento] != -1: 
        #Mientras el nodo por el que se esta pasando ahora está conectado a otro anterior (es decir, no es el inicial)
        camino.append(anterior[movimiento]) #Se agrega al camino el nodo padre desde el que se vino para llegar al que se esta viendo ahora
        for i in range(0,len(grafo.nodos[movimiento].adyacencia)): 
            #Buscar en la lista de adyacencia del nodo actual qué operación lleva al nodo anterior
            if grafo.nodos[movimiento].adyacencia[i][0]==anterior[movimiento]: #Cuando se encuentra
                operaciones=grafo.nodos[movimiento].adyacencia[i][1] #Se guarda
                break #Se deja de buscar
        movimiento=anterior[movimiento] #El siguiente nodo que se va a ver será el nodo anterior al actual
        listaDeOperaciones.append(operaciones) #Se agrega la operacion para ir desde el nodo actual al nodo anterior
    #Partiendo desde el estado inicial
    estadoActual=estadoInicial
    print('La distancia más corta es: '+str(distancia[0]))
    #La distancia más corta al 0 se encontró con el algoritmo BFS
    print('El camino y los pasos son los siguientes: ')
    for i in range(len(camino)-2,-1,-1):
        print('Cantidad de interruptores encendidos: '+str(camino[i+1]))
        #camino es la lista que tiene los nodos por los que se tuvo que pasar para llegar desde 0 al inicial y este
        #ciclo for parte en el ultimo indice de este camino (es decir, desde el nodo inicial), hasta llegar al final (el nodo 0)
        print('Estado Actual: ')
        print(estadoActual)
        print('Interruptores a mover: ')
        #La listaDeOperaciones, contiene los interruptores que hay que prender y apagar para ir desde el nodo 0 al inicial
        #Por lo que si desde un nodo "u" se tuvo que apagar "a" interruptores y prender "p" interruptores para llegar
        #a un nodo "v", entonces para el inverso, hay que prender "a" y apagar "p"
        apagar=listaDeOperaciones[i][0]
        encender=listaDeOperaciones[i][1]
        print('(',end='')
        for interruptor in range(0,len(estadoActual)): #Por cada interruptor del estado actual
            if estadoActual[interruptor]=='0' and encender>0: #Si quedan interruptores por prender y se está viendo uno apagado
                estadoActual[interruptor]='1' #Se prende
                encender-=1 #Queda uno menos que prender
                print(interruptor+1,end=' ') #Se printea el indice del interruptor que se encendió
            elif estadoActual[interruptor]=='1' and apagar>0: #Si quedan interruptores por apagar y se está viendo uno prendido
                estadoActual[interruptor]='0' #Se apaga
                apagar-=1 #Queda uno menos que apagar
                print(interruptor+1,end=' ') #Se printea el indice del interruptor que se apagó
            if apagar==0 and encender==0: break #Si no queda nada más que prender o apagar, se dejan de revisar los interruptores
        print(')')
    print('Estado Actual:')
    print(estadoActual)


n=int(input('n? ')) #Se pide el n
k=int(input('k? ')) #Se pide el k
estados=input('estados iniciales?: ') #Se piden los estados iniciales donde 1 es on y 0 es off, separados por espacios
estados=estados.split() #Se convierte el string de estados iniciales a una lista
sePuedeApagar=True #Se asume que es posible apagarlos todos
cantidadDeOn=0 #Inicialmente no se sabe cuantos hay encendidos
for i in range(0,len(estados)): #Se revisan los interruptores
    if estados[i]=='1': #Si el interruptor en la posición "i" está encendido
        cantidadDeOn+=1 #Se añade a la cuenta de interruptores encendidos
if k%2==0: #Si k es par
    if cantidadDeOn%2!=0: #Si hay una cantidad impar de interruptores encendidos
        sePuedeApagar=False #Entonces no se puede apagar
        print("No es posible apagar todos los interruptores, siempre quedará al menos 1 encendido")
    if sePuedeApagar: #Si se puede apagar, entonces hay una cantidad par de interruptores encendidos
        grafo=armarGrafo_K_Par(n,k) #Se arma el grafo
elif k%2!=0: #Si k es impar
    grafo=armarGrafo_K_Impar(n,k) #Se arma su grafo
if sePuedeApagar: #Si se pueden apagar todos los interruptores
    distanciaMinimaConPasos(grafo,cantidadDeOn,n,estados) #Se busca la cantidad minima de pasos y cuales pasos son
