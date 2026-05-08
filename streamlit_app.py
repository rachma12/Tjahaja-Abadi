import streamlit as st
import pandas as pd
import os

# Konfigurasi halaman
st.set_page_config(
    page_title="Buku Kas Warkop",
    layout="wide",
    page_icon="🍜"
)

FILE_NAME = "laporan_keuangan.csv"

# Styling modern
st.markdown("""
<style>
/* Background utama */
.stApp {
    background: #f5f5f5;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #b30000, #ff4500);
}

/* Teks sidebar */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Header box */
.header-box {
    background: #b30000;
    padding: 20px;
    border-radius: 0px 0px 25px 25px;
    margin-bottom: 20px;
}

/* Card metric */
[data-testid="stMetric"] {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
}

/* Card menu */
.menu-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
}

/* Tombol */
.stButton > button {
    background: linear-gradient(90deg, #ff8c00, #ff4500);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}

/* Input */
.stTextInput input,
.stNumberInput input,
.stSelectbox div {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-box">
    <h1 style="color:white;">TJAHAJA ABADI</h1>
    <p style="color:white;">Buku Kas Digital Warkop</p>
</div>
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
    st.title("📊 Dashboard Keuangan")

    if not df.empty:
        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Pemasukan",
            f"Rp {df['Pemasukan'].sum():,.0f}"
        )
        col2.metric(
            "Total Uang Masuk",
            f"Rp {df['Bayar'].sum():,.0f}"
        )
        col3.metric(
            "Total Kembalian",
            f"Rp {df['Kembalian'].sum():,.0f}"
        )
        col4.metric(
            "Saldo Akhir",
            f"Rp {df['Saldo'].iloc[-1]:,.0f}"
        )
    else:
        st.info("Belum ada transaksi")

# Input transaksi
elif menu_halaman == "Input Transaksi":
    st.title("🧾 Input Transaksi")

    tanggal = st.date_input("Tanggal")
    jam = st.time_input("Jam")

    menu = st.selectbox(
        "Pilih Menu",
        list(menu_list.keys())
    )

    harga = menu_list[menu]

    st.markdown(f"""
    <div class="menu-card">
        <h3>{menu}</h3>
        <p><b>Harga:</b> Rp {harga:,.0f}</p>
    </div>
    """, unsafe_allow_html=True)

    bayar = st.number_input(
        "Uang Dibayar",
        min_value=0,
        step=1000
    )

    selisih = bayar - harga

    if bayar > 0:
        if selisih < 0:
            st.error(
                f"Uang kurang: Rp {abs(selisih):,.0f}"
            )
            kembalian = 0
        else:
            st.success(
                f"Kembalian otomatis: Rp {selisih:,.0f}"
            )
            kembalian = selisih
    else:
        st.info("Masukkan uang bayar")
        kembalian = 0

    if st.button("Simpan"):
        if selisih >= 0:
            saldo_terakhir = (
                df["Saldo"].iloc[-1]
                if not df.empty else 0
            )

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

            df = pd.concat(
                [df, data_baru],
                ignore_index=True
            )

            df.to_csv(FILE_NAME, index=False)

            st.success("Transaksi berhasil disimpan")
        else:
            st.error("Uang bayar belum cukup")

# Laporan harian
elif menu_halaman == "Laporan Harian":
    st.title("📅 Laporan Harian")

    pilih_tanggal = st.date_input(
        "Pilih Tanggal"
    )

    laporan = df[
        df["Tanggal"] == str(pilih_tanggal)
    ]

    if not laporan.empty:
        st.dataframe(laporan)

        st.success(
            f"Total pemasukan: Rp {laporan['Pemasukan'].sum():,.0f}"
        )
    else:
        st.info(
            "Belum ada transaksi di tanggal ini"
        )

# Laporan bulanan
elif menu_halaman == "Laporan Bulanan":
    st.title("📈 Laporan Bulanan")

    if not df.empty:
        df["Tanggal"] = pd.to_datetime(
            df["Tanggal"]
        )

        df["Bulan"] = df["Tanggal"].dt.strftime(
            "%B %Y"
        )

        laporan_bulanan = (
            df.groupby("Bulan")["Pemasukan"]
            .sum()
            .reset_index()
        )

        st.subheader(
            "Rekap Pemasukan per Bulan"
        )

        st.dataframe(laporan_bulanan)

        pilih_bulan = st.selectbox(
            "Pilih Bulan",
            laporan_bulanan["Bulan"].unique()
        )

        detail_bulan = df[
            df["Bulan"] == pilih_bulan
        ]

        st.subheader(
            f"Detail Transaksi {pilih_bulan}"
        )

        st.dataframe(detail_bulan)

        total_bulan = detail_bulan[
            "Pemasukan"
        ].sum()

        st.success(
            f"Total pemasukan bulan ini: Rp {total_bulan:,.0f}"
        )

    else:
        st.info("Belum ada data transaksi")

# Buku kas
elif menu_halaman == "Buku Kas":
    st.title("📒 Buku Kas Digital")

    if not df.empty:
        st.dataframe(df)
    else:
        st.info("Belum ada data")
