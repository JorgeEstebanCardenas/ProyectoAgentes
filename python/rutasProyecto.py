import networkx as nx
import pandas as pd
from IPython.display import HTML
import matplotlib.pyplot as plt


def crearRutas(start,end):
    rutas = pd.read_csv("csv\precionProyecto.csv")

    DG=nx.DiGraph()
    for row in rutas.iterrows():
        DG.add_edge(row[1]["Origen"],
                    row[1]["Destino"],
                    duration=row[1]["Costo"])



    path = list(nx.dijkstra_path(DG, source=start, target=end, weight="Costo"))

    return path