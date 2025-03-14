import networkx as nx
import matplotlib.pyplot as plt

# Criar um grafo direcionado
G = nx.DiGraph()

# Adicionar nós (instruções)
nodes = [
    "MOV EAX, 5",
    "ADD EAX, 3",
    "MOV EBX, EAX",
    "SUB EBX, 2"
]
G.add_nodes_from(nodes)

# Adicionar arestas (dependências entre instruções)
edges = [
    ("MOV EAX, 5", "ADD EAX, 3"),
    ("ADD EAX, 3", "MOV EBX, EAX"),
    ("MOV EBX, EAX", "SUB EBX, 2")
]
G.add_edges_from(edges)

# Desenhar o grafo
plt.figure(figsize=(6, 4))
pos = nx.spring_layout(G)  # Layout do grafo
nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=10, font_weight="bold", edge_color="gray")
plt.title("Grafo de Dependência das Instruções")
plt.show()


