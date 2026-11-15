#!/usr/bin/env python3
"""Builds every SVG used by the profile README.

Edit the DATA block below (roles, toolkit, projects), then run:

    python3 scripts/build_assets.py

All visuals are plain, self-contained SVG (CSS + SMIL animation, system fonts),
so they render inside GitHub's image proxy with no external requests.
"""
from html import escape
from pathlib import Path
import math
import random

OUT = Path(__file__).resolve().parent.parent / "assets"

# ───────────────────────────── DATA ─────────────────────────────
NAME_LINES = ["Gorisi", "Deepak Reddy"]
TAGLINE = "I build AI systems that act, then prove they did."
LOCATION = "BUDAPEST, HU"

# First role is treated as the primary target; the rest follow in order.
ROLES = [
    "Forward Deployed AI Engineer",
    "AI Software Engineer",
    "Agentic AI Engineer",
    "Applied AI Engineer",
    "Multimodal AI Engineer",
    "AI Product Engineer",
    "Computer-Use Agent Engineer",
    "LLM / Agent Platform Engineer",
    "AI Automation Engineer",
    "Research Engineer, Agent Systems",
    "Data Scientist / ML Engineer",
    "BI & Decision Science",
]
EDUCATION = ["BSc Computer Science Engineering", "MSc Business Data Analytics"]

TOOLKIT = [
    ("LANGUAGES", ["Python", "TypeScript", "JavaScript", "SQL", "Swift", "Rust"]),
    ("AGENTS", ["Claude Agent SDK", "Gemini", "Ollama", "MCP", "tool calling", "structured outputs",
                "agent memory", "workflow learning", "multi-agent orchestration", "replay + recovery",
                "verification-driven execution"]),
    ("AI / ML", ["PyTorch", "Transformers", "Qwen 2.5-VL", "GRPO", "scikit-learn", "XGBoost", "SHAP",
                 "TensorFlow", "Keras", "Prophet", "SARIMAX", "embeddings", "RAG"]),
    ("BACKEND + DATA", ["FastAPI", "Node.js", "Express", "PostgreSQL", "SQLite", "Pandas", "NumPy", "ETL",
                        "REST", "WebSockets"]),
    ("FRONTEND + APPS", ["React", "Vite", "Electron", "Tauri", "Recharts", "Streamlit", "Tableau", "Power BI"]),
    ("SYSTEMS", ["WebRTC", "macOS automation", "accessibility APIs", "OCR", "Docker", "GitHub Actions",
                 "Render", "Vercel", "Google Cloud"]),
]
TOOLKIT_ACCENT = "AGENTS"

SECTIONS = [
    ("about", "01", "Principle", "how I think about AI systems"),
    ("echo", "02", "Flagship: Echo", "a local-first agent runtime for macOS"),
    ("work", "03", "Featured work", "products built around real users"),
    ("analytics", "04", "Analytics + applied ML", "models that end in a decision"),
    ("toolkit", "05", "Toolkit", "what I build with"),
    ("roles", "06", "Target roles", "where I fit"),
]

# ──────────────────────────── PALETTE ───────────────────────────
BG, PANEL, PANEL2, LINE, LINE2 = "#0B0F16", "#111824", "#161F2D", "#222C3B", "#2F3B4E"
TEXT, MUTE, DIM = "#E9EEF5", "#93A0B4", "#5D6A7D"
OK, WARN, BAD, INFO = "#4ADE9C", "#FFB84D", "#FF6B6B", "#6CB8FF"

BASE_CSS = f"""
.m{{font-family:ui-monospace,'SF Mono',SFMono-Regular,'JetBrains Mono',Menlo,Consolas,'Liberation Mono',monospace}}
.s{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.35}}}}
@keyframes flow{{to{{stroke-dashoffset:-24}}}}
.flow{{stroke-dasharray:4 8;animation:flow 1.2s linear infinite}}
.pulse{{animation:pulse 2.4s ease-in-out infinite}}
"""
REDUCED = "@media (prefers-reduced-motion:reduce){*{animation:none!important}.rm{opacity:1!important}}"


# ──────────────────────────── HELPERS ───────────────────────────
def e(s):
    return escape(str(s), quote=True)


