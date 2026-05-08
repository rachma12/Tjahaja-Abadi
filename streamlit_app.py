import streamlit as st
import pandas as pd
import os

# =========================
# LOGIN SYSTEM
# =========================
PASSWORD = "cahyadi_sejahtera"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Halaman login
if not st.session_state.authenticated:
    st.set_page_config(
        page_title="Login Buku Kas",
        layout="centered",
        page_icon="🔐"
    )

    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg,#8b0000,#d62828);
    }

    .login-box {
        background: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.2);
        margin-top: 100px;
    }

    .stButton > button {
        width: 100%;
        height: 50px;
        background: linear-gradient(90deg,#ff8c00,#ff4500);
        color: white;
        border-radius: 12px;
        border: none;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-box">
        <h1 style="text-align:center;">🔐 Login Buku Kas</h1>
        <p style="text-align:center;">
        Masukkan kode akses untuk membuka laporan keuangan
        </p>
    </div>
    """, unsafe_allow_html=True)

    password_input = st.text_input(
        "Kode Akses",
        type="password"
    )

    if st.button("Masuk"):
        if password_input == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Kode akses salah")

    st.stop()

# =========================
# MAIN APP
# =========================
st.set_page_config(
    page_title="Buku Kas Warkop",
    layout="wide",
    page_icon="🍜"
)

FILE_NAME = "laporan_keuangan.csv"

# Styling premium
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(180deg,#fff5f5,#ffeaea);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#8b0000,#d62828);
    padding-top: 20px;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Header */
.header-box {
    background: linear-gradient(90deg,#8b0000,#d62828);
    padding: 25px;
    border-radius: 20px;
    margin-bottom: 25px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

/* Dashboard Card */
[data-testid="stMetric"] {
    background: white;
    padding: 20px;
    border-radius: 20px;
    border-left: 8px solid #ff8c00;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.1);
}

/* Menu Card */
.menu-card {
    background: white;
    padding: 25px;
    border-radius: 20px;
    margin-bottom: 20px;
    border-left: 8px solid #d62828;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.08);
}

/* Button */
.stButton > button {
    width: 100%;
    height: 50px;
    background: linear-gradient(90deg,#ff8c00,#ff4500);
    color: white;
    border-radius: 15px;
    font-size: 18px;
    font-weight: bold;
    border: none;
}

/* Input */
.stTextInput input,
.stNumberInput input,
.stSelectbox div {
    border-radius: 12px;
    border: 2px solid #ff8c00;
}

/* Table */
div[data-testid="stDataFrame"] {
    background: white;
    border-radius: 20px;
    padding: 10px;
}

/* Alert */
.stSuccess, .stError, .stInfo {
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-box">
    <h1 style="color:white;">🍜 TJAHAJA ABADI</h1>
    <p style="color:white; font-size:18px;">
    Buku Kas Digital • Self Order • Laporan Keuangan
    </p>
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

# Sidebar menu
menu_halaman = st.sidebar.radio(
    "📌 Menu Navigasi",
    [
        "Dashboard",
        "Input Transaksi",
        "Laporan Harian",
        "Laporan Bulanan",
        "Buku Kas"
    ]
)

# Logout button
if st.sidebar.button("🚪 Logout"):
    st.session_state.authenticated = False
    st.rerun()

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

# DASHBOARD
if menu_halaman == "Dashboard":
    st.title("📊 Dashboard Keuangan")

    if not df.empty:
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        col1.metric("Total Pemasukan", f"Rp {df['Pemasukan'].sum():,.0f}")
        col2.metric("Total Uang Masuk", f"Rp {df['Bayar'].sum():,.0f}")
        col3.metric("Total Kembalian", f"Rp {df['Kembalian'].sum():,.0f}")
        col4.metric("Saldo Akhir", f"Rp {df['Saldo'].iloc[-1]:,.0f}")
    else:
        st.info("Belum ada transaksi")

# INPUT TRANSAKSI
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
        <h2>{menu}</h2>
        <h3 style="color:#d62828;">
            Rp {harga:,.0f}
        </h3>
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
            st.error(f"Uang kurang: Rp {abs(selisih):,.0f}")
            kembalian = 0
        else:
            st.success(f"Kembalian otomatis: Rp {selisih:,.0f}")
            kembalian = selisih
    else:
        st.info("Masukkan uang bayar")
        kembalian = 0

    if st.button("💾 Simpan Transaksi"):
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

            df = pd.concat(
                [df, data_baru],
                ignore_index=True
            )

            df.to_csv(FILE_NAME, index=False)

            st.success("Transaksi berhasil disimpan")
        else:
            st.error("Uang bayar belum cukup")

# LAPORAN HARIAN
elif menu_halaman == "Laporan Harian":
    st.title("📅 Laporan Harian")

    pilih_tanggal = st.date_input("Pilih Tanggal")

    laporan = df[df["Tanggal"] == str(pilih_tanggal)]

    if not laporan.empty:
        st.dataframe(laporan)
        total_harian = laporan["Pemasukan"].sum()

        st.success(
            f"Total pemasukan: Rp {total_harian:,.0f}"
        )
    else:
        st.info("Belum ada transaksi di tanggal ini")

# LAPORAN BULANAN
elif menu_halaman == "Laporan Bulanan":
    st.title("📈 Laporan Bulanan")

    if not df.empty:
        df["Tanggal"] = pd.to_datetime(df["Tanggal"])
        df["Bulan"] = df["Tanggal"].dt.strftime("%B %Y")

        laporan_bulanan = (
            df.groupby("Bulan")["Pemasukan"]
            .sum()
            .reset_index()
        )

        st.dataframe(laporan_bulanan)

        pilih_bulan = st.selectbox(
            "Pilih Bulan",
            laporan_bulanan["Bulan"].unique()
        )

        detail_bulan = df[df["Bulan"] == pilih_bulan]

        st.dataframe(detail_bulan)

        total_bulan = detail_bulan["Pemasukan"].sum()

        st.success(
            f"Total pemasukan bulan ini: Rp {total_bulan:,.0f}"
        )
    else:
        st.info("Belum ada data transaksi")

# BUKU KAS
elif menu_halaman == "Buku Kas":
    st.title("📒 Buku Kas Digital")

    if not df.empty:
        st.dataframe(df)
    else:
        st.info("Belum ada data")
