import numpy as np
from PIL import Image, ImageFilter
import os, random

W, H = 1920, 1280

def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# --- base diagonal gradient ---
tl = np.array(hex2rgb('#0b1024'), dtype=np.float64)   # deep midnight
br = np.array(hex2rgb('#241a4a'), dtype=np.float64)    # deep purple

ys = np.linspace(0, 1, H)[:, None]
xs = np.linspace(0, 1, W)[None, :]
# diagonal t = average of x and y
t = (0.55 * xs + 0.45 * ys)
base = (tl[None, None, :] * (1 - t[..., None]) + br[None, None, :] * t[..., None])

# --- nebula blobs (radial gaussian) ---
def blob(cx, cy, radius, color, strength):
    X, Y = np.meshgrid(np.linspace(0, 1, W), np.linspace(0, 1, H))
    d = np.sqrt(((X - cx) ** 2) * (W / H) ** 1.0 + (Y - cy) ** 2)
    g = np.exp(-(d / radius) ** 2)
    return g[..., None] * (np.array(hex2rgb(color), dtype=np.float64) * strength)[None, None, :]

img = base.copy()
img += blob(0.28, 0.32, 0.30, '#6c5ce7', 0.9)   # violet
img += blob(0.78, 0.62, 0.28, '#38bdf8', 0.55)  # cyan
img += blob(0.62, 0.22, 0.22, '#ec4899', 0.35)  # pink faint
img += blob(0.15, 0.80, 0.30, '#3b82f6', 0.30)  # blue faint

# clip
img = np.clip(img, 0, 255)

# --- stars ---
random.seed(42)
np.random.seed(42)
star_layer = np.zeros((H, W, 3), dtype=np.float64)
n_stars = 520
for _ in range(n_stars):
    x = np.random.randint(0, W)
    y = np.random.randint(0, H)
    b = np.random.uniform(0.25, 1.0)
    r = np.random.choice([0, 0, 0, 1, 1, 2])
    color = np.array([255, 255, 255], dtype=np.float64) * b
    if r == 0:
        star_layer[y, x] = np.maximum(star_layer[y, x], color)
    else:
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                yy, xx = y + dy, x + dx
                if 0 <= yy < H and 0 <= xx < W:
                    fall = max(0.0, 1 - (abs(dy) + abs(dx)) / (r + 1))
                    star_layer[yy, xx] = np.maximum(star_layer[yy, xx], color * fall * 0.9)

# blur stars slightly for glow
star_img = Image.fromarray(star_layer.astype(np.uint8))
glow = star_img.filter(ImageFilter.GaussianBlur(1.2))
star_img = Image.fromarray(np.clip(np.array(star_img, dtype=np.float64) + np.array(glow, dtype=np.float64) * 0.6, 0, 255).astype(np.uint8))

img = Image.fromarray(img.astype(np.uint8)).convert('RGB')
img = Image.fromarray(np.clip(np.array(img, dtype=np.float64) + np.array(star_img, dtype=np.float64), 0, 255).astype(np.uint8))

# --- vignette ---
X, Y = np.meshgrid(np.linspace(-1, 1, W), np.linspace(-1, 1, H))
vign = 1 - 0.45 * np.clip((X ** 2 + Y ** 2) / 2.0, 0, 1) ** 1.2
vign = np.clip(vign, 0.45, 1.0)[..., None]
arr = np.array(img, dtype=np.float64) * vign
img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

out_dir = r"C:\Users\26703\Documents\deepseek-harness\default-workspace\my-blog\source\img"
os.makedirs(out_dir, exist_ok=True)
home_path = os.path.join(out_dir, 'banner-home.jpg')
img.save(home_path, 'JPEG', quality=90, optimize=True)
print('home banner:', home_path, os.path.getsize(home_path), 'bytes')

# page banner: crop a shorter band (top-ish) same style for post/page headers
page = img.crop((0, 140, W, 140 + 760))
page_path = os.path.join(out_dir, 'banner-page.jpg')
page.save(page_path, 'JPEG', quality=90, optimize=True)
print('page banner:', page_path, os.path.getsize(page_path), 'bytes')
