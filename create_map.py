import streamlit as st
import googlemaps

google_api = 'AIzaSyBs7awZCabHHQm8pHV3mpRFp8W6op0bcWA'

def display_routes_with_google_maps(places_and_modes, api_key=google_api):
    # Initialize the Google Maps client
    gmaps = googlemaps.Client(key=api_key)

    # Create a Streamlit app title
    st.title("Route Planner with Google Maps")

    # Display the list of places and modes in the Streamlit app
    for item in places_and_modes:
        st.write(f"Place: {item['place']}, Mode of Transport: {item['mode']}")

    # Calculate and display routes for each pair of places
    for i in range(len(places_and_modes) - 1):
        from_place = places_and_modes[i]["place"]
        to_place = places_and_modes[i + 1]["place"]
        mode = places_and_modes[i]["mode"]

        # Get directions from Google Maps API
        directions = gmaps.directions(
            from_place,
            to_place,
            mode=mode,
            departure_time="now",
        )

        # Extract the route coordinates from the response
        route = directions[0]["legs"][0]["steps"]
        route_coordinates = [(step["start_location"]["lat"], step["start_location"]["lng"]) for step in route]

        # Display the route on a map using Streamlit
        st.map(route_coordinates)

# # Example usage:
# if __name__ == "__main__":
#     api_key = "YOUR_GOOGLE_MAPS_API_KEY"
#     places_and_modes = [
#         {"place": "Place A", "mode": "driving"},
#         {"place": "Place B", "mode": "walking"},
#         {"place": "Place C", "mode": "transit"},
#         # Add more places and modes as needed
#     ]
#     display_routes_with_google_maps(api_key, places_and_modes)
