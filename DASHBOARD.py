import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from geopy.distance import geodesic
import math

st.set_page_config(
    page_title="Dashboard Peta",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.sidebar.image("BLUE.png", width=150)
st.sidebar.title("SETTING")

# ===================== RADIUS SPPG =====================
st.sidebar.subheader("RADIUS SPPG")
locations = []
input_mode_sppg = st.sidebar.radio("Pilih cara input SPPG:", ["Manual", "Upload Excel"], key="input_sppg")

if input_mode_sppg == "Manual":
    jumlah_titik = st.sidebar.number_input("Jumlah SPPG", min_value=1, max_value=10, value=1)

    for i in range(jumlah_titik):
        st.sidebar.markdown(f"**SPPG {i + 1}**")
        nama_sppg = st.sidebar.text_input(f"Nama SPPG {i + 1}", value=f"SPPG {i + 1}", key=f"nama_sppg_{i}")
        lat = st.sidebar.number_input(f"Latitude SPPG {i + 1}", value=-2.059939, format="%.6f", key=f"lat_loc_{i}")
        lon = st.sidebar.number_input(f"Longitude SPPG {i + 1}", value=106.1004404, format="%.6f", key=f"lon_loc_{i}")
        radius = st.sidebar.number_input(f"Radius {i + 1} (meter)", min_value=100, max_value=20000, value=6000,
                                         key=f"rad_loc_{i}")
        locations.append((nama_sppg, lat, lon, radius))
else:
    uploaded_file_sppg = st.sidebar.file_uploader("Upload file Excel SPPG (Nama Yayasan, Latitude, Longitude, Radius (M))", type=["xlsx"])
    if uploaded_file_sppg is not None:
        df_sppg = pd.read_excel(uploaded_file_sppg)

        def find_column(df, possible_names):
            for name in df.columns:
                if str(name).strip().lower() in [n.lower() for n in possible_names]:
                    return name
            return None

        lat_col = find_column(df_sppg, ["Latitude", "Lat", "Y"])
        lon_col = find_column(df_sppg, ["Longitude", "Lon", "Long", "X"])
        nama_col = find_column(df_sppg, ["Nama SPPG", "Nama", "Name"])
        radius_col = find_column(df_sppg, ["Radius", "Radius (m)", "Rad"])

        if lat_col and lon_col and radius_col:
            if nama_col:
                locations = list(zip(df_sppg[nama_col], df_sppg[lat_col], df_sppg[lon_col], df_sppg[radius_col]))
            else:
                locations = [(f"SPPG {i + 1}", lat, lon, rad) 
                             for i, (lat, lon, rad) in enumerate(zip(df_sppg[lat_col], df_sppg[lon_col], df_sppg[radius_col]))]
            st.sidebar.success(f"Berhasil membaca {len(locations)} titik SPPG dari Excel")
        else:
            st.sidebar.error("File tidak memiliki kolom Latitude/Longitude/Radius yang valid")

# ===================== TITIK SEKOLAH =====================
st.sidebar.subheader("TITIK SEKOLAH")
markers = []
input_mode = st.sidebar.radio("Pilih cara input titik sekolah:", ["Manual", "Upload Excel"], key="input_marker")

if input_mode == "Manual":
    jumlah_marker = st.sidebar.number_input("Jumlah TITIK Sekolah", min_value=0, max_value=20, value=0)

    for i in range(jumlah_marker):
        st.sidebar.markdown(f"**Sekolah {i + 1}**")
        nama_sekolah = st.sidebar.text_input(f"Nama Sekolah {i + 1}", value=f"Sekolah {i + 1}", key=f"nama_sekolah_{i}")
        lat = st.sidebar.number_input(f"Latitude Sekolah {i + 1}", value=-2.059939, format="%.6f", key=f"lat_mark_{i}")
        lon = st.sidebar.number_input(f"Longitude Sekolah {i + 1}", value=106.1004404, format="%.6f", key=f"lon_mark_{i}")
        markers.append((nama_sekolah, lat, lon))

else:
    uploaded_file = st.sidebar.file_uploader("Upload file Excel (harus ada kolom Latitude & Longitude)", type=["xlsx"])
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)

        def find_column(df, possible_names):
            for name in df.columns:
                if str(name).strip().lower() in [n.lower() for n in possible_names]:
                    return name
            return None

        lat_col = find_column(df, ["Latitude", "Lat", "Lattitude", "Y"])
        lon_col = find_column(df, ["Longitude", "Lon", "Long", "X"])
        nama_col = find_column(df, ["Nama Sekolah", "Nama", "Sekolah", "Name"])

        if lat_col and lon_col:
            if nama_col:
                markers = list(zip(df[nama_col], df[lat_col], df[lon_col]))
            else:
                markers = [(f"Sekolah {i + 1}", lat, lon) for i, (lat, lon) in enumerate(zip(df[lat_col], df[lon_col]))]

            st.sidebar.success(f"Berhasil membaca {len(markers)} titik sekolah dari Excel")
        else:
            st.sidebar.error("File tidak memiliki kolom Latitude/Longitude yang valid")

