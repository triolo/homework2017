import gensim, logging
import networkx as nx
import matplotlib.pyplot as plt

pole = ["церковь_NOUN", "кадило_NOUN", "поп_NOUN", "священник_NOUN","крест_NOUN","митра_NOUN", "подрясник_NOUN", "дар_NOUN", "тело_NOUN", "кровь_NOUN", "пономарь_NOUN", "требник_NOUN", "святцы_NOUN", "купол_NOUN", "икона_NOUN", "иконостас_NOUN", "алтарь_NOUN", "святой_NOUN","чтец_NOUN", "часы_NOUN", "ладан_NOUN", "камилавка_NOUN", "молитва_NOUN", "бог_NOUN", "ангел_NOUN", "архангел_NOUN", "сила_NOUN", "херувим_NOUN", "серафим_NOUN", "ад_NOUN", "дьявол_NOUN", "содомит_NOUN", "подлость_NOUN", "гордыня_NOUN"]

m = 'ruscorpora_upos_skipgram_300_5_2018.vec'
if m.endswith('.vec'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
elif m.endswith('.bin'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
else:
    model = gensim.models.KeyedVectors.load(m)

nodes = {}
edges = {}
for i in range(len(pole)):
    for j in range(len(pole)):
        if (pole[i] in model) and (pole[j] in model):
            if pole[i] != pole[j]:
                sim = model.similarity(pole[i], pole[j])
                nodes[i] = pole[i].strip("_NOUN")
                edges[sim] = "{}:{}".format(i,j)
                print(pole[i], i, pole[j], j, sim)
                print('\n')
        else:
            # Увы!
            print('One of the words is not present in the model')
print(nodes)
print(edges)
G = nx.Graph()
for element, key in nodes.items():
    G.add_node(element, label=key)

mass = []
for element, key in edges.items():
    if element > 0.5:
        mass = key.split(":")
        G.add_edge(int(mass[0]), int(mass[1]))

nx.write_gexf(G, 'graph_file.gexf')

print("ноды", G.nodes())
print("ребра", G.edges())

pos=nx.spring_layout(G)

# То же, но добавим ещё подписи к узлам
nx.draw_networkx_nodes(G, pos, node_color='red', node_size=10)
nx.draw_networkx_edges(G, pos, edge_color='yellow')
nx.draw_networkx_labels(G, pos, labels=nodes, font_size=8, font_family='Arial')
plt.axis('off')
plt.show()


deg = nx.degree_centrality(G)
for nodeid in sorted(deg, key=deg.get, reverse=True):
    print("центральность", nodeid)

Gc = max(nx.connected_component_subgraphs(G), key=len)

print("радиус", nx.radius(Gc))

print("коэфф. класт.", nx.average_clustering(G))
