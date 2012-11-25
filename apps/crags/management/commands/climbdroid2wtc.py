import sqlite3
import sys
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand, CommandError
from crags.models import Crag

class Command(BaseCommand):
    def handle(self, *args, **options):
        conn = sqlite3.connect('climbdroid.db')
        res = conn.execute('SELECT * from crag')
        for crag in res:
            crag_id,crag_name, crag_comment = crag
            #print "-Tenemos la crag %s con el id %s"%(crag_name,crag_id)
            sectors = conn.execute("SELECT * FROM sector where _id_crag = %s"%crag_id)
            for sector in sectors:
                sector_id = sector[0]
                sector_name = sector[1]
                #print "--El sector %s con id %s"%(sector_name,sector_id)
                routes = conn.execute("SELECT * FROM route where _id_sector = %s"%sector_id)
                for route in routes:
                    route_id = route[0]
                    route_name = route[1]
                    #print "---La via %s con id %s"%(route_name,route_id)
                    #print ("SELECT * FROM gps_position where _id_route = %s"%route_id)
                    gps = conn.execute("SELECT * FROM gps_position where _id_route = %s"%route_id).fetchone()
                    try:
                        gps_lat,gps_lon = gps[2],gps[3],
                        
                        location = Point(gps_lon,gps_lat)
                        print "Buscamos..."
                        new_crag, new = Crag.objects.get_or_create(name=crag_name,climbing_type=0,location=location,valoracion=1)
                        print new_crag, new
                        if new:
                            print "...vamos a anadir la escuela %s con la posicion GPS: %s-%s"%(crag_name,gps_lat,gps_lon)
                            new_crag.save()
                            break
                        else:
                            print "...ya existe!"
                    except TypeError:
                        print  sys.exc_info()[0]
                        print "No tenemos posicion GPS de la escuela %s :("%crag_name
        conn.close()
