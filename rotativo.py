'''módulo de control para encoder rotativo
   Autor: RA_GAMA, 2024.
'''

from machine import Pin
from time import ticks_ms

class Rotativo:
    '''clase de control del encoder rotativo'''
    pines:list                           # pines de lectura (CLK y DT)
    minimo:float = 0                # mínimo deseado
    maximo:float = 5               # máximo deseado
    incremento:float =1           # incremento por paso del rotativo.
    actual:float = 0                 # valor actual.
    lectura_previa:list = [0,0]   # valores de lectura.
    tiempo:int = 0                   # tiempo de activación
    
    def __init__(self,_clk:int=4,_dt:int=2,_min:float=0,_max:float=5,_incr:float=1)->None:
        '''crea un encoder rotativo con los valores predeterminados'''
        self.minimo = _min        # guarda el mínimo valor mostrado.
        self.maximo = _max      # guarda el máximo valor mostrado.
        self.incremento = _incr   # guarda el incremento por paso del rotativo.
            # declara los pines de lectura.
        self.pines = [Pin(_clk,Pin.IN,Pin.PULL_UP),Pin(_dt,Pin.IN,Pin.PULL_UP)]
        for i in range(2):           # declara las solicitudes de interrupción.
            self.pines[i].irq(trigger=Pin.IRQ_RISING|Pin.IRQ_FALLING,handler=self.lectura)
    
    def lectura(self,pin)->None:
        '''Handler de la solicitud de interrupción de cada pin'''
        elevacion = pin.value() # Indica si la interrupción es por elevación o por baja de voltaje.
        v = [0,0] #valores actuales.
        for i in range(2): v[i]=self.pines[i].value() #lee los valores (CLK y DT)
        if v[0] and v[1] and elevacion: #conclusión del paso [1 1]
            if self.lectura_previa[0] and not self.lectura_previa[1]: # [1 0]
                self.giro_izquierda()
            elif not self.lectura_previa[0] and self.lectura_previa[1]:# [0 1]
                self.giro_derecha()
        else: # paso inconcluso [0 0] | [1 0] | [0 1]
            for i in range(2): self.lectura_previa[i]=v[i] # guarda los valores leídos
    
    def giro_derecha(self)->None:
        '''evento levantado cuando se detecta un giro en el sentido de las manecillas del reloj'''
        #control de señales de rebote:
        if ticks_ms() - self.tiempo > 50:
            # controla el valor actual con base al mínimo y máximo de manera cíclica.
            self.actual = self.actual+self.incremento if self.actual<self.maximo else self.minimo
            self.tiempo = ticks_ms() # actualiza el tiempo de activación
        
    def giro_izquierda(self)->None:
        '''evento levantado cuando se detecta un giro en contra de las manecillas del reloj'''
        # control de señales de rebote:
        if ticks_ms() - self.tiempo > 50:
            # controla el valor actual con base al mínimo y máximo de manera cíclica.
            self.actual = self.actual-self.incremento if self.actual>self.minimo else self.maximo
            self.tiempo = ticks_ms() #actualiza el tiempo de activación
    
    def __getattr__(self, nombre:str):
        '''devuelve el valor de un atributo, segun su nombre'''
        if nombre=='valor': return self.actual #devuelve el valor actual
    
    def cambiar(self,_min:float=0,_max:float=10,_incr:float=0.5)->None:
        '''modifica los valores de contador del rotativo y lo establece en el mínimo'''
        self.minimo = _min        # guarda el valor mínimo deseado
        self.actual = _min          # establece el valor actual en el mínimo
        self.maximo = _max       # guarda el valor máximo deseado
        self.incremento = _incr   # guarda el incremento deseado por paso del rotativo.
