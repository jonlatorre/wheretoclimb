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
from django.contrib.syndication.views import Feed
from models import Crag

class LatestEntriesFeed(Feed):
    title = "Ultimas Crags en Donde Escalar"
    link = "/latest/"
    description = "Ultimas Crags añadidas a dondeescalar.es"

    def items(self):
        return Crag.objects.order_by('-pub_date')[:5]

    def item_title(self, item):
        return item.slug

    def item_description(self, item):
        return item.descripcion
