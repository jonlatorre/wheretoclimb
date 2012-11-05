#!/usr/bin/python
# -*- coding: utf-8 -*-

### BEGIN LICENSE
#    This file is part of DondeEscalar.

#    DondeEscalar is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    DondeEscalar is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with DondeEscalar.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

from django.http import HttpResponse, HttpResponseNotFound, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.gis.geos import Point
from django.views.generic import DetailView, ListView, CreateView, UpdateView

#Modelos
from models import *
#from common.models import Municipio
#from eltiempo.models import *
from common.models import *
from topos.models import *
#Forms
from forms import *
from gmapi import maps
from django.contrib.localflavor.es.forms import *

import logging
import simplejson
l = logging.getLogger()
debug = l.debug
climbing_icon = '/site_media/static/icons/climbdroid_ico.png'
#climbing_icon_big = '/site_media/static/icons/climbdroid_ico_big.png'
climbing_icon_big=climbing_icon

class CragListView(ListView):
    model = Crag
    context_object_name = "crag_list"
    template_name = "crag_list.html"

def lista_provincia(request, id):
    lista_Crags = Crag.objects.filter(provincia=id)
    return render_to_response('lista.html',{'Crags': lista_Crags,'tipo':'provincia'},RequestContext(request))

def crags_crag_view(request, slug, id):
    try:
        my_crag = Crag.objects.get(slug=slug, id=id)
    #except ObjectDoesNotExist:
    except:
        my_crag=get_object_or_404(Crag, id=id)
        return HttpResponsePermanentRedirect(my_crag.get_absolute_url())
    #Mandamos la form con la Crag
    form_crag = CragForm(instance=my_crag)
    form_sector = SectorForm()
    gmap = maps.Map(opts = {
        'id': 'detail_map',
        'center': maps.LatLng(my_crag.location.coords[1], my_crag.location.coords[0]),
        'mapTypeId': maps.MapTypeId.ROADMAP,
        'zoom': 10,
        'mapTypeControlOptions': {
            'style': maps.MapTypeControlStyle.DROPDOWN_MENU
        },
    })
    marker = maps.Marker(opts = {
        'map': gmap,
        'position': maps.LatLng(my_crag.location.coords[1], my_crag.location.coords[0]),
        'icon': climbing_icon_big ,
    })
    return render_to_response('crag_detail.html',{'crag': my_crag, 'form_crag': form_crag, \
        'form': MapaDetalleForm(initial={'map': gmap}), 'form_sector': SectorForm(initial={'crag':my_crag}) ,'form_topo': TopoForm },\
        RequestContext(request))

def crags_map(request):
    print request
    ##Creamos el mapa
    #provincia_form = ProvinciaForm()
    gmap = maps.Map(opts = {
        'center': maps.LatLng(39.38, -3.93),
        'mapTypeId': maps.MapTypeId.ROADMAP,
        'zoom': 6,
        'mapTypeControlOptions': {
             'style': maps.MapTypeControlStyle.DROPDOWN_MENU
        },
    })
    ##Listamos las Crags y creamos los marcadores
    for e in Crag.objects.all():
        marker = maps.Marker(opts = {
            'map': gmap,
            'position': maps.LatLng(e.location.coords[1], e.location.coords[0]),
            'icon': climbing_icon ,
        })
        maps.event.addListener(marker, 'click', 'crags_map.viewInfo')
        #maps.event.addListener(marker, 'mouseout', 'myobj.markerOut')
        if e.photo:
            thumb_url = e.photo.thumbnail_image.url
        else:
            thumb_url=""

        contenido_info_window = '<div> \
                <div name="foto_Crag" style="border:1px solid black; width:100px; height:75px; float:left;">\
                    <img src="'+thumb_url+'" />\
                </div>\
                <div name="info_Crag" style="width:250px; height:75px; float:right;" > \
                    Crag  de '+e.get_type()+': <a href="/crags/'+str(e.slug)+'/'+str(e.id)+'/" > '+e.name+'</a>\
                </div>\
                </div>'
        #if e.meteo and e.meteo.eltiempoes:
        #    contenido_info_window +='<iframe src="'+e.meteo.eltiempoes.get_widget_url()+'"></iframe>'
        info = maps.InfoWindow({
            'content': contenido_info_window
        })
        info.open(gmap, marker)
    context = {'form': CragsMapForm(initial={'map': gmap})}
    #if request.mobile:
    #    template = 'mobile_mapa.html'
    #else:
    #    template = 'mapa.html'
    template = 'crags_map.html'
    return render_to_response(template, context,RequestContext(request))

