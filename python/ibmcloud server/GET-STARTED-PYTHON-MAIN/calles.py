
import numpy as np
import json
from search import dijkstra_search

class Window:
    def __init__(self, sim, config={}):
        # Simulation to draw
        self.sim = sim

        # Set default configurations
        self.set_default_config()

        # Update configurations
        for attr, val in config.items():
            setattr(self, attr, val)
        
    def set_default_config(self):
        """Set default configuration"""
        self.width = 1000
        self.height = 800
        self.bg_color = (250, 250, 250)

        self.fps = 60
        self.zoom = 2
        self.offset = (0,0)

        self.mouse_last = (0, 0)
        self.mouse_down = False
        
        self.step = 0


    def loop(self, loop=None):
        """Shows a window visualizing the simulation and runs the loop function."""


        # Draw loop
        running = True
        while running and self.step <= 2000:
            # Update simulation
            if loop: loop(self.sim)

            if self.sim.frame_count >10000:
                running = False

            self.draw()


                    
            self.step += 1

        with open("anim.json","w") as outfile:
            outfile.write(json.dumps(self.sim.anim))

        # pygame.quit()
        
    def run(self, steps_per_update=1):
        """Runs the simulation by updating in every loop."""
        def loop(sim):
            sim.run(steps_per_update)
        self.loop(loop)

    def convert(self, x, y=None):
        """Converts simulation coordinates to screen coordinates"""
        if isinstance(x, list):
            return [self.convert(e[0], e[1]) for e in x]
        if isinstance(x, tuple):
            return self.convert(*x)
        return (
            int(self.width/2 + (x + self.offset[0])*self.zoom),
            int(self.height/2 + (y + self.offset[1])*self.zoom)
        )

    def inverse_convert(self, x, y=None):
        """Converts screen coordinates to simulation coordinates"""
        if isinstance(x, list):
            return [self.convert(e[0], e[1]) for e in x]
        if isinstance(x, tuple):
            return self.convert(*x)
        return (
            int(-self.offset[0] + (x - self.width/2)/self.zoom),
            int(-self.offset[1] + (y - self.height/2)/self.zoom)
        )

 

    def draw_semaforos(self, frame_count):

        for road in self.sim.roads:

            if road.sem:
                cambio_x =(road.start[0] - road.end[0])
                cambio_y =(road.start[1] - road.end[1])

                if cambio_x > 0:
                    pos = (road.end[0] + 5, road.end[1])
                elif cambio_x < 0:
                    pos = (road.end[0] - 5, road.end[1])

                elif cambio_y > 0:
                    pos = (road.end[0], road.end[1] + 5)
                elif cambio_y < 0:
                    pos = (road.end[0], road.end[1] - 5)

                else:
                    pos = road.end



                if frame_count % 500 == 0:
                    road.semaforo.cambiar_estado()

                color = road.semaforo.colores[road.semaforo.estado_actual]


                agent = {
                    "Stepinfo": {
                        "agentId": road.semaforo.id,
                        "stepIndex": self.step,
                        "time":self.sim.t,
                        "state": road.semaforo.estado_actual, #(0 if carro.vel == 0 else 1),
                        "positionX": pos[0],
                        "positionY": pos[1],
                    }
                }
                
                self.sim.anim["steps"].append(agent)

    def draw_carro(self):
        for carro in self.sim.carros:

            roadindex = carro.road

            longitud = self.sim.roads[roadindex].length

            sin, cos = self.sim.roads[roadindex].angle_sin, self.sim.roads[roadindex].angle_cos
            h=2
            l=4
            x = self.sim.roads[roadindex].start[0] + cos * carro.pos
            y = self.sim.roads[roadindex].start[1] + sin * carro.pos 

            alpha = 0

            if self.sim.roads[roadindex].car_position(carro) > 0:
                pass
            
            carro.acc = carro.acc_max * (1 - (4/carro.vel_max)**2 - alpha**2)

            carro.vel = carro.vel + carro.acc * carro.step_size

            if self.sim.roads[roadindex].sem:
                if self.sim.roads[roadindex].semaforo.estado_actual == "rojo" and carro.pos >= longitud - 12 * self.sim.roads[roadindex].car_position(carro):
                    carro.vel = 0
                elif self.sim.roads[roadindex].semaforo.estado_actual == "amarillo" and carro.pos >= longitud/2:
                    carro.vel_max = 3.4
                    carro.pos = carro.pos + carro.vel * carro.step_size + (carro.acc * carro.step_size ** 2)/2
                else:
                    carro.vel_max = 4.25
                    carro.pos = carro.pos + carro.vel * carro.step_size + (carro.acc * carro.step_size ** 2)/2
            else:
                carro.vel_max = 4.25
                carro.pos = carro.pos + carro.vel * carro.step_size + (carro.acc * carro.step_size ** 2)/2


            if carro.pos >= longitud:
                self.sim.roads[roadindex].car_exit(carro)

                carro.road  += 1


                if carro.road > len(carro.path)-1:
                    carro.road = 0
    
                self.sim.roads[carro.road].car_enter(carro)
                carro.pos = 0
                carro.vel = carro.vel * 0.8
            
            agent = {
                "Stepinfo": {
                    "agentId": carro.id,
                    "stepIndex": self.step,
                    "time":self.sim.t,
                    "state": -1, #(0 if carro.vel == 0 else 1),
                    "positionX": x,
                    "positionY": y,
                }
            }
            
            self.sim.anim["steps"].append(agent)


    def draw_roads(self, screen):
        for road in self.sim.roads:

            if road.length > 5: 
                for i in np.arange(-0.5*road.length, 0.5*road.length, 10):
                    pos = (
                        road.start[0] + (road.length/2 + i + 3) * road.angle_cos,
                        road.start[1] + (road.length/2 + i + 3) * road.angle_sin
                    )

            


    def draw(self):
        self.draw_carro()
        
        self.draw_semaforos(self.sim.frame_count)



