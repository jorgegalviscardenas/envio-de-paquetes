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
Valida que la cadena es un número
@param string cadena Cadena a validar
@return boolean si es número retorna True, de lo contrario False
'''


def es_numero(cadena):
    return True if re.match(r'[+-]?([0-9]*[.])?[0-9]+', cadena) != None else False


'''
Valida que la cadena es un email
@param string cadena cadena a validar
@return boolean si es email retorna True, de lo contrario False
'''


def es_email(cadena):
    return True if re.search(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', cadena) != None else False

'''
Valida que la cadena solo contiene numeros
@param string cadena cadena a validar
@return boolean si contiene solo números retorna True, de lo contrario False
'''
def contiene_solo_numeros(cadena):
    return True if re.match(r'^([\s\d]+)$', cadena) != None else False
