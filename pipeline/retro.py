"""실사 사진을 부고란 톤으로 보정하고 100KB 이하로 압축한다.

사용:
  python3 pipeline/retro.py 입력.jpg 출력.jpg --style riso     # 리소 2도 (일러스트와 같은 먹·주홍)
  python3 pipeline/retro.py 입력.jpg 출력.jpg --style halftone # 옛 신문 망점 (먹 한 도)
  python3 pipeline/retro.py 입력.jpg 출력.jpg --style faded    # 바랜 컬러 (사진 느낌 유지)

공통: 가로 1200px로 줄이고, 종이 질감 입자를 얹고, 100KB 이하가 될 때까지 JPEG 품질을 낮춘다.
"""
import argparse
import io
import random

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageOps

PAPER = (251, 244, 228)
INK = (43, 41, 36)
RED = (232, 112, 84)
WIDTH = 1200
LIMIT = 100_000


def _resize(im):
    im = ImageOps.exif_transpose(im).convert("RGB")
    if im.width > WIDTH:
        im = im.resize((WIDTH, round(im.height * WIDTH / im.width)), Image.LANCZOS)
    return im


def _grain(im, amount=18, seed=7):
    """종이 입자: 밝기 잡음을 아주 약하게 곱한다."""
    random.seed(seed)
    noise = Image.effect_noise(im.size, amount).convert("RGB")
    noise = noise.point(lambda v: 225 + v // 8)
    return ImageChops.multiply(im, noise)


def _gradient_map(gray, stops):
    """흑백 값을 색 구간에 대응시킨다. stops: [(위치0~255, (r,g,b)), ...]"""
    lut = []
    for ch in range(3):
        table = []
        for v in range(256):
            for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
                if p0 <= v <= p1:
                    t = (v - p0) / max(1, p1 - p0)
                    table.append(round(c0[ch] + (c1[ch] - c0[ch]) * t))
                    break
        lut.append(table)
    g = gray.convert("L")
    return Image.merge("RGB", [g.point(lut[0]), g.point(lut[1]), g.point(lut[2])])


def riso(im):
    """먹(어두운 곳) - 주홍(중간) - 종이(밝은 곳) 3단 색 대응 + 주홍판 살짝 어긋남."""
    gray = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=2)
    gray = ImageEnhance.Contrast(gray).enhance(1.25)
    base = _gradient_map(gray, [(0, INK), (95, INK), (140, RED), (200, PAPER), (255, PAPER)])
    # 주홍판 어긋남: 중간톤 마스크를 2px 옮겨 한 번 더 찍는다
    mid = gray.point(lambda v: 255 if 110 < v < 185 else 0).filter(ImageFilter.GaussianBlur(1.2))
    shifted = ImageChops.offset(mid, 2, 1)
    red_layer = Image.new("RGB", im.size, RED)
    base = Image.composite(ImageChops.multiply(base, red_layer), base, shifted.point(lambda v: v // 3))
    return _grain(base, 30)


def halftone(im, cell=8):
    """먹 한 도 망점. 셀마다 어두운 만큼 큰 점을 찍는다."""
    gray = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=2)
    small = gray.resize((im.width // cell, im.height // cell), Image.BILINEAR)
    out = Image.new("RGB", im.size, PAPER)
    d = ImageDraw.Draw(out)
    for y in range(small.height):
        for x in range(small.width):
            v = small.getpixel((x, y))
            r = (1 - v / 255) * cell * 0.72
            if r > 0.4:
                cx, cy = x * cell + cell / 2, y * cell + cell / 2
                d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=INK)
    return out.filter(ImageFilter.GaussianBlur(0.4))


def faded(im):
    """바랜 컬러: 채도와 대비를 낮추고, 검은색을 들어 올리고, 따뜻한 종이색을 겹친다."""
    im = ImageOps.autocontrast(im, cutoff=1)  # 원본이 이미 옅으면 먼저 명암을 편다
    im = ImageEnhance.Color(im).enhance(0.55)
    im = ImageEnhance.Contrast(im).enhance(0.85)
    # 검은색 들어 올리기 (필름이 바랜 느낌)
    im = im.point(lambda v: round(28 + v * (235 - 28) / 255))
    warm = Image.new("RGB", im.size, (244, 226, 196))
    im = Image.blend(im, ImageChops.multiply(im, warm), 0.55)
    # 가장자리 어둡게
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).ellipse((-im.width * 0.15, -im.height * 0.2, im.width * 1.15, im.height * 1.2), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(im.width // 8))
    dark = ImageEnhance.Brightness(im).enhance(0.78)
    im = Image.composite(im, dark, mask)
    return _grain(im, 22)


STYLES = {"riso": riso, "halftone": halftone, "faded": faded}


def save_under_limit(im, path, limit=LIMIT):
    """품질을 84에서 50까지 낮춰 보고, 그래도 크면 가로를 10%씩 줄인다."""
    while True:
        for q in range(84, 46, -4):
            buf = io.BytesIO()
            im.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
            if buf.tell() <= limit:
                with open(path, "wb") as f:
                    f.write(buf.getvalue())
                return q, buf.tell()
        im = im.resize((round(im.width * 0.9), round(im.height * 0.9)), Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--style", choices=sorted(STYLES), default="riso")
    a = ap.parse_args()
    im = _resize(Image.open(a.src))
    out = STYLES[a.style](im)
    q, size = save_under_limit(out, a.dst)
    print(f"{a.dst} {out.size[0]}x{out.size[1]} {a.style} q={q} {size / 1024:.1f}KB")


if __name__ == "__main__":
    main()
