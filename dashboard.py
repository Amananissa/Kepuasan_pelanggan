# ===============================
# Dashboard Kepuasan Pelanggan POPUP
# Dibuat dengan Streamlit + Plotly
# ===============================

import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Konfigurasi Halaman
# -------------------------------
st.set_page_config(page_title="Dashboard Kepuasan Pelanggan", layout="wide")

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("jawaban.csv", sep=",", encoding="utf-8", on_bad_lines="skip")
    return df


df = load_data()

# -------------------------------
# Header Dashboard
# -------------------------------
st.title("📊 Dashboard Kepuasan Pelanggan POPUP")
st.markdown("Dashboard ini menampilkan hasil survei kepuasan pelanggan terhadap layanan POPUP.")

st.divider()

# -------------------------------
# Bagian 1: Statistik Utama
# -------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Responden", len(df))

with col2:
    mean_score = df['kepuasan'].value_counts(normalize=True).max() * 100
    st.metric("Persentase Kepuasan Tertinggi", f"{mean_score:.1f}%")

with col3:
    if 'alamat' in df.columns:
        st.metric("Jumlah Kota Terdata", df['alamat'].nunique())

st.divider()

# -------------------------------
# Bagian 2: Visualisasi Umum
# -------------------------------
st.subheader("📈 Distribusi Kepuasan Pelanggan")

tab1, tab2 = st.tabs(["Bar Chart", "Pie Chart"])

with tab1:
    fig_bar = px.bar(df, x='kepuasan', color='kepuasan',
                     title="Distribusi Tingkat Kepuasan Pelanggan",
                     color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    fig_pie = px.pie(df, names='kepuasan', hole=0.3,
                     title="Persentase Kepuasan Pelanggan",
                     color_discrete_sequence=px.colors.qualitative.Safe)
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# -------------------------------
# Bagian 3: Filter Berdasarkan Kota
# -------------------------------
if 'alamat' in df.columns:
    st.subheader("📍 Analisis Berdasarkan Kota")
    kota_list = df['alamat'].dropna().unique()
    kota = st.selectbox("Pilih Kota:", kota_list)
    filtered = df[df['alamat'] == kota]

    st.write(f"Jumlah responden dari **{kota}**: {len(filtered)}")

    fig_kota = px.histogram(filtered, x='kepuasan', color='kepuasan',
                            title=f"Tingkat Kepuasan Pelanggan di {kota}",
                            color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_kota, use_container_width=True)

st.divider()

# -------------------------------
# Bagian 4: Tabel Data
# -------------------------------
st.subheader("🧾 Data Responden (Preview)")
st.dataframe(df, use_container_width=True)

# -------------------------------
# Bagian 5: Insight Otomatis
# -------------------------------
st.divider()
st.subheader("💡 Insight Otomatis")

dominant = df['kepuasan'].value_counts().idxmax()
persentase = df['kepuasan'].value_counts(normalize=True).max() * 100
st.markdown(f"- Mayoritas pelanggan merasa **{dominant}** dengan persentase **{persentase:.2f}%**.")
if 'alamat' in df.columns:
    top_city = df['alamat'].value_counts().idxmax()
    st.markdown(f"- Kota dengan respon terbanyak: **{top_city}**.")
st.markdown("- Tingkat kepuasan keseluruhan dapat dijadikan indikator kualitas layanan POPUP saat ini.")
