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

#from django.db import models
from django.contrib.gis.db import models
from django.contrib import admin
from django.template import defaultfilters
from django.contrib.auth.models import User
##Paises y provincias
from django_countries import CountryField
from django_countries.countries import COUNTRIES
#from django.contrib.localflavor.es.es_provinces import PROVINCE_CHOICES
#Modelos de otros modulos

from common.models import Photo
from topos.models import Topo
##Para trabajar con la api geo de google
import json

# Create your models here.
VALORACION = (
    (1, 'Interes local'),
    (2, 'Merece una visita'),
    (3, 'Buena'),
    (4, 'Visita obligada'),
)
CLIMBING_TYPE = (
    (1, 'Sport Climbing'),
    (2, 'Multipitch Climbing'),
    (3, 'Trad Climbing'),
    (4, 'Ice Climbing'),
    (5, 'Deep Water Soloing'),
    (6, 'Mountaenering'),
    (7, 'Rocodromo'),
)

class Grade(models.Model):
    value=models.DecimalField(max_digits=2, decimal_places=0)
    name=models.CharField(max_length=5)
    def __unicode__(self):
        return self.name


class Crag(models.Model):
    name=models.CharField(max_length=200)
    slug = models.SlugField()
    climbing_type=models.DecimalField(max_digits=2, decimal_places=0,choices=CLIMBING_TYPE)
    location = models.PointField(srid=4326)
    owner = models.ForeignKey(User,blank=True,null=True)
    country=CountryField(choices=COUNTRIES,default="ES", blank=True)
    description=models.TextField(blank=True,null=True)
    pub_date = models.DateTimeField('date published',auto_now_add=True)
    photo = models.ForeignKey(Photo,blank=True,null=True,default=1)
    valoracion = models.DecimalField(max_digits=1, decimal_places=0,choices=VALORACION, blank=True)
    topos = models.ManyToManyField(Topo,blank=True,null=True,related_name='crags')
    def __unicode__(self):
        return self.name
    objects = models.GeoManager()
    ##Métodos
    def get_type(self):
        return CLIMBING_TYPE[int(self.climbing_type)][1]

    def save(self, *args, **kwargs):
        self.slug = defaultfilters.slugify(self.name)
        super(Crag, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return "/crags/%s/%i/" % (self.slug,self.id)

class Sector(models.Model):
    name=models.CharField(max_length=200)
    crag=models.ForeignKey(Crag, related_name="sectors")
    photo = models.ForeignKey(Photo,blank=True,null=True)
    comment=models.TextField(blank=True,null=True)
    pub_date = models.DateTimeField('date published',auto_now_add=True)
    location = models.PointField(srid=4326,blank=True,null=True)
    slug = models.SlugField(blank=True,null=True)
    topos = models.ManyToManyField(Topo,blank=True,null=True,related_name='sectors')
    
    def __unicode__(self):
        return self.name
    objects = models.GeoManager()

    ##Métodos
    def save(self, *args, **kwargs):
        self.slug = defaultfilters.slugify(self.name)
        super(Sector, self).save(*args, **kwargs)
    def get_absolute_url(self):
        return "/crags/sector/%s/%i" % (self.slug,self.id)
        
class Route(models.Model):
    crag=models.ForeignKey(Crag,blank=True,null=True,related_name="routes")
    name=models.CharField(max_length=200)
    photo = models.ForeignKey(Photo,blank=True,null=True)
    sector = models.ForeignKey(Sector,blank=True,null=True,related_name="routes")
    location = models.PointField(srid=4326,blank=True,null=True)
    grade = models.ForeignKey(Grade,null=True)
    climbing_type = models.DecimalField(max_digits=2, decimal_places=0,choices=CLIMBING_TYPE)
    #estilo = models.CharField(max_length=50)
    longitude = models.DecimalField(decimal_places=0,max_digits=4,blank=True,null=True)
#    material = models.CharField(max_length=50,blank=True,null=True)
#    largos=models.DecimalField(decimal_places=0,max_digits=4,null=True,default=1)
#    comentario=models.TextField(blank=True,null=True)
#    pegues = models.CharField(max_length=200)
    slug = models.SlugField(blank=True,null=True)
    pub_date = models.DateTimeField('date published',auto_now_add=True)
    topo = models.ManyToManyField(Topo,blank=True,null=True,related_name='routes')
    def __unicode__(self):
        return self.name

    objects = models.GeoManager()

    ##Métodos
    def save(self, *args, **kwargs):
        self.slug = defaultfilters.slugify(self.name)
        super(Via, self).save(*args, **kwargs)
    def get_absolute_url(self):
        return "/crags/route/%s/%i" % (self.slug,self.id)
    def get_type(self):
        return CLIMBING_TYPE[int(self.climbing_type)][1]
