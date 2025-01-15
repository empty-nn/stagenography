import cv2
from PIL import Image

def hide_pvd(image_path, message):
    img = cv2.imread(image_path)
    message_length = len(message)

# Prepend the length and a delimiter to the message
    message = str(message_length) + ":" + message

# Convert the message to binary
    message_bin = ''.join(format(ord(i), '08b') for i in message) 
    h, w, _ = img.shape

    idx = 0
    for i in range(h):
        for j in range(w - 1):  # Process pixels one by one
            if idx >= len(message_bin):
                break
            for c in range(3):  # Iterate over the color channels
                if idx >= len(message_bin):
                    break
                current_pixel = img[i, j, c]
                next_pixel = img[i, j + 1, c]
                diff = int(next_pixel) - int(current_pixel)
                m = int(message_bin[idx])  # current bit of message

                if diff % 2 == m:
                    idx += 1  # Move to the next bit
                elif diff % 2 == 0 and m == 1:
                    if diff > 0:
                        if img[i, j + 1, c] == 255:
                            img[i, j + 1, c] = 254
                        else:
                            img[i, j + 1, c] = min(255, img[i, j + 1, c] + 1)
                    else:
                        img[i, j + 1, c] = max(0, img[i, j + 1, c] - 1)
                    idx += 1  # Move to the next bit
                elif diff % 2 == 1 and m == 0:
                    if diff > 0:
                        img[i, j + 1, c] = max(0, img[i, j + 1, c] - 1)
                    else:
                        if img[i, j + 1, c] == 255:
                            img[i, j + 1, c] = 254
                        else:
                            img[i, j + 1, c] = min(255, img[i, j + 1, c] + 1)
                    idx += 1  # Move to the next bit
                
 
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


def reveal_pvd(image_path):
    img = cv2.imread(image_path)
    h, w, _ = img.shape

    message_bin = ""
    bit_count = 0

    # Extract bits until we find the delimiter ':'
    found_delimiter = False
    for i in range(h):
        for j in range(w - 1):
            for c in range(3):  # Iterate over the color channels
                current_pixel = img[i, j, c]
                next_pixel = img[i, j + 1, c]
                diff = abs(int(next_pixel) - int(current_pixel))
                message_bin += str(diff % 2)
                bit_count += 1

                # Check if we have found the delimiter ':'
                if len(message_bin) >= 8 and message_bin[-8:] == format(ord(':'), '08b'):
                    found_delimiter = True
                    break
            if found_delimiter:
                break
        if found_delimiter:
            break

    # Extract the length of the message
    length_bin = message_bin[:-8]  # Exclude the delimiter ':'
    message_length = int(''.join(chr(int(length_bin[i:i+8], 2)) for i in range(0, len(length_bin), 8)))
    # Calculate the total number of bits to extract
    total_bits = bit_count + message_length * 8
    bit_count = 0
    # Continue extracting the remaining bits of the message
    for i in range(h):
        for j in range(w - 1):
            for c in range(3):  # Iterate over the color channels
                if bit_count < total_bits:
                    current_pixel = img[i, j, c]
                    next_pixel = img[i, j + 1, c]
                    diff = abs(int(next_pixel) - int(current_pixel))
                    message_bin += str(diff % 2)
                    bit_count += 1
                else:
                    break
            if bit_count >= total_bits:
                break
        if bit_count >= total_bits:
            break

    # Extract the actual message binary
    message_bin = message_bin[bit_count - message_length * 8:]  # Skip the length and delimiter

    # Convert binary message to text
    delimiter_pos = message_bin.find(format(ord(':'), '08b'))

    # Remove data up to the first ':'
    if delimiter_pos != -1:
        message_bin = message_bin[delimiter_pos + 8:]

    # Decode the remaining binary message
    message = ""
    for i in range(0, len(message_bin), 8):
        byte = message_bin[i:i + 8]
        message += chr(int(byte, 2))

    return message