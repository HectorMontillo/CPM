import networkx as nx #Libreria para manejo de grafos
from numbers import Number
import matplotlib.pyplot as plt
#Clase para un proyecto
class Proyecto():
    def __init__(self,nombre):
        self.nombre = nombre
        self.actividades = []
        self.redcpm = nx.DiGraph() 
        self.redcpm.add_node(0, data=Cpmnode(1))
        self.indexnodes = 0
        self.indexfic = 0

    def agregaractividad(self,nombre,duracion,predecesoras):
        for i in predecesoras:
            if i not in self.actividades:
                return 0
        if not isinstance(duracion, Number):
            return 0 
        actividad = Actividad(nombre,duracion,predecesoras)
        self.actividades.append(actividad)
        self.actualizarred(actividad)
        return 1

    def agregaractividadficticia(self,nodoinicio,nodofinalizacion):
        edge = (nodoinicio,nodofinalizacion)
        if( edge not in self.redcpm.edges()):
            actividad = Actividad("F"+str(self.indexfic),0,[])
            #self.actividades.append(actividad)
            self.indexfic+=1
            self.redcpm.add_edge(nodoinicio,nodofinalizacion,weight=actividad)

    def agregarnodored(self,actividad,nodoinicio):
        self.indexnodes+=1
        self.redcpm.add_node(self.indexnodes, data=Cpmnode(self.indexnodes))
        self.redcpm.add_edge(nodoinicio,self.indexnodes,weight=actividad)
        actividad.nodofinalizacion = self.indexnodes

    def actualizarred(self,actividad):
        if not actividad.predecesoras:
            self.agregarnodored(actividad,0)
        elif len(actividad.predecesoras)==1:
            self.agregarnodored(actividad,actividad.predecesoras[0].nodofinalizacion)
        else:
            nodos = [i.nodofinalizacion for i in actividad.predecesoras]
            nodos.sort()
            i = 0
            j = 1
            while(j<len(nodos)):
                nodoinicio = nodos[i]
                nodofinalizacion = nodos[j]
                if nodoinicio != nodofinalizacion:
                    self.agregaractividadficticia(nodoinicio,nodofinalizacion)
                i+=1
                j+=1
            self.agregarnodored(actividad,nodos[j-1])
    
    def DibujarRed(self):
        pos = nx.shell_layout(self.redcpm)
        edge_labels=dict([((u,v,),d['weight'])
                    for u,v,d in self.redcpm.edges(data=True)])
        nx.draw_networkx_nodes(self.redcpm,pos)
        nx.draw_networkx_labels(self.redcpm,pos)
        nx.draw_networkx_edges(self.redcpm,pos)
        nx.draw_networkx_edge_labels(self.redcpm,pos, edge_labels=edge_labels)
        plt.show()
                    

#Clase para una actividad, aristas de la red cpm
class Actividad():
    def __init__(self,nombre,duracion,predecesoras):
        self.nombre = nombre
        self.predecesoras = predecesoras
        self.duracion_m = duracion #Duracion mas probable "m"
        self.duracion_a = duracion #Duracion mas corta de la actividad "a"
        self.duracion_b = duracion #Duracion mas larga de la actividad "b"
        self.nodofinalizacion = None
        # a <= m <= b
    def __str__(self):
        return str(self.nombre)+" : "+str(self.duracion_m)

#Clase para los nodos de la red cpm
class Cpmnode():
    def __init__(self,id):
        self.id = id
        self.tiempomastemprano = 0
        self.tiempomastardio = 0
        self.nodocritico = False
        
    def __hash__(self):
        return int(self.id)


if __name__=="__main__":
    proyecto = Proyecto("Prueba")
    
    print(proyecto.agregaractividad("A",6,[]))
    print(proyecto.agregaractividad("B",9,[]))

    print(proyecto.agregaractividad("C",8,[proyecto.actividades[0],proyecto.actividades[1]]))
    print(proyecto.agregaractividad("D",7,[proyecto.actividades[0],proyecto.actividades[1]]))
    print(proyecto.agregaractividad("E",10,[proyecto.actividades[3]]))
    print(proyecto.agregaractividad("F",12,[proyecto.actividades[2],proyecto.actividades[4]]))
    print(proyecto.agregaractividad("G",14,[proyecto.actividades[2],proyecto.actividades[4]]))
    print(proyecto.agregaractividad("H",15,[proyecto.actividades[6],proyecto.actividades[5]]))
    print(proyecto.agregaractividad("I",10,[proyecto.actividades[7]]))
    print(proyecto.agregaractividad("J",12,[]))
    print(proyecto.agregaractividad("K",15,[proyecto.actividades[8],proyecto.actividades[9]]))

    print(proyecto.redcpm.nodes())
    #print(proyecto.redcpm.edges())
    '''
    for i in proyecto.redcpm.edges():
        print(str(i)+" weight: "+str(proyecto.redcpm[i[0]][i[1]]['weight']))

    '''
    proyecto.DibujarRed()
    

    
