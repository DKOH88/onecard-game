from PIL import Image
import os

# Define the suits and their input/output paths
suits = {
    'diamond': {
        'input': r'c:\gemini\원카드\다이아몬드.jpg',
        'output': r'c:\gemini\원카드\diamond_row.png'
    },
    'spade': {
        'input': r'c:\gemini\원카드\스페이스.png',
        'output': r'c:\gemini\원카드\spade_row.png'
    },
    'club': {
        'input': r'c:\gemini\원카드\클로버.png',
        'output': r'c:\gemini\원카드\club_row.png'
    },
    'heart': {
        'input': r'c:\gemini\원카드\하트.png',
        'output': r'c:\gemini\원카드\heart_row.png'
    }
}

def process_grid_to_row(input_path, output_path, suit_name):
    """Process a 4x4 grid image into a 13-card horizontal row"""
    try:
        with Image.open(input_path) as img:
            img = img.convert('RGBA')
            w, h = img.size
            
            # 4x4 grid
            cols = 4
            rows = 4
            card_w = w // cols
            card_h = h // rows
            
            # We need 13 cards (A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K)
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
            print(f"[OK] {suit_name}: {output_path}")
            print(f"     Card dimensions: {card_w}x{card_h}")
            return True
            
    except Exception as e:
        print(f"[ERROR] {suit_name}: {e}")
        return False

# Process all suits
print("=" * 50)
print("Processing all suit images...")
print("=" * 50)

success_count = 0
for suit_name, paths in suits.items():
    if os.path.exists(paths['input']):
        if process_grid_to_row(paths['input'], paths['output'], suit_name):
            success_count += 1
    else:
        print(f"[SKIP] {suit_name}: Input file not found - {paths['input']}")

print("=" * 50)
print(f"Completed: {success_count}/{len(suits)} suits processed")
print("=" * 50)
