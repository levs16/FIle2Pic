from tkinter import Tk, filedialog
from PIL import Image, ImageDraw
import os
import time
import datetime

# encode by char
def encode_character(character):
    ascii_value = ord(character)
    color = (ascii_value % 256, (ascii_value // 256) % 256, (ascii_value // 256 // 256) % 256)
    return color

# decode by char
def decode_image(image_path):
    image = Image.open(image_path)
    pixels = list(image.getdata())
    decoded_text = ""
    for pixel in pixels:
        ascii_value = sum(pixel)
        decoded_text += chr(ascii_value)
    return decoded_text

# encode to image
def encode_text(text, output_image_path):
    # Determine the size of the square based on the length of the text
    square_size = int(len(text) ** 0.5) + 1
    image_size = (square_size, square_size)
    image = Image.new("RGB", image_size, "white")
    draw = ImageDraw.Draw(image)
    
    # pick encoding color for a character square and append to image
    for i, char in enumerate(text):
        color = encode_character(char)
        x = i % square_size
        y = i // square_size
        draw.rectangle([x, y, x+1, y+1], fill=color)
    image.save(output_image_path)

# file picker
def pick_file():
    root = Tk()
    root.withdraw()
    global file_path
    file_path = filedialog.askopenfilename()
    root.destroy()
    return file_path

# main function(read input, call functions)
def main():
    # get choice from user
    print("'e': encode\n'd': decode")
    choice = input("Enter your option>> ")
    
    # if "e", encode
    if choice == 'e':
        input_file = pick_file()
        if not input_file:
            print("No file selected.")
            return
        output_image = os.path.join(os.getcwd(), f"{file_path}_encoded_{datetime.datetime.now()}.png")
        with open(input_file, 'r') as file:
            text = file.read()
            encode_text(text, output_image)
            print("Encoding complete. Image saved to:", output_image)
    # if "d", decode
    elif choice == 'd':
        input_image = pick_file()
        if not input_image:
            print("No file selected.")
            return
        decoded_text = decode_image(input_image)
        output_file = os.path.join(os.getcwd(), f"{file_path}_decoded_{datetime.datetime.now()}.txt")
        with open(output_file, 'w') as file:
            file.write(decoded_text)
            print("Decoded text saved to:", output_file)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
