import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image


def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(0, file_path)


def embed_data():
    file_path = entry_file_path.get()
    secret_message = entry_message.get()

    if not file_path or not secret_message:
        messagebox.showerror("Input Error", "Please provide both a file and a secret message.")
        return

    if file_path.endswith(('.png', '.jpg', '.jpeg')):
        embed_in_image(file_path, secret_message)
    else:
        messagebox.showerror("Unsupported File", "This file type is not supported for embedding.")


def extract_data():
    file_path = entry_file_path.get()

    if not file_path:
        messagebox.showerror("Input Error", "Please provide a file to extract data from.")
        return

    if file_path.endswith(('.png', '.jpg', '.jpeg')):
        extracted_message = extract_from_image(file_path)
        messagebox.showinfo("Extracted Message", f"Secret Message: {extracted_message}")
    else:
        messagebox.showerror("Unsupported File", "This file type is not supported for extraction.")


def embed_in_image(file_path, message):
    image = Image.open(file_path)
    encoded_image = image.copy()

    width, height = image.size
    message += "#####"
    message_binary = ''.join([format(ord(char), '08b') for char in message])

    data_index = 0
    for y in range(height):
        for x in range(width):
            pixel = list(image.getpixel((x, y)))

            for i in range(3):  # R, G, B
                if data_index < len(message_binary):
                    pixel[i] = int(format(pixel[i], '08b')[:-1] + message_binary[data_index], 2)
                    data_index += 1

            encoded_image.putpixel((x, y), tuple(pixel))
            if data_index >= len(message_binary):
                break
        if data_index >= len(message_binary):
            break

    output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if output_path:
        encoded_image.save(output_path)
        messagebox.showinfo("Success", f"Message embedded successfully! Saved as {output_path}")


def extract_from_image(file_path):
    image = Image.open(file_path)

    binary_data = ""
    for y in range(image.height):
        for x in range(image.width):
            pixel = image.getpixel((x, y))
            for i in range(3):  # R, G, B
                binary_data += format(pixel[i], '08b')[-1]

    binary_chars = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]
    extracted_message = ''.join([chr(int(char, 2)) for char in binary_chars])

    return extracted_message.split("#####")[0]


# UI Setup
root = tk.Tk()
root.title("Image Steganography Tool")

tk.Label(root, text="File Path:").grid(row=0, column=0, padx=10, pady=5)
entry_file_path = tk.Entry(root, width=50)
entry_file_path.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_file).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Secret Message:").grid(row=1, column=0, padx=10, pady=5)
entry_message = tk.Entry(root, width=50)
entry_message.grid(row=1, column=1, padx=10, pady=5)

tk.Button(root, text="Embed Data", command=embed_data).grid(row=2, column=0, padx=10, pady=10)
tk.Button(root, text="Extract Data", command=extract_data).grid(row=2, column=1, padx=10, pady=10)

root.mainloop()