def crags_crag_edit(request,id):
    Crag = Crag.objects.get(id=id)

    gmap = maps.Map(opts = {
        'center': maps.LatLng(Crag.lat, Crag.lon),
        'mapTypeId': maps.MapTypeId.ROADMAP,
        'zoom': 10,
        'mapTypeControlOptions': {
            'style': maps.MapTypeControlStyle.DROPDOWN_MENU
        },
    })
    marker = maps.Marker(opts = {
        'map': gmap,
        'position': maps.LatLng(Crag.lat, Crag.lon),
        'draggable': True,
    })
    #maps.event.addListener(marker, 'mouseover', 'myobj.markerOver')
    maps.event.addListener(marker, 'dragend', 'Crag.arrastrar')
    if request.method == 'POST': # If the form has been submitted...
        form = CragForm(request.POST,instance=Crag) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            Crag.save(force_update=True)
            ##return HttpResponseRedirect('/Crags/gracias/',{'Crag':Crag}) # Redirect after POST

            return render_to_response('detalle.html',{'Crag': Crag, 'form_Crag': form, 'form': MapaDetalleForm(initial={'map': gmap}),'mensaje': "Gracias por editar la Crag"},RequestContext(request))

        else:
            for error in form.errors:
                debug(error)
            return HttpResponseNotFound('<h1>Algo ha ido mal!</h1>')
    else:
        form = CragForm(instance=Crag) # A form bound to the POST data
        context = {'form': form, 'mapa': MapaDetalleForm(initial={'map': gmap}), 'Crag':Crag}
        return render_to_response('editar.html', context, context_instance=RequestContext(request))

