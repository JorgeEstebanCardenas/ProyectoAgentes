from asyncio.windows_events import NULL
import pygame
from pygame import gfxdraw
import numpy as np
import json

from rutasProyecto import crearRutas

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
        
        # Create a pygame window
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.flip()

        # Fixed fps
        clock = pygame.time.Clock()

        # To draw text
        pygame.font.init()
        self.text_font = pygame.font.SysFont('Lucida Console', 16)

        # Draw loop
        running = True
        while running and self.step <= 2000:
            # Update simulation
            if loop: loop(self.sim)

            if sim.frame_count >10000:
                running = False

            # Draw simulation
            self.draw()

            # Update window
            pygame.display.update()
            clock.tick(self.fps)

            # Handle all events
            for event in pygame.event.get():
                # Quit program if window is closed
                if event.type == pygame.QUIT:
                    running = False
                    
            self.step += 1

        with open("anim.json","w") as outfile:
            outfile.write(json.dumps(self.sim.anim))

        pygame.quit()
        
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

    def background(self, r, g, b):
        """Fills screen with one color."""
        self.screen.fill((r, g, b))

    def line(self, start_pos, end_pos, color):
        """Draws a line."""
        gfxdraw.line(
            self.screen,
            *start_pos,
            *end_pos,
            color
        )

    def rect(self, pos, size, color):
        """Draws a rectangle."""
        gfxdraw.rectangle(self.screen, (*pos, *size), color)

    def box(self, pos, size, color):
        """Draws a rectangle."""
        gfxdraw.box(self.screen, (*pos, *size), color)

    def circle(self, pos, radius, color, filled=True):
        gfxdraw.aacircle(self.screen, *pos, radius, color)
        if filled:
            gfxdraw.filled_circle(self.screen, *pos, radius, color)

    def polygon(self, vertices, color, filled=True):
        gfxdraw.aapolygon(self.screen, vertices, color)
        if filled:
            gfxdraw.filled_polygon(self.screen, vertices, color)

    def rotated_box(self, pos, size, angle=None, cos=None, sin=None, centered=True, color=(0, 0, 255), filled=True):
        """Draws a rectangle center at *pos* with size *size* rotated anti-clockwise by *angle*."""
        x, y = pos
        l, h = size

        if angle:
            cos, sin = np.cos(angle), np.sin(angle)
        
        vertex = lambda e1, e2: (
            x + (e1*l*cos + e2*h*sin)/2,
            y + (e1*l*sin - e2*h*cos)/2
        )

        if centered:
            vertices = self.convert(
                [vertex(*e) for e in [(-1,-1), (-1, 1), (1,1), (1,-1)]]
            )
        else:
            vertices = self.convert(
                [vertex(*e) for e in [(0,-1), (0, 1), (2,1), (2,-1)]]
            )

        self.polygon(vertices, color, filled=filled)

    def rotated_rect(self, pos, size, angle=None, cos=None, sin=None, centered=True, color=(0, 0, 255)):
        self.rotated_box(pos, size, angle=angle, cos=cos, sin=sin, centered=centered, color=color, filled=False)

    def arrow(self, pos, size, angle=None, cos=None, sin=None, color=(150, 150, 190)):
        if angle:
            cos, sin = np.cos(angle), np.sin(angle)
        
        self.rotated_box(
            pos,
            size,
            cos=(cos - sin) / np.sqrt(2),
            sin=(cos + sin) / np.sqrt(2),
            color=color,
            centered=False
        )

        self.rotated_box(
            pos,
            size,
            cos=(cos + sin) / np.sqrt(2),
            sin=(sin - cos) / np.sqrt(2),
            color=color,
            centered=False
        )

    def draw_axes(self, color=(100, 100, 100)):
        x_start, y_start = self.inverse_convert(0, 0)
        x_end, y_end = self.inverse_convert(self.width, self.height)
        self.line(
            self.convert((0, y_start)),
            self.convert((0, y_end)),
            color
        )
        self.line(
            self.convert((x_start, 0)),
            self.convert((x_end, 0)),
            color
        )

    def draw_grid(self, unit=50, color=(150,150,150)):
        x_start, y_start = self.inverse_convert(0, 0)
        x_end, y_end = self.inverse_convert(self.width, self.height)

        n_x = int(x_start / unit)
        n_y = int(y_start / unit)
        m_x = int(x_end / unit)+1
        m_y = int(y_end / unit)+1

        for i in range(n_x, m_x):
            self.line(
                self.convert((unit*i, y_start)),
                self.convert((unit*i, y_end)),
                color
            )
        for i in range(n_y, m_y):
            self.line(
                self.convert((x_start, unit*i)),
                self.convert((x_end, unit*i)),
                color
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
                self.rotated_box(
                    pos, 
                    (4, 5),  
                    cos=road.angle_cos,
                    sin=road.angle_sin,
                    color=color, 
                    filled=True
                )

                
                agent = {
                    "Stepinfo": {
                        "agentId": road.sem_id - 1,
                        "stepIndex": self.step,
                        "time":self.sim.t,
                        "state": road.semaforo.estado_actual,
                        "positionX": pos[0],
                        "positionY": pos[1],
                    }
                }
                #print(agent)
                
                self.sim.anim["steps"].append(agent)

    def draw_carro(self):
        for carro in self.sim.carros:

            roadindex = carro.path[carro.road]

            longitud = self.sim.roads[roadindex].length

            sin, cos = self.sim.roads[roadindex].angle_sin, self.sim.roads[roadindex].angle_cos
            h=2
            l=4
            x = self.sim.roads[roadindex].start[0] + cos * carro.pos
            y = self.sim.roads[roadindex].start[1] + sin * carro.pos 

            self.rotated_box((x, y), (l, h), cos=cos, sin=sin, centered=True)

            alpha = 0.5
            b_max = 1
            s0 = 4
            T = 1
            ab = 2 * (carro.acc_max - b_max) ** 0.5

            if carro.vel + carro.acc * carro.step_size < 0:
                carro.pos = carro.pos - 0.5 * carro.vel * carro.vel/carro.acc
                carro.vel = 0
            else:
                carro.vel = carro.vel + carro.acc * carro.step_size
                carro.pos = carro.pos + carro.vel * carro.step_size + carro.acc * carro.step_size**2 / 2

            if self.sim.roads[roadindex].car_position(carro) > 1:
                leader = self.sim.roads[roadindex].get_leader(self.sim.roads[roadindex].car_position(carro) - 1)

                delta_x = leader.pos - carro.pos - l
                delta_v = carro.vel - leader.vel

                if delta_x == 0:
                    delta_x = self.sim.roads[roadindex].car_position(carro)-1


                alpha = (s0 + max(0, T*carro.vel + delta_v*carro.vel/ab)) / delta_x


            # carro.acc = carro.acc_max * (1 - (4/carro.vel_max)**2 - alpha**2)
            if carro.vel_max <= 0:
                carro.vel_max = 0.001

            if carro.parar == True:
            #    carro.acc = -b_max * carro.vel/carro.vel_max
                carro.acc = 0
                carro.vel = 0
            else:
                carro.acc = carro.acc_max * (1 - (carro.vel/carro.vel_max)**4 - alpha**2)



            if self.sim.roads[roadindex].sem:
                if self.sim.roads[roadindex].semaforo.estado_actual == "rojo" and carro.pos >= 13*longitud/17 and carro.pos <= longitud - 5:
                    # carro.vel = 0
                    carro.parar = True
                elif self.sim.roads[roadindex].semaforo.estado_actual == "amarillo" and carro.pos >= 2*longitud/3 and carro.pos <= longitud - 5:
                    carro.vel_max = carro.vel * 0.85

                    # carro.pos = carro.pos + carro.vel * carro.step_size + (carro.acc * carro.step_size ** 2)/2
                else:
                    carro.parar = False
                    carro.vel_max = carro.vel_max_CONST
                    # carro.vel_max = 4.25
                    # carro.pos = carro.pos + carro.vel * carro.step_size + (carro.acc * carro.step_size ** 2)/2
            # else:
                # carro.vel_max = 4.25
                # carro.pos = carro.pos + carro.vel * carro.step_size + (carro.acc * carro.step_size ** 2)/2


            if carro.pos >= longitud:
                self.sim.roads[roadindex].car_exit(carro)
                carro.road  += 1


                if carro.road > len(carro.path)-1:
                    carro.road = 0
    
                self.sim.roads[carro.path[carro.road]].car_enter(carro)
                carro.pos = 0
                carro.vel = carro.vel * 0.8
            
            
            
            agent = {
                "Stepinfo": {
                    "agentId": carro.id,
                    "stepIndex": self.step,
                    "time":self.sim.t,
                    "state": "none", #(0 if carro.vel == 0 else 1),
                    "positionX": x,
                    "positionY": y,
                }
            }
            
<<<<<<< HEAD
            #if(carro.parar and carro.id == 5):
                #print(x, " ", y)
                #print(agent)
=======
            if(carro.parar and carro.id == 5):
                #print(x, " ", y)
                print(agent)
>>>>>>> c8c1c7c7fd5d697273837472a7328d8dad5d9f5c
            self.sim.anim["steps"].append(agent)


    def draw_roads(self):
        for road in self.sim.roads:
            # Draw road background
            self.rotated_box(
                road.start,
                (road.length, 3.7),
                cos=road.angle_cos,
                sin=road.angle_sin,
                color=(180, 180, 220),
                centered=False
            )

            # Draw road lines
            # self.rotated_box(
            #     road.start,
            #     (road.length, 0.25),
            #     cos=road.angle_cos,
            #     sin=road.angle_sin,
            #     color=(0, 0, 0),
            #     centered=False
            # )

            # Draw road arrow
            if road.length > 5: 
                for i in np.arange(-0.5*road.length, 0.5*road.length, 10):
                    pos = (
                        road.start[0] + (road.length/2 + i + 3) * road.angle_cos,
                        road.start[1] + (road.length/2 + i + 3) * road.angle_sin
                    )

                    self.arrow(
                        pos,
                        (-1.25, 0.2),
                        cos=road.angle_cos,
                        sin=road.angle_sin
                    )   
            
    def draw_status(self):
        text_fps = self.text_font.render(f't={self.sim.t:.5}', False, (0, 0, 0))
        text_frc = self.text_font.render(f'n={self.sim.frame_count}', False, (0, 0, 0))
        
        self.screen.blit(text_fps, (0, 0))
        self.screen.blit(text_frc, (100, 0))

    def draw(self):
        # Fill background
        self.background(*self.bg_color)

        # Major and minor grid and axes
        self.draw_grid(10, (220,220,220))
        self.draw_grid(100, (200,200,200))
        self.draw_axes()

        self.draw_roads()
        #self.draw_vehicles()
        #self.draw_signals()

        # Draw status info
        self.draw_status()

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

            # print(road.semaforo.id)
            self.anim["agents"].append({
                "id": self.idcounter,
                "type": 1
            })
            self.idcounter += 1
        road = Road(start, end, sem, ciclo, self.idcounter)
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
        
        self.road = 0

        self.step_size = 0.5
        
        self.acc_max_CONST = 1.4

        self.acc_max = self.acc_max_CONST
        
        self.vel_max_CONST = 4.25

        self.vel_max = self.vel_max_CONST

        self.vel = 0

        self.acc = 0

        self.parar = False

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
    def __init__(self, start, end,sem, ciclo, jsonId):
        self.start = start
        
        self.end = end

        self.sem = sem

        self.vehicles = []

        self.ciclo = ciclo

        self.sem_id = jsonId

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

    def get_leader(self, position):
        if position == 0:
            return self.vehicles[0]
        else:
            return self.vehicles[position-1]

    def car_position(self,car):
        return (self.vehicles.index(car) + 1)
        
    def update(self, dt):           
        n = len(self.vehicles)
  
  
sim = Simulation()

#puntos
escala = 2


puntos = [
    (0*escala,0*escala),
    (45*escala,0*escala),
    (90*escala,0*escala),
    (0*escala,45*escala),
    (45*escala,45*escala),
    (90*escala,45*escala),
    (0*escala,90*escala),
    (45*escala,90*escala),
    (90*escala,90*escala),
    (45*escala,-30*escala),
    (45*escala,120*escala),
    (120*escala,45*escala),
    (-30*escala,45*escala),
]

calles = [
    (puntos[0],puntos[1]),
    (puntos[0],puntos[3]),
    (puntos[0],puntos[4]),
    (puntos[0],puntos[9]),
    (puntos[0],puntos[12]),
    (puntos[1],puntos[0]),
    (puntos[1],puntos[2]),
    (puntos[1],puntos[3]),
    (puntos[1],puntos[4],(True), (0)),
    (puntos[1],puntos[5]),
    (puntos[1],puntos[9]),
    (puntos[2],puntos[1]),
    (puntos[2],puntos[4]),
    (puntos[2],puntos[5]),
    (puntos[2],puntos[9]),
    (puntos[2],puntos[11]),
    (puntos[3],puntos[0]),
    (puntos[3],puntos[4],(True),(1)),
    (puntos[3],puntos[6]),
    (puntos[4],puntos[0]),
    (puntos[4],puntos[1]),
    (puntos[4],puntos[2]),
    (puntos[4],puntos[3]),
    (puntos[4],puntos[5]),
    (puntos[4],puntos[6]),
    (puntos[4],puntos[7]),
    (puntos[4],puntos[8]),
    (puntos[5],puntos[2]),
    (puntos[5],puntos[4],(True),(0)),
    (puntos[5],puntos[8]),
    (puntos[6],puntos[3]),
    (puntos[6],puntos[4]),
    (puntos[6],puntos[7]),
    (puntos[6],puntos[10]),
    (puntos[6],puntos[12]),
    (puntos[7],puntos[3]),
    (puntos[7],puntos[4],(True),(1)),
    (puntos[7],puntos[5]),
    (puntos[7],puntos[6]),
    (puntos[7],puntos[8]),
    (puntos[7],puntos[10]),
    (puntos[8],puntos[4]),
    (puntos[8],puntos[5]),
    (puntos[8],puntos[7]),
    (puntos[8],puntos[11]),
    (puntos[8],puntos[10]),
    (puntos[9],puntos[0]),
    (puntos[9],puntos[1]),
    (puntos[9],puntos[2]),
    (puntos[10],puntos[6]),
    (puntos[10],puntos[7]),
    (puntos[10],puntos[8]),
    (puntos[11],puntos[2]),
    (puntos[11],puntos[8]),
    (puntos[12],puntos[0]),
    (puntos[12],puntos[6]),
]


sim.create_roads(calles)


# ruta = crearRutas(9,8,calles,puntos)
# ruta2 = crearRutas(1,8,calles,puntos)


sim.create_cars(
   (
       crearRutas(1,8,calles,puntos),
        crearRutas(1,8,calles,puntos),
        crearRutas(3,12,calles,puntos),
        crearRutas(9,1,calles,puntos),
        crearRutas(10,0,calles,puntos),
        crearRutas(5,11,calles,puntos)
   )
)

# Start simulation
win = Window(sim)
win.offset = (-150, -90)
win.run(steps_per_update=5)