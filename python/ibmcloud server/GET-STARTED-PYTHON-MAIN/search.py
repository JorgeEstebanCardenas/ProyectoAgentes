import numpy as np
import pandas as pd
import networkx as nx

archivo = "OliverRutasV2.csv"

def crearRutas(start, end, calles, puntos):
    rutas = pd.read_csv(archivo)
    
    DG = nx.DiGraph()
    
    for row in rutas.iterrows():
        DG.add_edge(row[1]["Origen"],
                    row[1]["Destino"], 
                    Costo=row[1]["Costo"]
                    )
    
    path = list(nx.dijkstra_path(DG, source=start, target=end, weight="Costo"))

    ruta = []

    for i in range(0,len(path)-1):
        calle = (puntos[path[i]],puntos[path[i+1]])
        # print(calle)
        try:
            index = calles.index(calle)
        except ValueError:
            try:
                index = calles.index((puntos[path[i]],puntos[path[i+1]], (True), (0)))
            except ValueError:
                index = calles.index((puntos[path[i]],puntos[path[i+1]], (True), (1)))
            
            
        ruta.append(index)

    return ruta