def crags_crag_new(request):
    form_crag = CragForm(initial={'lat': 39.38,'lon': -3.93, 'climbing_type': 0, 'valoracion': 1, \
        'description': "Add here a description of the Crag."})
    if request.method == 'POST': # If the form has been submitted...
        form = CragForm(request.POST) # A form bound to the POST data
        form_photo = PhotoForm(request.POST, request.FILES)
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            #municipio_id = request.POST['municipio_id']
            ##Creamos el objecto punto gis con los campos del form
            location = Point(form.cleaned_data['lon'], form.cleaned_data['lat'])

            Crag = form.save(commit=False)
            Crag.location = location
            Crag.save()
            
            if form_photo.is_valid():
                debug("Guardamos la foto")
                photo = form_photo.save()
                debug("Ponemos normbre y guardamos la foto")
                photo.name = "foto_Crag_"+str(Crag.id)+"_"+Crag.nombre
            else:
                debug("pues no hay foto, habrá que añadir la generica")
                photo = Photo.objects.get(name="nofoto")
            debug("Añadidos la foto a la Crag")
            Crag.photo = photo
            debug("Guardamos la Crag otra vez")
            Crag.save()
            if request.user.is_authenticated():
                debug("Crag creada por %s"%request.user)
                Crag.owner = request.user
                Crag.save()
            return redirect("/crags")
            #return render_to_response('/Crags/mapa.html',{'mensaje': "Graciás por añadirla Crag."})
        else:
            gmap = maps.Map(opts = {
                'center': maps.LatLng(form.data['lat'], form.data['lon']),
                'mapTypeId': maps.MapTypeId.ROADMAP,
                'zoom': 6,
                'mapTypeControlOptions': {
                     'style': maps.MapTypeControlStyle.DROPDOWN_MENU
                },
            })
            marker = maps.Marker(opts = {
                    'map': gmap,
                    'position': maps.LatLng(form.data['lat'], form.data['lon']),
                    'draggable': True,
                    'title': "Nueva Crag",
                })

            context = {'form_Crag': form,
                'form_photo': form_photo,
                'mapa': MapaDetalleForm(initial={'map': gmap})}
            return render_to_response('detalle.html',{'Crag': Crag, \
                'form': MapaDetalleForm(initial={'map': gmap}),\
                'mensaje': "Gracias por editar la Crag"},RequestContext(request))
    ##Si no es post....
    else:
        form_photo = PhotoForm()
        gmap = maps.Map(opts = {
            'center': maps.LatLng(39.38, -3.93),
            'mapTypeId': maps.MapTypeId.ROADMAP,
            'zoom': 6,
            'mapTypeControlOptions': {
                 'style': maps.MapTypeControlStyle.DROPDOWN_MENU
            },
        })
        marker = maps.Marker(opts = {
            'map': gmap,
            'position': maps.LatLng(39.38, -3.93),
            'draggable': True,
            'title': "New Crag",
        })

        maps.event.addListener(marker, 'dragend', 'crag.drag')
        #maps.event.addListener(gmap, 'click', 'Crag.crearMarcador')
        context = {'form_crag': form_crag,
            'form_photo': form_photo,
            'mapa': MapaNuevaForm(initial={'map': gmap})}
        template = 'crag_new.html'
        return render_to_response(template, context, context_instance=RequestContext(request))

def crags_route_new(request,id):
    """Recibimos el id del sector a la que queremos añadir la nueva via"""
    sector = Sector.objects.get(id=id)
    template = 'Crags/via_nueva.html'
    if request.method == 'POST': # If the form has been submitted...
        form = ViaForm(request.POST) # A form bound to the POST data
        form_foto = FotoForm(request.POST, request.FILES)
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            via = form.save()
            if form_foto.is_valid():
                foto = form_foto.save()
                foto.name = "foto_via_"+Crag.id+"_"+Crag.nombre
            else:
                debug("pues no hay foto, habrá que añadir la generica")
                foto = Foto.objects.get(name="nofoto")
            debug("Añadidos la foto a la via")
            via.foto = foto
            debug("Guardamos la via otra vez")
            via.save()
            if request.user.is_authenticated():
                via.owner = request.user
                via.save()
            #return render_to_response('/Crags/gracias.html',{'elemento':via})
            #return redirect(Crag.get_absolute_url())
            return render_to_response('close_dialog.html',{'mensaje': "Gracias por añadir la via",'dialogo':'dialogvia'})
            #return redirect(ver_Crag,sector.Crag.slug,sector.Crag.id)
        else:
            ##Algo está mal en el form
            context = {'form_via': form,
            'form_foto': form_foto,
            'sector': sector}
            return render_to_response(template, context, context_instance=RequestContext(request))

    ##Si no es post....
    else:
        form_via = ViaForm(initial={'tipo':0,'sector':sector,'Crag':sector.Crag})
        form_foto = FotoForm()
        context = {'form_via': form_via,
            'form_foto': form_foto,
            'sector': sector}

        return render_to_response(template, context, context_instance=RequestContext(request))

def crags_route_view(request, slug, id):
    try:
        via = Via.objects.get(slug=slug, id=id)
    #except ObjectDoesNotExist:
    except:
        via = get_object_or_404(Via, id=id)
        return HttpResponsePermanentRedirect(via.get_absolute_url())
    return render_to_response('via_detalle.html',{'via': via },RequestContext(request))

