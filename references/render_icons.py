import math, os
from PIL import Image, ImageDraw, ImageFilter, ImageChops

S, SS = 1024, 4
W = S * SS
OUT = os.path.dirname(os.path.abspath(__file__))

INK    = (62, 52, 46, 248)      # warm umber, never pure black
STROKE = 0.0248

# ---------------- geometry ----------------
def squircle(n=4.6, steps=1440):
    p = []
    for i in range(steps):
        t = 2*math.pi*i/steps; c, s = math.cos(t), math.sin(t)
        p.append((0.5+0.5*math.copysign(abs(c)**(2.0/n), c),
                  0.5+0.5*math.copysign(abs(s)**(2.0/n), s)))
    return p

def arc(cx, cy, r, a0, a1, steps=None):
    steps = steps or max(10, int(abs(a1-a0)/(math.pi/90)))
    return [(cx+r*math.cos(a0+(a1-a0)*i/steps), cy+r*math.sin(a0+(a1-a0)*i/steps))
            for i in range(steps+1)]

def circle(cx, cy, r, steps=240):
    return [(cx+r*math.cos(2*math.pi*i/steps), cy+r*math.sin(2*math.pi*i/steps))
            for i in range(steps)]

def seg(p0, p1, steps=30):
    return [(p0[0]+(p1[0]-p0[0])*i/steps, p0[1]+(p1[1]-p0[1])*i/steps) for i in range(steps+1)]

def bez(p0, p1, p2, p3, steps=70):
    o = []
    for i in range(steps+1):
        t = i/steps; u = 1-t
        o.append((u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0],
                  u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1]))
    return o

def rrect(x, y, w, h, r):
    x2, y2 = x+w, y+h
    return (seg((x+r, y), (x2-r, y)) + arc(x2-r, y+r, r, -math.pi/2, 0)
          + seg((x2, y+r), (x2, y2-r)) + arc(x2-r, y2-r, r, 0, math.pi/2)
          + seg((x2-r, y2), (x+r, y2)) + arc(x+r, y2-r, r, math.pi/2, math.pi)
          + seg((x, y2-r), (x, y+r)) + arc(x+r, y+r, r, math.pi, 1.5*math.pi))

def sparkle(cx, cy, r, pinch=0.32):
    tips = [(cx, cy-r), (cx+r, cy), (cx, cy+r), (cx-r, cy)]
    p = []
    for i in range(4):
        a, b = tips[i], tips[(i+1) % 4]
        c1 = (a[0]+(cx-a[0])*(1-pinch), a[1]+(cy-a[1])*(1-pinch))
        c2 = (b[0]+(cx-b[0])*(1-pinch), b[1]+(cy-b[1])*(1-pinch))
        p += bez(a, c1, c2, b, 30)[:-1]
    return p

# ---------------- the hand: slow, not jittery ----------------
def soften(pts, closed, amp, seed):
    """Low-frequency only (k=1,2,3). High harmonics are what made the lines look cracked."""
    K = (1, 2, 3)
    ph = [((seed*53 + j*149) % 197)/197.0*2*math.pi for j in range(len(K))]
    n = len(pts); out = []
    for i, (px, py) in enumerate(pts):
        a = pts[(i-1) % n] if closed else pts[max(i-1, 0)]
        b = pts[(i+1) % n] if closed else pts[min(i+1, n-1)]
        dx, dy = b[0]-a[0], b[1]-a[1]; L = math.hypot(dx, dy) or 1e-9
        t = i/n if closed else i/(n-1)
        d = sum(math.sin(2*math.pi*K[j]*t + ph[j])/(j+1.4) for j in range(len(K)))
        if not closed:
            d *= math.sin(math.pi*t)**0.5
        out.append((px - dy/L*amp*d, py + dx/L*amp*d))
    return out

