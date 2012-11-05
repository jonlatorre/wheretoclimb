from django.conf.urls.defaults import *
#from views import *
from models import *
#from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import DetailView, ListView, CreateView, UpdateView



urlpatterns = patterns('croquis/',
	url(r'view/(?P<pk>\d+)/$',DetailView.as_view(model=Topo), name="croquis_view"),
    url(r'new$',CreateView.as_view(model=Topo), name="croquis_new"),
    url(r'$',ListView.as_view(model=Topo), name="croquis_index"),
)
