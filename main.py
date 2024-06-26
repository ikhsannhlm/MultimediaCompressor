import streamlit as st
from Dashboard import dashboard
from Image_Compressor import kompresi_gambar
from Audio_Compressor import kompresi_audio
from Video_Compressor import compress_video_huffman, compress_video_brotli

# Sidebar navigation function
def sidebar():
    st.set_page_config(page_title='Multimedia Compressor')

    with st.sidebar:
        st.title('Kelompok Raventrio')
        st.write(
            """
            - Muhammad Ikhsan Nurhalim - 1217050097
            - Khafka Fadilah Wibawa Nurdiansyah - 1217050072
            - Ansyarullah - 1217050017
            """
        )

        st.title('Compression Menu')
        options = {
            'Dashboard': ' ',
            'Image Compress': ' ',
            'Audio Compress': ' ',
            'Video Compress': ' '
        }

        selected_option = st.selectbox('Choose Menu', list(options.keys()), format_func=lambda x: f'{options[x]} {x}')

    if selected_option == 'Dashboard':
        dashboard()
    elif selected_option == 'Image Compress':
        kompresi_gambar()
    elif selected_option == 'Audio Compress':
        kompresi_audio()
    elif selected_option == 'Video Compress':
        uploaded_file = st.file_uploader("Upload Video", type=['mp4'])
        
        if uploaded_file is not None:
            st.video(uploaded_file)
            method = st.radio("Choose compression method:", ("Huffman Coding", "Brotli Algorithm"))
            
            if st.button("Compress"):
                if method == "Huffman Coding":
                    filename_huffman = compress_video_huffman(uploaded_file)
                    st.write("Huffman compressed file:", filename_huffman)
                    # Implement download button for Huffman compressed file if needed
                elif method == "Brotli Algorithm":
                    filename_brotli = compress_video_brotli(uploaded_file)
                    st.write("Brotli compressed file:", filename_brotli)
                    # Implement download button for Brotli compressed file if needed

# Run the app
if __name__ == '__main__':
    sidebar()
