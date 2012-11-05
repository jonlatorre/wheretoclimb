#!/usr/bin/python
# -*- coding: utf-8 -*-

### BEGIN LICENSE
#    This file is part of "Where To Climb".

#    "Where To Climb" is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    "Where To Climb" is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with "Where To Climb".  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

from django.db import models
from common.models import Photo

class Topo(Photo):
    comment = models.CharField(max_length=200,blank=True)
    origen = models.CharField(max_length=100,blank=True)
    
class GuideBook(models.Model):
    nombre = models.CharField(max_length=50,blank=True)
    comment = models.CharField(max_length=200,blank=True)

class Link(models.Model):
    url = models.CharField(max_length=200,blank=True)
    comment = models.CharField(max_length=200,blank=True)
