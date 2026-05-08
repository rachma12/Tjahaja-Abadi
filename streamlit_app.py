import streamlit as st
import pandas as pd
import os
from datetime import datetime

FILE_NAME = "laporan_keuangan.csv"

st.title("Buku Kas Digital Warkop Tjahaja Abadi")
st.markdown("### Buku kas harian untuk mencatat pemasukan seperti buku keuangan manual")

# Load data
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
else:
    df = pd.DataFrame(columns=[
        "Tanggal", "Jam", "Keterangan", "Pemasukan", "Bayar", "Kembalian", "Saldo"
    ])

# Input transaksi
st.subheader("Input Transaksi")

tanggal = st.date_input("Tanggal")
jam = st.time_input("Jam")
menu = st.text_input("Keterangan Transaksi")
harga = st.number_input("Harga", min_value=0)
bayar = st.number_input("Uang Dibayar", min_value=0)

kembalian = bayar - harga if bayar >= harga else 0

st.write("Kembalian:", kembalian)

if st.button("Simpan Transaksi"):
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

# Kalender laporan
st.subheader("Laporan Berdasarkan Tanggal")

if not df.empty:
    pilih_tanggal = st.date_input("Pilih tanggal laporan")

    laporan_harian = df[df["Tanggal"] == str(pilih_tanggal)]

    if not laporan_harian.empty:
        total_pemasukan = laporan_harian["Pemasukan"].sum()
        total_bayar = laporan_harian["Bayar"].sum()
        total_kembalian = laporan_harian["Kembalian"].sum()

        st.write("Total Pemasukan:", total_pemasukan)
        st.write("Total Uang Masuk:", total_bayar)
        st.write("Total Kembalian:", total_kembalian)

        st.dataframe(laporan_harian)
    else:
        st.info("Belum ada transaksi di tanggal ini")

# Riwayat lengkap
st.subheader("Buku Kas (Riwayat Transaksi)")
st.markdown("Format dibuat seperti buku kas: tanggal, jam, keterangan, pemasukan, uang bayar, kembalian, dan saldo berjalan.")
if not df.empty:
    st.dataframe(df)
else:
    st.info("Belum ada data transaksi")
