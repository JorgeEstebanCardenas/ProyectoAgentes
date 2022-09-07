import networkx as nx
import pandas as pd
from IPython.display import HTML
import matplotlib.pyplot as plt


def crearRutas(start,end,calles,puntos):
    rutas = pd.read_csv("csv\OliverRutasV2.csv")

    DG=nx.DiGraph()
    for row in rutas.iterrows():
        DG.add_edge(row[1]["Origen"],
                    row[1]["Destino"],
                    duration=row[1]["Costo"])

    

    

    path = list(nx.dijkstra_path(DG, source=start, target=end, weight="Costo"))

    ruta = []

    for i in range(0,len(path)-1):
        calle = (puntos[path[i]],puntos[path[i+1]])
        index = calles.index(calle)
        print(index, calle)
        ruta.append(index)

    return ruta