# ===================== TAMPILKAN PETA =====================
if locations or markers:
    if locations:
        center_lat, center_lon = locations[0][1], locations[0][2]
    else:
        center_lat, center_lon = markers[0][1], markers[0][2]

    m = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles="OpenStreetMap")

    circle_colors = ["cadetblue", "red", "green"]

    # Tambahkan lingkaran SPPG
    for idx, (nama_sppg, lat, lon, radius) in enumerate(locations, start=1):
        color = circle_colors[idx % len(circle_colors)]
        folium.Circle(
            location=[lat, lon],
            radius=radius,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.3,
            popup=f"{nama_sppg} - Radius {radius} m"
        ).add_to(m)

    marker_colors = ["red"]

    # Filter marker sekolah valid
    valid_markers = []
    for nama, lat, lon in markers:
        if lat is not None and lon is not None and not (math.isnan(lat) or math.isnan(lon)):
            valid_markers.append((nama, lat, lon))

    # Tambahkan marker sekolah
    for idx, (nama, lat, lon) in enumerate(valid_markers, start=1):
        color = marker_colors[idx % len(marker_colors)]
        folium.Marker(
            location=[lat, lon],
            popup=f"{nama}",
            icon=folium.Icon(color=color, icon="")
        ).add_to(m)

    st_data = st_folium(m, height=800, use_container_width=True)

    # ===================== HITUNG JARAK =====================
    if valid_markers and locations:
        results = []
        for s_idx, (nama, s_lat, s_lon) in enumerate(valid_markers, start=1):
            for l_idx, (nama_sppg, l_lat, l_lon, l_radius) in enumerate(locations, start=1):
                distance_m = geodesic((s_lat, s_lon), (l_lat, l_lon)).meters
                status = "Dalam Radius" if distance_m <= l_radius else "Luar Radius"
                results.append({
                    "Sekolah": nama,
                    "SPPG": nama_sppg,
                    "Jarak (m)": round(distance_m, 2),
                    "Radius (m)": l_radius,
                    "Status": status
                })

        df_results = pd.DataFrame(results)
        df_dalam_radius = df_results[df_results["Status"] == "Dalam Radius"].reset_index(drop=True)
        df_dalam_radius = df_dalam_radius[["Sekolah", "SPPG", "Jarak (m)"]]

        st.subheader("Semua Jarak Sekolah - SPPG")
        st.dataframe(df_results, use_container_width=True)

        st.subheader("Sekolah Dalam Radius SPPG")
        st.dataframe(df_dalam_radius, use_container_width=True)

# ===================== WATERMARK =====================
st.markdown(
    """
    <style>
    .watermark {
        position: fixed;
        bottom: 45px;
        right: 10px;
        color: gray;
        font-size: 20px;
        opacity: 0.6;
        z-index: 1000;
    }
    </style>
    <div class="watermark">
        © 2025 Hypo Krates
    </div>
    """,
    unsafe_allow_html=True
)

