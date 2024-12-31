# Ejemplo de uso del módulo de control del encoder rotativo:

from rotativo import ROTATIVO

_pin_clk = 2          # Pin de entrada (CLK)
_pin_dt = 4           # Pin de entrada (DT)
_valor_minimo = 1     # Puede ser un decimal
_valor_maximo = 10    # Puede ser un decimal
_incremento = 1       # Puede ser un decimal

  # Declaración del objeto del rotativo
encoder = ROTATIVO(_pin_clk, _pin_dt, _valor_minimo, _valor_maximo, _incremento)
  # Declaración de un valor de referencia
ultimo_valor = 0

while True:
  # Verifica si el valor actual del encoder es diferente del último valor
  if rot.valor!=ultimo_valor:   # hubo un cambio de valor.
      ultimo_valor = rot.valor  # actualiza el ultimo valor conocido.
      print('El valor del rotativo actual es de {}'.format(ultimo_valor))
