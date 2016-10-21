'''
Created on 21/10/2016
@author: ernesto
'''
import logging
import fileinput

nivel_log = logging.ERROR
#nivel_log = logging.DEBUG

logger_cagada = None

class Punto():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return "(%u,%u)" % (self.x, self.y)
    
    def __repr__(self):
        return self.__str__()

class Marco():
    def __init__(self, valores, putos):
        self.valores = valores
        self.putos = putos
        
    def __str__(self):
        return "Valores: %s, Putos %s" % (self.valores, self.putos)
        

def cacas_cebolla_core(matrix, matrix_resultante, num_rotaciones, tam_x, tam_y):
    marcos = []
    
    tam_min = min(tam_x, tam_y)
    
    num_capas = tam_min // 2
    
    tam_x_act = tam_x
    tam_y_act = tam_y
    for num_caca in range(num_capas) :
        x_act = 0
        y_act = 0
        valores = []
        putos = []
        
        logger_cagada.debug("en la capa %u" % (num_caca))
        
        x_act = num_caca
        y_act = num_caca
        
        for x_mov in range(x_act, x_act + tam_x_act):
            valores.append(matrix[y_act][x_mov])
            putos.append(Punto(x_mov, y_act))
        
        x_act = x_mov 
        
        for y_mov in range(y_act + 1, y_act + tam_y_act):
            valores.append(matrix[y_mov][x_act])
            putos.append(Punto(x_act, y_mov))
        
        y_act = y_mov
        
        for x_mov in range(x_act - 1, num_caca - 1, -1):
            valores.append(matrix[y_act][x_mov])
            putos.append(Punto(x_mov, y_act))
        
        x_act = x_mov 
        
        for y_mov in range(y_act - 1, num_caca , -1):
            valores.append(matrix[y_mov][x_act])
            putos.append(Punto(x_act, y_mov))
        
        y_act = y_mov
        
        logger_cagada.debug("los valores quedaron %s" % valores)
        logger_cagada.debug("los putos quedaron %s" % putos)
        assert y_act - 1 == num_caca and x_act == num_caca, "no se regreso al inicio, se kedo en %u, %u" % (y_act - 1, x_act)
        
        marcos.append(Marco(valores, putos))
        
        tam_x_act -= 2
        tam_y_act -= 2
        
    for marco in marcos:
        idx_valor_inicial = 0
        num_rotaciones_real = 0
        logger_cagada.debug("rotando el marco %s %u veces" % (marco, num_rotaciones))
        
        num_rotaciones_real = num_rotaciones % len(marco.putos)
        
        logger_cagada.debug("las rotaciones reales %u" % num_rotaciones_real)
        
        if(num_rotaciones_real):
            idx_valor_inicial = (len(marco.valores) - num_rotaciones_real) * -1
        
        for idx_punto, idx_valor in enumerate(range(idx_valor_inicial, idx_valor_inicial + len(marco.valores))):
            valor_actual = 0
            puto_actual = None
            logger_cagada.debug("el idx punto %u el idx valor %u" % (idx_punto, idx_valor))
            
            valor_actual = marco.valores[idx_valor]
            puto_actual = marco.putos[idx_punto]
            
            logger_cagada.debug("el valor %u el puto %s" % (valor_actual, puto_actual))
            
            matrix_resultante[puto_actual.y][puto_actual.x] = valor_actual
            
        logger_cagada.debug("la matrix resultante va \n%s" % ('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in matrix_resultante])))
        
def cacas_cebolla_main():
    lineas = []
    matrix = None
    matrix_resultante = None
   
    lineas = list(fileinput.input())
   
    filas, columnas, num_rotaciones = [int(numerin) for numerin in lineas[0].strip().split(" ")]
   
    logger_cagada.debug("filas %u cols %u rotacaca %u" % (filas, columnas, num_rotaciones))

    matrix = [[ 0 for _ in range(columnas)] for _ in range(filas)]
    matrix_resultante = [[ 0 for _ in range(columnas)] for _ in range(filas)]
    
    logger_cagada.debug("la matrix vacia es\n%s" % ('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in matrix])))
    
    for fila, linea in enumerate(lineas[1:]):
        logger_cagada.debug("en fila %s la linea es %s" % (fila, linea))
        matrix[fila] = [int(numerin) for numerin in linea.strip().split(" ")]
        
    
    logger_cagada.debug("la matrix original es %s" % ('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in matrix])))
    
    cacas_cebolla_core(matrix, matrix_resultante, num_rotaciones, columnas, filas)
    logger_cagada.debug("la matrix resultante queda finalmente\n%s" % ('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in matrix_resultante])))
    print("%s" % ('\n'.join([' '.join(['{:0}'.format(item) for item in row]) for row in matrix_resultante])))
        

if __name__ == '__main__':
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(level=nivel_log, format=FORMAT)
    logger_cagada = logging.getLogger("asa")
    logger_cagada.setLevel(nivel_log)

    cacas_cebolla_main()
