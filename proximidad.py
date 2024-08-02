import numpy as np
from scipy.spatial import KDTree
import folium
from geopy.distance import geodesic

# Coordenadas de las sucursales en Puno
branches = np.array([
    [-15.840221, -70.021881],  # Sucursal 1
    [-15.839005, -70.012345],  # Sucursal 2
    [-15.834678, -70.016947],  # Sucursal 3
    [-15.835123, -70.030456],  # Sucursal 4
    [-15.829876, -70.020134]   # Sucursal 5
])

# Coordenada del cliente en Puno
customer_location = np.array([-15.837833, -70.019851])

# Crear el kd-tree con las coordenadas de las sucursales
tree = KDTree(branches)

# Definir un radio (en kilómetros)
radius_km = 1.0

# Encontrar las sucursales dentro del radio
indices_within_radius = tree.query_ball_point(customer_location, radius_km / 6371.0)  # Dividido por el radio de la Tierra en km

# Crear un mapa centrado en la ubicación del cliente
m = folium.Map(location=customer_location.tolist(), zoom_start=15)

# Añadir la ubicación del cliente al mapa
folium.Marker(
    location=customer_location.tolist(),
    popup='Cliente',
    icon=folium.Icon(color='red')
).add_to(m)

# Añadir un círculo de radio alrededor del cliente
folium.Circle(
    radius=radius_km * 1000,  # Conversión a metros
    location=customer_location.tolist(),
    popup='Radio de búsqueda',
    color='blue',
    fill=True,
    fill_color='blue'
).add_to(m)

# Añadir las sucursales al mapa
for idx, branch in enumerate(branches):
    folium.Marker(
        location=branch.tolist(),
        popup=f'Sucursal {idx + 1}',
        icon=folium.Icon(color='blue' if idx in indices_within_radius else 'gray')
    ).add_to(m)

# Mostrar el mapa
m.save('mapa_sucursales.html')
m

