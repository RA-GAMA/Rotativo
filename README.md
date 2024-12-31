# Rotativo
Módulo de control para un control rotativo

El encoder rotativo es un control que emplea dos señales digitales, las cuales cambian con respecto al giro del control mismo.

Estas señales son denomiandas como reloj (CLK) y Data o Salida B (DT).

Al ser señales digitales, el controlador debe observar los cambios que sufren estas señales para determinar la acción que sucede en el encoder, de manera general, estas señales solo pueden tener dos valores, pero al contar con dos, el estado general puede ser entendido de 4 manras diferentes:

    Estado | [CLK | DT]
     1     =   0  |  0    
     2     =   1  |  0    
     3     =   0  |  1    
     4     =   1  |  1  

     -- Nota: Considera que los pines han sido declarados como PULL_UP y que su cambio de estado está activado por una solicitud de interrupción (IRQ)

===== DISTINCIÓN DE GIRO =====

Para detectar un giro y su dirección, el controlador hace uso de estos cuatro estados diferentes para determinar los cambios del encoder o codificador rotativo, de manera tal que:

    ESTADO               | Significado
      1 (clk=0, DT=0)    = Sin cambios en el encoder rotativo. El rotativo se encuentra en posición estable.
      2 (clk=1, DT=0)    = Giro a la Izquierda en progreso. El rotativo no ha llegado a una posición estable.
      3 (clk=0, DT=1)    = Giro a la Derecha en progreso. El rotativo no ha llegado a una posición estable.
      4 (clk=1, DT=1)    = Fin de giro detectado. El rotativo se encuentra en posición estable

De este modo, el controlador debe detectar una secuencia de cambios del estado, de modo que existen tres estados generales en cada giro detectado:

      Dirección|  Estado 1  |  Estado 2  |  Estado 3  |
      Izquierda| clk=0,dt=0 | clk=0,dt=1 | clk=1,dt=1 |
      Derecha  | clk=0,dt=0 | clk=1,dt=1 | clk=1,dt=1 |

Ya que el objetivo del módulo es detectar un cambio de estado del rotativo de una posición estbale a otra, se busca detectar el tercer cambio de estado para concluir la realización de un giro.

========= FILTRACIÓN DE SEÑALES DE REBOTE ==========

Las señales de rebote son señales que interfieren la lectura "congruente" del encoder rotativo, estas pueden ser ocasionadas por:

  1) Alteraciones en la red eléctrica que alimenta el controlador y/o al encoder.
  2) Ligeras variaciones involuntarias durante el giro del encoder desde una posición estable hacia otra.

Existen en general dos maneras de filtrar las señales de entrada y determinar su procedencia:

  1) Colocar un capacitor entre los pines de entrada y tierra del controlador, ralentizando el cambio de estado del pin de entrada dada la staruación del capacitor.
  2) Aplicar un filtro de tiempo de espera, midiendo el valor de entrada dos veces para verificar la persistencia de dicha señal de entrada.


El presente módulo hace uso del segundo modelo y considera un tiempo de 50 milisegundos para evitar incongruencias en el sentido del giro del rotativo.
