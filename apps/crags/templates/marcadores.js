console.log('Empezamos con los maracdores de escuelas');
var icono = new GIcon(image="/site_media/static/image/escuela_deportiva.png");
{% for e in escuelas %}
    var texto = "<a href='/escuelas/detalle/{{e.id}}'>{{e.nombre}}</a><br />";
    var pos{{ forloop.counter }} = new GLatLng({{ e.posicion.lat.to_eng_string }}, {{ e.posicion.lon.to_eng_string }});
    //trace(pos{{ forloop.counter }}.toString());
    trace({{marker_opts}});
    var marker{{ forloop.counter }} = new GMarker(pos{{ forloop.counter }},{{marker_opts}});
    GEvent.addListener(marker{{ forloop.counter }}, "click", function() {
    	marker{{ forloop.counter }}.openInfoWindowHtml(texto);
	});
    map.addOverlay(marker{{ forloop.counter }});
{% endfor %}

trace("No a petado!");
