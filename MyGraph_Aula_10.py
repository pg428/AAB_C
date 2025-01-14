
## Graph represented as adjacency list using a dictionary
## keys are vertices
## values of the dictionary represent the list of adjacent vertices of the key node

class MyGraph:
    
    def __init__(self, g = {}):
        ''' Constructor - takes dictionary to fill the graph as input; default is empty dictionary '''
        self.graph = g    

    def print_graph(self):
        ''' Prints the content of the graph as adjacency list '''
        for v in self.graph.keys():
            print (v, " -> ", self.graph[v])

    ## get basic info

    def get_nodes(self):
        ''' Returns list of nodes in the graph '''
        return list(self.graph.keys())
        
    def get_edges(self): 
        ''' Returns edges in the graph as a list of tuples (origin, destination) '''
        edges = []
        for v in self.graph.keys():
            for d in self.graph[v]:
                edges.append((v,d)) #origem, destino
        return edges
      
    def size(self):
        ''' Returns size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())
      
    ## add nodes and edges    
    
    def add_vertex(self, v):
        ''' Add a vertex to the graph; tests if vertex exists not adding if it does '''
        if v not in self.graph.keys():
            self.graph[v] = []
        
    def add_edge(self, o, d):
        ''' Add edge to the graph; if vertices do not exist, they are added to the graph ''' 
        if o not in self.graph.keys():
            self.add_vertex(o)
        if d not in self.graph.keys():
            self.add_vertex(d)  
        if d not in self.graph[o]:
            self.graph[o].append(d)

    ## successors, predecessors, adjacent nodes
        
    def get_successors(self, v):
        return list(self.graph[v])     # needed to avoid list being overwritten of result of the function is used           
             
    def get_predecessors(self, v):
        res = []
        for k in self.graph.keys(): 
            if v in self.graph[k]: 
                res.append(k)
        return res
    
    def get_adjacents(self, v):
        suc = self.get_successors(v)
        pred = self.get_predecessors(v)
        res = pred
        for p in suc: 
            if p not in res: res.append(p)
        return res
        
    ## degrees    
    
    def out_degree(self, v):
        return len(self.graph[v])
    
    def in_degree(self, v):
        return len(self.get_predecessors(v))
        
    def degree(self, v):
        return len(self.get_adjacents(v))
        
    def all_degrees(self, deg_type = "inout"):
        ''' Computes the degree (of a given type) for all nodes.
        deg_type can be "in", "out", or "inout" '''
        degs = {}
        for v in self.graph.keys():
            if deg_type == "out" or deg_type == "inout":
                degs[v] = len(self.graph[v])
            else: degs[v] = 0
        if deg_type == "in" or deg_type == "inout":
            for v in self.graph.keys():
                for d in self.graph[v]:
                    if deg_type == "in" or v not in self.graph[d]:
                        degs[d] = degs[d] + 1
        return degs
    
    def highest_degrees(self, all_deg= None, deg_type = "inout", top= 10):
        if all_deg is None: 
            all_deg = self.all_degrees(deg_type)
        ord_deg = sorted(list(all_deg.items()), key=lambda x : x[1], reverse = True)
        return list(map(lambda x:x[0], ord_deg[:top]))
        
    
    ## topological metrics over degrees

    def mean_degree(self, deg_type = "inout"):
        degs = self.all_degrees(deg_type)
        return sum(degs.values()) / float(len(degs))
        
    def prob_degree(self, deg_type = "inout"):
        degs = self.all_degrees(deg_type)
        res = {}
        for k in degs.keys():
            if degs[k] in res.keys():
                res[degs[k]] += 1
            else:
                res[degs[k]] = 1
        for k in res.keys():
            res[k] /= float(len(degs))
        return res    
    
    
    ## BFS and DFS searches    
    
    def reachable_bfs(self, v):
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v: res.append(node)
            for elem in self.graph[node]:
                if elem not in res and elem not in l and elem != node:
                    l.append(elem)
        return res
        
    def reachable_dfs(self, v):
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v: res.append(node)
            s = 0
            for elem in self.graph[node]:
                if elem not in res and elem not in l:
                    l.insert(s, elem)
                    s += 1
        return res    
    
    def distance(self, s, d):
        if s == d: return 0
        l = [(s,0)]
        visited = [s]
        while len(l) > 0:
            node, dist = l.pop(0)
            for elem in self.graph[node]:
                if elem == d: return dist + 1
                elif elem not in visited: 
                    l.append((elem,dist+1))
                    visited.append(elem)
        return None
        
    def shortest_path(self, s, d):
        if s == d: return []
        l = [(s,[])]
        visited = [s]
        while len(l) > 0:
            node, preds = l.pop(0)
            for elem in self.graph[node]:
                if elem == d: return preds+[node,elem]
                elif elem not in visited: 
                    l.append((elem,preds+[node]))
                    visited.append(elem)
        return None
        
    def reachable_with_dist(self, s):
        res = []
        l = [(s,0)]
        while len(l) > 0:
            node, dist = l.pop(0)
            if node != s: res.append((node,dist))
            for elem in self.graph[node]:
                if not is_in_tuple_list(l,elem) and not is_in_tuple_list(res,elem): 
                    l.append((elem,dist+1))
        return res
 
    ## mean distances ignoring unreachable nodes
    def mean_distances(self):
        tot = 0
        num_reachable = 0
        for k in self.graph.keys(): 
            distsk = self.reachable_with_dist(k)
            for _, dist in distsk:
                tot += dist
            num_reachable += len(distsk)
        meandist = float(tot) / num_reachable
        n = len(self.get_nodes())
        return meandist, float(num_reachable)/((n-1)*n)  
    
    def closeness_centrality(self, node):
        dist = self.reachable_with_dist(node)
        if len(dist)==0: return 0.0
        s = 0.0
        for d in dist: s += d[1]
        return len(dist) / s
        
    
    def highest_closeness(self, top = 10): 
        cc = {}
        for k in self.graph.keys():
            cc[k] = self.closeness_centrality(k)
        ord_cl = sorted(list(cc.items()), key=lambda x : x[1], reverse = True)
        return list(map(lambda x:x[0], ord_cl[:top]))
            
    
    def betweenness_centrality(self, node):
        total_sp = 0
        sps_with_node = 0
        for s in self.graph.keys(): 
            for t in self.graph.keys(): 
                if s != t and s != node and t != node:
                    sp = self.shortest_path(s, t)
                    if sp is not None:
                        total_sp += 1
                        if node in sp: sps_with_node += 1 
        return sps_with_node / total_sp
                    
    
    ## cycles    
    def node_has_cycle (self, v):
        """Ver se a partir do nó voltamos ao nó"""
        l = [v]
        res = False
        visited = [v]
        while len(l) > 0:
            node = l.pop(0)
            for elem in self.graph[node]:
                if elem == v: return True
                elif elem not in visited: 
                    l.append(elem)
                    visited.append(elem)
        return res       
    
    def has_cycle(self):
        """Ver se o grafo em si tem um ciclo, ou seja, se começando num nó
        e correndo todos conseguimos voltar ao nó inicial"""
        res = False
        for v in self.graph.keys():
            if self.node_has_cycle(v): return True
        return res

    ## clustering
        
    def clustering_coef(self, v):
        adjs = self.get_adjacents(v)
        if len(adjs) <=1: return 0.0
        ligs = 0
        for i in adjs:
            for j in adjs:
                if i != j:
                    if j in self.graph[i] or i in self.graph[j]: 
                        ligs = ligs + 1
        return float(ligs)/(len(adjs)*(len(adjs)-1))
        
    def all_clustering_coefs(self):
        ccs = {}
        for k in self.graph.keys():
            ccs[k] = self.clustering_coef(k)
        return ccs
        
    def mean_clustering_coef(self):
        ccs = self.all_clustering_coefs()
        return sum(ccs.values()) / float(len(ccs))
            
    def mean_clustering_perdegree(self, deg_type = "inout"):
        degs = self.all_degrees(deg_type)
        ccs = self.all_clustering_coefs()
        degs_k = {}
        for k in degs.keys():
            if degs[k] in degs_k.keys(): degs_k[degs[k]].append(k)
            else: degs_k[degs[k]] = [k]
        ck = {}
        for k in degs_k.keys():
            tot = 0
            for v in degs_k[k]: tot += ccs[v]
            ck[k] = float(tot) / len(degs_k[k])
        return ck

    ## Hamiltonian

    def check_if_valid_path(self, p): #recebe o path do grafo
        if p[0] not in self.graph.keys(): # se o nó incial do nosso path não estiver no grafo
            return False #return false
        for i in range(1,len(p)): #por cada i, começando em 1 e indo até ao tamanho do path
            if p[i] not in self.graph.keys() or p[i] not in self.graph[p[i-1]]: #se o nó não estiver nas keys no grafo ou como edge do nó anterior a ela
                return False #return false porque o caminho não é válid
        return True #se passar nas condições todas dá true porque o caminho é válido
        
    def check_if_hamiltonian_path(self, p):
        if not self.check_if_valid_path(p):
            return False #se o caminho não for válido dá return de false
        to_visit = list(self.get_nodes()) #cria a lsita comos nós a visitar
        if len(p) != len(to_visit): #se o tamanho do caminiho for diferente da lista dos nós s visitar
            return False #retorna falso, porque o tamaho tem que ser o memso porque tem qeu passar por todos os nós
        for i in range(len(p)): #vai dar o indice a procurar na lista
            if p[i] in to_visit: #se o nó estiver na lsiat dos nós a visitar
                to_visit.remove(p[i]) #remover da lista o nó referente ao i em questão
            else: #se p[i] não estiver na lista dos a visitar
                return False #return false porque o nó do path não vai estar nos a visitar (pode ser poruqe já se passou nesse nó)
        if not to_visit: # = a to_visit == []
            return True #se a lista dos a visitar estiver vazia, return tru porque passou por todos exatamente uma vez
        else:
            return False #se lista não vazia é falso porque falta passar por algum
    
    def search_hamiltonian_path(self): #vê se há um caminho halmitoniano e dá logo o primeiro
        for ke in self.graph.keys(): #por cada nó no grafo
            p = self.search_hamiltonian_path_from_node(ke) #vamos procurar se existe um caminho hamiltoniano a começar nele
            if p != None: #se não for none
                return p #dá return do caminho hamiltoniano (ocorre assim que apareça 1, mesmo que haj mais vai dar return do 1º)
        return None #se p sempre none dá return de none porque não há caminho hamiltoniano
    
    def search_hamiltonian_path_from_node(self, start):
        """Criar a estrura do grafo como se fosse uma arvore de procura"""
        current = start #onde estou, inicializado com o 1º nó dado como input, ou seja, o start
        visited = {start:0} #os que já foram visitados / indice do proximo nó a explorar
        path = [start] #caminho atual
        while len(path) < len(self.get_nodes()): #enquanto o tamanho do path não for == ao nº de nós
            nxt_index = visited[current] #ir ao visited e ver o que tenho no index do curent
            #caso em que o nó é adicionado ao caminho
            if len(self.graph[current]) > nxt_index: #ver que o index do current é < que a lista de vizinhos para o current
                nxtnode = self.graph[current][nxt_index]
                visited[current] += 1 #aumenta o index do nó currente , avalia o proximo vizinho do current
                if nxtnode not in path: #se o novo nó não estiver vai ser adicionadado e depois vamos aumentar à árvore
                    path.append(nxtnode)
                    visited[nxtnode] = 0 #o indice do nxtnode vai passar a ser 0
                    current = nxtnode #o nó current vai passar a ser o nxtnode
            else:
                #Backtracking
                if len(path) > 1: 
                    rmvnode = path.pop()
                    del visited[rmvnode] #temos que remover o nó inútil porque como vamos subir para o nó anterior, isto tem que ser feito porque ele pode voltar a aparecer e ia dar asneira
                    current = path[-1] #o nosso current vai ser o nó anterior ao que nós retiramos da lista, ou seja vai ser o último valor da mesma
                else:
                    return None #quando fazemos backtraking e não há nada
        return path

    # Eulerian
    
    def check_balanced_node(self, node): #vê se o nó é balanceado, ou sejam se o nº de arcos que partem é = ao nº de arcos que chegam ao nó
        return self.in_degree(node) == self.out_degree(node)
        
    def check_balanced_graph(self): #vê se o grafo é balanceado
        for n in self.graph.keys(): #por cada nó do grafo
            if not self.check_balanced_node(n): #se o nó não é balanceado
                return False #return false
        return True #se todos são balanceados return True
    
    def check_nearly_balanced_graph(self):
        res = None, None
        for n in self.graph.keys(): #por cada nó do grafo
            indeg= self.in_degree(n) #graus de entrada
            outdeg= self.out_degree(n) #graus de saida
            if indeg - outdeg == 1 and res[1] is None: #
                res = res[0], n # dá o nó não balenceado com mais 1 entrada que saida
            elif indeg - outdeg == -1 and res[0] is None:
                res = n, res[1] #dá o nó não balanceado com mais 1 saida que entrada
            elif indeg == outdeg: #se graus iguais avança
                pass
            else:
                return None, None
        return res

    def is_connected(self):
        total = len(self.graph.keys()) - 1 #nº total de arcos que devem existir
        for v in self.graph.keys(): #por cada nó
            reachable_v = self.reachable_bfs(v) #nó atingivel é igual ao caminho para o atintigir em pesquisa em largura
            if (len(reachable_v) < total): # se o tamanho do caminho para chegar a v for menor que o nº total de arcos do grafo
                return False #retorna falso porque não estão todos conetados
        return True #se tudo conetado da true

    def eulerian_cycle(self):
        if not self.is_connected() or not self.check_balanced_graph(): #se o grafo não estiver totalmente conetado ou se não estiver balaceado
            return None #return none
        edges_visit = list(self.get_edges()) #lista de edges a visitar, par origem destino
        res = []
        while edges_visit: #enquanto houver edges a visitar
            par = edges_visit[0] #1º valor da lista de edges a visitar, vai ser o tuplo (origem, destino)
            i = 1
            if res != []:
                while par[0] not in res: #enauqnto que a origem do ciclo não estiver no res
                    par = edges_visit[i] #par vai aumentar para par origem destino seguinte
                    i = i + 1 #aqui vai para o proximo elemento da lista
            edges_visit.remove(par) #remove da lista o par já visitado para não voltar lá
            inicio, proximo = par #desconpacta o tuplo par em origem e distino como varáveis diferentes
            ciclo = [inicio, proximo] #caminho do ciclo temos o inicio, o próximo e depois vamos adicionando
            while proximo != inicio: #enquanto que o proximo for != do inicio, ou seja, enquanto não houver um ciclo
                for suce in self.graph[proximo]: #por cada sucessor do vertice proximo
                    if (proximo, suce) in edges_visit: # se o proximo e o seu sucessro estiverem nas lista a visitar
                        par = (proximo, suce) #o par vai ser redefinido como próximo e o seu sucessor
                        proximo = suce #o sucessor (suce vai passar a ser o proximo)
                        ciclo.append(proximo) #vamo dar apende ao cilco,ou seja, ao caminho do proximo que vai ter o valor de suce
                        edges_visit.remove(par) #vamos remover o par dos a visitar uma vez que já foi visitado
            if res == []: #se res é lista vazia
                res = ciclo #então res vai ser = ao ciclo 1º ciclo obtido
            else:
                #isto vai juntar os ciclos todos
                pos = res.index(ciclo[0])
                for i in range(len(ciclo)-1):
                    res.insert(pos + i + 1, ciclo[i + 1])
        return res #retorna o ciclo euleriano
      
    def eulerian_path(self):
        unb = self.check_nearly_balanced_graph() #vai ser os nós não balanceados
        if unb[0] is None or unb[1] is None: #se um deles der none
            return None #none e não há path
        self.graph[unb[1]].append(unb[0]) #adicionar ao grafo com a key do não balenceado com uma entrada a mais vamos adicionar como saida o nó com entrada a menos
        cycle = self.eulerian_cycle() #ver o ciclo com o grapho jaá alterado e balanceado
        for i in range(len(cycle)-1): #por cada i no range do tamanho do ciclo - 1
            if cycle[i] == unb[1] and cycle[i+1] ==  unb[0]: # se  a orige e destino do ciclo com o indice i for igual à orim destino dos não balanceados
                break #quebra o ciclo
        path = cycle[i+1:] + cycle[1:i+1] #o path vai ser definido de i+1 até ao fim o ciclo + desde 1 até i+1 do ciclo
        return path #retorna o path


def is_in_tuple_list(tl, val):
    res = False
    for (x,y) in tl:
        if val == x:
            return True
    return res


def test1():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    gr.print_graph()
    print (gr.get_nodes())
    print (gr.get_edges())
    

def test2():
    gr2 = MyGraph()
    gr2.add_vertex(1)
    gr2.add_vertex(2)
    gr2.add_vertex(3)
    gr2.add_vertex(4)
    
    gr2.add_edge(1,2)
    gr2.add_edge(2,3)
    gr2.add_edge(3,2)
    gr2.add_edge(3,4)
    gr2.add_edge(4,2)
    
    gr2.print_graph()
  
def test3():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    gr.print_graph()

    print (gr.get_successors(2))
    print (gr.get_predecessors(2))
    print (gr.get_adjacents(2))
    print (gr.in_degree(2))
    print (gr.out_degree(2))
    print (gr.degree(2))

def test4():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    print (gr.shortest_path(1,4))
    print (gr.shortest_path(4,3))

    print (gr.reachable_with_dist(1))
    print (gr.reachable_with_dist(3))

    
    gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
    print (gr2.shortest_path(1,5))
    print (gr2.shortest_path(2,1))

    print (gr2.reachable_with_dist(1))
    print (gr2.reachable_with_dist(5))

def test5():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    print (gr.node_has_cycle(2))
    print (gr. node_has_cycle(1))
    print (gr.has_cycle())

    gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
    print (gr2. node_has_cycle(1))
    print (gr2.has_cycle())

def test6():
    gr = MyGraph()
    gr.add_vertex(1)
    gr.add_vertex(2)
    gr.add_vertex(3)
    gr.add_vertex(4)
    gr.add_edge(1,2)
    gr.add_edge(2,3)
    gr.add_edge(3,2)
    gr.add_edge(3,4)
    gr.add_edge(4,2)
    gr.print_graph()
    print(gr.size())
    
    print (gr.get_successors(2))
    print (gr.get_predecessors(2))
    print (gr.get_adjacents(2))
    
    print (gr.in_degree(2))
    print (gr.out_degree(2))
    print (gr.degree(2))
    
    print(gr.all_degrees("inout"))
    print(gr.all_degrees("in"))
    print(gr.all_degrees("out"))
    
    gr2 = MyGraph({1:[2,3,4], 2:[5,6],3:[6,8],4:[8],5:[7],6:[],7:[],8:[]})
    print(gr2.reachable_bfs(1))
    print(gr2.reachable_dfs(1))
    
    print(gr2.distance(1,7))
    print(gr2.shortest_path(1,7))
    print(gr2.distance(1,8))
    print(gr2.shortest_path(1,8))
    print(gr2.distance(6,1))
    print(gr2.shortest_path(6,1))
    
    print(gr2.reachable_with_dist(1))
    
    print(gr.has_cycle())
    print(gr2.has_cycle())
    
    print(gr.mean_degree())
    print(gr.prob_degree())
    print(gr.mean_distances())
    print (gr.clustering_coef(1))
    print (gr.clustering_coef(2))

if __name__ == "__main__":
    #test1()
    #test2()
    #test3()
    test4()
    #test5()
    #test6()
    
    
