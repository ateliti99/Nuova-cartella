import streamlit as st
import datetime

from geopy.geocoders import Nominatim
from prompt_generator import generate_prompt
from geopath import create_map, folium_static
from create_map import display_routes_with_google_maps

# Title of the app
st.title("Travel Buddy App")

with st.container():
    # Location
    address = st.text_input('Where are you starting from?', '')
    geocode_button = st.button('Check Location')
    geolocator = Nominatim(user_agent="TravelBuddyApp")
    if geocode_button:
        if address:
            location = geolocator.geocode(address)
            if not location:
                st.error('Error: Location not found.')
        else:
            st.error('Error: Please enter a location.')     
    
    
    # Add a text area and save the input to a variable
    txt = st.text_area('Tell me about you', 'Write here...')
    
    # Filters container
    with st.container():
        # Transport filters
        transportation = st.selectbox(
            'How would you like to move?',
            ('walking', 'bicycling', 'transit', 'sharing vehicle', 'driving'))

        # People filters
        people = st.slider('How many people are you?', 1, 10, 1)
        age = []
        for person in range(people):
            age.append(st.number_input(f'Age of person {person+1}', 1, 100, 18))
        
        # Date filters
        col1, col2 = st.columns(2)
        with col1:
            arrival_date = st.date_input('Arriving', 
                                         min_value=datetime.date.today(), 
                                         max_value=None)
        with col2:
            departure_date = st.date_input('Departure', 
                                         min_value=None, 
                                         max_value=None)
        if arrival_date > departure_date:
            st.error('Error: Departure date must fall after arrival date.')
            
        # Active Timeslot filters
        col1, col2 = st.columns(2)
        with col1:
            start_time = st.time_input('Start Time', datetime.time(8, 45))
        with col2:
            end_time = st.time_input('End Time', datetime.time(17, 45))
        if start_time > end_time:
            st.error('Error: End time must fall after start time.')
            
        # Budget filters
        col1, col2 = st.columns(2)
        with col1:
            free_checkbox = st.checkbox('Free', value=True)
            if not free_checkbox:
                    budget = st.number_input('Budget', 0, 1000, 0)
                    
with st.container():
    col1, col2, col3 = st.columns(3)
    s = None
    with col2:
        generate_itinerary_button = st.button('Generate Itinerary')
        if generate_itinerary_button:
            travel_info = {
                'transportation': transportation,
                'number_of_people': people,
                'age': age,
                'arrival_date': arrival_date.strftime("%Y-%m-%d"),
                'departure_date': departure_date.strftime("%Y-%m-%d"),
                'start_time': start_time.strftime("%H:%M"),
                'end_time': end_time.strftime("%H:%M"),
                'budget': budget if not free_checkbox else 0
            }
            s = generate_prompt(travel_info, txt)
    
with st.container():
    if s:
        st.write(s)
    # Create the map
    #create_map(s)
    import streamlit as st
    import folium
    import osmnx as ox
    
    # Create a Streamlit app title
    st.title("Route Between Multiple Locations")

    # Define coordinates for multiple locations
    locations = [
        {"name": "Location 1", "lat": 40.7128, "lon": -74.0060},
        {"name": "Location 2", "lat": 34.0522, "lon": -118.2437},
        {"name": "Location 3", "lat": 51.5074, "lon": -0.1278},
        # Add more locations as needed
    ]

    # Choose a transportation mode (e.g., 'car', 'bike', 'foot')
    transport_mode = 'car'

    # Create a Folium map centered on a specific location (e.g., Location 1)
    m = folium.Map(location=[locations[0]['lat'], locations[0]['lon']], zoom_start=10)

    # Add markers for each location
    for location in locations:
        folium.Marker([location['lat'], location['lon']], tooltip=location['name']).add_to(m)

    # Calculate and add a route between locations using osmnx
    for i in range(len(locations) - 1):
        start_coords = (locations[i]['lat'], locations[i]['lon'])
        end_coords = (locations[i + 1]['lat'], locations[i + 1]['lon'])
        
        # Calculate the route using osmnx
        graph = ox.graph_from_point(start_coords, distance=500, network_type=transport_mode)
        route = ox.shortest_path(graph, start_coords, end_coords, weight='length')
        
        # Convert the route to a list of coordinates
        route_coords = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in route]
        
        # Add the route to the Folium map
        folium.PolyLine(locations=route_coords, color="blue").add_to(m)

    # Display the Folium map in Streamlit
    folium_static(m)