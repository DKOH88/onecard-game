from PIL import Image
import os

path = r'c:\gemini\원카드\다이아몬드.jpg'
try:
    with Image.open(path) as img:
        print(f"Format: {img.format} Width: {img.width} Height: {img.height}")
except Exception as e:
    print(f"Error: {e}")
