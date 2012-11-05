<script type="text/javascript" language="javascript">
//Anadimos el marcador para la escuela que estamos editando

//Las funciones que gestionan el arrastre
GEvent.addListener(marker, "dragstart", function() {
  map.closeInfoWindow();
  });
//..sobre todo al soltar, que almacenamos los valores en los inputs

function fin_arrastrar ()
{
    alert("nos hemos movido!");
//    marker.openInfoWindowHtml("Cambiado la posicion de la escuela");
//    pos = marker.getLatLng();
//    trace('Tenemos lat='+escape(pos.lat())+'&lon='+escape(pos.lng()));
//    document.getElementById('id_lat').value = escape(pos.lat());
//    document.getElementById('id_long').value = escape(pos.lng());
//    trace("Guardados los valores en los inputs ocultos");
}

trace("Vamos a añadir el codigo para la gestión del doble click");
GEvent.addListener(map, 'dblclick', function(marker, point) {
    //**  ... Suppression de tous les recouvrements (marqueurs, polyline, info-bulle, etc...) de la carte nommée 'map' ... **//
    trace("Doble cick");
    //Limpiamos
    map.clearOverlays();
    marker = new GMarker(point, {draggable: true});
GEvent.addListener(marker, "dragstart", function() {
  map.closeInfoWindow();
  });
GEvent.addListener(marker, "dragend", function() {
    marker.openInfoWindowHtml("Cambiado la posicion de la escuela");
    pos = marker.getLatLng();
    trace('Tenemos lat='+escape(pos.lat())+'&lon='+escape(pos.lng()));
    document.getElementById('id_lat').value = escape(pos.lat());
    document.getElementById('id_long').value = escape(pos.lng());
    trace("Guardados los valores en los inputs ocultos");
  });
    map.addOverlay(marker);
    pos = marker.getLatLng();
    document.getElementById('id_lat').value = escape(pos.lat());
    document.getElementById('id_long').value = escape(pos.lng());
    trace("Guardados los valores en los inputs ocultos");
});
</script>
