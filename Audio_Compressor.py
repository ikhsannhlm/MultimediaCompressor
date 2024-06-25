import numpy as np
import pywt
import wave
import struct
from io import BytesIO
from scipy.fftpack import dct, idct
from pydub import AudioSegment
import tempfile
import os
import streamlit as st
import brotli
import heapq
from collections import defaultdict, Counter

# Fungsi untuk membaca file audio
def read_audio(file_bytes):
    try:
        with wave.open(BytesIO(file_bytes), 'rb') as wav_file:
            params = wav_file.getparams()
            frames = wav_file.readframes(params.nframes)
            audio = np.frombuffer(frames, dtype=np.int16)
        return audio, params
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, None

# Fungsi untuk menulis file audio
def write_audio(audio, params, format='wav'):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_wav_file:
            with wave.open(temp_wav_file.name, 'wb') as wav_file:
                wav_file.setparams(params)
                frames = struct.pack("%dh" % len(audio), *audio)
                wav_file.writeframes(frames)

            # Load temporary WAV file and export to MP3 using pydub
            audio_segment = AudioSegment.from_wav(temp_wav_file.name)
            mp3_filename = temp_wav_file.name.replace('.wav', '.mp3')
            audio_segment.export(mp3_filename, format='mp3')

        # Read the MP3 file back as bytes
        with open(mp3_filename, 'rb') as mp3_file:
            mp3_bytes = mp3_file.read()

        # Remove temporary files
        os.remove(temp_wav_file.name)
        os.remove(mp3_filename)

        return mp3_bytes
    except FileNotFoundError:
        st.error("ffmpeg not found. ensure ffmpeg installed and added to PATH.")
        return None

# Fungsi untuk kompresi audio menggunakan Brotli
def brotli_compress(audio):
    audio_bytes = audio.tobytes()
    compressed_audio = brotli.compress(audio_bytes)
    return compressed_audio

# Fungsi untuk dekompresi audio menggunakan Brotli
def brotli_decompress(compressed_audio, original_length):
    decompressed_audio_bytes = brotli.decompress(compressed_audio)
    decompressed_audio = np.frombuffer(decompressed_audio_bytes, dtype=np.int16)
    return decompressed_audio[:original_length]

# Huffman coding functions
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(freq):
    heap = [HuffmanNode(char, freq) for char, freq in freq.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)
    
    return heap[0]

def generate_huffman_codes(node, code, codes):
    if node:
        if node.char is not None:
            codes[node.char] = code
        generate_huffman_codes(node.left, code + '0', codes)
        generate_huffman_codes(node.right, code + '1', codes)

def huffman_compress(audio_bytes):
    freq = Counter(audio_bytes)
    huffman_tree = build_huffman_tree(freq)
    huffman_codes = {}
    generate_huffman_codes(huffman_tree, '', huffman_codes)

    encoded_audio = ''.join(huffman_codes[byte] for byte in audio_bytes)
    padded_encoded_audio = encoded_audio + '0' * (8 - len(encoded_audio) % 8)
    b = bytearray()
    for i in range(0, len(padded_encoded_audio), 8):
        byte = padded_encoded_audio[i:i+8]
        b.append(int(byte, 2))

    return b, huffman_tree

def huffman_decompress(encoded_audio, tree, original_length):
    encoded_bits = ''.join(f'{byte:08b}' for byte in encoded_audio)
    decoded_audio = []
    node = tree

    for bit in encoded_bits:
        if bit == '0':
            node = node.left
        else:
            node = node.right

        if node.char is not None:
            decoded_audio.append(node.char)
            node = tree

        if len(decoded_audio) == original_length:
            break

    return bytearray(decoded_audio)

# Fungsi untuk menampilkan tombol unduh
def download_button(data_bytes, file_name, mime_type):
    st.download_button(
        label=f"Unduh {file_name}",
        data=data_bytes,
        file_name=file_name,
        mime=mime_type
    )

# Fungsi utama kompresi audio
def kompresi_audio():
    st.title('Audio Compressor')
    st.write("Compress your WAV file with Brotli Algorithm or Huffman Algorithm.")

    uploaded_file = st.file_uploader("Pick Audio WAV file", type=["wav"], accept_multiple_files=False)

    if uploaded_file is not None:
        st.write('File uploaded:', uploaded_file.name)

        audio, params = read_audio(uploaded_file.read())

        if audio is None or params is None:
            return

        algorithm = st.selectbox("Choose Algorithm:", ["Huffman", "Brotli"])

        if st.button('Compress'):
            if algorithm == "Huffman":
                compressed_audio, tree = huffman_compress(audio.tobytes())
                decompressed_audio = huffman_decompress(compressed_audio, tree, len(audio))
                compressed_audio = decompressed_audio
                file_name = "compressed_audio_huffman.wav"
            elif algorithm == "Brotli":
                compressed_audio = brotli_compress(audio)
                decompressed_audio = brotli_decompress(compressed_audio, len(audio))
                compressed_audio = decompressed_audio
                file_name = "compressed_audio_brotli.wav"

            compressed_audio_bytes = write_audio(compressed_audio, params, format='mp3')
            if compressed_audio_bytes:
                st.audio(compressed_audio_bytes, format='audio/mp3', start_time=0)

                st.download_button(
                    label="Download Comrpessed Audio",
                    data=compressed_audio_bytes,
                    file_name=file_name.replace('.wav', '.mp3'),
                    mime="audio/mp3"
                )
                st.success(f"Compress Audio Success! File saved as {file_name.replace('.wav', '.mp3')}")

if __name__ == "__main__":
    kompresi_audio()
