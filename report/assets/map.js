var map = L.map('map',{ zoomControl: false }).setView([35.6926,51.40000], 13);
function MapMode() {
    if (document.getElementById("dark").checked == true){
    
      var layer = new L.TileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png');
      map.addLayer(layer);
    }
    else{

      var layer = new L.TileLayer( 'http://{s}.tile.openstreetmap.de/tiles/osmde/{z}/{x}/ {y}.png');
      map.addLayer(layer);
    }
  }
function CreateMap(circule_poses,circule_messages,circule_color,marker_poses){
    var mapOptions = {
        center: [17.385044, 78.486671],
        zoom: 10
        }
        // Creating a map object
        
        let messages = circule_messages;
        var me = "my name is\nreza";
        const myArray = messages.split(",");
        var circule_poses = circule_poses;
        var circule_color = circule_color;
        const myArray_color = circule_color.split(",");
        document.getElementById("light").checked = true  
       
       

        //location of points
        var marker_poses = marker_poses;
        let  text;

        // Creating a Layer object
        //serialize data here
        for (let i = 0; i < circule_poses[0].length; i++) {
        
           text = circule_poses[0][i]
           var circle = L.circle(circule_poses[0][i],5, {
            color: myArray_color[i].substring(7,14),
            fillColor: myArray_color[i].substring(7,14),
            fillOpacity: 0.5
        }).addTo(map);
        message = myArray[i].replace('[','')
        message = myArray[i].replace(']','')
        message = myArray[i].replace(']','')
        message = message.replaceAll('//','<br/>')
        circle.bindPopup(message); 
      
        
           
          }
        //add layer and here when change the mode and close menu then changed map mode
        var layer = new L.TileLayer('http://{s}.tile.openstreetmap.de/tiles/osmde/{z}/{x}/ {y}.png');
       
        var marker = L.marker(text).addTo(map);
        marker.bindPopup(me+"<br/>"+" rezaaaaaaaaaaa "); 
    
    
        // Adding layer to the map
        map.addLayer(layer);
       
}


//   {% comment %} var zoomOptions = {
//     position :'topright',
//     zoomInText: '1',
//     zoomOutText: '0',
//  };
//  // Creating zoom control
//  var zoom = L.control.zoom(zoomOptions);
//  zoom.addTo(map) {% endcomment %}

// {% comment %} function toggleMenu() {
          
          
//     menuClose.addEventListener("click", () => {
//      console.log(document.getElementById("dark").checked)
      
//       if (document.getElementById("dark").checked == true){
    
//         var layer = new L.TileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png');
//         console.log(layer)
//         map.addLayer(layer);
//       }
//       else{
 
//         var layer = new L.TileLayer( 'http://{s}.tile.openstreetmap.de/tiles/osmde/{z}/{x}/ {y}.png');
//         map.addLayer(layer);
//       }

//     });
//   } {% endcomment %}
 
//   {% comment %} toggleMenu();  {% endcomment %}