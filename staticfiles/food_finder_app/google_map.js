// Initialize and add the map
let map;

async function initMap() {
    var events = {{ event_list }}
    events.forEach(function(event) {
        const position = { lat:event.event_lattitude, lng:event.event_longitude};
        const marker = new AdvancedMarkerElement({
            map: map,
            position: position,
            title: event.event_description,
        });
  });
  // Request needed libraries.
  //@ts-ignore
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  // The map, centered at Uluru
  map = new Map(document.getElementById("map"), {
    zoom: 4,
    center: position,
    mapId: "DEMO_MAP_ID",
  });


}

initMap();

//
//    $(document).ready(function(){
//        $.ajax({
//            url: "{% url 'mydata'%}",
//            method: 'GET',
//            success: function (data) {
//                console.log(data);
//                initMap(data);
//            }
//      });
//    });
//
//    function initMap(data) {
//       const map = new google.maps.Map(document.getElementById('map'), {
//          zoom: 4,
//          center: {lat: 51.5944418, lng: 4.7492914}
//       });
//       const markers = data?.map((i) => {
//            const marker = new google.maps.Marker({
//                position: { lat: parseFloat(i.latitude), lng: parseFloat(i.longitude)},
//                map: map,
//            })
//        });
//     }
//
//      var events = {{ event_list }};
//        locations.forEach(function(location) {
//            var marker = new google.maps.Marker({
//                position: {lat: location.latitude, lng: location.longitude},
//                map: map
//            });
//        });