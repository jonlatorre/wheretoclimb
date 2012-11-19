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

from django.conf.urls.defaults import *
from views import *
from models import *
from feeds import LatestEntriesFeed

info_dict = {
    'queryset': Crag.objects.all(),
}

# Uncomment the next two lines to enable the admin:
urlpatterns = patterns('',
    url(r'sector/new/(?P<id>\d+)/$', crags_sector_new, name="crags_sector_new"),
    url(r'sector/(?P<slug>[-\w]+)/(?P<id>\d+)/$', crags_sector_view),
    url(r'topo/new/(?P<id>\d+)/$', crags_topo_new, name="crags_topo_new"),
    url(r'list/$', CragListView.as_view(), name="crags_list"),
    #(r'provincia/(?P<id>\d+)/$', lista_provincia),
    url(r'(?P<slug>[-\w]+)/(?P<id>\d+)/$', crags_crag_view, name="crags_crag_detail"),
    url(r'map/$', crags_map, name="crags_map"),
    url(r'new/$', crags_crag_new, name="crags_crag_new"),
    url(r'edit/(\d+)/$', crags_crag_edit),
    url(r'latest/$', LatestEntriesFeed()),
    url(r'find/$',crags_find),
    url(r'route/new/(?P<id>\d+)/$', crags_route_new),
    url(r'route/(?P<slug>[-\w]+)/(?P<id>\d+)/$', crags_route_view),
    url(r'$', crags_map, name="crags_map"),
)
