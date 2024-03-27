def read_graph(file_path):
    adjacency_matrix = []
    adjacency_list = {}
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
        lines.pop(0)
        for i in range(len(lines)):
            lines[i] = lines[i].split()
            lines[i] = [int(x) for x in lines[i]]
        for line in lines:
            adjacency_matrix.append(line)
        for i in range(len(adjacency_matrix)):
            adjacency_list[i] = []
            for j in range(len(adjacency_matrix[i])):
                if adjacency_matrix[i][j] == 1:
                    adjacency_list[i].append(j)
                    

    
    return adjacency_matrix, adjacency_list
adjacency_matrix, adjacency_list = read_graph('graph_14.txt')
print("Adjacency Matrix:")
for row in adjacency_matrix:
    print(row)
print("Adjacency List:")
for vertex, neighbors in adjacency_list.items():
    print(f"{vertex}: {neighbors}")

#Grafo.txt é tudo azul
#graph_2.txt tem aresta de retorno pra dfs
#todos os outros grafos disponibilizados pelo dropbox não são direcionais. portanto sem arestas verdes e amarelas para dfs
#digrafo é o grafo direcional do slide 125 do busca_em_grafos visto em sala
visited = []
pai = {}
colors = {}

def depth_first_search(graph, start_vertex):
    global visited, pai, colors
    t = 0
    t = t + 1
    visited.append(start_vertex)
    for vertex in graph[start_vertex]:
        if vertex not in visited:
            pai[vertex] = start_vertex
            print(f"{start_vertex} -> {vertex}")
            if (start_vertex, vertex) not in colors and (vertex, start_vertex) not in colors:
                colors[(start_vertex, vertex)] = "'0,0,255'" # azul
            visited.append(vertex)
            depth_first_search(graph, vertex)
        else:
            if (start_vertex, vertex) not in colors and (vertex, start_vertex) not in colors:
                colors[(start_vertex, vertex)] = "'255,0,0'" # vermelho - de retorno

depth_first_search(adjacency_list, 0)
print("Colors:")
colors = {(min(a, b), max(a, b)): color for (a, b), color in colors.items()}
colors = dict(sorted(colors.items()))

for edge, color in colors.items():
    print(f"{edge}: {color}")
visited = []
pai = {}
colors = {}

depth_first_search(adjacency_list, 0)
print("Colors:")
colors = {(min(a, b), max(a, b)): color for (a, b), color in colors.items()}
colors = dict(sorted(colors.items()))
coresdfs = colors

for edge, color in colors.items():
    print(f"{edge}: {color}")
with open('arvore_DFS1.gdf', 'w') as file:
    file.write("nodedef>name VARCHAR,label VARCHAR\n")
with open('arvore_DFS1.gdf', 'a') as file:
    for i in range(len(adjacency_list)):
        file.write(f"{i+1},{i+1}\n")
    file.write("edgedef>node1 VARCHAR,node2 VARCHAR,directed BOOLEAN,color VARCHAR\n")
with open('arvore_DFS1.gdf', 'a') as file:
    for edge, color in coresdfs.items():
        file.write(f"{edge[0]+1},{edge[1]+1},false,{color}\n")

from collections import deque

def breadth_first_search(graph, start_vertex):
    visited = []
    pai = {}
    profundidade = {}
    colors = {}
    queue = deque([start_vertex])
    profundidade[start_vertex] = 0 

    while queue:
        vertex = queue.popleft()
        visited.append(vertex)

        for neighbor in graph[vertex]:
            if neighbor not in visited and neighbor not in queue: #condição adicional
                queue.append(neighbor)
                pai[neighbor] = vertex
                profundidade[neighbor] = profundidade[vertex] + 1
                if (vertex, neighbor) not in colors and (neighbor, vertex) not in colors:
                    colors[(vertex, neighbor)] = "'0,0,255'" # azul - pai
            else:
                if (vertex, neighbor) not in colors and (neighbor, vertex) not in colors:
                    if pai[vertex] != pai[neighbor]:
                        if profundidade[vertex] != profundidade[neighbor]:
                            colors[(vertex, neighbor)] = "'0,255,0'" # verde - tio
                        else:
                            colors[(vertex, neighbor)] = "255,255,0" # amarelo - primo
                    else:
                        colors[(vertex, neighbor)] = "'255,0,0'" # vermelho - irmão

    max_level = max(profundidade.values())
    profundidade.pop(start_vertex)

    colors = {(min(a, b), max(a, b)): color for (a, b), color in colors.items()}
    colors = dict(sorted(colors.items()))
    
    return colors, max_level, profundidade
vinicial = 0
coresbfs, level, dist = breadth_first_search(adjacency_list, vinicial)
print(coresbfs)
print(level)
print(dist)
with open('arvore_BFS1.gdf', 'w') as file:
    file.write("nodedef>name VARCHAR,label VARCHAR\n")
with open('arvore_BFS1.gdf', 'a') as file:
    for i in range(len(adjacency_list)):
        file.write(f"{i+1},{i+1}\n")
    file.write("edgedef>node1 VARCHAR,node2 VARCHAR,directed BOOLEAN,color VARCHAR\n")
with open('arvore_BFS1.gdf', 'a') as file:
    for edge, color in coresbfs.items():
        file.write(f"{edge[0]+1},{edge[1]+1},false,{color}\n")
#excentricidade de um ponto é a profundidade da arvore bfs a partir dele
#o raio de um grafo é a menor excentricidade de seus pontos
#o diametro de um grafo é a maior excentricidade de seus pontos

def raio_e_diametro(listaAdj):
    raio = 99
    diametro = 0
    soma_dist = 0
    
    for vertice in listaAdj.keys():
        colors, level, dist = breadth_first_search(listaAdj, vertice)
        if level > diametro:
            diametro = level
        if level < raio:
            raio = level
        # distancia media
        soma_dist = soma_dist + sum(dist.values())
    
    denominador_media = (len(dist.values())**2)/2
    dist_media = soma_dist/denominador_media

    return raio, diametro, dist_media

raio, diametro, dist_media = raio_e_diametro(adjacency_list)
print(f"Raio: {raio}")
print(f"Diametro: {diametro}")
print(f"dist_media: {dist_media}")