# ======================================================== #

from ast import Pass
from copy import deepcopy


class Simulation:
    def __init__(self, config={}):
        self.idcounter = 0
        
        #agent type 0 = car
        #agent type 1 = semaphore
        self.anim = {
            "agents":[],
            "steps":[]
        }

        # Set default configuration
        self.set_default_config()

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)

    def set_default_config(self):
        self.t = 0.0            # Time keeping
        self.frame_count = 0    # Frame count keeping
        self.dt = 1/60          # Simulation time step
        self.roads = []         # Array to store roads
        self.carros = []
        
    def create_car(self,path):
        carro = Carro(path,self.idcounter)
        self.idcounter += 1
        self.carros.append(carro)
        self.roads[path[0]].car_enter(carro)

        return carro
        
    def create_cars(self, car_list):
        for car in car_list:
            self.anim["agents"].append({
                "id": self.idcounter,
                "type": 0
            })
            self.create_car(car)

    def create_road(self, start, end, sem=False, ciclo=0):
        
        if sem:
            road = Road(start,end,sem,ciclo,self.idcounter)
            self.anim["agents"].append({
                "id": self.idcounter,
                "type": 1
            })
            self.idcounter += 1

        road = Road(start, end, sem, ciclo)
        self.roads.append(road)

        return road

    def create_roads(self, road_list):
        for road in road_list:
            self.create_road(*road)

    def update(self):
        # Update every road
        for road in self.roads:
            road.update(self.dt)

        
        # Increment time
        self.t += self.dt
        self.frame_count += 1

    def run(self, steps):
        for _ in range(steps):
            self.update()
  
  
from scipy.spatial import distance
from collections import deque

