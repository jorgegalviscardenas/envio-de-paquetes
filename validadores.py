'''
Encargado de validar tipos de datos

@author Sebastian Noreña Marquez <sebastian.norenam@autonoma.edu.co>
@author Camilo Andres Lengua Duque <camiloa.lenguad@autonoma.eu.co>
@author Alejandro Gomez Alzate <alejandro.gomez@autonoma.edu.co>
@author Jorge Galvis Cárdenas <jorge.galvisc@autonoma.edu.co>

@version 20210212
'''
import re

'''
Indica si la cadena es un número
@param string cadena cadena a validar
@return boolean si es número retorna True, de lo contrario False
'''


def es_numero(cadena):
    return True if re.match(r'[+-]?([0-9]*[.])?[0-9]+', cadena) != None else False
