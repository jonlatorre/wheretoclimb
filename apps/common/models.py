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
#    along with DondeEscalar.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

from django.db import models
#from django.contrib.auth.models import User

from imagekit.models import ImageSpec
from imagekit.processors import Adjust
from imagekit.processors.resize import ResizeToFit as Fit

# Create your models here.
class Photo(models.Model):
    original_image = models.ImageField(upload_to='photos')
    num_views = models.PositiveIntegerField(editable=False, default=0)
    formatted_image = ImageSpec(image_field='original_image', format='JPEG',
            options={'quality': 90})
    thumbnail_image = ImageSpec([Adjust(contrast=1.2, sharpness=1.1),
            Fit(50, 50)], image_field='original_image',
            format='JPEG', options={'quality': 90})
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name
