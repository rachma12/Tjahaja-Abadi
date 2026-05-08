import streamlit as st
import pandas as pd
import os

FILE_NAME = "data_keuangan.csv"

st.title("Sistem Keuangan Warkop Tjahaja Abadi")

# Load data
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
else:
    df = pd.DataFrame(columns=["Tanggal", "Jenis", "Keterangan", "Nominal"])

# Form input
tanggal = st.date_input("Tanggal")
jenis = st.selectbox("Jenis Transaksi", ["Pemasukan", "Pengeluaran"])
keterangan = st.text_input("Keterangan")
nominal = st.number_input("Nominal", min_value=0)

# Tombol simpan
if st.button("Simpan"):
    data_baru = pd.DataFrame({
        "Tanggal": [tanggal],
        "Jenis": [jenis],
        "Keterangan": [keterangan],
        "Nominal": [nominal]
    })

    df = pd.concat([df, data_baru], ignore_index=True)
    df.to_csv(FILE_NAME, index=False)

    st.success("Transaksi berhasil disimpan!")

# Dashboard
if not df.empty:
    pemasukan = df[df["Jenis"] == "Pemasukan"]["Nominal"].sum()
    pengeluaran = df[df["Jenis"] == "Pengeluaran"]["Nominal"].sum()
    saldo = pemasukan - pengeluaran

    st.subheader("Dashboard")
    st.write("Total Pemasukan: Rp", pemasukan)
    st.write("Total Pengeluaran: Rp", pengeluaran)
    st.write("Saldo Akhir: Rp", saldo)

    st.subheader("Riwayat Transaksi")
    st.dataframe(df)
else:
    st.info("Belum ada data transaksi.")
