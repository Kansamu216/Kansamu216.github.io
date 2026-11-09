from PIL import Image, ImageDraw, ImageFont
import os

out = r"C:\Users\26703\Documents\deepseek-harness\default-workspace\my-blog\source\img"
os.makedirs(out, exist_ok=True)

def lerp(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def gradient(w, h, top, bottom):
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        c = lerp(top, bottom, y / max(1, h - 1))
        for x in range(w):
            px[x, y] = c
    return img

def make_icon(size, radius_ratio=0.22, text="K"):
    # vertical gradient purple -> indigo
    base = gradient(size, size, (139, 124, 240), (76, 61, 196))
    # rounded mask
    mask = Image.new("L", (size, size), 0)
    md = ImageDraw.Draw(mask)
    r = int(size * radius_ratio)
    md.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=255)
    icon = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    icon.paste(base, (0, 0), mask)

    d = ImageDraw.Draw(icon)
    # font
    fpath = None
    for p in [r"C:\Windows\Fonts\segoeuib.ttf", r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf"]:
        if os.path.exists(p):
            fpath = p
            break
    font = ImageFont.truetype(fpath, int(size * 0.62)) if fpath else ImageFont.load_default()
    # center text
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (size - tw) / 2 - bbox[0]
    ty = (size - th) / 2 - bbox[1] - size * 0.02
    # subtle shadow
    d.text((tx + size * 0.015, ty + size * 0.02), text, font=font, fill=(30, 20, 70, 90))
    d.text((tx, ty), text, font=font, fill=(255, 255, 255, 255))
    return icon

# favicon 64
make_icon(64, 0.24).save(os.path.join(out, "favicon-kq.png"))
print("favicon", os.path.getsize(os.path.join(out, "favicon-kq.png")))

# avatar 256 (rounded square looks fine; theme shows it in a circle-ish frame)
make_icon(256, 0.20).convert("RGB").save(os.path.join(out, "avatar-kq.png"))
print("avatar", os.path.getsize(os.path.join(out, "avatar-kq.png")))
