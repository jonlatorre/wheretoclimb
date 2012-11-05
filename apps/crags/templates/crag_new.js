//trace("Vamos a añadir el codigo para la gestión del doble click");
GEvent.addListener(map, 'dblclick', function(marker, point) {
	//**  ... Suppression de tous les recouvrements (marqueurs, polyline, info-bulle, etc...) de la carte nommée 'map' ... **//
    map.clearOverlays();

    //**  ... On centre la carte nommée 'map' sur le point 'point', et 
    // avec le niveau de zoom actuel de la carte ( map.getZoom() ) ... **//
    //map.setCenter(point, map.getZoom());
    //**... un nouveau marqueur nommé 'monMarqueur' est créé. Celui est 
    // ancré aux coordonnées géographiques du point 'point' représentant le 
    // centre du cercle ... **//
    trace(point)
    monMarqueur = new GMarker(point, {draggable: true});
    //**... Affichage du marqueur nommé 'nomMarqueur' sur la carte nommée 'map' ... **//
    map.addOverlay(monMarqueur);
    //**... la variable 'centre' est égale aux coorconnées géographiques 
    // du point central de la carte affichée 'map' ... **//
    //centre = map.getCenter();
    pos = monMarqueur.getLatLng();
    trace('Tenemos lat='+escape(pos.lat())+'&lon='+escape(pos.lng()));
    document.getElementById('id_lat').value = escape(pos.lat());
    document.getElementById('id_long').value = escape(pos.lng());
    trace("Guardados los valores en los inputs ocultos");
    /** GDownloadUrl('addpoint?lat='+escape(pos.lat())+'&lon='+escape(pos.lng()), function(text, code){
    //     trace(code+text)
    });**/

	});
//trace("Fin 333");
