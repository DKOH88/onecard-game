from PIL import Image
import os

input_path = r'c:\gemini\원카드\다이아몬드.jpg'
output_path = r'c:\gemini\원카드\diamond_row.png'

try:
    with Image.open(input_path) as img:
        img = img.convert('RGBA')
        w, h = img.size
        # Assuming 4x4 grid for 13 cards
        cols = 4
        rows = 4
        card_w = w // cols
        card_h = h // rows
        
        # We need 13 cards
        num_cards = 13
        
        # Create a new image for the row: (13*card_w) x card_h
        row_img = Image.new('RGBA', (num_cards * card_w, card_h))
        
        count = 0
        for r in range(rows):
            for c in range(cols):
                if count >= num_cards:
                    break
                
                left = c * card_w
                top = r * card_h
                right = left + card_w
                bottom = top + card_h
                
                card = img.crop((left, top, right, bottom))
                row_img.paste(card, (count * card_w, 0))
                count += 1
            if count >= num_cards:
                break
        
        row_img.save(output_path)
        print(f"Successfully created sprite sheet: {output_path}")
        print(f"Single card dimensions: {card_w}x{card_h}")

except Exception as e:
    print(f"Error processing image: {e}")