class Sheet:
    def __init__(self, bg):
        self.img  = bg
        self.wash  = Image.new("RGBA", (W, W), (0, 0, 0, 0))
        self.shade = Image.new("RGBA", (W, W), (0, 0, 0, 0))
        self.ink   = Image.new("RGBA", (W, W), (0, 0, 0, 0))
        self.wd  = ImageDraw.Draw(self.wash)
        self.sd  = ImageDraw.Draw(self.shade)
        self.idr = ImageDraw.Draw(self.ink)
        self.shadow = (118, 94, 76, 64)

    def paint(self, pts, color, dx=0.006, dy=0.005, seed=1):
        """Flat colour laid down slightly off the line, the way a brush misses."""
        p = soften(pts, True, 0.004, seed)
        self.sd.polygon([((x+0.016)*W, (y+0.020)*W) for x, y in p], fill=self.shadow)
        self.wd.polygon([((x+dx)*W, (y+dy)*W) for x, y in p], fill=color)

    def stroke(self, pts, closed, seed=0, amp=0.0035, w=STROKE):
        p = soften(pts, closed, amp, seed)
        px = [(x*W, y*W) for x, y in p]
        if closed:
            px.append(px[0])
        n = len(px); base = w*W
        for i in range(n-1):
            t = i/(n-1)
            lw = base*(0.90 + 0.10*math.sin(2*math.pi*2*t + seed))
            if not closed:
                lw *= max(0.42, math.sin(math.pi*t)**0.22)      # brush lifts at the ends
            r = lw/2.0
            self.idr.line([px[i], px[i+1]], fill=INK, width=max(1, int(lw)))
            self.idr.ellipse([px[i][0]-r, px[i][1]-r, px[i][0]+r, px[i][1]+r], fill=INK)

    def dot(self, cx, cy, r):
        self.idr.ellipse([(cx-r)*W, (cy-r)*W, (cx+r)*W, (cy+r)*W], fill=INK)

    def flatten(self):
        self.img.alpha_composite(self.shade.filter(ImageFilter.GaussianBlur(7.0*SS)))
        self.img.alpha_composite(self.wash.filter(ImageFilter.GaussianBlur(2.2*SS)))
        self.img.alpha_composite(self.ink.filter(ImageFilter.GaussianBlur(0.35*SS)))
        return self.img

# ---------------- grounds: painted, not flat ----------------
def ground(top, bottom, glow):
    g = Image.new("RGBA", (1, 256))
    for y in range(256):
        t = y/255.0
        g.putpixel((0, y), tuple(int(top[c]+(bottom[c]-top[c])*t) for c in range(3)) + (255,))
    img = g.resize((W, W), Image.BICUBIC)
    lit = Image.new("L", (W, W), 0)
    ImageDraw.Draw(lit).ellipse([-0.14*W, -0.32*W, 0.78*W, 0.62*W], fill=255)
    img.paste(Image.new("RGBA", (W, W), glow + (255,)),
              (0, 0), lit.filter(ImageFilter.GaussianBlur(0.24*W)).point(lambda v: int(v*0.62)))
    return img

