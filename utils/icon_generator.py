"""
utils/icon_generator.py

Beschrijving: Genereer standaard icons voor de applicatie
Applicatie: Project Generator
Versie: 1.0.3
Auteur: Barremans
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def create_app_icon(size: int = 256) -> Image.Image:
    """Maak een applicatie icon."""
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Achtergrond gradient (blauw)
    for y in range(size):
        alpha = int(255 * (1 - y / size))
        color = (33, 150, 243, 255)
        draw.rectangle([0, y, size, y+1], fill=color)
    
    # Border
    draw.rectangle([0, 0, size-1, size-1], outline=(21, 101, 192, 255), width=8)
    
    # Tekst "PG"
    try:
        font = ImageFont.truetype("arial.ttf", size // 3)
    except:
        font = ImageFont.load_default()
    
    text = "PG"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 10
    
    # Shadow
    draw.text((x+3, y+3), text, fill=(0, 0, 0, 128), font=font)
    # Text
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    return img


def create_folder_icon(size: int = 64) -> Image.Image:
    """Maak een folder icon."""
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Folder body
    folder_color = (255, 193, 7, 255)
    draw.rectangle([5, 20, size-5, size-10], fill=folder_color, outline=(230, 170, 0, 255), width=2)
    
    # Folder tab
    draw.rectangle([5, 15, size//2, 25], fill=folder_color, outline=(230, 170, 0, 255), width=2)
    
    return img


def create_file_icon(size: int = 64) -> Image.Image:
    """Maak een file icon."""
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # File body
    file_color = (255, 255, 255, 255)
    draw.rectangle([10, 5, size-10, size-5], fill=file_color, outline=(200, 200, 200, 255), width=2)
    
    # Corner fold
    fold_size = 12
    draw.polygon([
        (size-10-fold_size, 5),
        (size-10, 5+fold_size),
        (size-10, 5)
    ], fill=(220, 220, 220, 255), outline=(200, 200, 200, 255))
    
    # Lines
    for i in range(3):
        y = 20 + i * 12
        draw.line([15, y, size-15, y], fill=(150, 150, 150, 255), width=2)
    
    return img


def create_settings_icon(size: int = 64) -> Image.Image:
    """Maak een settings (gear) icon."""
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    center = size // 2
    outer_radius = size // 2 - 5
    inner_radius = size // 4
    
    # Gear teeth (simplified)
    gear_color = (158, 158, 158, 255)
    draw.ellipse([center-outer_radius, center-outer_radius, 
                  center+outer_radius, center+outer_radius], 
                 fill=gear_color, outline=(100, 100, 100, 255), width=2)
    
    # Center hole
    draw.ellipse([center-inner_radius, center-inner_radius,
                  center+inner_radius, center+inner_radius],
                 fill=(255, 255, 255, 0), outline=(100, 100, 100, 255), width=2)
    
    return img


def create_help_icon(size: int = 64) -> Image.Image:
    """Maak een help (?) icon."""
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    center = size // 2
    radius = size // 2 - 5
    
    # Circle
    circle_color = (33, 150, 243, 255)
    draw.ellipse([center-radius, center-radius, center+radius, center+radius],
                 fill=circle_color, outline=(21, 101, 192, 255), width=3)
    
    # Question mark
    try:
        font = ImageFont.truetype("arial.ttf", size // 2)
    except:
        font = ImageFont.load_default()
    
    text = "?"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 5
    
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    return img


def create_info_icon(size: int = 64) -> Image.Image:
    """Maak een info (i) icon."""
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    center = size // 2
    radius = size // 2 - 5
    
    # Circle
    circle_color = (76, 175, 80, 255)
    draw.ellipse([center-radius, center-radius, center+radius, center+radius],
                 fill=circle_color, outline=(56, 142, 60, 255), width=3)
    
    # Info "i"
    try:
        font = ImageFont.truetype("arial.ttf", size // 2)
    except:
        font = ImageFont.load_default()
    
    text = "i"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 5
    
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    return img


def generate_all_icons(output_dir: Path):
    """Genereer alle standaard icons."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    icons = {
        'app_icon.png': create_app_icon(256),
        'app_icon_64.png': create_app_icon(64),
        'app_icon_32.png': create_app_icon(32),
        'app_icon_16.png': create_app_icon(16),
        'folder.png': create_folder_icon(64),
        'file.png': create_file_icon(64),
        'settings.png': create_settings_icon(64),
        'help.png': create_help_icon(64),
        'info.png': create_info_icon(64),
    }
    
    for filename, img in icons.items():
        filepath = output_dir / filename
        img.save(filepath)
        print(f"✅ Created: {filepath}")
    
    # Maak ook een .ico bestand voor Windows
    ico_path = output_dir / "app_icon.ico"
    app_icon = create_app_icon(256)
    app_icon.save(ico_path, format='ICO', sizes=[(16, 16), (32, 32), (64, 64), (256, 256)])
    print(f"✅ Created: {ico_path}")


if __name__ == "__main__":
    # Run dit script om icons te genereren
    project_root = Path(__file__).parent.parent
    icons_dir = project_root / "assets" / "icons"
    
    print("🎨 Genereren van icons...")
    generate_all_icons(icons_dir)
    print("\n✅ Alle icons zijn aangemaakt!")