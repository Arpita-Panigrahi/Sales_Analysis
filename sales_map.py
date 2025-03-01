import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from folium.features import DivIcon

# Sample data for US cities with coordinates and sales
city_data = pd.DataFrame({
    'city': ['San Francisco', 'Los Angeles', 'New York', 'Boston', 'Atlanta',
             'Dallas', 'Chicago', 'Portland', 'Austin', 'Seattle'],
    'lat': [37.7749, 34.0522, 40.7128, 42.3601, 33.7490,
            32.7767, 41.8781, 45.5152, 30.2672, 47.6062],
    'lon': [-122.4194, -118.2437, -74.0060, -71.0589, -84.3880,
            -96.7970, -87.6298, -122.6784, -97.7431, -122.3321],
    'sales_millions': [8.2, 5.7, 4.8, 3.9, 3.1, 2.8, 2.5, 2.2, 1.9, 1.7]
})

# Create a base map centered on the US
map_center = [39.8283, -98.5795]  # Approximate center of USA
us_map = folium.Map(location=map_center, zoom_start=4, 
                    tiles='cartodbpositron')

# Add a heatmap layer
heat_data = [[row['lat'], row['lon'], row['sales_millions']] for idx, row in city_data.iterrows()]
HeatMap(heat_data, radius=35, blur=25, max_zoom=13).add_to(us_map)

# Add markers for each city with sales information
for idx, row in city_data.iterrows():
    # Scale marker size based on sales
    marker_size = 20 + (row['sales_millions'] * 3)
    
    # Create a tooltip with city and sales info
    tooltip = f"{row['city']}: ${row['sales_millions']}M"
    
    # Add a circle marker
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=marker_size,
        color='#4E79A7',
        fill=True,
        fill_color='#4E79A7',
        fill_opacity=0.7,
        tooltip=tooltip,
        popup=f"<strong>{row['city']}</strong><br>Sales: ${row['sales_millions']}M"
    ).add_to(us_map)
    
    # Add city labels for top 5 cities
    if idx < 5:
        folium.map.Marker(
            [row['lat'], row['lon']],
            icon=DivIcon(
                icon_size=(150,36),
                icon_anchor=(75,0),
                html=f'<div style="font-size: 12pt; color: black; font-weight: bold; text-shadow: 1px 1px 1px white;">{row["city"]}</div>'
            )
        ).add_to(us_map)

# Add a choropleth layer for state-level analysis (if we had state data)
# This is a placeholder - you'd need state-level sales data to implement

# Add a title
title_html = '''
    <h3 align="center" style="font-size:16px">
        <b>Geographic Distribution of Sales</b>
    </h3>
'''
us_map.get_root().html.add_child(folium.Element(title_html))

# Save the map
us_map.save('sales_geographic_distribution.html')
