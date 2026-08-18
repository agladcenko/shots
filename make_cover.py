"""Генератор обложек для Kwork.

Меняешь блок НАСТРОЙКИ — получаешь обложку под другую услугу.
Запуск: python make_cover.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

# ============ НАСТРОЙКИ ============

SCREENSHOT = "demo.png"
OUTPUT = "cover_bot.png"

TITLE = "Телеграм-бот"
SUBTITLE = "на Python под вашу задачу"
BULLETS = [
    "Кнопочное меню",
    "База данных и внешние API",
    "Размещение на сервере 24/7",
]

# ============ ОФОРМЛЕНИЕ ============

W, H = 1200, 800
BG = (24, 28, 38)
PANEL = (32, 38, 51)
ACCENT = (56, 189, 172)
TEXT = (236, 240, 245)
MUTED = (150, 160, 175)

PAD = 60
GAP = 40

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\segoeuib.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
FONT_CANDIDATES_REG = [
    r"C:\Windows\Fonts\segoeui.ttf",
    r"C:\Windows\Fonts\arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def load_font(candidates, size):
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    raise FileNotFoundError(
        "Не найден ни один шрифт. Добавь путь к .ttf в FONT_CANDIDATES."
    )


def rounded_screenshot(path, box_w, box_h, radius=14):
    """Вписывает картинку в box с сохранением пропорций, скругляет углы."""
    img = Image.open(path).convert("RGB")
    scale = min(box_w / img.width, box_h / img.height)
    size = (int(img.width * scale), int(img.height * scale))
    img = img.resize(size, Image.LANCZOS)

    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1],
                                           radius=radius, fill=255)
    out = Image.new("RGBA", size)
    out.paste(img, (0, 0))
    out.putalpha(mask)
    return out


def main():
    f_title = load_font(FONT_CANDIDATES, 72)
    f_sub = load_font(FONT_CANDIDATES_REG, 34)
    f_bullet = load_font(FONT_CANDIDATES_REG, 28)

    canvas = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(canvas)

    # правая колонка — скриншот
    shot_box_w = 420
    shot = rounded_screenshot(SCREENSHOT, shot_box_w, H - PAD * 2)
    shot_x = W - PAD - shot.width
    shot_y = (H - shot.height) // 2

    # подложка под скриншот
    draw.rounded_rectangle(
        [shot_x - 16, shot_y - 16, shot_x + shot.width + 16, shot_y + shot.height + 16],
        radius=22, fill=PANEL,
    )
    canvas.paste(shot, (shot_x, shot_y), shot)

    # левая колонка — текст
    x = PAD
    y = PAD + 40

    draw.text((x, y), TITLE, font=f_title, fill=TEXT)
    y += 88

    draw.text((x, y), SUBTITLE, font=f_sub, fill=ACCENT)
    y += 70

    # разделитель
    draw.rectangle([x, y, x + 90, y + 4], fill=ACCENT)
    y += GAP + 10

    for item in BULLETS:
        draw.ellipse([x + 2, y + 11, x + 12, y + 21], fill=ACCENT)
        draw.text((x + 28, y), item, font=f_bullet, fill=MUTED)
        y += 52

    canvas.save(OUTPUT, quality=95)
    print(f"Готово: {OUTPUT} ({W}x{H})")


if __name__ == "__main__":
    main()
