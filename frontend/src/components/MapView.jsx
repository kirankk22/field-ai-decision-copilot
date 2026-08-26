import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

import L from "leaflet";


// Fix Leaflet marker icons when using Vite

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",

  iconUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",

  shadowUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});


function MapView({
  detections,
  onDetectionSelect,
}) {

  const center = [
    20.2961,
    85.8245,
  ];


  return (
    <MapContainer
      center={center}
      zoom={13}
      className="map-container"
    >

      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />


      {detections.map(
        (detection) => (

          <Marker
            key={detection.id}
            position={[
              detection.latitude,
              detection.longitude,
            ]}
            eventHandlers={{
              click: () =>
                onDetectionSelect(
                  detection
                ),
            }}
          >

            <Popup>

              <strong>
                {detection.type}
              </strong>

              <br />

              Detection:
              {" "}
              {detection.id}

              <br />

              Confidence:
              {" "}
              {(detection.confidence * 100)
                .toFixed(0)}
              %

            </Popup>

          </Marker>

        )
      )}

    </MapContainer>
  );
}


export default MapView;