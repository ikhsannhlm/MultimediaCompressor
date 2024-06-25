import cv2
import numpy as np
import streamlit as st
from PIL import Image
from io import BytesIO
import brotli

# Function to compress image using Brotli
def compress_image_brotli(image, quality=50):
    image_bytes = cv2.imencode('.jpg', image)[1].tobytes()
    compressed_image = brotli.compress(image_bytes, quality=quality)
    return compressed_image

# Function to decompress image using Brotli
def decompress_image_brotli(compressed_image):
    decompressed_image_bytes = brotli.decompress(compressed_image)
    decompressed_image = cv2.imdecode(np.frombuffer(decompressed_image_bytes, np.uint8), cv2.IMREAD_COLOR)
    return decompressed_image

# Function to calculate frequency of bytes in image
def calculate_byte_frequency(image):
    image_bytes = cv2.imencode('.png', image)[1].tobytes()
    freq = {}
    for byte in image_bytes:
        if byte in freq:
            freq[byte] += 1
        else:
            freq[byte] = 1
    return freq

# Function to build Huffman tree from frequency dictionary
def build_huffman_tree(freq):
    nodes = [(f, c) for c, f in freq.items()]
    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda x: x[0])
        f1, char1 = nodes.pop(0)
        f2, char2 = nodes.pop(0)
        merged_node = (f1 + f2, {'0': char1, '1': char2})
        nodes.append((merged_node[0], merged_node[1]))
    return nodes[0][1]

# Function to generate Huffman codes from Huffman tree
def generate_huffman_codes(tree, prefix=''):
    codes = {}

    def _generate_codes(node, prefix=''):
        if isinstance(node, dict):
            for k, v in node.items():
                _generate_codes(v, prefix + k)
        else:
            codes[node] = prefix

    _generate_codes(tree)
    return codes

# Function to encode image using Huffman codes
def encode_image(image, codes):
    image_bytes = cv2.imencode('.png', image)[1].tobytes()
    encoded_image = ''.join(codes[byte] for byte in image_bytes)
    return encoded_image

# Function to decode image using Huffman tree
def decode_image(encoded_image, huffman_tree):
    decoded_image = []
    node = huffman_tree

    for bit in encoded_image:
        if bit == '0':
            node = node['0']  # Traverse left child
        elif bit == '1':
            node = node['1']  # Traverse right child

        if isinstance(node, int):  # Leaf node reached, append character
            decoded_image.append(node)
            node = huffman_tree  # Reset to root for next character

    return bytearray(decoded_image)

# Function to download button
def download_button(data, filename):
    st.download_button(
        label="Download Compressed File",
        data=data,
        file_name=filename,
        mime="image/jpeg"
    )

# Main function for image compression
def kompresi_gambar():
    st.title('Image Compressor')
    st.write("Compress your JPG, PNG, and JPEG file with Brotli Algorithm or Huffman Algorithm.")

    uploaded_file = st.file_uploader("Pick Image", type=["jpg", "jpeg", "png"], accept_multiple_files=False)
    algorithm_selected = st.selectbox("Choose Algorithm: ", ["Brotli", "Huffman"])
    quality = st.slider("Compress Quality (1-100)", 1, 100, 50)

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image_np = np.array(image)

        if algorithm_selected == "Brotli":
            compressed_image = compress_image_brotli(image_np, quality=quality)
            decompressed_image = decompress_image_brotli(compressed_image)
        elif algorithm_selected == "Huffman":
            freq = calculate_byte_frequency(image_np)
            huffman_tree = build_huffman_tree(freq)
            huffman_codes = generate_huffman_codes(huffman_tree)
            encoded_image = encode_image(image_np, huffman_codes)
            decompressed_bytes = decode_image(encoded_image, huffman_tree)
            decompressed_image = cv2.imdecode(np.frombuffer(decompressed_bytes, np.uint8), cv2.IMREAD_COLOR)

        decompressed_image_pil = Image.fromarray(decompressed_image.astype(np.uint8))
        st.image(decompressed_image_pil, caption=f"Image Compressed With {algorithm_selected} Algorithm")
        
        buffer = BytesIO()
        decompressed_image_pil.save(buffer, format="JPEG")
        buffer.seek(0)
        download_button(buffer, "compressed_image.jpg")

if __name__ == "__main__":
    kompresi_gambar()
