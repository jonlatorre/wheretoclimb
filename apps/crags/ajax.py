from django.utils import simplejson
from dajax.core import Dajax
from dajaxice.core import dajaxice_functions

from forms import CragForm, SectorForm, RouteForm

def send_escuela_form(request, form):
    print "hemos recibido los datos",form
    dajax = Dajax()
    form = CragForm(form)
    print "Los datos pasana  ser la form....",form
    if form.is_valid():
        print "Es valido!"
        #dajax.remove_css_class('#my_form input','error')
        #dajax.alert("This form is_valid(), the climb spot name is: %s" % form.cleaned_data.get('nombre'))
    else:
        print "No es valido!"
        dajax.remove_css_class('#escuela_form input','ui-state-error')
        for error in form.errors:
            print "Esta mal el campo %s"%error
            dajax.add_css_class('#id_%s' % error,'ui-state-error')
            #dajax.alert("Error en "+error)
    return dajax.json()

def send_sector_form(request, form):
    print "hemos recibido los datos",form
    dajax = Dajax()
    form = CragForm(form)
    print "Los datos pasana  ser la form....",form
    if form.is_valid():
        print "Es valido!"
        #dajax.remove_css_class('#my_form input','error')
        #dajax.alert("This form is_valid(), the climb spot name is: %s" % form.cleaned_data.get('nombre'))
    else:
        print "No es valido!"
        dajax.remove_css_class('#escuela_form input','ui-state-error')
        for error in form.errors:
            print "Esta mal el campo %s"%error
            dajax.add_css_class('#id_%s' % error,'ui-state-error')
            #dajax.alert("Error en "+error)
    return dajax.json()
def send_via_form(request, form):
    print "hemos recibido los datos",form
    dajax = Dajax()
    form = EscuelaForm(form)
    print "Los datos pasana  ser la form....",form
    if form.is_valid():
        print "Es valido!"
        #dajax.remove_css_class('#my_form input','error')
        #dajax.alert("This form is_valid(), the climb spot name is: %s" % form.cleaned_data.get('nombre'))
    else:
        print "No es valido!"
        dajax.remove_css_class('#escuela_form input','ui-state-error')
        for error in form.errors:
            print "Esta mal el campo %s"%error
            dajax.add_css_class('#id_%s' % error,'ui-state-error')
            #dajax.alert("Error en "+error)
    return dajax.json()

dajaxice_functions.register(send_escuela_form)
dajaxice_functions.register(send_sector_form)
dajaxice_functions.register(send_via_form)
