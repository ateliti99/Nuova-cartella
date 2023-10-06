import streamlit as st
import folium
import googlemaps
from datetime import datetime

#from input_ex.txt

# Inizializza il client Google Maps con la tua chiave API
gmaps = googlemaps.Client(key='AIzaSyBs7awZCabHHQm8pHV3mpRFp8W6op0bcWA')
def create_map(response: dict):
    st.title("Visualizza Tappe e Percorsi su Google Maps")
    addresses_list = [    {
      "Place": "Pinacoteca di Brera",      "Duration": "2h:30min",
      "Tag": "Art"    },
    {      "Place": "Biblioteca Nazionale Braidense",
      "Duration": "1h:30min",      "Tag": "Books"
    },    {
      "Place": "Sforza Castle",      "Duration": "2h",
      "Tag": "Art"    },
    {      "Place": "Leonardo da Vinci's Last Supper",
      "Duration": "1h",      "Tag": "Art"
    },    {
      "Place": "Navigli District",      "Duration": "3h",
      "Tag": "Art"    },
    {      "Place": "Giardini Pubblici Indro Montanelli",
      "Duration": "2h",      "Tag": "Art"
    }  ]
    
    # Bottone per visualizzare le tappe e i percorsi sulla mappa
    if st.button("Visualizza Tappe e Percorsi"):
        # Ottieni le coordinate per ogni tappa
        coordinates = []
        for address in addresses_list:
            # Ottieni le coordinate per l'indirizzo dalla API di Google Maps Geocoding
            geocode_result = gmaps.geocode(address)
            if geocode_result:
                location = geocode_result[0]['geometry']['location']
                coordinates.append([location['lat'], location['lng']])
            else:
                st.warning(f"Impossibile trovare coordinate per l'indirizzo: {address}")

        # Crea una mappa folium centrata sulla prima tappa
        if coordinates:
            m = folium.Map(location=[coordinates[0][0], coordinates[0][1]], zoom_start=12)

            # Aggiungi le tappe sulla mappa come marcatori
            for coord in coordinates:
                folium.Marker([coord[0], coord[1]]).add_to(m)

            # Crea i percorsi tra le tappe come polyline
            for i in range(len(coordinates) - 1):
                folium.PolyLine(locations=[coordinates[i], coordinates[i+1]], color="blue", weight=2.5, opacity=1).add_to(m)

            # Visualizza la mappa interattiva
            folium_static(m)
        else:
            st.warning("Nessuna coordinata disponibile per le tappe inserite.")

# Funzione per visualizzare la mappa folium in Streamlit
def folium_static(fig, width=700, height=500):
    fig.save("map.html")
    st.components.v1.html(open("map.html", 'r', encoding='utf-8').read(), width=width, height=height)