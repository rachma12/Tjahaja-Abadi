import streamlit as st
import pandas as pd
import os

# Konfigurasi halaman
st.set_page_config(page_title="Buku Kas Warkop", layout="wide")

FILE_NAME = "laporan_keuangan.csv"

# Styling tema merah + sidebar oranye
st.markdown("""
<style>
.stApp {
    background-color: #b30000;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #ff8c00;
}

h1, h2, h3, p, label, div {
    color: white !important;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.stButton > button {
    background-color: #ff8c00;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px;
}

.stTextInput input,
.stNumberInput input,
.stSelectbox div {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# Load data
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
else:
    df = pd.DataFrame(columns=[
        "Tanggal", "Jam", "Keterangan",
        "Pemasukan", "Bayar", "Kembalian", "Saldo"
    ])

# Sidebar navigasi
menu_halaman = st.sidebar.radio(
    "Pilih Halaman",
    [
        "Dashboard",
        "Input Transaksi",
        "Laporan Harian",
        "Laporan Bulanan",
        "Buku Kas"
    ]
)

# Data menu
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

# Dashboard
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

# Input transaksi
elif menu_halaman == "Input Transaksi":
    st.title("Input Transaksi")

    tanggal = st.date_input("Tanggal")
    jam = st.time_input("Jam")
    menu = st.selectbox("Pilih Menu", list(menu_list.keys()))

    harga = menu_list[menu]
    bayar = st.number_input("Uang Dibayar", min_value=0, step=1000)

    selisih = bayar - harga

    if bayar > 0:
        kembalian = selisih
    else:
        kembalian = 0

    st.write(f"Harga: Rp {harga:,.0f}")

    if bayar == 0:
        st.info("Masukkan uang bayar")
    elif selisih < 0:
        st.error(f"Uang kurang: Rp {abs(selisih):,.0f}")
    else:
        st.success(f"Kembalian otomatis: Rp {kembalian:,.0f}")

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

# Laporan harian
elif menu_halaman == "Laporan Harian":
    st.title("Laporan Harian")

    pilih_tanggal = st.date_input("Pilih Tanggal")
    laporan = df[df["Tanggal"] == str(pilih_tanggal)]

    if not laporan.empty:
        st.dataframe(laporan)
        st.write(f"Total pemasukan: Rp {laporan['Pemasukan'].sum():,.0f}")
    else:
        st.info("Belum ada transaksi di tanggal ini")

# Laporan bulanan
elif menu_halaman == "Laporan Bulanan":
    st.title("Laporan Bulanan")

    if not df.empty:
        df["Tanggal"] = pd.to_datetime(df["Tanggal"])
        df["Bulan"] = df["Tanggal"].dt.strftime("%B %Y")

        laporan_bulanan = df.groupby("Bulan")["Pemasukan"].sum().reset_index()

        st.subheader("Rekap Pemasukan per Bulan")
        st.dataframe(laporan_bulanan)

        pilih_bulan = st.selectbox(
            "Pilih Bulan",
            laporan_bulanan["Bulan"].unique()
        )

        detail_bulan = df[df["Bulan"] == pilih_bulan]

        st.subheader(f"Detail Transaksi {pilih_bulan}")
        st.dataframe(detail_bulan)

        total_bulan = detail_bulan["Pemasukan"].sum()
        st.success(f"Total pemasukan bulan ini: Rp {total_bulan:,.0f}")

    else:
        st.info("Belum ada data transaksi")

# Buku kas
elif menu_halaman == "Buku Kas":
    st.title("Buku Kas Digital")

    if not df.empty:
        st.dataframe(df)
    else:
        st.info("Belum ada data")
