"""
Image processing utilities
"""
from PIL import Image, ImageDraw, ImageFont
import io

def create_profile_card(username, level, money, bank):
    """Create a profile card image"""
    img = Image.new('RGB', (400, 300), color='#1e1e2e')
    draw = ImageDraw.Draw(img)
    
    # Draw text
    draw.text((20, 20), f"@{username}", fill='white')
    draw.text((20, 60), f"Level {level}", fill='#00ff00')
    draw.text((20, 100), f"Wallet: {money:,} 💰", fill='#ffff00')
    draw.text((20, 140), f"Bank: {bank:,} 💰", fill='#00ffff')
    
    return img

def resize_image(image, max_width, max_height):
    """Resize image while maintaining aspect ratio"""
    image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    return image

def add_watermark(image, text):
    """Add watermark to image"""
    draw = ImageDraw.Draw(image)
    width, height = image.size
    draw.text((width - 100, height - 20), text, fill='gray')
    return image