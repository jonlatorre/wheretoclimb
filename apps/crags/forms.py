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
from django import forms
from django.forms import ModelForm
from gmapi.forms.widgets import GoogleMap
from models import *
from django.forms.models import inlineformset_factory
#from django.contrib.localflavor.es.forms import *
#from django.contrib.localflavor.es.es_provinces import PROVINCE_CHOICES

#class ProvinciaForm(forms.Form):
#    provincia = forms.ChoiceField(widget=ESProvinceSelect(),choices=PROVINCE_CHOICES)


class CragsMapForm(forms.Form):
    map = forms.Field(widget=GoogleMap(attrs={'width':1100, 'height':768,
        'name':'crags_map', 'id':'crags_map', 'nojquery': True}))

class MapaDetalleForm(forms.Form):
    map = forms.Field(widget=GoogleMap(attrs={'width':300, 'height':300,
        'name':'mapa_detalle', 'id':'mapa_detalle', 'class':'mapa_detalle', 'nojquery': True}))

class CragNewFormMap(forms.Form):
    map = forms.Field(widget=GoogleMap(attrs={'width':420, 'height':420,
        'name':'mapa_nueva', 'id':'mapa_nueva', 'class':'mapa_nueva', 'nojquery': True}))


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        exclude = ('name',)


class CragForm(ModelForm):
    lat = forms.FloatField(required=False)
    lon = forms.FloatField(required=False)
    class Meta:
        model = Crag
        exclude = ('slug','owner','photo','topos','location')

class SectorForm(ModelForm):
    class Meta:
        model = Sector
        exclude = ('slug','Photo',)
        
class RouteForm(ModelForm):
    class Meta:
        model = Route
        exclude = ('slug','photo','topoes')
        
class TopoForm(ModelForm):
    class Meta:
        model = Topo

CragInlineFormSet = inlineformset_factory(Photo,Crag)
