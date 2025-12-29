from PIL import Image
import os

# Define the suits and their input paths
suits = {
    'spade': r'c:\gemini\원카드\스페이스.png',
    'club': r'c:\gemini\원카드\클로버.png',
    'heart': r'c:\gemini\원카드\하트.png',
    'diamond': r'c:\gemini\원카드\다이아몬드.jpg'
}

# Card values in order (A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K)
values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

# Output directory
output_dir = r'c:\gemini\원카드\cards'
os.makedirs(output_dir, exist_ok=True)

def process_grid_to_individual(input_path, suit_name):
    """Process a 4x4 grid image into 13 individual card images"""
    try:
        with Image.open(input_path) as img:
            img = img.convert('RGBA')
            w, h = img.size
            
            # 4x4 grid
            cols = 4
            rows = 4
            card_w = w // cols
            card_h = h // rows
            
            print(f"[{suit_name}] Image size: {w}x{h}, Card size: {card_w}x{card_h}")
            
            count = 0
            for r in range(rows):
                for c in range(cols):
                    if count >= 13:
                        break
                    
                    left = c * card_w
                    top = r * card_h
                    right = left + card_w
                    bottom = top + card_h
                    
                    card = img.crop((left, top, right, bottom))
                    
                    # Save individual card
                    value = values[count]
                    filename = f"{suit_name}_{value}.png"
                    filepath = os.path.join(output_dir, filename)
                    card.save(filepath)
                    print(f"  Saved: {filename}")
                    
                    count += 1
                if count >= 13:
                    break
            
            return True
            
    except Exception as e:
        print(f"[ERROR] {suit_name}: {e}")
        return False

# Process all suits
print("=" * 50)
print("Splitting cards into individual images...")
print(f"Output directory: {output_dir}")
print("=" * 50)

success_count = 0
for suit_name, input_path in suits.items():
    if os.path.exists(input_path):
        if process_grid_to_individual(input_path, suit_name):
            success_count += 1
    else:
        print(f"[SKIP] {suit_name}: Input file not found - {input_path}")

print("=" * 50)
print(f"Completed: {success_count}/{len(suits)} suits processed")
print(f"Total cards: {success_count * 13} individual images")
print("=" * 50)
