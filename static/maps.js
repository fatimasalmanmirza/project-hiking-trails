	
		const trail_info = ({{ list_trails_info | tojson }});

		function addFaveTrail(target) {
			
			let button = target;// $(target);
			let img = button.dataset.trailImage;
			let trailDir = button.dataset.trailDirections;
			let trailurl = button.dataset.trailUrl;
			let trailName = button.dataset.trailName;
			let data = {
				trailImage: img,
				trailDirections: trailDir,
				trailUrl: trailurl,
				trailName: trailName
			};
			$.post("/save-trails", data, (result) =>{ 
				document.getElementById(button.id).innerHTML = "Added!";
				document.getElementById(button.id).disabled = true;
				
			});



		}

		function myMap() {

			avg_lat = 0; avg_lon = 0;
			for(i = 0; i < trail_info.length; i++){
			trail = trail_info[i];
			avg_lat += trail["coordinates"]["latitude"];
			avg_lon += trail["coordinates"]["longitude"];
			}
			avg_lat /= trail_info.length;
			avg_lon /= trail_info.length;

			let myCenter = {lat: avg_lat, lng: avg_lon};

			let map = new google.maps.Map(document.getElementById('map'),{
				zoom: 11,
				center: myCenter,
			});

			let infoWindow = new google.maps.InfoWindow;


			trail_info.forEach((trail) =>{
				lati = trail.coordinates.latitude;
				longi = trail.coordinates.longitude;
			

				let marker = new google.maps.Marker({
					position: new google.maps.LatLng(lati, longi),
					map: map,
					animation: google.maps.Animation.DROP,
					draggable: true,

				});

				const html = `
					<div style="width:250px; height:200px">
						<div class="window-content">
				        	<img src="${trail.image_url}"
				        	     alt="Trail image"
				        	     style=width:100px; height:100
				        	     class="thumbnail">
				            <p>
				            	<b>Trail name: </b>${trail.name}
				            </p>
				            <a href="${trail.google_directions_address}">
				   				Get Directions
				   			</a><br><br>
				            <a href="${trail.url}">
				            	Find me on Yelp
				            </a><br><br>
				            <button
				            	id="trail.${trail.id}"
				            	data-trail-image="${trail.image_url}"
				            	data-trail-directions="${trail.google_directions_address}"
				            	data-trail-url="${trail.url}"
				            	data-trail-name="${trail.name}"
				            	class="add-fave-btn"
				            	name="redirect"
				            	onclick="addFaveTrail(this)"
				            >
				            	Add to favorites
				            </button>
				        </div>
				    </div>
				`;

				bindInfoWindow(marker, map, infoWindow, html);
			});


		}