from models import *
#from django.contrib import admin
from django.contrib.gis import admin

class CragAdmin(admin.GeoModelAdmin):
    search_fields = (['name'])
    #inlines = [ImagesInline]
class SectorAdmin(admin.ModelAdmin):
    pass
class RouteAdmin(admin.GeoModelAdmin):
    pass
class GradeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Crag, CragAdmin)
admin.site.register(Sector, SectorAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Grade, GradeAdmin)
