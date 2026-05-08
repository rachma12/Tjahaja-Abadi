st.markdown("""
<style>
/* Background utama */
.stApp {
    background-color: #b30000;
    color: white;
}

/* Sidebar jadi oranye */
section[data-testid="stSidebar"] {
    background-color: #ff8c00;
}

/* Teks sidebar putih */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Judul dan teks */
h1, h2, h3, p, label {
    color: white !important;
}

/* Tombol */
.stButton > button {
    background-color: #ff8c00;
    color: white;
    border-radius: 10px;
    border: none;
}

/* Input box */
.stTextInput input, 
.stNumberInput input, 
.stSelectbox div {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)