class Carro:
    def __init__(self,path,jsonId) -> None:
        self.id = jsonId

        self.pos = 0 # x
        
        self.path = path
        
        self.road = path[0]

        self.step_size = 0.5

        self.acc_max = 1.4

        self.vel_max = 4.25

        self.vel = 0

        self.acc = 0

        self.state = {
            "verde":(0,255,0),
            "amarillo":(255,255,0),
            "rojo":(255,0,0)
        }
    
    def update():
        pass

    
class semaforo: # ===================== El id del semaforo de guarda como 0 en JSON ============================= #
    def __init__(self, ciclo, pos, jsonId) -> None:
        self.id = jsonId
        
        self.estados = [["verde","amarillo","rojo","rojo"],["rojo","rojo","verde","amarillo"]]

        self.ciclo = ciclo

        self.index = 0

        self.estado_actual = self.estados[self.ciclo][self.index]

        self.pos = pos

        # self.contador = 0

        # self.cambio = 10000

        self.colores = {
            "verde":(0,255,0),
            "amarillo":(255,255,0),
            "rojo":(255,0,0)
        }

    def cambiar_estado(self):
        self.index += 1

        if self.index > len(self.estados[self.ciclo])-1:
            self.index = 0

        self.estado_actual = self.estados[self.ciclo][self.index]

class Road:
    def __init__(self, start, end,sem, ciclo, jsonId=0):
        self.start = start
        
        self.end = end

        self.sem = sem

        self.vehicles = []

        self.ciclo = ciclo

        self.init_properties()

        if self.sem:  
            self.semaforo = semaforo(self.ciclo,self.end,jsonId)

    def init_properties(self):
        self.length = distance.euclidean(self.start, self.end)
        self.angle_sin = (self.end[1]-self.start[1]) / self.length
        self.angle_cos = (self.end[0]-self.start[0]) / self.length

    def car_enter(self,car):
        self.vehicles.append(car)
        
    def car_exit(self,car):
        self.vehicles.remove(car)

    def car_position(self,car):
        return (self.vehicles.index(car) + 1)
        
    def update(self, dt):           
        n = len(self.vehicles)
  
def main_simulation():
    sim = Simulation()

    escala = 2.5
    p0 = (0*escala,0*escala)
    p1 = (45*escala,0*escala)
    p2 = (90*escala,0*escala)
    p3 = (0*escala,45*escala)
    p4 = (45*escala,45*escala)
    p5 = (90*escala,45*escala)
    #p6 = (12*escala,90*escala)
    p6 = (0*escala,90*escala)
    p7 = (45*escala,90*escala)
    p8 = (90*escala,90*escala)
    pN = (45*escala,-30*escala)
    pS = (45*escala,120*escala)
    pE = (120*escala,45*escala)
    pO = (-30*escala,45*escala)

    # Add multiple roads
    lista_caminos = [
        (p0,p1),
        (p0,p2),
        (p0,p3),
        (p4,p3),
        (p2,p5),
        (p6,p5),
        (p6,p0),
        (p4,p5),
        (p3,p5),
        (p1,p4),
        (p1,p3),
        (p2,p3),
        (p6,p2),
        (p6,p4),
        (p4,p1),
        (p0,p6),
        (p7,p8),
        (p8,p5),
        (p6,p7),
        (p4,p7),
        (p5,p6),
        (p5,p3),
        (p5,p8),
        #polares
        (p0,pN),
        (pN,p2),
        (p2,pE),
        (pE,p8),
        (p8,pS),
        (pS,p6),
        (p6,pO),
        (pO,p0)
    ]

    sim.create_roads(lista_caminos)

    sim.create_cars(
    (
        dijkstra_search(0, 7), # [0,1,2,3,4,5,6,7],
        dijkstra_search(1, 0) # [1,2,3,4,5,6,7,0]
    )
    )

    # Start simulation
    win = Window(sim)
    win.offset = (-150, -90)
    win.run(steps_per_update=5)
    
    return sim.anim