def paper(img, strength=0.30):
    """Tooth. Two scales of grain, laid over everything so line and ground share one surface."""
    n = img.size[0]
    base = img.convert("RGB")
    fine   = Image.effect_noise((n//2, n//2), 26).resize((n, n), Image.BICUBIC)
    coarse = Image.effect_noise((n//14, n//14), 20).resize((n, n), Image.BICUBIC) \
                  .filter(ImageFilter.GaussianBlur(1.2))
    grain  = Image.blend(fine, coarse, 0.45)
    tex    = ImageChops.overlay(base, Image.merge("RGB", (grain,)*3))
    return Image.blend(base, tex, strength).convert("RGBA")

# ---------------- the three marks ----------------
def worth_asking(sh, wash):
    bx, by, bw, bh, br = 0.215, 0.268, 0.520, 0.402, 0.120
    x2, y2 = bx+bw, by+bh
    p  = seg((bx+br, by), (x2-br, by)) + arc(x2-br, by+br, br, -math.pi/2, 0)
    p += seg((x2, by+br), (x2, y2-br)) + arc(x2-br, y2-br, br, 0, math.pi/2)
    p += seg((x2-br, y2), (0.408, y2), 20)
    p += bez((0.408, y2), (0.386, y2+0.034), (0.354, y2+0.062), (0.302, y2+0.112), 34)
    p += bez((0.302, y2+0.112), (0.322, y2+0.054), (0.328, y2+0.024), (0.328, y2), 28)
    p += seg((0.328, y2), (bx+br, y2), 14) + arc(bx+br, y2-br, br, math.pi/2, math.pi)
    p += seg((bx, y2-br), (bx, by+br)) + arc(bx+br, by+br, br, math.pi, 1.5*math.pi)
    sh.paint(p, wash, seed=2)
    sh.stroke(p, True, seed=3, amp=0.0038)

    hook = bez((0.380, 0.432), (0.382, 0.352), (0.496, 0.338), (0.549, 0.396)) \
         + bez((0.549, 0.396), (0.595, 0.452), (0.492, 0.472), (0.475, 0.528))[1:]
    sh.stroke(hook, False, seed=8, amp=0.0016)
    sh.stroke(seg((0.475, 0.528), (0.475, 0.552), 10), False, seed=12, amp=0.0006)
    sh.dot(0.475, 0.608, 0.0172)
    sh.stroke(sparkle(0.806, 0.232, 0.056), True, seed=21, amp=0.0012)

def github_portfolio(sh, wash):
    cx, cy, cw, ch, cr = 0.205, 0.300, 0.530, 0.430, 0.088
    card = rrect(cx, cy, cw, ch, cr)
    sh.paint(card, wash, seed=4)
    sh.stroke(card, True, seed=5, amp=0.0038)
    sh.stroke(seg((cx+0.004, cy+0.098), (cx+cw-0.004, cy+0.098), 40), False, seed=9, amp=0.0010)
    sh.dot(cx+0.052, cy+0.050, 0.0122); sh.dot(cx+0.096, cy+0.050, 0.0122)

    sh.stroke(circle(0.312, 0.527, 0.058), True, seed=14, amp=0.0016)
    sh.stroke(bez((0.248, 0.636), (0.258, 0.566), (0.366, 0.566), (0.376, 0.636)),
              False, seed=17, amp=0.0010)
    for i, (y, xe) in enumerate(((0.492, 0.672), (0.548, 0.650), (0.604, 0.600))):
        sh.stroke(seg((0.425, y), (xe, y), 26), False, seed=30+i, amp=0.0008)
    sh.stroke(sparkle(0.806, 0.258, 0.056), True, seed=23, amp=0.0012)

def secure_your_data(sh, wash):
    bx, by, bw, bh, br = 0.300, 0.435, 0.400, 0.335, 0.086
    body = rrect(bx, by, bw, bh, br)
    sr, sy = 0.112, 0.388
    shk = seg((0.500-sr, by), (0.500-sr, sy), 10) + arc(0.500, sy, sr, math.pi, 2*math.pi) \
        + seg((0.500+sr, sy), (0.500+sr, by), 10)
    sh.paint(shk + shk[::-1], wash, seed=6)
    sh.paint(body, wash, seed=7)
    sh.stroke(shk, False, seed=11, amp=0.0014)
    sh.stroke(body, True, seed=7, amp=0.0038)

    sh.stroke(circle(0.500, 0.552, 0.045), True, seed=19, amp=0.0014)
    sh.stroke(seg((0.500, 0.597), (0.500, 0.632), 12), False, seed=27, amp=0.0006)
    for x in (0.420, 0.500, 0.580):
        sh.dot(x, 0.706, 0.0130)
    sh.stroke(sparkle(0.800, 0.302, 0.054), True, seed=25, amp=0.0012)

ICONS = [
    ("worth-asking",             (229, 238, 239), (190, 212, 218), (255, 246, 224),
     (250, 246, 234, 198), worth_asking),
    ("github-portfolio-creator", (251, 239, 222), (235, 206, 180), (255, 247, 223),
     (254, 248, 236, 198), github_portfolio),
    ("secure-your-data",         (234, 238, 219), (196, 209, 185), (255, 250, 226),
     (251, 250, 236, 198), secure_your_data),
]

mask = Image.new("L", (W, W), 0)
ImageDraw.Draw(mask).polygon([(x*W, y*W) for x, y in squircle()], fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(0.8*SS))

for name, top, bot, glow, wash, fn in ICONS:
    sheet = Sheet(ground(top, bot, glow))
    fn(sheet, wash)
    img = sheet.flatten()
    img.putalpha(mask)
    small = img.resize((S, S), Image.LANCZOS)
    a = small.getchannel("A")
    small = paper(small)
    small.putalpha(a)
    small.save(os.path.join(OUT, f"{name}.png"))
    print("wrote", name)

cs = Image.new("RGBA", (S*3+160*4, S+320), (252, 251, 248, 255))
for i, (name, *_ ) in enumerate(ICONS):
    cs.alpha_composite(Image.open(os.path.join(OUT, f"{name}.png")), (160+i*(S+160), 160))
cs.resize((cs.width//3, cs.height//3), Image.LANCZOS).save(os.path.join(OUT, "_contact-sheet.png"))
print("sheet")
