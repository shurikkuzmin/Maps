  function initMap() {
    
    var resultJSON = JSON.parse("{{ result | escapejs }}");

    // Create a map object and specify the DOM element for display.
    var map = new google.maps.Map(document.getElementById('map'), 
    {
      center: {lat: 45.5017, lng : -73.5673},
      scrollwheel: false,
      zoom: 6
    });

    admins = map.data.addGeoJson(resultJSON.admins);
    cities = map.data.addGeoJson(resultJSON.cities);
    villages = map.data.addGeoJson(resultJSON.villages);

    for (var i = 0; i < resultJSON.info.labels.length; i++) 
    {
      var marker = new google.maps.Marker({
                        map: map,
                        animation: google.maps.Animation.DROP,
                        position: resultJSON.info.locations[i],
                        label: resultJSON.info.labels[i],
                        scrollwheel: true,
                        scaleControl: true,
                      }); 
    }

  };
