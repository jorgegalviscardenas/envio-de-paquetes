'''
Encargado de ayudar con ciertas conversiones de tipos

@author Sebastian Noreña Marquez <sebastian.norenam@autonoma.edu.co>
@author Camilo Andres Lengua Duque <camiloa.lenguad@autonoma.eu.co>
@author Alejandro Gomez Alzate <alejandro.gomez@autonoma.edu.co>
@author Jorge Galvis Cárdenas <jorge.galvisc@autonoma.edu.co>

@version 20210217
'''
import datetime

'''
Convierte la fecha a un formato bonito
@param string fecha la fecha a convertir
@return string la fecha en formato bonito
'''


def formato_fecha_bonita(fecha):
    return fecha.strftime("%A %d de %B del %Y a las %I:%M %p")
'''
Redondea el número a los decimales estipulados
@param float numero el numero a redondear
@param integer decimales la cantidad de decimales a redondear
@return string
'''
def formato_decimal(numero,decimales):
    return str(round(numero, decimales))