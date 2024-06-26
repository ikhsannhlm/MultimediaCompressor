import streamlit as st

# Main function for home page
def dashboard():
    st.title('Dashboard')
    st.write("""
    Website ini perbandingan kompresi multimedia file dengan menggunakan Algoritma Huffman dengan Algotritma Brotli. adapun sedikit penjelasan mengenai website ini adalah sebagai berikut:""")
    st.subheader("Algoritma Huffman Coding")
    st.write("adalah algoritma kompresi lossless yang menggunakan frekuensi kemunculan karakter untuk menghasilkan kode biner dengan panjang variabel.")
    st.write(
            """
            Cara kerja:
            - Hitung frekuensi setiap karakter.
            - Bangun pohon Huffman berdasarkan frekuensi, gabungkan node dengan berat terendah.
            - Buat kode biner untuk setiap karakter dari pohon.
            - Gantikan karakter dalam data asli dengan kode biner yang dihasilkan.
            """
        )
    st.subheader("Algoritma Brotli")
    st.write("adalah algoritma kompresi data lossless yang efisien, dikembangkan oleh Google, yang menggunakan kombinasi metode kompresi berbasis LZ77 dan pohon Huffman.")
    st.write(
            """
            Cara kerja:
            - Analisis data untuk menemukan pola berulang.
            - Kompres pola menggunakan LZ77.
            - Gunakan pohon Huffman untuk mengkodekan hasil kompresi LZ77.
            - Hasilnya adalah data terkompresi yang lebih kecil dengan tetap mempertahankan informasi aslinya.
            """
        )