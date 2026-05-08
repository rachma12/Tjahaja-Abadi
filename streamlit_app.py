import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Buku Kas Warkop", layout="wide")

FILE_NAME = "laporan_keuangan.csv"

# Styling warna merah
st.markdown('''
<style>
.stApp {
    background-color: #b30000;
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
</style>
''', unsafe_allow_html=True)

# Load data
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
else:
    df = pd.DataFrame(columns=[
        "Tanggal", "Jam", "Keterangan",
        "Pemasukan", "Bayar", "Kembalian", "Saldo"
    ])

# Sidebar navigasi (multi halaman)
menu_halaman = st.sidebar.radio(
    "Pilih Halaman",
    ["Dashboard", "Input Transaksi", "Laporan Harian", "Buku Kas"]
)

# Menu makanan
menu_list = {
    "Mie Dok Dok": 17000,
    "Mie Habib": 17000,
    "Mie Bangladesh": 20000,
    "Mie Carbonara": 20000,
    "Mie Ramen": 18000,
    "Kentang Goreng": 10000,
    "Mix Platter": 15000,
    "Dimsum Tjahyadi": 15000,
    "Nasi Dadar Cryspi": 13000,
    "Magelangan": 20000,
    "Roti Bakar Susu": 10000,
    "Kopi Susu Tjahyadi": 20000,
    "Teh Manis": 7000,
    "Air Mineral": 5000
}

# HALAMAN DASHBOARD
if menu_halaman == "Dashboard":
    st.title("Dashboard Keuangan Warkop Tjahaja Abadi")

    if not df.empty:
        total_pemasukan = df["Pemasukan"].sum()
        total_bayar = df["Bayar"].sum()
        total_kembalian = df["Kembalian"].sum()
        saldo_akhir = df["Saldo"].iloc[-1]

        st.metric("Total Pemasukan", f"Rp {total_pemasukan:,.0f}")
        st.metric("Total Uang Masuk", f"Rp {total_bayar:,.0f}")
        st.metric("Total Kembalian", f"Rp {total_kembalian:,.0f}")
        st.metric("Saldo Akhir", f"Rp {saldo_akhir:,.0f}")
    else:
        st.info("Belum ada transaksi")

# HALAMAN INPUT TRANSAKSI
elif menu_halaman == "Input Transaksi":
    st.title("Input Transaksi")

    tanggal = st.date_input("Tanggal")
    jam = st.time_input("Jam")
    menu = st.selectbox("Pilih Menu", list(menu_list.keys()))

    harga = menu_list[menu]
    bayar = st.number_input("Uang Dibayar", min_value=0, step=1000)

    # Kalkulator otomatis (real-time)
    selisih = bayar - harga

    # Hitung kembalian otomatis
    if bayar > 0:
        kembalian = selisih
    else:
        kembalian = 0

    st.write(f"Harga: Rp {harga:,.0f}")

    if bayar == 0:
        st.info("Masukkan uang bayar untuk menghitung otomatis")
    elif selisih < 0:
        st.error(f"Uang kurang: Rp {abs(selisih):,.0f}")
    else:
        st.success(f"Kembalian otomatis: Rp {kembalian:,.0f}")

    # Simpan transaksi
    if st.button("Simpan"):
        if selisih >= 0:
            saldo_terakhir = df["Saldo"].iloc[-1] if not df.empty else 0
            saldo_baru = saldo_terakhir + harga

            data_baru = pd.DataFrame({
                "Tanggal": [tanggal],
                "Jam": [jam],
                "Keterangan": [menu],
                "Pemasukan": [harga],
                "Bayar": [bayar],
                "Kembalian": [kembalian],
                "Saldo": [saldo_baru]
            })

            df = pd.concat([df, data_baru], ignore_index=True)
            df.to_csv(FILE_NAME, index=False)

            st.success("Transaksi berhasil disimpan")
        else:
            st.error("Uang bayar belum cukup")

# HALAMAN LAPORAN HARIAN
elif menu_halaman == "Laporan Harian":
    st.title("Laporan Harian")

    pilih_tanggal = st.date_input("Pilih Tanggal")
    laporan = df[df["Tanggal"] == str(pilih_tanggal)]

    if not laporan.empty:
        st.dataframe(laporan)
        st.write(
            f"Total pemasukan: Rp {laporan['Pemasukan'].sum():,.0f}"
        )
    else:
        st.info("Belum ada transaksi di tanggal ini")

# HALAMAN BUKU KAS
elif menu_halaman == "Buku Kas":
    st.title("Buku Kas Digital")

    if not df.empty:
        st.dataframe(df)
    else:
        st.info("Belum ada data")
