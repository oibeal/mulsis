RADIO_HORMIGA = 0.4 # radio al rededor del cuerpo de la hormiga (r_d)
RADIO_VISUAL = 1.2 # radio del campo visual (r_p)
L_HORMIGA = 0.8 # longitud del cuerpo de la hormiga (beta)
L_ANTENA = 0.4 # longitud de las antenas (phi)
V_DESEADA = 13 # cm/s
V_MIN = 2 # cm/s
ACELERACION = 50 # cm/s^2
GRADOS_ANTENA = 45 # grados entre la cabeza y la antena (alpha)

T_STEP = 0.02 # tiempo que dura cada step (s)
CANT_FEROMONA = 1.2e-6 # g/cm^-1 (Q)
COEF_DIFUSION = 0.01 # cm^2/s (D)
T_DIFUSION = 300 # (tau)
CONCENTRACION_MAX = 1.2e-6 # g/cm^3 (C_max)
VEL_APROX_C_MAX = 100 # const. que controla velocidad a la que la concentración se acerca a su valor máximo (k)
GIRO_FEROMONA = 500 # grados que gira hacia la feromona (grados/s)
GIRO_EVITAR = 1000 # grados que gira para evitar hormigas (grados/s)
PESO_PREFERENCIA = 1
GIRO_EVITAR_RETURN = GIRO_EVITAR/2

MEDIA_ERROR_SATURACION = 0
DESVIACION_ERROR_SATURACION = 0.5 # desviacion estandar de los giros
MEDIA_GIROS = 0
DESVIACION_GIROS = 0.5 # desviacion estandar de los giros

N_HORMIGAS = 50 # cantidad de hormigas de la simulación
T_MAX = 500 # (s)

PREF_LEAVE = 0
PREF_RETURN = 1

BORDER = 1
VISUAL = 0
CONSOLE = 1

GRAPH_MIN_TIME = 10