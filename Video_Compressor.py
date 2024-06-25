from tempfile import NamedTemporaryFile
import streamlit as st
from moviepy.editor import VideoFileClip
import brotli
import heapq
from collections import defaultdict
import os

# Function to compress video using Huffman coding
def compress_video_huffman(uploaded_file):
    st.write("Compressing video using Huffman coding...")

    try:
        # Save the uploaded file to a temporary file
        with NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
            temp_filename = temp_file.name
            temp_file.write(uploaded_file.read())  # Write uploaded file content to the temporary file

        # Read video file from the temporary file
        video_clip = VideoFileClip(temp_filename)

        # Process video frames
        compressed_frames = []
        for frame in video_clip.iter_frames():
            # Convert frame to bytes
            frame_bytes = frame.tobytes()

            # Compress frame using Huffman
            compressed_frame = huffman_compress(frame_bytes)

            # Append compressed frame to list
            compressed_frames.append(compressed_frame)

        # Create a temporary file to save the compressed video
        with NamedTemporaryFile(suffix='.mp4', delete=False) as temp_output_file:
            temp_output_filename = temp_output_file.name

            # Write compressed frames to the temporary output file
            for compressed_frame in compressed_frames:
                temp_output_file.write(compressed_frame)

        st.write(f"Video compressed using Huffman coding saved to: {temp_output_filename}")

        # Return the temporary output filename
        return temp_output_filename

    except Exception as e:
        st.error(f"Error compressing video: {e}")
        return None

# Function to compress video using Brotli algorithm
def compress_video_brotli(uploaded_file):
    st.write("Compressing video using Brotli algorithm...")

    try:
        # Save the uploaded file to a temporary file
        with NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
            temp_filename = temp_file.name
            temp_file.write(uploaded_file.read())  # Write uploaded file content to the temporary file

        # Read video file from the temporary file
        video_clip = VideoFileClip(temp_filename)

        # Process video frames
        compressed_frames = []
        for frame in video_clip.iter_frames():
            # Convert frame to bytes
            frame_bytes = frame.tobytes()

            # Compress frame using Brotli
            compressed_frame = brotli.compress(frame_bytes)

            # Append compressed frame to list
            compressed_frames.append(compressed_frame)

        # Create a temporary file to save the compressed video
        with NamedTemporaryFile(suffix='.mp4', delete=False) as temp_output_file:
            temp_output_filename = temp_output_file.name

            # Write compressed frames to the temporary output file
            for compressed_frame in compressed_frames:
                temp_output_file.write(compressed_frame)

        st.write(f"Video compressed using Brotli algorithm saved to: {temp_output_filename}")

        # Return the temporary output filename
        return temp_output_filename

    except Exception as e:
        st.error(f"Error compressing video: {e}")
        return None

# Huffman coding helper functions
def build_huffman_tree(data):
    freq = defaultdict(int)
    for byte in data:
        freq[byte] += 1
    
    heap = [[weight, [byte, ""]] for byte, weight in freq.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
        
    return heap[0][1:]

def huffman_compress(data):
    tree = build_huffman_tree(data)
    byte_to_code = {byte: code for byte, code in tree}
    encoded_data = ''.join([byte_to_code[byte] for byte in data])
    return bytes(int(encoded_data[i:i+8], 2) for i in range(0, len(encoded_data), 8))

# Example usage or additional functions can be added below if necessar