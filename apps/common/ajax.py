#from dajax.core import Dajax
from django.utils import simplejson
from dajaxice.core import dajaxice_functions
from models import *

import logging
l = logging.getLogger()
debug = l.debug

def get_municipio_code(request, nombre):
    try:
        debug("Buscando %s"%nombre)
        municipio = Municipio.objects.get(nombre__icontains=nombre)
        debug("Encontrado el municipio con id %s"%municipio.id)
        mensaje ="Hola %s!"%(municipio.get_code())
        id = municipio.id
        code = municipio.get_code()
    except:
        id = 0
        code = 0
        mensaje = "No lo hemos encontrado"
    return simplejson.dumps({'message':mensaje, 'id': id, 'loc_id':code})

dajaxice_functions.register(get_municipio_code)
