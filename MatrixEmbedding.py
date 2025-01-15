from PIL import Image
import numpy as np

def encode_matrix_embedding(image_path, message, block_size=2):
    image = Image.open(image_path)
    pixels = np.array(image)
    h, w, _ = pixels.shape
    message_bin = ''.join(format(ord(char), '08b') for char in message)
    message_bin += '00000000'  # End delimiter

    idx = 0
    for i in range(0, h - block_size + 1, block_size):
        for j in range(0, w - block_size + 1, block_size):
            if idx >= len(message_bin):
                break

            block = pixels[i:i+block_size, j:j+block_size]
            # Example matrix operation: simple mean adjustment for demonstration
            block_mean = np.mean(block)
            # Modify block to encode message
            block_flat = block.flatten()
            
            for k in range(len(block_flat)):
                if idx < len(message_bin):
                    bit = int(message_bin[idx])
                    if block_flat[k] % 2 != bit:
                        if block_flat[k] < block_mean:
                            block_flat[k] = min(255, block_flat[k] + 1)
                        else:
                            block_flat[k] = max(0, block_flat[k] - 1)
                    idx += 1
            pixels[i:i+block_size, j:j+block_size] = block_flat.reshape(block.shape)
            if idx >= len(message_bin):
                break

    encoded_image = Image.fromarray(pixels)
    return encoded_image

encode_matrix_embedding('download.png', 'Hello, World!').save('encoded_image.png')

def decode_matrix_embedding(image_path, block_size=2):
    image = Image.open(image_path)
    pixels = np.array(image)
    h, w, _ = pixels.shape

    message_bin = ''
    for i in range(0, h - block_size + 1, block_size):
        for j in range(0, w - block_size + 1, block_size):
            block = pixels[i:i+block_size, j:j+block_size]
            block_flat = block.flatten()
            # Extract data from block
            for k in range(len(block_flat)):
                if len(message_bin) % 8 == 0 and message_bin[-8:] == '00000000':
                    break
                message_bin += str(block_flat[k] % 2)
    
    # Convert binary message to text
    message = ''
    for i in range(0, len(message_bin), 8):
        byte = message_bin[i:i+8]
        if byte == '00000000':  # End delimiter
            break
        message += chr(int(byte, 2))

    return message


