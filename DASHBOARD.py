import streamlit as st
import folium
from streamlit_folium import st_folium
from branca.element import Template, MacroElement

st.set_page_config(
    page_title="Dashboard Peta",
    layout="wide",   # wide mode
    initial_sidebar_state="expanded"
)

st.sidebar.title("SETTING")

# -----------------------------
# Bagian untuk RADIUS SPPG (Circle)
# -----------------------------
st.sidebar.subheader("RADIUS SPPG")

locations = []
jumlah_titik = st.sidebar.number_input("Jumlah SPPG", min_value=1, max_value=10, value=1)

for i in range(jumlah_titik):
    st.sidebar.text(f"SPPG {i+1}")
    lat = st.sidebar.number_input(f"Latitude {i+1}", value=-2.059939, format="%.6f", key=f"lat_loc_{i}")
    lon = st.sidebar.number_input(f"Longitude {i+1}", value=106.1004404, format="%.6f", key=f"lon_loc_{i}")
    radius = st.sidebar.number_input(f"Radius {i+1} (meter)", min_value=100, max_value=20000, value=6000, key=f"rad_loc_{i}")
    locations.append((lat, lon, radius))

# -----------------------------
# Bagian untuk TITIK SEKOLAH (Marker)
# -----------------------------
st.sidebar.subheader("TITIK SEKOLAH")

markers = []
jumlah_marker = st.sidebar.number_input("Jumlah TITIK Sekolah", min_value=0, max_value=20, value=0)

for i in range(jumlah_marker):
    st.sidebar.text(f"Sekolah {i+1}")
    lat = st.sidebar.number_input(f"Latitude Sekolah {i+1}", value=-2.059939, format="%.6f", key=f"lat_mark_{i}")
    lon = st.sidebar.number_input(f"Longitude Sekolah {i+1}", value=106.1004404, format="%.6f", key=f"lon_mark_{i}")
    markers.append((lat, lon))

# -----------------------------
# Membuat MAP
# -----------------------------
if locations or markers:
    if locations:
        center_lat, center_lon = locations[0][0], locations[0][1]
    else:
        center_lat, center_lon = markers[0][0], markers[0][1]

    m = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles="OpenStreetMap")

    # Warna untuk Circle
    circle_colors = [
        "red", "blue", "green", "purple", "orange",
        "darkred", "lightred", "beige", "darkblue", "darkgreen",
        "cadetblue", "darkpurple", "pink", "lightblue",
        "lightgreen", "gray", "black", "lightgray"
    ]

    # Tambahkan Circle dengan warna berbeda
    for idx, (lat, lon, radius) in enumerate(locations, start=1):
        color = circle_colors[idx % len(circle_colors)]
        folium.Circle(
            location=[lat, lon],
            radius=radius,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.3,
            popup=f"SPPG {idx} - Radius {radius} m"
        ).add_to(m)

    # Warna untuk Marker
    marker_colors = [
        "red", "blue", "green", "purple", "orange",
        "darkred", "lightred", "beige", "darkblue", "darkgreen",
        "cadetblue", "darkpurple", "white", "pink", "lightblue",
        "lightgreen", "gray", "black", "lightgray"
    ]

    # Tambahkan Marker dengan warna berbeda
    for idx, (lat, lon) in enumerate(markers, start=1):
        color = marker_colors[idx % len(marker_colors)]
        folium.Marker(
            location=[lat, lon],
            popup=f"Sekolah {idx}",
            icon=folium.Icon(color=color, icon="")
        ).add_to(m)

    # Tampilkan peta
    st_data = st_folium(m, height=800, use_container_width=True)
