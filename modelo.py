import networkx as nx #Libreria para manejo de grafos
from numbers import Number
import matplotlib.pyplot as plt
#Clase para un proyecto
class Proyecto():
    def __init__(self,nombre):
        self.nombre = nombre
        self.actividades = []
        self.redcpm = nx.DiGraph() 
        self.redcpm.add_node(0, data=Cpmnode(0))
        self.rutacritica = set()
        self.rutacriticanodos = set()
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
        #self.Cpm('m')
        edges = self.redcpm.edges()
        pos = nx.shell_layout(self.redcpm)
        edge_labels=dict([((u,v,),d['weight'])
                    for u,v,d in self.redcpm.edges(data=True)])
        nombres =[self.redcpm[u][v]['weight'].nombre for u,v in edges]
        colors = []
        colornodos = []
        weights = []
        weightnodo = []
        for nodo in self.redcpm.nodes():
            colornodos.append('r' if nodo in self.rutacriticanodos else 'r')
            weightnodo.append(500 if nodo in self.rutacriticanodos else 300)
        
        for edge in nombres:
            colors.append('g' if edge in self.rutacritica else 'black')
            weights.append( 3 if edge in self.rutacritica else 1)
        nx.draw_networkx_nodes(self.redcpm,pos,node_color=colornodos, node_size=weightnodo)
        nx.draw_networkx_labels(self.redcpm,pos)
        nx.draw_networkx_edges(self.redcpm,pos,edge_color=colors, width=weights)
        nx.draw_networkx_edge_labels(self.redcpm,pos, edge_labels=edge_labels, )
        print("Graficando Red...")
        plt.show()
        print("Grafico cerrado...")

    def Cpm(self, tiempo):
        self.rutacritica = set()
        self.rutacriticanodos = set()
        nodos = list(self.redcpm.nodes().data())
        edges = list(self.redcpm.edges().data())
        mayor = 0
        for nodo in nodos:
            nodo[1]['data'].tiempomastemprano = 0
        for edge in edges:
            nodo1 = nodos[edge[1]][1]['data'] 
            nodo0 = nodos[edge[0]][1]['data']
            edgeval = 0
            if tiempo=='a':
                edgeval = edge[2]['weight'].duracion_a
            elif tiempo=='b':
                edgeval = edge[2]['weight'].duracion_b
            else:
                edgeval = edge[2]['weight'].duracion_m

            if nodo1.tiempomastemprano < nodo0.tiempomastemprano+edgeval:
                nodo1.tiempomastemprano = nodo0.tiempomastemprano+edgeval
                if mayor < nodo1.tiempomastemprano:
                    mayor = nodo1.tiempomastemprano
        
        edges.reverse()
        '''
        newedges=list()
        for nodo in nodos:
            if nodo[1]['data'].tiempomastemprano == mayor:
                nodo[1]['data'].nodocritico = True
                self.rutacriticanodos.add(nodo[1]['data'].id)
                for edge in edges:
                    if edge[1] == nodo[1]['data'].id:
                        newedges.append(edge)
        
        for edge in newedges:
            edges.remove(edge)
        
        newedges.extend(edges)
        print(newedges)
        '''

        
        
        nodos[-1][1]['data'].nodocritico = True
        self.rutacriticanodos.add(nodos[-1][1]['data'].id)
        for nodo in nodos:
            nodo[1]['data'].tiempomastardio = nodos[-1][1]['data'].tiempomastemprano
            
        for edge in edges:
            nodo1 = nodos[edge[0]][1]['data'] 
            nodo0 = nodos[edge[1]][1]['data']
            edgeval = 0
            if tiempo=='a':
                edgeval = edge[2]['weight'].duracion_a
            elif tiempo=='b':
                edgeval = edge[2]['weight'].duracion_b
            else:
                edgeval = edge[2]['weight'].duracion_m
            
            if nodo1.tiempomastardio > nodo0.tiempomastardio-edgeval:
                nodo1.tiempomastardio = nodo0.tiempomastardio-edgeval
                if nodo1.tiempomastardio==nodo1.tiempomastemprano:
                    nodo1.nodocritico = True
                    self.rutacritica.add(edge[2]['weight'].nombre)
                    self.rutacriticanodos.add(nodo1.id)
    def BuscarActividad(self,nombres):
        nombreslist = nombres.split()
        print(str(nombreslist)+"-----------------------------")
        actlist = []
        
        actividadesnombres = [act.nombre for act in self.actividades]
        for nombre in nombreslist:
            if not (nombre in actividadesnombres):
                 return "ERROR"
        for act in self.actividades:
            if act.nombre in nombreslist:
                actlist.append(act)

        print("Predecesoras encontradas :"+str(actlist))
        return actlist

    def DuracionProyecto(self):
        return self.redcpm.nodes().data()[self.indexnodes]['data'].tiempomastardio

    

        
        
        

                    

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
        return str(self.nombre)+" : "+str(self.duracion_m)+ " : "+str(list(act.nombre for act in self.predecesoras))

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
    
    proyecto.Cpm('m')
    for node in proyecto.redcpm.nodes().data():
        print(str(node[1]['data'].tiempomastemprano)+" :" +str(node[1]['data'].tiempomastardio)+" "+str(node[1]['data'].nodocritico))
    print(list(proyecto.rutacritica).reverse())
    print(proyecto.DuracionProyecto())
    '''
    print(list(proyecto.redcpm.nodes().data()))
    print(list(proyecto.redcpm.edges().data()))
    '''

    '''
    for i in proyecto.redcpm.edges():
        print(str(i)+" weight: "+str(proyecto.redcpm[i[0]][i[1]]['weight']))

    '''
    proyecto.DibujarRed()
    

    
