import os
import shutil
from pathlib import Path
from rembg import remove
from PIL import Image

def process_game_sprites():
    """
    Специально для вашей структуры папок Ren'Py
    """
    base_dir = Path("images/sprites")
    
    # Папки с персонажами
    character_folders = ['player', 'kyle', 'irma', 'silas', 'jean', 'harding']
    
    for folder in character_folders:
        folder_path = base_dir / folder
        if not folder_path.exists():
            print(f"Папка не найдена: {folder_path}")
            continue
        
        # Создаем backup перед обработкой
        backup_path = base_dir / f"{folder}_backup"
        if not backup_path.exists():
            shutil.copytree(folder_path, backup_path)
            print(f"📦 Бэкап создан: {backup_path}")
        
        # Обрабатываем все PNG
        png_files = list(folder_path.glob("*.png"))
        
        for png_file in png_files:
            print(f"Обработка: {png_file.name}")
            
            with open(png_file, 'rb') as f:
                img_data = f.read()
            
            # Удаляем фон
            result = remove(img_data)
            
            # Сохраняем с тем же именем (перезаписываем)
            with open(png_file, 'wb') as f:
                f.write(result)
            
            print(f"  ✓ Готово: {png_file.name}")
        
        print(f"\n✅ Папка '{folder}' обработана\n")

def add_transparency_to_harding():
    """
    Для harding_shadow.png - делаем полупрозрачным
    """
    harding_path = Path("game/sprites/harding/harding_shadow.png")
    
    if harding_path.exists():
        img = Image.open(harding_path)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Делаем весь силуэт полупрозрачным (50%)
        pixels = img.load()
        for x in range(img.width):
            for y in range(img.height):
                r, g, b, a = pixels[x, y]
                if a > 0:  # Если пиксель не полностью прозрачный
                    pixels[x, y] = (r, g, b, 128)  # 50% прозрачности
        
        img.save(harding_path)
        print("✓ Harding shadow обработан (добавлена прозрачность)")

if __name__ == "__main__":
    print("🚀 Запуск удаления фона для игры 'ДОПРОС'\n")
    process_game_sprites()
    add_transparency_to_harding()
    print("\n✨ Все спрайты обработаны!")