def crags_sector_new(request,id):
    """Recibimos el id de la Crag a la que queremos añadir el nuevo sector"""
    selected_crag = Crag.objects.get(id=id)
    template = 'sector_nuevo.html'
    if request.method == 'POST': # If the form has been submitted...
        form = SectorForm(request.POST) # A form bound to the POST data
        form_photo = PhotoForm(request.POST, request.FILES)
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            sector = form.save()
            if form_photo.is_valid():
                photo = form_photo.save()
                photo.name = "photo_sector_"+selected_crag.id+"_"+selected_crag.nombre
            else:
                debug("pues no hay foto, habrá que añadir la generica")
                photo = Photo.objects.get(name="nofoto")
            debug("Añadidos la foto al sector")
            sector.photo = photo
            debug("Guardamos el sector")
            sector.save()
            #return render_to_response('/Crags/gracias.html',{'elemento':sector})
            return redirect(selected_crag.get_absolute_url())
            #return render_to_response('close_dialog.html',{'mensaje': "Gracias por añadir el sector",
            #    "destino": "%s#detalle"%Crag.get_absolute_url(),'dialogo':'dialogcroquis'})
        else:
            context = {'form_sector': form,
            'form_photo': form_photo,
            'crag': selected_crag}
        return render_to_response(template, context, context_instance=RequestContext(request))
    ##Si no es post....
    else:
        form_sector = SectorForm(initial={'crag':selected_crag})
        form_photo = PhotoForm()
        context = {'form_sector': form_sector,
            'form_foto': form_photo,
            'crag': selected_crag}
        return render_to_response(template, context, context_instance=RequestContext(request))

def crags_sector_view(request, slug, id):
    debug("Somos ver sector")
    try:
        sector = Sector.objects.get(slug=slug, id=id)
        ##Buscamos las vias.....
    ##Si ha cambiado el slug le mandamos a la nueva url
    except:
        debug("No hemos encontrado el sector, tratamos de sacar su absolute_url")
        sector = get_object_or_404(Sector, id=id)
        return HttpResponsePermanentRedirect(sector.get_absolute_url())
    return render_to_response('sector_detail.html',{'sector': sector},RequestContext(request))

def nuevo_croquis(request,id):
    """Recibimos el id de la Crag a la que queremos añadir el nuevo croquis"""
    Crag = Crag.objects.get(id=id)
    template = 'croquis_nuevo.html'
    if request.method == 'POST': # If the form has been submitted...
        debug("Nos quieren subir un croquis")
        form = CroquisForm(request.POST, request.FILES) # Creamos el form con los datos POST y el fichero
        if form.is_valid(): # All validation rules pass
            debug("Todos los campos OK. Vamos a guardarlo")
            # Process the data in form.cleaned_data
            croquis = form.save()
            debug("Despues de guardar el croquis lo añadimos a la Crag")
            Crag.croquises.add(croquis)
            #return render_to_response('/Crags/gracias.html',{'elemento':croquis})
            #return redirect(Crag.get_absolute_url())
            return render_to_response('close_dialog.html',{'mensaje': "Gracias por añadir el croquis",
                "destino": "%s#croquis"%Crag.get_absolute_url(),'dialogo':'dialogcroquis'})
        else:
            debug("Algun campo no esta bien :(")
            debug(form.errors)
            context = {'form': form,
            'Crag': Crag}
            return render_to_response(template, context, context_instance=RequestContext(request))

    ##Si no es post....
    else:
        form = CroquisForm(initial={'Crag':Crag})
        context = {'form': form,
            'Crag': Crag}
        return render_to_response(template, context, context_instance=RequestContext(request))

def crags_find(self,request):
    texto = self.GET['string']
    debug ("Vamos a buscar Crags con texto: %s"%texto)
    lista = []
    resultado = Crag.objects.filter(nombre__contains=texto)
    for Crag in resultado:
        lista.append(Crag.name)
    return HttpResponse(simplejson.dumps(lista), mimetype='application/javascript')

