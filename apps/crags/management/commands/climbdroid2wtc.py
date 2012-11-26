import sqlite3
import sys
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand, CommandError
from crags.models import *

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
                    route_grade_text = route[2]
                    try:
                        print "Buscamos el grado...",route_grade_text
                        route_grade=Grade.objects.get(name=route_grade_text)
                    except:
                        route_grade=Grade.objects.get(name="5c")
                    route_type = route[3]
                    route_meters = route[8]
                    route_gear = route[9]
                    route_pitches = route[10]
                    route_comment = route[11]
                    
                    #print "---La via %s con id %s"%(route_name,route_id)
                    #print ("SELECT * FROM gps_position where _id_route = %s"%route_id)
                    gps = conn.execute("SELECT * FROM gps_position where _id_route = %s"%route_id).fetchone()
                    try:
                        gps_lat,gps_lon = gps[2],gps[3],
                    except TypeError:
                        print "No tenemos posicion GPS de la via %s con id %s :("%(route_name,route_id)
                        break

                    try:
                        new_crag = Crag.objects.get(name=crag_name)
                    except Crag.DoesNotExist:
                        print "...vamos a anadir la escuela %s con la posicion GPS: %s-%s"%(crag_name,gps_lat,gps_lon)
                        new_crag = Crag(name=crag_name,location = Point(gps_lon,gps_lat),climbing_type=0,valoracion=1)
                        new_crag.save()

                    try:
                        new_sector = Sector.objects.get(name=sector_name)
                        print "Ya existe el sector" 
                    except Sector.DoesNotExist:
                        print "Anadimos sector %s"%sector_name
                        new_sector=Sector(name=sector_name,crag=new_crag,location = Point(gps_lon,gps_lat))
                        new_sector.save()
                    try:
                        new_route=Route.objects.get(name=route_name)
                        print "ya esta la ruta"
                    except Route.DoesNotExist:
                        print "Creamos la ruta"
                        new_route = Route(name=route_name,location=Point(gps_lon,gps_lat),grade=route_grade,\
                            climbing_type=route_type,longitude=route_meters,pitches=route_pitches,\
                            comment=route_comment,sector=new_sector)
                        new_route.save()
                        


        conn.close()