def doc(w, h, body, label, css="", defs="", rx=18):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{e(label)}">
<title>{e(label)}</title>
<defs>
<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#1A2331"/></pattern>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0E131C"/><stop offset="1" stop-color="#080B11"/></linearGradient>
<clipPath id="frame"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>
{defs}</defs>
<style>{BASE_CSS}{css}{REDUCED}</style>
<g clip-path="url(#frame)">
<rect width="{w}" height="{h}" fill="url(#bg)"/>
<rect width="{w}" height="{h}" fill="url(#grid)"/>
{body}
</g>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{rx - .5}" fill="none" stroke="{LINE}"/>
</svg>
"""


def t(x, y, s, cls="m", size=15, fill=TEXT, anchor=None, weight=None, ls=None, extra=""):
    a = f' text-anchor="{anchor}"' if anchor else ""
    wt = f' font-weight="{weight}"' if weight else ""
    l = f' letter-spacing="{ls}"' if ls is not None else ""
    return f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" fill="{fill}"{a}{wt}{l}{extra}>{e(s)}</text>'


def mw(s, size):
    """Width of monospace text."""
    return len(s) * size * 0.6


def chip(x, y, s, size=14, color=MUTE, stroke=LINE2, fill=PANEL, pad=11, extra=""):
    """Rounded mono chip. (x, y) is the top-left corner. Returns (svg, width, height)."""
    w = mw(s, size) + pad * 2
    h = size + 15
    svg = (f'<g{extra}><rect x="{x}" y="{y}" width="{w:.1f}" height="{h}" rx="{h / 2}" fill="{fill}" stroke="{stroke}"/>'
           f'{t(x + pad, y + h / 2 + size * 0.35, s, size=size, fill=color)}</g>')
    return svg, w, h


def check(x, y, color=OK, s=1.0, sw=2.2):
    return (f'<path d="M{x - 5 * s:.1f} {y:.1f}l{3.6 * s:.1f} {3.8 * s:.1f}l{6.6 * s:.1f} {-7.6 * s:.1f}" fill="none" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')


def arrow_ne(x, y, color=MUTE, s=1.0):
    return (f'<path d="M{x} {y + 10 * s}L{x + 10 * s} {y}M{x + 3 * s} {y}H{x + 10 * s}V{y + 7 * s}" fill="none" '
            f'stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')


def panel(x, y, w, h, title=None, rx=12):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{PANEL}" stroke="{LINE}"/>'
    if title:
        s += t(x + 18, y + 28, title, size=12.5, fill=DIM, ls=2)
    return s


def cycle_css(name, n, slot_s, fade=0.14, shift=True):
    """One keyframe reused by n elements with staggered delays: each is visible for one slot."""
    slot = 100 / n
    a, b = slot * fade, slot * (1 - fade)
    tr0 = "transform:translateY(7px);" if shift else ""
    tr1 = "transform:translateY(0);" if shift else ""
    tr2 = "transform:translateY(-7px);" if shift else ""
    css = (f"@keyframes {name}{{0%{{opacity:0;{tr0}}}{a:.3f}%{{opacity:1;{tr1}}}{b:.3f}%{{opacity:1;{tr1}}}"
           f"{slot:.3f}%{{opacity:0;{tr2}}}100%{{opacity:0;{tr2}}}}}"
           f".{name}{{opacity:0;animation:{name} {n * slot_s:.2f}s linear infinite}}")
    return css


def bezier_len(p0, p1, p2, p3, n=60):
    pts = []
    for i in range(n + 1):
        u = i / n
        x = (1 - u) ** 3 * p0[0] + 3 * (1 - u) ** 2 * u * p1[0] + 3 * (1 - u) * u * u * p2[0] + u ** 3 * p3[0]
        y = (1 - u) ** 3 * p0[1] + 3 * (1 - u) ** 2 * u * p1[1] + 3 * (1 - u) * u * u * p2[1] + u ** 3 * p3[1]
        pts.append((x, y))
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(n))


# ───────────────────────────── HERO ─────────────────────────────
def hero():
    W, H = 1200, 480
    cx, cy, r = 940, 232, 132
    n = len(ROLES)
    css = cycle_css("role", n, 2.6) + cycle_css("st", 4, 2.0, fade=0.1, shift=False)
    css += ("@keyframes node{0%,22%{opacity:1}30%,100%{opacity:.28}}"
            ".node{opacity:.28;animation:node 8s linear infinite}"
            "@keyframes ring{0%{r:9;opacity:.9}25%{r:26;opacity:0}100%{r:26;opacity:0}}"
            ".ring{opacity:0;animation:ring 8s ease-out infinite}"
            "@keyframes scan{0%{transform:translateY(-40px)}100%{transform:translateY(520px)}}"
            ".scan{animation:scan 9s linear infinite}"
            "@keyframes spin{to{transform:rotate(360deg)}}"
            f".spin{{transform-origin:{cx}px {cy}px;animation:spin 60s linear infinite}}")
    defs = (f'<radialGradient id="glow" cx="{cx}" cy="{cy}" r="330" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{OK}" stop-opacity=".17"/><stop offset="1" stop-color="{OK}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="scanG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{OK}" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="{OK}" stop-opacity=".07"/></linearGradient>')
    b = [f'<rect width="{W}" height="{H}" fill="url(#glow)"/>',
         f'<rect class="scan" x="0" y="0" width="{W}" height="40" fill="url(#scanG)"/>']

    # left column
    b.append(f'<circle class="pulse" cx="66" cy="63" r="5" fill="{OK}"/>')
    b.append(t(82, 68, f"AGENT SYSTEMS  /  {LOCATION}  /  OPEN TO ROLES", size=14, fill=MUTE, ls=2.2))
    b.append(t(56, 182, NAME_LINES[0], cls="s", size=92, weight=800, ls=-3))
    b.append(t(56, 276, NAME_LINES[1], cls="s", size=92, weight=800, ls=-3))
    b.append(t(60, 330, TAGLINE, cls="s", size=25, fill=MUTE))
    # role ticker
    b.append(f'<rect x="60" y="372" width="620" height="56" rx="10" fill="{PANEL}" stroke="{LINE}"/>')
    b.append(t(80, 407, "target_role", size=17, fill=DIM))
    b.append(t(80 + mw("target_role ", 17), 407, "=", size=17, fill=DIM))
    rx0 = 80 + mw("target_role = ", 17)
    for i, role in enumerate(ROLES):
        cur_x = rx0 + mw(f'"{role}"', 19) + 5
        b.append(f'<g class="role{" rm" if i == 0 else ""}" style="animation-delay:{i * 2.6:.1f}s">'
                 f'{t(rx0, 408, chr(34) + role + chr(34), size=19, fill=OK, weight=600)}'
                 f'<rect x="{cur_x:.0f}" y="391" width="10" height="21" fill="{OK}" style="animation:blink 1s steps(1) infinite"/></g>')

    # right: observe → reason → act → verify loop
    b.append(f'<g class="spin"><circle cx="{cx}" cy="{cy}" r="{r + 44}" fill="none" stroke="{LINE}" stroke-dasharray="2 10"/></g>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LINE2}" stroke-width="1.5"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{OK}" stroke-width="1.5" class="flow" opacity=".55"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r - 46}" fill="{BG}" stroke="{LINE}"/>')
    nodes = [("OBSERVE", cx, cy - r, "middle", 0, -24), ("REASON", cx + r, cy, "start", 22, 5),
             ("ACT", cx, cy + r, "middle", 0, 36), ("VERIFY", cx - r, cy, "end", -22, 5)]
    for i, (lab, x, y, anc, dx, dy) in enumerate(nodes):
        d = f"animation-delay:{i * 2}s"
        col = OK if lab == "VERIFY" else TEXT
        b.append(f'<circle class="ring" cx="{x}" cy="{y}" r="9" fill="none" stroke="{OK}" stroke-width="1.5" style="{d}"/>')
        b.append(f'<circle cx="{x}" cy="{y}" r="9" fill="{BG}" stroke="{LINE2}" stroke-width="1.5"/>')
        b.append(f'<g class="node" style="{d}"><circle cx="{x}" cy="{y}" r="5" fill="{OK}"/>'
                 f'{t(x + dx, y + dy, lab, size=15, fill=col, anchor=anc, ls=2, weight=600)}</g>')
    path = f"M{cx} {cy - r}A{r} {r} 0 1 1 {cx - 0.01} {cy - r}"
    b.append(f'<circle r="6" fill="{OK}"><animateMotion dur="8s" repeatCount="indefinite" path="{path}"/></circle>')
    b.append(f'<circle r="13" fill="{OK}" opacity=".18"><animateMotion dur="8s" repeatCount="indefinite" path="{path}"/></circle>')
    words = [("observing", MUTE), ("reasoning", WARN), ("acting", INFO), ("verified", OK)]
    for i, (wd, col) in enumerate(words):
        g = t(cx, cy + 6, wd, size=17, fill=col, anchor="middle", weight=600)
        if wd == "verified":
            g = check(cx, cy - 18, s=1.5, sw=2.6) + t(cx, cy + 14, wd, size=17, fill=col, anchor="middle", weight=600)
        b.append(f'<g class="st{" rm" if wd == "verified" else ""}" style="animation-delay:{i * 2}s">{g}</g>')
    b.append(t(cx, cy + r + 78, "a tool response is not proof of success", size=13.5, fill=DIM, anchor="middle", ls=.5))
    return doc(W, H, "".join(b), f"{' '.join(NAME_LINES)}. {TAGLINE} Target roles: {', '.join(ROLES)}.", css, defs)


# ─────────────────────────── PRINCIPLE ──────────────────────────
def principle():
    W, H = 1200, 430
    rnd = random.Random(7)
    gate_x = 600
    lanes = [(246, "computed result"), (292, "enforced boundary"), (338, "verified outcome")]
    css = ("@keyframes wob{0%,100%{transform:translate(0,0)}25%{transform:translate(9px,-7px)}"
           "50%{transform:translate(-6px,8px)}75%{transform:translate(7px,5px)}}"
           ".wob{animation:wob 5s ease-in-out infinite}"
           "@keyframes gate{0%,100%{opacity:.45}50%{opacity:1}}.gate{animation:gate 2.2s ease-in-out infinite}")
    b = [t(60, 62, "DESIGN PRINCIPLE", size=14, fill=MUTE, ls=2.6),
         t(58, 116, "Probabilistic reasoning,", cls="s", size=40, weight=800, ls=-1, fill=WARN),
         t(58, 164, "deterministic execution boundaries.", cls="s", size=40, weight=800, ls=-1, fill=OK)]

    # fuzzy cloud (left)
    for i in range(46):
        x, y = rnd.uniform(70, 500), rnd.uniform(216, 364)
        rr = rnd.uniform(1.6, 4.2)
        b.append(f'<circle class="wob" cx="{x:.0f}" cy="{y:.0f}" r="{rr:.1f}" fill="{WARN}" opacity="{rnd.uniform(.12, .42):.2f}" '
                 f'style="animation-duration:{rnd.uniform(3.5, 8):.1f}s;animation-delay:-{rnd.uniform(0, 6):.1f}s"/>')
    # lanes (right)
    for ly, lab in lanes:
        b.append(f'<line x1="{gate_x}" y1="{ly}" x2="1096" y2="{ly}" stroke="{LINE2}" stroke-width="1.5"/>')
        b.append(f'<line x1="{gate_x}" y1="{ly}" x2="1096" y2="{ly}" stroke="{OK}" stroke-width="1.5" class="flow" opacity=".5"/>')
        for k in range(1, 6):
            b.append(f'<rect x="{gate_x + k * 80 - 3}" y="{ly - 3}" width="6" height="6" fill="{BG}" stroke="{LINE2}"/>')
        b.append(f'<rect x="1100" y="{ly - 14}" width="28" height="28" rx="6" fill="{PANEL}" stroke="{OK}"/>{check(1114, ly)}')
        b.append(t(1090, ly - 11, lab, size=13, fill=MUTE, anchor="end"))
    # gate
    b.append(f'<line x1="{gate_x}" y1="206" x2="{gate_x}" y2="378" stroke="{LINE2}" stroke-width="2"/>')
    for ly, _ in lanes:
        b.append(f'<rect x="{gate_x - 7}" y="{ly - 13}" width="14" height="26" rx="3" fill="{BG}" stroke="{OK}" stroke-width="1.6" class="gate"/>')
    # particles crossing the gate
    for li, (ly, _) in enumerate(lanes):
        for k in range(4):
            sx, sy = rnd.uniform(70, 260), rnd.uniform(216, 364)
            c1 = (sx + rnd.uniform(80, 170), sy + rnd.uniform(-80, 80))
            c2 = (gate_x - rnd.uniform(90, 160), ly + rnd.uniform(-50, 50))
            l1 = bezier_len((sx, sy), c1, c2, (gate_x, ly))
            l2 = 1096 - gate_x
            f = l1 / (l1 + l2)
            dur = rnd.uniform(5.5, 8.5)
            beg = -rnd.uniform(0, dur)
            d = f"M{sx:.0f} {sy:.0f}C{c1[0]:.0f} {c1[1]:.0f} {c2[0]:.0f} {c2[1]:.0f} {gate_x} {ly}L1096 {ly}"
            kt = f"0;{max(f - .02, .01):.3f};{min(f + .02, .99):.3f};1"
            b.append(f'<circle r="4.5" fill="{WARN}"><animateMotion dur="{dur:.1f}s" begin="{beg:.1f}s" repeatCount="indefinite" path="{d}"/>'
                     f'<animate attributeName="fill" dur="{dur:.1f}s" begin="{beg:.1f}s" repeatCount="indefinite" values="{WARN};{WARN};{OK};{OK}" keyTimes="{kt}"/>'
                     f'<animate attributeName="opacity" dur="{dur:.1f}s" begin="{beg:.1f}s" repeatCount="indefinite" values="0;1;1;0" keyTimes="0;.08;.95;1"/></circle>')
    gl = "TYPED TOOLS · PERMISSIONS · SAFETY POLICY"
    b.append(f'<rect x="{gate_x - mw(gl, 12.5) / 2 - 12}" y="384" width="{mw(gl, 12.5) + 24}" height="26" rx="13" fill="{BG}" stroke="{LINE2}"/>')
    b.append(t(gate_x, 402, gl, size=12.5, fill=TEXT, anchor="middle", ls=0))
    b.append(t(60, 402, "AI interprets · retrieves · selects", size=14, fill=WARN))
    b.append(t(1140, 402, "systems compute · tools enforce", size=14, fill=OK, anchor="end"))
    return doc(W, H, "".join(b),
               "Design principle: probabilistic reasoning with deterministic execution boundaries. AI interprets intent, "
               "retrieves evidence and selects tools; typed tools, permissions and safety policy form the gate; "
               "authoritative systems compute results and verification decides success.", css)


# ───────────────────────────── ECHO ─────────────────────────────
def echo():
    W, H = 1200, 664
    css, b = "", []
    # window chrome
    b.append(f'<rect width="{W}" height="56" fill="{PANEL}"/><line x1="0" y1="56" x2="{W}" y2="56" stroke="{LINE}"/>')
    for i, c in enumerate([BAD, WARN, OK]):
        b.append(f'<circle cx="{34 + i * 22}" cy="28" r="6.5" fill="{c}" opacity=".85"/>')
    b.append(t(112, 33, "echo", size=16, fill=TEXT, weight=700))
    b.append(t(112 + mw("echo ", 16), 33, "— executive computer heuristic operator", size=15, fill=MUTE))
    b.append(f'<circle class="pulse" cx="1050" cy="28" r="5" fill="{OK}"/>')
    b.append(t(1064, 33, "runtime live", size=14, fill=OK))

    # A: loop
    ax, ay, aw, ah = 28, 80, 262, 448
    b.append(panel(ax, ay, aw, ah, "LOOP"))
    steps = [("PERCEIVE", "screen · OCR · AX tree"), ("PLAN", "preview before execution"),
             ("ACT", "semantic control + tools"), ("VERIFY", "task postconditions"),
             ("RECOVER", "no blind repeats"), ("LEARN", "skills from demos")]
    n = len(steps)
    slot = 100 / n
    css += (f"@keyframes step{{0%,{slot:.2f}%{{opacity:1}}{slot + 3:.2f}%,97%{{opacity:0}}100%{{opacity:1}}}}"
            f".step{{opacity:0;animation:step {n * 2}s linear infinite}}")
    for i, (nm, sub) in enumerate(steps):
        y = ay + 52 + i * 64
        b.append(f'<g class="step{" rm" if nm == "VERIFY" else ""}" style="animation-delay:{i * 2}s">'
                 f'<rect x="{ax + 10}" y="{y - 6}" width="{aw - 20}" height="56" rx="9" fill="{OK}" fill-opacity=".1" stroke="{OK}" stroke-opacity=".55"/>'
                 f'<rect x="{ax + 10}" y="{y + 6}" width="3" height="32" rx="1.5" fill="{OK}"/></g>')
        b.append(t(ax + 26, y + 18, f"{i + 1:02d}", size=13, fill=DIM))
        b.append(t(ax + 56, y + 18, nm, size=16, fill=TEXT, weight=700, ls=1.5))
        b.append(t(ax + 56, y + 38, sub, size=13.5, fill=MUTE))

    # B: screen
    bx, by, bw, bh = 306, 80, 510, 448
    b.append(panel(bx, by, bw, bh, "SCREEN"))
    b.append(t(bx + bw - 18, by + 28, "see · target · act", size=12.5, fill=DIM, anchor="end"))
    dx, dy, dw, dh = bx + 18, by + 44, bw - 36, 300
    b.append(f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" rx="8" fill="{BG}" stroke="{LINE}"/>')
    b.append(f'<rect x="{dx}" y="{dy}" width="{dw}" height="20" rx="8" fill="{PANEL2}"/>')
    for i in range(5):
        b.append(f'<rect x="{dx + 12 + i * 44}" y="{dy + 7}" width="30" height="6" rx="3" fill="{LINE2}"/>')
    # app window
    wx, wy, ww, wh = dx + 26, dy + 40, dw - 52, dh - 62
    b.append(f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="8" fill="{PANEL}" stroke="{LINE2}"/>')
    for i, c in enumerate([BAD, WARN, OK]):
        b.append(f'<circle cx="{wx + 16 + i * 14}" cy="{wy + 15}" r="4" fill="{c}" opacity=".6"/>')
    # search field (target 1)
    sfx, sfy = wx + 150, wy + 7
    b.append(f'<rect x="{sfx}" y="{sfy}" width="170" height="17" rx="8.5" fill="{BG}" stroke="{LINE2}"/>')
    b.append(f'<line x1="{wx}" y1="{wy + 30}" x2="{wx + ww}" y2="{wy + 30}" stroke="{LINE}"/>')
    b.append(f'<line x1="{wx + 110}" y1="{wy + 30}" x2="{wx + 110}" y2="{wy + wh}" stroke="{LINE}"/>')
    for i in range(6):
        b.append(f'<rect x="{wx + 14}" y="{wy + 46 + i * 24}" width="{[70, 54, 80, 62, 48, 72][i]}" height="7" rx="3.5" fill="{LINE2}"/>')
    b.append(f'<rect x="{wx + 8}" y="{wy + 63}" width="94" height="20" rx="5" fill="{OK}" fill-opacity=".08"/>')
    # document lines (target 2 = OCR)
    lx = wx + 128
    widths = [250, 286, 210, 268, 180]
    css += ("@keyframes ocr{0%,30%{opacity:0}36%,62%{opacity:1}68%,100%{opacity:0}}"
            ".ocr{opacity:0;animation:ocr 9s linear infinite}")
    for i, wd in enumerate(widths):
        yy = wy + 50 + i * 22
        b.append(f'<rect x="{lx}" y="{yy}" width="{wd}" height="7" rx="3.5" fill="{LINE2}"/>')
        b.append(f'<rect class="ocr" x="{lx - 5}" y="{yy - 6}" width="{wd + 10}" height="19" rx="3" fill="none" stroke="{INFO}" stroke-dasharray="3 3" '
                 f'style="animation-delay:{i * .18:.2f}s"/>')
    # send button (target 3)
    sbx, sby = wx + ww - 104, wy + wh - 44
    css += (f"@keyframes sent{{0%,70%{{fill:{PANEL2};stroke:{LINE2}}}76%,96%{{fill:#14402E;stroke:{OK}}}100%{{fill:{PANEL2};stroke:{LINE2}}}}}"
            ".sent{animation:sent 9s linear infinite}")
    b.append(f'<rect class="sent" x="{sbx}" y="{sby}" width="86" height="28" rx="7" fill="{PANEL2}" stroke="{LINE2}"/>')
    b.append(t(sbx + 43, sby + 19, "Send", cls="s", size=14, fill=TEXT, anchor="middle", weight=600))
    # reticle
    t1 = (sfx + 85, sfy + 8.5)
    t2 = (lx + 120, wy + 50 + 2 * 22 + 3)
    t3 = (sbx + 43, sby + 14)
    css += (f"@keyframes ret{{0%,22%{{transform:translate({t1[0]}px,{t1[1]}px)}}33%,62%{{transform:translate({t2[0]}px,{t2[1]}px)}}"
            f"72%,94%{{transform:translate({t3[0]}px,{t3[1]}px)}}100%{{transform:translate({t1[0]}px,{t1[1]}px)}}}}"
            f".ret{{transform:translate({t3[0]}px,{t3[1]}px);animation:ret 9s cubic-bezier(.6,0,.3,1) infinite}}"
            "@keyframes rpulse{0%,100%{transform:scale(1)}50%{transform:scale(.82)}}"
            ".rp{animation:rpulse 1.2s ease-in-out infinite}")
    ret = "".join(f'<path d="M{sx * 22} {sy * 13}v{-sy * 9}h{-sx * 0}M{sx * 22} {sy * 13}h{-sx * 9}" fill="none" stroke="{OK}" stroke-width="2.2" stroke-linecap="round"/>'
                  for sx in (-1, 1) for sy in (-1, 1))
    b.append(f'<g class="ret"><g class="rp">{ret}</g><circle r="2.5" fill="{OK}"/></g>')
    # target tags
    css += cycle_css("tag", 3, 3.0, fade=0.1, shift=False)
    tags = [("AXSearchField · focus", t1, 14, 30), ("OCR · 5 lines · 0.98", t2, -60, -50), ('AXButton "Send" · click', t3, -168, -34)]
    for i, (lab, (tx, ty), ox, oy) in enumerate(tags):
        w = mw(lab, 12) + 16
        b.append(f'<g class="tag{" rm" if i == 2 else ""}" style="animation-delay:{i * 3}s"><rect x="{tx + ox:.0f}" y="{ty + oy:.0f}" width="{w:.0f}" height="22" rx="5" fill="{BG}" stroke="{OK}"/>'
                 f'{t(tx + ox + 8, ty + oy + 15.5, lab, size=12, fill=OK)}</g>')
    # voice strip
    vy = dy + dh + 20
    b.append(t(bx + 18, vy + 20, "VOICE", size=12.5, fill=DIM, ls=2))
    css += ("@keyframes bar{0%,100%{transform:scaleY(.25)}50%{transform:scaleY(1)}}"
            ".bar{transform-box:fill-box;transform-origin:center;animation:bar 1s ease-in-out infinite}")
    rnd = random.Random(3)
    for i in range(34):
        hh = rnd.choice([10, 16, 24, 30, 20, 14])
        b.append(f'<rect class="bar" x="{bx + 84 + i * 6.4:.1f}" y="{vy + 16 - hh / 2}" width="3.2" height="{hh}" rx="1.6" fill="{OK}" opacity=".8" '
                 f'style="animation-duration:{rnd.uniform(.7, 1.5):.2f}s;animation-delay:-{rnd.uniform(0, 1.2):.2f}s"/>')
    b.append(t(bx + bw - 18, vy + 20, "wake · VAD · STT · TTS", size=12.5, fill=MUTE, anchor="end"))
    b.append(t(bx + 18, vy + 52, "barge-in interruption · local-first transcription", size=12.5, fill=DIM))

    # C: journal
    jx, jy, jw, jh = 832, 80, 340, 448
    b.append(panel(jx, jy, jw, jh, "AGENT JOURNAL"))
    entries = [("09:41:02", "observe", "screen + AX tree", None), ("09:41:03", "plan", "3 steps · preview ok", None),
               ("09:41:05", "act", 'click AXButton "Send"', None), ("09:41:06", "verify", "postcondition met", ("verified", OK)),
               ("09:41:09", "act", "upload report.pdf", ("uncertain", WARN)),
               ("09:41:10", "recover", "re-observe, no repeat", ("partial", INFO)),
               ("09:41:12", "verify", "file present in thread", ("verified", OK))]
    cyc = 14.0
    for i, (tm, verb, det, st) in enumerate(entries):
        a = (0.3 + i * 1.0) / cyc * 100
        css += (f"@keyframes j{i}{{0%,{a:.2f}%{{opacity:0;transform:translateX(-8px)}}{a + 2.5:.2f}%,93%{{opacity:1;transform:translateX(0)}}"
                f"98%,100%{{opacity:0;transform:translateX(0)}}}}.j{i}{{animation:j{i} {cyc}s linear infinite}}")
        y = jy + 62 + i * 54
        vc = OK if verb == "verify" else (INFO if verb == "recover" else TEXT)
        g = t(jx + 18, y, tm, size=12.5, fill=DIM) + t(jx + 92, y, verb, size=14, fill=vc, weight=700)
        g += t(jx + 92, y + 20, det, size=13.5, fill=MUTE)
        if st:
            c, w, h = chip(jx + jw - 18 - (mw(st[0], 11.5) + 16), y - 20, st[0], size=11.5, color=st[1], stroke=st[1], fill=BG, pad=8)
            g += c
        if i < len(entries) - 1:
            g += f'<line x1="{jx + 18}" y1="{y + 33}" x2="{jx + jw - 18}" y2="{y + 33}" stroke="{LINE}"/>'
        b.append(f'<g class="j{i} rm">{g}</g>')

    # bottom strip: brains + capabilities
    sy = 546
    b.append(f'<rect x="28" y="{sy}" width="{W - 56}" height="90" rx="12" fill="{PANEL}" stroke="{LINE}"/>')
    b.append(t(46, sy + 28, "BRAIN", size=12.5, fill=DIM, ls=2))
    brains = ["Claude", "Gemini", "Ollama · local"]
    css += cycle_css("brain", 3, 3.2, fade=0.08, shift=False)
    x = 46
    for i, br in enumerate(brains):
        w = mw(br, 15) + 28
        b.append(f'<rect x="{x}" y="{sy + 42}" width="{w:.0f}" height="34" rx="8" fill="{BG}" stroke="{LINE2}"/>')
        b.append(f'<rect class="brain{" rm" if i == 0 else ""}" x="{x}" y="{sy + 42}" width="{w:.0f}" height="34" rx="8" fill="{OK}" fill-opacity=".14" stroke="{OK}" style="animation-delay:{i * 3.2}s"/>')
        b.append(t(x + 14, sy + 64, br, size=15, fill=TEXT, weight=600))
        x += w + 10
    b.append(t(x + 6, sy + 64, "live switch", size=12.5, fill=DIM))
    b.append(f'<line x1="470" y1="{sy + 16}" x2="470" y2="{sy + 74}" stroke="{LINE}"/>')
    b.append(t(492, sy + 28, "RUNTIME", size=12.5, fill=DIM, ls=2))
    caps = ["project-scoped memory", "durable checkpoints", "run replay", "multi-agent missions"]
    x = 492
    for c_ in caps:
        c, w, h = chip(x, sy + 44, c_, size=12.5, color=TEXT, fill=BG, pad=10)
        b.append(c)
        x += w + 8
    return doc(W, H, "".join(b),
               "Echo, Executive Computer Heuristic Operator: a local-first autonomous agent runtime for macOS. "
               "Loop: perceive, plan, act, verify, recover, learn. It sees the screen through screenshots, OCR and accessibility APIs, "
               "targets controls semantically, streams voice, and keeps an agent journal that tracks verified, uncertain, "
               "partial and failed operations separately. Brains switch live between Claude, Gemini and local Ollama.", css)


# ───────────────────────── TRAINING LOOP ────────────────────────
def training():
    W, H = 1200, 330
    nodes = [("Frontier", "teacher", MUTE), ("Echo", "trajectories", MUTE), ("Filter · label", "verify", OK),
             ("Synthetic + real", "dataset", MUTE), ("Qwen 2.5-VL", "GRPO fine-tune", WARN), ("Local", "multimodal agent", OK)]
    bw, gap, x0, y0, bh = 164, 23, 50, 104, 84
    b = [t(60, 58, "AGENT TRAINING LOOP", size=14, fill=MUTE, ls=2.6),
         t(1140, 58, "distilling reliable computer use into a local model", size=14, fill=DIM, anchor="end")]
    cxs = []
    for i, (a, c, col) in enumerate(nodes):
        x = x0 + i * (bw + gap)
        cxs.append(x + bw / 2)
        b.append(f'<rect x="{x}" y="{y0}" width="{bw}" height="{bh}" rx="12" fill="{PANEL}" stroke="{col if col != MUTE else LINE2}"/>')
        b.append(t(x + 16, y0 + 26, f"{i + 1:02d}", size=12, fill=DIM))
        b.append(t(x + 16, y0 + 50, a, cls="s", size=17, fill=TEXT, weight=700))
        b.append(t(x + 16, y0 + 70, c, size=12.5, fill=col))
        if i < len(nodes) - 1:
            xa, xb = x + bw, x + bw + gap
            b.append(f'<line x1="{xa}" y1="{y0 + bh / 2}" x2="{xb}" y2="{y0 + bh / 2}" stroke="{OK}" stroke-width="2" class="flow"/>')
    # return arc
    ya = y0 + bh
    xl, xr = cxs[0], cxs[-1]
    arc = f"M{xr} {ya}V{ya + 44}Q{xr} {ya + 64} {xr - 20} {ya + 64}H{xl + 20}Q{xl} {ya + 64} {xl} {ya + 44}V{ya + 8}"
    b.append(f'<path d="{arc}" fill="none" stroke="{LINE2}" stroke-width="1.5"/>')
    b.append(f'<path d="{arc}" fill="none" stroke="{OK}" stroke-width="1.5" class="flow" opacity=".7"/>')
    b.append(f'<path d="M{xl - 6} {ya + 15}L{xl} {ya + 6}L{xl + 6} {ya + 15}" fill="none" stroke="{OK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    for k in range(3):
        b.append(f'<circle r="4.5" fill="{OK}"><animateMotion dur="7s" begin="-{k * 2.33:.2f}s" repeatCount="indefinite" path="{arc}"/></circle>')
    lab = "new verified trajectories + evaluation"
    lw = mw(lab, 13.5) + 28
    b.append(f'<rect x="{600 - lw / 2}" y="{ya + 50}" width="{lw}" height="28" rx="14" fill="{BG}" stroke="{LINE2}"/>')
    b.append(t(600, ya + 69, lab, size=13.5, fill=TEXT, anchor="middle"))
    return doc(W, H, "".join(b),
               "Agent training loop: frontier-model teacher, Echo observations and tool calls, filter label and verify trajectories, "
               "synthetic plus real dataset, Qwen 2.5-VL fine-tuning with GRPO, local multimodal agent, then new verified "
               "trajectories and evaluation feed back into the loop.")


# ──────────────────────── PROJECT CARDS ─────────────────────────
def ill_aira():
    b, css = [], ""
    gx, gy = 300, 226
    left = [("WEB", 172), ("MACOS", 216), ("WINDOWS", 260)]
    right = [("BROWSER", 172), ("CODE", 216), ("MCP", 260)]
    for lab, y in left:
        b.append(f'<rect x="40" y="{y}" width="112" height="32" rx="7" fill="{PANEL}" stroke="{LINE2}"/>{t(96, y + 21, lab, size=12.5, fill=TEXT, anchor="middle", ls=1)}')
        p = f"M152 {y + 16}C200 {y + 16} 200 {gy} 244 {gy}"
        b.append(f'<path d="{p}" fill="none" stroke="{LINE2}" stroke-width="1.5"/>')
        b.append(f'<circle r="3.5" fill="{INFO}"><animateMotion dur="2.4s" begin="-{y % 7 * .3:.1f}s" repeatCount="indefinite" path="{p}"/></circle>')
    for lab, y in right:
        b.append(f'<rect x="448" y="{y}" width="112" height="32" rx="7" fill="{PANEL}" stroke="{LINE2}"/>{t(504, y + 21, lab, size=12.5, fill=TEXT, anchor="middle", ls=1)}')
        p = f"M356 {gy}C400 {gy} 400 {y + 16} 448 {y + 16}"
        b.append(f'<path d="{p}" fill="none" stroke="{LINE2}" stroke-width="1.5"/>')
        b.append(f'<circle r="3.5" fill="{OK}"><animateMotion dur="2.4s" begin="-{y % 5 * .4:.1f}s" repeatCount="indefinite" path="{p}"/></circle>')
    b.append(f'<rect x="244" y="188" width="112" height="76" rx="12" fill="{PANEL2}" stroke="{OK}"/>')
    b.append(f'<path d="M293 219v-5a7 7 0 0 1 14 0v5" fill="none" stroke="{OK}" stroke-width="2"/><rect x="289" y="219" width="22" height="16" rx="3.5" fill="{OK}"/>')
    b.append(t(300, 254, "GATEWAY", size=12.5, fill=TEXT, anchor="middle", ls=1.5))
    b.append(t(300, 290, "approve → execute", size=12.5, fill=DIM, anchor="middle"))
    return "".join(b), css


def ill_studio():
    b = []
    css = ("@keyframes grow{0%{transform:scaleY(.15)}35%,85%{transform:scaleY(1)}100%{transform:scaleY(.15)}}"
           ".grow{transform-box:fill-box;transform-origin:bottom;animation:grow 6s ease-in-out infinite}"
           "@keyframes growx{0%{transform:scaleX(.05)}40%,85%{transform:scaleX(1)}100%{transform:scaleX(.05)}}"
           ".growx{transform-box:fill-box;transform-origin:left;animation:growx 6s ease-in-out infinite}"
           "@keyframes draw{0%{stroke-dashoffset:320}45%,85%{stroke-dashoffset:0}100%{stroke-dashoffset:320}}"
           ".draw{stroke-dasharray:320;animation:draw 6s ease-in-out infinite}")
    b.append(f'<path d="M44 168V292H296" fill="none" stroke="{LINE2}" stroke-width="1.5"/>')
    hs = [38, 54, 46, 70, 62, 88, 80, 104]
    pts = []
    for i, h in enumerate(hs):
        x = 58 + i * 29
        b.append(f'<rect class="grow" x="{x}" y="{292 - h}" width="17" height="{h}" rx="3" fill="{INFO}" opacity=".5" style="animation-delay:{i * .08:.2f}s"/>')
        pts.append(f"{x + 8.5} {292 - h - 12}")
    b.append(f'<path class="draw" d="M{" L".join(pts)}" fill="none" stroke="{OK}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
    b.append(t(330, 180, "SHAP", size=12.5, fill=DIM, ls=2))
    feats = [("tenure", 120, OK), ("spend", 92, OK), ("region", -64, BAD), ("visits", 50, OK), ("age", -30, BAD)]
    for i, (f, v, c) in enumerate(feats):
        y = 194 + i * 21
        b.append(t(330, y + 11, f, size=12.5, fill=MUTE))
        b.append(f'<rect class="growx" x="400" y="{y}" width="{abs(v) * 1.3:.0f}" height="13" rx="3" fill="{c}" opacity=".85" style="animation-delay:{i * .1:.1f}s"/>')
    return "".join(b), css


def ill_talktual():
    b = []
    css = ("@keyframes bar{0%,100%{transform:scaleY(.25)}50%{transform:scaleY(1)}}"
           ".bar{transform-box:fill-box;transform-origin:center;animation:bar 1s ease-in-out infinite}")
    css += cycle_css("lang", 3, 2.8, fade=0.12)
    b.append(f'<path d="M52 170h188a12 12 0 0 1 12 12v32a12 12 0 0 1-12 12H76l-18 16v-16h-6a12 12 0 0 1-12-12v-32a12 12 0 0 1 12-12z" fill="{PANEL}" stroke="{LINE2}"/>')
    b.append(t(58, 194, "EN", size=12, fill=DIM, ls=1.5))
    b.append(t(58, 215, "Hello, how are you?", cls="s", size=16, fill=TEXT, weight=600))
    b.append(f'<path d="M360 226h188a12 12 0 0 1 12 12v32a12 12 0 0 1-12 12h-6v16l-18-16H360a12 12 0 0 1-12-12v-32a12 12 0 0 1 12-12z" fill="{PANEL2}" stroke="{OK}"/>')
    langs = [("HU", "Szia, hogy vagy?"), ("ES", "Hola, ¿cómo estás?"), ("DE", "Hallo, wie geht's?")]
    for i, (code, s) in enumerate(langs):
        b.append(f'<g class="lang{" rm" if i == 0 else ""}" style="animation-delay:{i * 2.8:.1f}s">{t(366, 250, code, size=12, fill=OK, ls=1.5)}'
                 f'{t(366, 271, s, cls="s", size=16, fill=TEXT, weight=600)}</g>')
    rnd = random.Random(11)
    for i in range(13):
        hh = rnd.choice([10, 18, 26, 34, 22])
        b.append(f'<rect class="bar" x="{266 + i * 5.4:.1f}" y="{226 - hh / 2}" width="3" height="{hh}" rx="1.5" fill="{OK}" '
                 f'style="animation-duration:{rnd.uniform(.7, 1.4):.2f}s;animation-delay:-{rnd.uniform(0, 1):.2f}s"/>')
    b.append(t(300, 262, "live", size=12, fill=DIM, anchor="middle"))
    return "".join(b), css


def ill_transfer():
    b = []
    css = ("@keyframes fill{0%{width:0}85%,100%{width:400px}}.fill{animation:fill 6s cubic-bezier(.4,0,.2,1) infinite}")
    for x, lab in ((76, "PEER A"), (524, "PEER B")):
        b.append(f'<circle cx="{x}" cy="208" r="26" fill="{PANEL}" stroke="{LINE2}" stroke-width="1.5"/><circle cx="{x}" cy="208" r="6" fill="{OK}"/>')
        b.append(t(x, 256, lab, size=12, fill=MUTE, anchor="middle", ls=1.5))
    b.append(f'<line x1="102" y1="208" x2="498" y2="208" stroke="{LINE2}" stroke-width="12" stroke-linecap="round"/>')
    b.append(f'<line x1="102" y1="208" x2="498" y2="208" stroke="{BG}" stroke-width="8" stroke-linecap="round"/>')
    for k in range(7):
        b.append(f'<rect x="-9" y="-3" width="18" height="6" rx="3" fill="{OK}"><animateMotion dur="2.8s" begin="-{k * .4:.1f}s" repeatCount="indefinite" path="M110 208H490"/></rect>')
    b.append(f'<rect x="270" y="182" width="60" height="52" rx="10" fill="{PANEL2}" stroke="{OK}"/>')
    b.append(f'<path d="M293 205v-5a7 7 0 0 1 14 0v5" fill="none" stroke="{OK}" stroke-width="2"/><rect x="289" y="205" width="22" height="16" rx="3.5" fill="{OK}"/>')
    b.append(t(300, 256, "AES-GCM", size=12, fill=OK, anchor="middle", ls=1))
    b.append(f'<rect x="100" y="280" width="400" height="10" rx="5" fill="{PANEL2}"/>')
    b.append(f'<rect class="fill" x="100" y="280" width="400" height="10" rx="5" fill="{OK}"/>')
    b.append(t(512, 290, "100GB+", size=13, fill=TEXT, weight=700))
    b.append(t(40, 290, "disk", size=12.5, fill=DIM))
    return "".join(b), css


def ill_gita():
    b = []
    cols, total, sx, sy, x0, y0 = 47, 701, 11.2, 9.4, 42, 172
    d = []
    for i in range(total):
        d.append(f"M{x0 + (i % cols) * sx:.1f} {y0 + (i // cols) * sy:.1f}h0")
    b.append(f'<path d="{"".join(d)}" stroke="{LINE2}" stroke-width="3.4" stroke-linecap="round" fill="none"/>')
    css = ("@keyframes sweep{0%{transform:translateX(0)}100%{transform:translateX(540px)}}"
           ".sweep{animation:sweep 5s linear infinite}"
           "@keyframes hit{0%,100%{r:7;opacity:.9}50%{r:11;opacity:.25}}.hit{animation:hit 1.8s ease-in-out infinite}")
    b.append(f'<rect class="sweep" x="24" y="162" width="16" height="148" fill="url(#sw)"/>')
    hits = [(9, 2), (21, 6), (30, 3), (38, 11), (15, 12)]
    qx, qy = 196, 326
    for i, (c, r) in enumerate(hits):
        x, y = x0 + c * sx, y0 + r * sy
        b.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{qx}" y2="{qy - 12}" stroke="{OK}" stroke-width="1" opacity=".35"/>')
        b.append(f'<circle class="hit" cx="{x:.1f}" cy="{y:.1f}" r="7" fill="none" stroke="{OK}" stroke-width="1.5" style="animation-delay:-{i * .35:.2f}s"/>')
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="{OK}"/>')
    b.append(f'<circle cx="{qx}" cy="{qy - 12}" r="4.5" fill="{WARN}"/>')
    b.append(t(qx + 12, qy - 8, "a personal question → 5 grounded verses", size=12, fill=MUTE))
    return "".join(b), css


def ill_analytics():
    b = []
    css = ("@keyframes draw2{0%{stroke-dashoffset:420}40%,88%{stroke-dashoffset:0}100%{stroke-dashoffset:420}}"
           ".draw2{stroke-dasharray:420;animation:draw2 7s ease-in-out infinite}"
           "@keyframes band{0%,35%{opacity:0}55%,88%{opacity:1}100%{opacity:0}}.band{animation:band 7s ease-in-out infinite}")
    for y in (190, 230, 270):
        b.append(f'<line x1="40" y1="{y}" x2="560" y2="{y}" stroke="{LINE}" stroke-dasharray="2 6"/>')
    hist = "M40 276L72 262L104 268L136 244L168 250L200 226L232 236L264 214L296 220L330 204"
    b.append(f'<path class="draw2" d="{hist}" fill="none" stroke="{TEXT}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
    b.append(f'<g class="band rm"><path d="M330 204L400 184L470 168L560 146L560 204L470 204L400 204Z" fill="{OK}" opacity=".13"/>'
             f'<path d="M330 204L400 194L470 186L560 175" fill="none" stroke="{OK}" stroke-width="2.4" stroke-dasharray="6 6" stroke-linecap="round"/>'
             f'<circle cx="560" cy="175" r="4.5" fill="{OK}"/></g>')
    b.append(f'<line x1="330" y1="162" x2="330" y2="300" stroke="{WARN}" stroke-dasharray="3 4"/>')
    b.append(t(338, 298, "decision point", size=12, fill=WARN))
    b.append(t(40, 298, "history", size=12, fill=DIM))
    b.append(t(560, 298, "forecast ± band", size=12, fill=OK, anchor="end"))
    return "".join(b), css


CARDS = [
    ("aira", "AI WORKSPACE", "Aira.AI", "Cross-platform AI workspace behind a permission gateway.",
     "Tauri · MCP · OpenCode · server-side keys", False, ill_aira),
    ("studio", "DATA SCIENCE", "Data Science Studio", "Real server-side EDA and training; the LLM only narrates.",
     "React · FastAPI · XGBoost · SHAP · CI", True, ill_studio),
    ("talktual", "REAL-TIME VOICE", "Talktual", "Two people, two languages, one natural conversation.",
     "WebRTC · QR handshake · STT · translate · TTS", True, ill_talktual),
    ("transfer", "P2P TRANSFER", "Tata Dransfer", "Encrypted peer-to-peer files, calls and chat.",
     "WebRTC · direct-to-disk streaming · calls", True, ill_transfer),
    ("gita", "RETRIEVAL", "Gita.AI", "Grounded in all 701 verses, not in model memory.",
     "embeddings · RAG · multilingual · donated to ISKCON", False, ill_gita),
    ("analytics", "DECISION SCIENCE", "Analytics + applied ML", "Eight systems where the model ends in a decision.",
     "forecasting · churn · risk · SQL · Tableau", False, ill_analytics),
]


def card(idx, kind, title, desc, stack, live, ill):
    W, H = 600, 372
    body, css = ill()
    defs = (f'<linearGradient id="sw" x1="0" x2="1"><stop offset="0" stop-color="{OK}" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="{OK}" stop-opacity=".28"/></linearGradient>')
    b = [t(36, 50, f"{idx:02d}", size=14, fill=OK, weight=700), t(66, 50, kind, size=13.5, fill=MUTE, ls=2.2)]
    if live:
        b.append(f'<rect x="494" y="32" width="70" height="26" rx="13" fill="{BG}" stroke="{OK}"/>'
                 f'<circle class="pulse" cx="511" cy="45" r="4" fill="{OK}"/>{t(522, 50, "LIVE", size=12.5, fill=OK, ls=1.5, weight=700)}')
    else:
        b.append(arrow_ne(548, 36, MUTE, 1.3))
    b.append(t(35, 100, title, cls="s", size=34, weight=800, ls=-.8))
    b.append(t(36, 132, desc, cls="s", size=17, fill=MUTE))
    b.append(body)
    b.append(f'<line x1="36" y1="326" x2="564" y2="326" stroke="{LINE}"/>')
    b.append(t(36, 351, stack, size=13, fill=DIM))
    return doc(W, H, "".join(b), f"{title}: {desc} {stack}", css, defs, rx=16)


# ──────────────────────────── TOOLKIT ───────────────────────────
def toolkit():
    W = 1200
    x_lab, x0, x_max, size, row_h = 56, 258, 1148, 14.5, 40
    b, y = [], 96
    css = f"@keyframes lit{{0%,6%{{stroke:{OK};fill:#12261E}}12%,100%{{stroke:{LINE2};fill:{PANEL}}}}}"
    k = 0
    chips_out = []
    for lab, items in TOOLKIT:
        acc = lab == TOOLKIT_ACCENT
        b.append(t(x_lab, y + 20, lab, size=13, fill=OK if acc else MUTE, ls=2))
        x = x0
        for it in items:
            w = mw(it, size) + 24
            if x + w > x_max:
                x, y = x0, y + row_h
            chips_out.append((x, y, w, it, acc, k))
            k += 1
            x += w + 9
        y += row_h + 18
        b.append(f'<line x1="{x_lab}" y1="{y - 13}" x2="{x_max}" y2="{y - 13}" stroke="{LINE}" stroke-dasharray="2 6"/>')
    b.pop()
    total = k
    dur = total * 0.22
    css += f".lit{{animation:lit {dur:.1f}s linear infinite}}"
    for x, yy, w, it, acc, i in chips_out:
        b.append(f'<rect class="lit" x="{x:.1f}" y="{yy}" width="{w:.1f}" height="30" rx="8" fill="{PANEL}" stroke="{LINE2}" style="animation-delay:{i * .22 - dur:.2f}s"/>')
        b.append(t(x + 12, yy + 20, it, size=size, fill=OK if acc else TEXT))
    H = y - 6
    head = [t(56, 58, "TECHNICAL TOOLKIT", size=14, fill=MUTE, ls=2.6),
            t(1144, 58, "agent engineering is the centre of gravity", size=14, fill=DIM, anchor="end")]
    return doc(W, H, "".join(head + b), "Technical toolkit. " + " ".join(f"{l}: {', '.join(i)}." for l, i in TOOLKIT), css)


# ───────────────────────────── ROLES ────────────────────────────
def roles():
    W = 1200
    primary, rest = ROLES[0], ROLES[1:]
    n = len(rest)
    css = (f"@keyframes lock{{0%,{100 / n * .85:.2f}%{{opacity:1}}{100 / n:.2f}%,100%{{opacity:0}}}}"
           f".lock{{opacity:0;animation:lock {n * 1.4:.1f}s linear infinite}}"
           "@keyframes corner{0%,100%{transform:scale(1)}50%{transform:scale(1.012)}}"
           ".corner{transform-box:fill-box;transform-origin:center;animation:corner 2.8s ease-in-out infinite}")
    b = [t(56, 58, "TARGET ROLES", size=14, fill=MUTE, ls=2.6),
         f'<circle class="pulse" cx="{1144 - mw("open to roles · EU + international", 14) - 14:.0f}" cy="53" r="5" fill="{OK}"/>',
         t(1144, 58, "open to roles · EU + international", size=14, fill=OK, anchor="end")]
    # primary
    px, py, pw, ph = 56, 86, 1088, 128
    b.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="14" fill="{OK}" fill-opacity=".06"/>')
    cs = 22
    cor = ""
    for (cx_, cy_, sx, sy) in ((px, py, 1, 1), (px + pw, py, -1, 1), (px, py + ph, 1, -1), (px + pw, py + ph, -1, -1)):
        cor += f'<path d="M{cx_} {cy_ + sy * cs}V{cy_}H{cx_ + sx * cs}" fill="none" stroke="{OK}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
    b.append(f'<g class="corner">{cor}</g>')
    b.append(t(px + 34, py + 44, "PRIMARY", size=13, fill=OK, ls=2.6, weight=700))
    b.append(t(px + 32, py + 98, primary, cls="s", size=50, weight=800, ls=-1.4))
    b.append(t(px + pw - 34, py + 60, "customer problem → working", size=14, fill=MUTE, anchor="end"))
    b.append(t(px + pw - 34, py + 82, "agent → verified outcome", size=14, fill=MUTE, anchor="end"))
    # others
    x, y, size, x_max = 56, 240, 16, 1144
    for i, r in enumerate(rest):
        w = mw(r, size) + 34
        if x + w > x_max:
            x, y = 56, y + 52
        b.append(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="40" rx="10" fill="{PANEL}" stroke="{LINE2}"/>')
        b.append(f'<rect class="lock" x="{x}" y="{y}" width="{w:.0f}" height="40" rx="10" fill="{OK}" fill-opacity=".12" stroke="{OK}" style="animation-delay:{i * 1.4:.1f}s"/>')
        b.append(t(x + 17, y + 26, r, size=size, fill=TEXT))
        x += w + 10
    y += 40 + 30
    b.append(f'<line x1="56" y1="{y}" x2="1144" y2="{y}" stroke="{LINE}"/>')
    y += 38
    b.append(t(56, y, "EDUCATION", size=13, fill=DIM, ls=2.6))
    x = 56 + mw("EDUCATION", 13) + 9 * 2.6 + 22
    for i, ed in enumerate(EDUCATION):
        if i:
            b.append(t(x, y + 1, "+", size=18, fill=OK, weight=700))
            x += 28
        b.append(t(x, y + 1, ed, cls="s", size=18, fill=TEXT, weight=600))
        x += len(ed) * 18 * 0.54 + 18
    H = y + 34
    return doc(W, H, "".join(b), f"Target roles. Primary: {primary}. Also: {', '.join(rest)}. Education: {' and '.join(EDUCATION)}.", css)


# ─────────────────────── HEADERS / FOOTER ───────────────────────
def header(num, title, sub):
    W, H = 1200, 72
    tw = len(title) * 28 * 0.56
    x_line = 104 + tw + 26
    b = [t(34, 46, num, size=20, fill=OK, weight=700),
         f'<line x1="74" y1="22" x2="74" y2="50" stroke="{LINE2}" stroke-width="1.5"/>',
         t(92, 47, title, cls="s", size=28, weight=800, ls=-.5),
         f'<line x1="{x_line:.0f}" y1="37" x2="{1166 - mw(sub, 14) - 22:.0f}" y2="37" stroke="{LINE2}" stroke-dasharray="2 8" class="flow"/>',
         t(1166, 42, sub, size=14, fill=MUTE, anchor="end")]
    return doc(W, H, "".join(b), f"{num} {title}: {sub}", rx=14)


def footer():
    W, H = 1200, 250
    css = ("@keyframes scanx{0%{transform:translateX(-200px)}100%{transform:translateX(1300px)}}.scanx{animation:scanx 6s linear infinite}")
    defs = (f'<linearGradient id="fx" x1="0" x2="1"><stop offset="0" stop-color="{OK}" stop-opacity="0"/><stop offset=".5" stop-color="{OK}" stop-opacity=".1"/>'
            f'<stop offset="1" stop-color="{OK}" stop-opacity="0"/></linearGradient>')
    b = [f'<rect class="scanx" x="0" y="0" width="200" height="{H}" fill="url(#fx)"/>',
         f'<circle class="pulse" cx="66" cy="57" r="5" fill="{OK}"/>',
         t(82, 62, "STATUS: AVAILABLE", size=14, fill=OK, ls=2.6),
         t(56, 128, "Building agents that have to be right?", cls="s", size=48, weight=800, ls=-1.4),
         t(58, 172, "Reliable AI products, autonomous agents, data platforms, decision systems.", cls="s", size=21, fill=MUTE),
         t(58, 216, "$ connect --with deepak", size=16, fill=OK),
         f'<rect x="{58 + mw("$ connect --with deepak ", 16):.0f}" y="201" width="9" height="19" fill="{OK}" style="animation:blink 1s steps(1) infinite"/>']
    return doc(W, H, "".join(b), "Status: available. Building agents that have to be right? Let's connect.", css, defs)


def button(label, sub):
    W, H = 380, 84
    b = [t(26, 37, label, cls="s", size=20, weight=700), t(26, 60, sub, size=13, fill=MUTE), arrow_ne(332, 30, OK, 1.6)]
    return doc(W, H, "".join(b), f"{label}: {sub}", rx=14)


# ───────────────────────────── BUILD ────────────────────────────
def main():
    OUT.mkdir(exist_ok=True)
    files = {
        "hero.svg": hero(), "principle.svg": principle(), "echo.svg": echo(), "training-loop.svg": training(),
        "toolkit.svg": toolkit(), "roles.svg": roles(), "footer.svg": footer(),
        "btn-email.svg": button("Email", "thedeepakreddy1@gmail.com"),
        "btn-linkedin.svg": button("LinkedIn", "in/deepak-reddy"),
        "btn-github.svg": button("GitHub", "all repositories"),
    }
    for slug, num, title, sub in SECTIONS:
        files[f"h-{slug}.svg"] = header(num, title, sub)
    for i, (slug, kind, title, desc, stack, live, ill) in enumerate(CARDS, 1):
        files[f"card-{slug}.svg"] = card(i, kind, title, desc, stack, live, ill)
    for name, svg in files.items():
        (OUT / name).write_text(svg, encoding="utf-8")
        print(f"{name:22s} {len(svg) / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
