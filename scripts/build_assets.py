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
    ("AGENTS", ["Claude Agent SDK", "Gemini", "Ollama", "MCP", "LangGraph", "tool calling", "structured outputs",
                "agent memory", "workflow learning", "multi-agent orchestration", "replay + recovery",
                "verification-driven execution"]),
    ("AI / ML", ["PyTorch", "Transformers", "Qwen 2.5-VL", "GRPO", "scikit-learn", "XGBoost", "SHAP",
                 "TensorFlow", "Keras", "Prophet", "SARIMAX", "embeddings", "RAG"]),
    ("BACKEND + DATA", ["FastAPI", "Node.js", "Express", "PostgreSQL", "Redis", "SQLite", "Pandas", "NumPy", "ETL",
                        "REST", "WebSockets"]),
    ("FRONTEND + APPS", ["React", "Vite", "Electron", "Tauri", "Chrome MV3", "Recharts", "Streamlit", "Tableau", "Power BI"]),
    ("SYSTEMS", ["WebRTC", "macOS automation", "accessibility APIs", "OCR", "Docker", "GitHub Actions",
                 "Render", "Vercel", "Google Cloud"]),
]
TOOLKIT_ACCENT = "AGENTS"

SECTIONS = [
    ("about", "01", "Principle", "how I think about AI systems"),
    ("echo", "02", "Flagship: Echo", "a local-first agent runtime for macOS"),
    ("systems", "03", "Major systems", "platforms, research and models"),
    ("work", "04", "More products", "built around real people"),
    ("analytics", "05", "Analytics + applied ML", "models that end in a decision"),
    ("toolkit", "06", "Toolkit", "what I build with"),
    ("roles", "07", "Target roles", "where I fit"),
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


# ───────────────────────── ECHO ECOSYSTEM ───────────────────────
def echo_family():
    W, H = 1200, 326
    css = cycle_css("tier", 4, 1.5, fade=0.1, shift=False)
    b = [t(56, 58, "ECHO ECOSYSTEM", size=14, fill=MUTE, ls=2.6),
         t(1144, 58, "one agent, three surfaces", size=14, fill=DIM, anchor="end")]
    bw, by, bh = 320, 86, 196
    xs = [56, 440, 824]

    def box(x, kind, title, l1, l2, live=False, accent=LINE2):
        s = f'<rect x="{x}" y="{by}" width="{bw}" height="{bh}" rx="14" fill="{PANEL}" stroke="{accent}"/>'
        s += t(x + 22, by + 34, kind, size=12.5, fill=MUTE, ls=2)
        if live:
            s += (f'<rect x="{x + bw - 90}" y="{by + 17}" width="70" height="26" rx="13" fill="{BG}" stroke="{OK}"/>'
                  f'<circle class="pulse" cx="{x + bw - 73}" cy="{by + 30}" r="4" fill="{OK}"/>{t(x + bw - 62, by + 35, "LIVE", size=12.5, fill=OK, ls=1.5, weight=700)}')
        s += t(x + 21, by + 72, title, cls="s", size=28, weight=800, ls=-.6)
        s += t(x + 22, by + 98, l1, size=13.5, fill=MUTE) + t(x + 22, by + 118, l2, size=13.5, fill=MUTE)
        return s

    # phone
    x = xs[0]
    b.append(box(x, "PHONE", "Echo Phone", "standalone assistant", "optional relay to Echo on your Mac", live=True))
    cx_ = x + 22
    for c_ in ["Today", "Bots", "Briefing", "Brain"]:
        c, w, h = chip(cx_, by + 144, c_, size=12.5, color=TEXT, fill=BG, pad=10)
        b.append(c)
        cx_ += w + 7
    # mac
    x = xs[1]
    b.append(box(x, "MAC · FLAGSHIP", "Echo Mac", "local-first agent runtime", "sees, acts, verifies on the desktop", accent=OK))
    cx_ = x + 22
    for i, c_ in enumerate(["perceive", "act", "verify"]):
        c, w, h = chip(cx_, by + 144, c_, size=12.5, color=OK if c_ == "verify" else TEXT, stroke=OK if c_ == "verify" else LINE2, fill=BG, pad=10)
        b.append(c)
        cx_ += w
        if i < 2:
            b.append(f'<line x1="{cx_:.0f}" y1="{by + 157.5}" x2="{cx_ + 16:.0f}" y2="{by + 157.5}" stroke="{OK}" stroke-width="1.8" class="flow"/>')
        cx_ += 16
    # browser
    x = xs[2]
    b.append(box(x, "CHROME MV3", "Echo Online", "tab agents with approval gates", "MCP bridge to Claude Desktop/Code"))
    cx_ = x + 22
    for i, c_ in enumerate(["instant", "cached", "device", "cloud"]):
        w = mw(c_, 12.5) + 18
        b.append(f'<rect x="{cx_:.0f}" y="{by + 144}" width="{w:.0f}" height="27.5" rx="13.75" fill="{BG}" stroke="{LINE2}"/>')
        b.append(f'<rect class="tier{" rm" if i == 0 else ""}" x="{cx_:.0f}" y="{by + 144}" width="{w:.0f}" height="27.5" rx="13.75" fill="#12261E" stroke="{OK}" style="animation-delay:{i * 1.5:.1f}s"/>')
        b.append(t(cx_ + 9, by + 162.4, c_, size=12.5, fill=TEXT))
        cx_ += w + 6
    # connectors
    y = by + bh / 2
    for xa, xb, lab in ((xs[0] + bw, xs[1], "relay"),):
        b.append(f'<line x1="{xa}" y1="{y}" x2="{xb}" y2="{y}" stroke="{OK}" stroke-width="1.8" class="flow"/>')
        w = mw(lab, 12) + 14
        m = (xa + xb) / 2
        b.append(f'<rect x="{m - w / 2:.1f}" y="{y - 11}" width="{w:.1f}" height="22" rx="11" fill="{BG}" stroke="{LINE2}"/>{t(m, y + 4.3, lab, size=12, fill=TEXT, anchor="middle")}')
    b.append(t(xs[0], 309, "Your Mac never opens a port: Echo holds outgoing requests to the relay.", size=13, fill=DIM))
    b.append(t(1144, 309, "four-tier routing tries local before cloud", size=13, fill=DIM, anchor="end"))
    return doc(W, H, "".join(b),
               "Echo ecosystem: Echo Phone, a standalone phone assistant with an optional relay to Echo on your Mac; Echo Mac, the "
               "local-first agent runtime; and Echo Online, a Chrome extension with tab-scoped agents, four-tier local-first routing "
               "and an MCP bridge to Claude Desktop and Claude Code.", css)


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


# ─────────────────────── MAJOR SYSTEM VISUALS ───────────────────
def chrome(W, name, tagline, status, col=OK):
    b = [f'<rect width="{W}" height="56" fill="{PANEL}"/><line x1="0" y1="56" x2="{W}" y2="56" stroke="{LINE}"/>']
    for i, c in enumerate([BAD, WARN, OK]):
        b.append(f'<circle cx="{34 + i * 22}" cy="28" r="6.5" fill="{c}" opacity=".85"/>')
    b.append(t(112, 33, name, size=16, fill=TEXT, weight=700))
    b.append(t(112 + mw(name + " ", 16), 33, "— " + tagline, size=15, fill=MUTE))
    b.append(f'<circle class="pulse" cx="{W - 36 - mw(status, 14) - 14:.0f}" cy="28" r="5" fill="{col}"/>')
    b.append(t(W - 36, 33, status, size=14, fill=col, anchor="end"))
    return b


def strip(y, W, label, items, size=12.5):
    """Bottom strip: a label and wrapped chips. Returns (svg, height)."""
    x0 = 46 + mw(label, 12.5) + len(label) * 2 + 26
    x, row, out = x0, 0, []
    for it in items:
        w = mw(it, size) + 20
        if x + w > W - 46:
            x, row = x0, row + 1
        c, w, h = chip(x, y + 14 + row * 36, it, size=size, color=TEXT, fill=BG, pad=10)
        out.append(c)
        x += w + 8
    h = 14 + (row + 1) * 36 + 8
    s = f'<rect x="28" y="{y}" width="{W - 56}" height="{h}" rx="12" fill="{PANEL}" stroke="{LINE}"/>'
    s += t(46, y + 33, label, size=12.5, fill=DIM, ls=2)
    return s + "".join(out), h


def rows_cycle(b, name, x, y0, w, step, rows, slot=1.5, sub_size=12, rm=0):
    """Numbered rows with a highlight that cycles through them. rows = [(title, sub)]."""
    css = cycle_css(name, len(rows), slot, fade=0.08, shift=False)
    for i, (n_, s_) in enumerate(rows):
        y = y0 + i * step
        b.append(f'<g class="{name}{" rm" if i == rm else ""}" style="animation-delay:{i * slot:.1f}s">'
                 f'<rect x="{x + 10}" y="{y - 6}" width="{w - 20}" height="{step - 8}" rx="9" fill="{OK}" fill-opacity=".1" stroke="{OK}" stroke-opacity=".55"/>'
                 f'<rect x="{x + 10}" y="{y + 4}" width="3" height="{step - 28}" rx="1.5" fill="{OK}"/></g>')
        b.append(t(x + 26, y + 17, f"{i + 1:02d}", size=12.5, fill=DIM))
        b.append(t(x + 56, y + 17, n_, cls="s", size=15.5, fill=TEXT, weight=700))
        b.append(t(x + 56, y + 35, s_, size=sub_size, fill=MUTE))
    return css


def lock(x, y, col=OK, s=1.0):
    return (f'<path d="M{x - 7 * s} {y}v{-5 * s}a{7 * s} {7 * s} 0 0 1 {14 * s} 0v{5 * s}" fill="none" stroke="{col}" stroke-width="2"/>'
            f'<rect x="{x - 11 * s}" y="{y}" width="{22 * s}" height="{16 * s}" rx="3.5" fill="{col}"/>')


def big_syntra():
    W = 1200
    b = chrome(W, "syntra", "synchronized intelligence for autonomous software engineering", "mission running")
    # A: layers
    ax, ay, aw, ah = 28, 80, 300, 440
    b.append(panel(ax, ay, aw, ah, "7 LAYERS"))
    layers = [("Control plane", "FastAPI · PostgreSQL 16 · RBAC"), ("Workflow", "LangGraph 13-stage state graph"),
              ("Scheduling", "SKIP LOCKED · leases · Redis 8"), ("MCP + tools", "capability policies · scrubbing"),
              ("Execution", "Docker · read-only · no network"), ("Memory", "SHA-256 content-addressed"),
              ("Verification", "QA · security · peer review")]
    css = rows_cycle(b, "ly", ax, ay + 50, aw, 55, layers, slot=1.6, rm=4)
    # B: mission
    bx, by, bw, bh = 344, 80, 520, 440
    b.append(panel(bx, by, bw, bh, "MISSION"))
    b.append(t(bx + bw - 18, by + 28, "objective + budget in, verified release out", size=12.5, fill=DIM, anchor="end"))
    lanes = [("PLAN · non-coding", [("Product Manager", "PRD"), ("Architect", "ADR"), ("Eng Manager", "task DAG")], True),
             ("BUILD · sandboxed", [("Backend", "unified diff"), ("Frontend", "target repo"), ("DevOps", "infra")], False),
             ("VERIFY · independent", [("QA Engineer", "test evidence"), ("Security", "audit report"), ("Code Review", "attestation")], True)]
    css += cycle_css("rl", 9, 1.0, fade=0.1, shift=False)
    k = 0
    for li, (lab, roles_, chain) in enumerate(lanes):
        ly = by + 42 + li * 98
        b.append(f'<rect x="{bx + 14}" y="{ly}" width="{bw - 28}" height="88" rx="10" fill="{BG}" stroke="{LINE}"/>')
        b.append(t(bx + 26, ly + 21, lab, size=11.5, fill=DIM, ls=1.5))
        if li == 2:
            b.append(t(bx + bw - 26, ly + 21, "debugger: minimal fix, re-verify", size=11.5, fill=WARN, anchor="end"))
        for ri, (nm, art) in enumerate(roles_):
            x = bx + 24 + ri * 162
            b.append(f'<rect x="{x}" y="{ly + 32}" width="148" height="44" rx="8" fill="{PANEL}" stroke="{LINE2}"/>')
            b.append(f'<rect class="rl{" rm" if k == 6 else ""}" x="{x}" y="{ly + 32}" width="148" height="44" rx="8" fill="#12261E" stroke="{OK}" style="animation-delay:{k * 1.0:.1f}s"/>')
            b.append(t(x + 12, ly + 51, nm, cls="s", size=14, fill=TEXT, weight=700))
            b.append(t(x + 12, ly + 67, art, size=11.5, fill=MUTE))
            if ri < 2 and chain:
                b.append(f'<line x1="{x + 148}" y1="{ly + 54}" x2="{x + 162}" y2="{ly + 54}" stroke="{OK}" stroke-width="1.8" class="flow"/>')
            if li < 2:
                b.append(f'<line x1="{x + 74}" y1="{ly + 88}" x2="{x + 74}" y2="{ly + 98}" stroke="{OK}" stroke-width="1.8" class="flow"/>')
            k += 1
    gy = by + 42 + 3 * 98
    b.append(f'<line x1="{bx + bw / 2}" y1="{gy - 10}" x2="{bx + bw / 2}" y2="{gy}" stroke="{WARN}" stroke-width="1.8" class="flow"/>')
    b.append(f'<rect x="{bx + 14}" y="{gy}" width="{bw - 28}" height="{by + bh - gy - 14}" rx="10" fill="{PANEL2}" stroke="{WARN}"/>')
    b.append(lock(bx + 46, gy + 30, WARN))
    b.append(t(bx + 74, gy + 32, "Human delivery gate", cls="s", size=16, fill=TEXT, weight=700))
    b.append(t(bx + 74, gy + 52, "approval digest → git push / pull request", size=12.5, fill=MUTE))
    b.append(t(bx + bw - 30, gy + 32, "no agent can release", size=12.5, fill=WARN, anchor="end"))
    # C: ledger
    cx, cy, cw, ch = 880, 80, 292, 440
    b.append(panel(cx, cy, cw, ch, "ARTIFACT LEDGER"))
    arts = [("PRD.md", "a3f9", "Product Manager", None), ("ADR-001.md", "7c1e", "Architect", None),
            ("task-plan.json", "e02b", "Eng Manager", None), ("patch.diff", "5d88", "Backend", None),
            ("verification-run", "b41a", "QA", ("passed", OK)), ("audit-report", "9f60", "Security", ("clean", OK)),
            ("review-attestation", "2c7d", "Reviewer", ("approved", OK))]
    cyc = 13.0
    for i, (nm, hs, who, st) in enumerate(arts):
        a = (0.3 + i * 1.0) / cyc * 100
        css += (f"@keyframes a{i}{{0%,{a:.2f}%{{opacity:0;transform:translateX(-8px)}}{a + 2.5:.2f}%,93%{{opacity:1;transform:translateX(0)}}"
                f"98%,100%{{opacity:0;transform:translateX(0)}}}}.a{i}{{animation:a{i} {cyc}s linear infinite}}")
        y = cy + 62 + i * 54
        g = t(cx + 18, y, nm, size=13.5, fill=TEXT, weight=700) + t(cx + 18, y + 20, f"sha256:{hs}…  ·  {who}", size=12, fill=DIM)
        if st:
            c, w, h = chip(cx + cw - 18 - (mw(st[0], 11.5) + 16), y - 18, st[0], size=11.5, color=st[1], stroke=st[1], fill=BG, pad=8)
            g += c
        if i < len(arts) - 1:
            g += f'<line x1="{cx + 18}" y1="{y + 33}" x2="{cx + cw - 18}" y2="{y + 33}" stroke="{LINE}"/>'
        b.append(f'<g class="a{i} rm">{g}</g>')
    s, h = strip(536, W, "INVARIANTS", ["roles, not chatbots", "state lives in PostgreSQL", "immutable hashed handoffs",
                                       "no agent verifies its own work", "humans hold the release gate", "headless: API + CLI"])
    b.append(s)
    return doc(W, 536 + h + 28, "".join(b),
               "SYNTRA: an autonomous multi-agent software engineering platform. Seven layers from control plane to verification. "
               "Planning roles produce a PRD, ADR and task DAG; sandboxed engineers produce diffs; QA, security and code review verify "
               "independently; every handoff is a SHA-256 hashed artifact; a human delivery gate controls release.", css)


def big_pluto():
    W = 1200
    b = chrome(W, "pluto", "a language model built from scratch, on the way to Mini-Live", "M3 in progress", WARN)
    css = ""
    # A: pipeline
    ax, ay, aw, ah = 28, 80, 364, 430
    b.append(panel(ax, ay, aw, ah, "PIPELINE"))
    b.append(t(ax + aw - 18, ay + 28, "hand-built on plain PyTorch", size=12.5, fill=DIM, anchor="end"))
    steps = [("raw text", "TinyStories · 2.1M stories"), ("clean + dedupe", "15.1% exact duplicates removed"),
             ("byte-level BPE", "own tokenizer · vocab 4096"), ("token shards", "197M tokens + manifest"),
             ("GPT", "own Transformer · ~6M parameters"), ("training loop", "mixed precision · exact resume")]
    css += cycle_css("pp", 6, 1.2, fade=0.1, shift=False)
    for i, (nm, det) in enumerate(steps):
        y = ay + 44 + i * 63
        b.append(f'<rect x="{ax + 18}" y="{y}" width="{aw - 36}" height="50" rx="9" fill="{BG}" stroke="{LINE2}"/>')
        b.append(f'<rect class="pp{" rm" if i == 2 else ""}" x="{ax + 18}" y="{y}" width="{aw - 36}" height="50" rx="9" fill="#12261E" stroke="{OK}" style="animation-delay:{i * 1.2:.1f}s"/>')
        b.append(t(ax + 34, y + 21, nm, cls="s", size=15, fill=TEXT, weight=700))
        b.append(t(ax + 34, y + 39, det, size=12, fill=MUTE))
        b.append(t(ax + aw - 34, y + 30, f"{i + 1:02d}", size=12.5, fill=DIM, anchor="end"))
        if i < len(steps) - 1:
            b.append(f'<line x1="{ax + aw / 2}" y1="{y + 50}" x2="{ax + aw / 2}" y2="{y + 63}" stroke="{OK}" stroke-width="1.8" class="flow"/>')
    # B: run
    bx, by, bw, bh = 408, 80, 416, 430
    b.append(panel(bx, by, bw, bh, "RUN · MILESTONE 1"))
    b.append(t(bx + bw - 18, by + 28, "free Kaggle T4", size=12.5, fill=DIM, anchor="end"))
    gx0, gx1, gy0, gy1 = bx + 30, bx + bw - 24, by + 54, by + 252
    for i in range(4):
        yy = gy0 + i * (gy1 - gy0) / 4
        b.append(f'<line x1="{gx0}" y1="{yy:.0f}" x2="{gx1}" y2="{yy:.0f}" stroke="{LINE}" stroke-dasharray="2 6"/>')
    b.append(f'<path d="M{gx0} {gy0}V{gy1}H{gx1}" fill="none" stroke="{LINE2}" stroke-width="1.5"/>')
    pts = []
    for i in range(61):
        u = i / 60
        x = gx0 + 8 + u * (gx1 - gx0 - 16)
        y = gy1 - 26 - 150 * math.exp(-4.4 * u) + 3 * math.sin(i * 1.9) * (1 - u)
        pts.append(f"{x:.1f} {y:.1f}")
    css += ("@keyframes drawL{0%{stroke-dashoffset:520}50%,90%{stroke-dashoffset:0}100%{stroke-dashoffset:520}}"
            ".drawL{stroke-dasharray:520;animation:drawL 8s ease-in-out infinite}")
    b.append(f'<path class="drawL" d="M{" L".join(pts)}" fill="none" stroke="{OK}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')
    rx_ = gx0 + 8 + (gx1 - gx0 - 16) / 6
    b.append(f'<line x1="{rx_:.0f}" y1="{gy0 + 4}" x2="{rx_:.0f}" y2="{gy1}" stroke="{WARN}" stroke-dasharray="3 4"/>')
    b.append(t(rx_ + 8, gy0 + 18, "step 500: interrupt, then exact resume", size=12, fill=WARN))
    b.append(t(gx1, gy1 + 18, "step 3,000", size=11.5, fill=DIM, anchor="end"))
    b.append(t(gx0, gy1 + 18, "validation loss", size=11.5, fill=DIM))
    tiles = [("197M", "tokens trained"), ("18 min", "from random weights"), ("1.738", "validation loss"), ("0.640", "bits per byte")]
    for i, (num, lab) in enumerate(tiles):
        x = bx + 18 + (i % 2) * 194
        y = by + 292 + (i // 2) * 66
        b.append(f'<rect x="{x}" y="{y}" width="186" height="58" rx="9" fill="{BG}" stroke="{LINE}"/>')
        b.append(t(x + 14, y + 27, num, cls="s", size=21, fill=TEXT, weight=800))
        b.append(t(x + 14, y + 46, lab, size=12, fill=MUTE))
    # C: roadmap
    cx, cy, cw, ch = 840, 80, 332, 430
    b.append(panel(cx, cy, cw, ch, "ROADMAP"))
    ms = [("M1", "Text pipeline, end to end", "report published", 2), ("M2", "First voice · ~30M", "18.8% WER on held-out passages", 2),
          ("M3", "Text brain · ~400M", "16k context · data prep on Modal", 1), ("M4", "Brain + voice", "multi-voice · fixed word timing", 0),
          ("M5", "Mini-Live", "full-duplex: thinks while listening", 0), ("M6", "Tools + memory", "search · code · research agent", 0)]
    lx = cx + 30
    b.append(f'<line x1="{lx}" y1="{cy + 62}" x2="{lx}" y2="{cy + 62 + 5 * 62}" stroke="{LINE2}" stroke-width="1.5"/>')
    for i, (m_, ttl, sub, st) in enumerate(ms):
        y = cy + 62 + i * 62
        if st == 2:
            b.append(f'<circle cx="{lx}" cy="{y}" r="10" fill="#14402E" stroke="{OK}" stroke-width="1.5"/>{check(lx, y, s=.85, sw=2)}')
        elif st == 1:
            b.append(f'<circle cx="{lx}" cy="{y}" r="10" fill="{BG}" stroke="{WARN}" stroke-width="1.5"/><circle class="pulse" cx="{lx}" cy="{y}" r="4.5" fill="{WARN}"/>')
        else:
            b.append(f'<circle cx="{lx}" cy="{y}" r="10" fill="{BG}" stroke="{LINE2}" stroke-width="1.5"/>')
        col = [DIM, WARN, OK][st]
        b.append(t(lx + 22, y - 2, m_, size=13, fill=col, weight=700))
        b.append(t(lx + 50, y - 2, ttl, cls="s", size=15, fill=TEXT if st else MUTE, weight=700))
        b.append(t(lx + 22, y + 17, sub, size=12, fill=MUTE if st else DIM))
    # strip: Mini-Live
    sy = 526
    b.append(f'<rect x="28" y="{sy}" width="{W - 56}" height="76" rx="12" fill="{PANEL}" stroke="{LINE}"/>')
    b.append(t(46, sy + 44, "MINI-LIVE", size=12.5, fill=DIM, ls=2))
    css += ("@keyframes bar{0%,100%{transform:scaleY(.25)}50%{transform:scaleY(1)}}"
            ".bar{transform-box:fill-box;transform-origin:center;animation:bar 1s ease-in-out infinite}")
    rnd = random.Random(5)

    def wave(x0, col, n=22):
        out = ""
        for i in range(n):
            hh = rnd.choice([10, 16, 24, 32, 20, 14])
            out += (f'<rect class="bar" x="{x0 + i * 6.2:.1f}" y="{sy + 38 - hh / 2}" width="3.2" height="{hh}" rx="1.6" fill="{col}" '
                    f'style="animation-duration:{rnd.uniform(.7, 1.5):.2f}s;animation-delay:-{rnd.uniform(0, 1.2):.2f}s"/>')
        return out

    x = 180
    b.append(t(x, sy + 22, "you speak", size=11.5, fill=DIM))
    b.append(wave(x, INFO))
    x += 150
    for lab, sub in (("brain", "8 layers · d 384"), ("voice box", "3 layers · 8 Mimi codebooks")):
        b.append(f'<line x1="{x}" y1="{sy + 38}" x2="{x + 26}" y2="{sy + 38}" stroke="{OK}" stroke-width="1.8" class="flow"/>')
        x += 34
        w = max(mw(sub, 12), 90) + 28
        b.append(f'<rect x="{x}" y="{sy + 14}" width="{w:.0f}" height="48" rx="9" fill="{BG}" stroke="{LINE2}"/>')
        b.append(t(x + 14, sy + 34, lab, cls="s", size=14.5, fill=TEXT, weight=700))
        b.append(t(x + 14, sy + 51, sub, size=12, fill=MUTE))
        x += w + 8
    b.append(f'<line x1="{x}" y1="{sy + 38}" x2="{x + 26}" y2="{sy + 38}" stroke="{OK}" stroke-width="1.8" class="flow"/>')
    x += 34
    b.append(t(x, sy + 22, "it answers", size=11.5, fill=DIM))
    b.append(wave(x, OK))
    b.append(t(W - 46, sy + 43, "real-time speech + text", size=12.5, fill=MUTE, anchor="end"))
    return doc(W, sy + 76 + 28, "".join(b),
               "Pluto: a language model built from scratch in plain PyTorch. Pipeline: raw text, clean and dedupe, byte-level BPE "
               "tokenizer, token shards, GPT, training loop with exact resume. Milestone 1: about 6M parameters trained on 197M "
               "tokens in 18 minutes on a free T4, validation loss 1.738. Milestone 2: first voice model, 18.8% WER. Roadmap to "
               "Mini-Live, a real-time speech and text model.", css)


def big_atlas():
    W = 1200
    b = chrome(W, "atlas", "understanding the physical world", "research · proposed architecture", INFO)
    # A: scene
    ax, ay, aw, ah = 28, 80, 672, 470
    b.append(panel(ax, ay, aw, ah, "SCENE · 3D + TIME"))
    b.append(t(ax + aw - 18, ay + 28, "solid = measured · dashed = inferred", size=12.5, fill=DIM, anchor="end"))
    ox, oy, s = 364, 182, 29

    def iso(x, y, z=0):
        return ox + (x - y) * 0.866 * s, oy + (x + y) * 0.5 * s - z * s

    def P(*p):
        x, y = iso(*p)
        return f"{x:.1f} {y:.1f}"

    for i in range(9):
        b.append(f'<path d="M{P(i, 0)}L{P(i, 8)}M{P(0, i)}L{P(8, i)}" stroke="{LINE2}" stroke-width="1" fill="none"/>')

    def cuboid(x, y, w, d, h, col, dash="", fo=.1):
        top = f"M{P(x, y, h)}L{P(x + w, y, h)}L{P(x + w, y + d, h)}L{P(x, y + d, h)}Z"
        left = f"M{P(x, y + d, 0)}L{P(x + w, y + d, 0)}L{P(x + w, y + d, h)}L{P(x, y + d, h)}Z"
        right = f"M{P(x + w, y, 0)}L{P(x + w, y + d, 0)}L{P(x + w, y + d, h)}L{P(x + w, y, h)}Z"
        da = f' stroke-dasharray="{dash}"' if dash else ""
        return "".join(f'<path d="{p}" fill="{col}" fill-opacity="{f_}" stroke="{col}" stroke-width="1.5" stroke-linejoin="round"{da}/>'
                       for p, f_ in ((left, fo * .7), (right, fo * .4), (top, fo)))

    def tag(px, py, s_, col):
        w = mw(s_, 11.5) + 14
        return (f'<rect x="{px:.0f}" y="{py:.0f}" width="{w:.0f}" height="21" rx="5" fill="{BG}" stroke="{col}"/>'
                f'{t(px + 7, py + 15, s_, size=11.5, fill=col)}')

    # sensor frustum
    sx_, sy_ = iso(-0.6, 8.6, 2.2)
    f1, f2 = iso(2, 3), iso(6.5, 7)
    b.append(f'<path class="pulse" d="M{sx_:.0f} {sy_:.0f}L{f1[0]:.0f} {f1[1]:.0f}L{f2[0]:.0f} {f2[1]:.0f}Z" fill="{INFO}" fill-opacity=".06" stroke="{INFO}" stroke-opacity=".5" stroke-dasharray="3 5"/>')
    b.append(f'<circle cx="{sx_:.0f}" cy="{sy_:.0f}" r="6" fill="{INFO}"/>')
    b.append(t(sx_ + 12, sy_ - 8, "sensor", size=11.5, fill=INFO))
    b.append(cuboid(.5, .5, 1.2, 2.6, 2.1, INFO, fo=.14))
    b.append(tag(iso(.5, .5, 2.1)[0] - 150, iso(.5, .5, 2.1)[1] - 26, "obj_02 shelf · measured", INFO))
    b.append(cuboid(4.6, 1.0, 2.0, 1.4, .9, MUTE, fo=.1))
    b.append(cuboid(6.4, 5.6, 1.1, 1.1, 1.5, WARN, dash="4 4", fo=.05))
    b.append(tag(iso(7.5, 5.6, 1.5)[0] - 20, iso(7.5, 5.6, 1.5)[1] - 30, "obj_05 · inferred", WARN))
    css = cycle_css("mv", 4, 1.8, fade=0.12, shift=False)
    trail = [(1.4, 5.8), (2.9, 5.5), (4.2, 4.6), (5.2, 3.4)]
    pth = "M" + "L".join(P(x + .45, y + .45) for x, y in trail)
    b.append(f'<path d="{pth}" fill="none" stroke="{OK}" stroke-width="1.5" stroke-dasharray="2 6" opacity=".7"/>')
    for i, (x, y) in enumerate(trail):
        b.append(cuboid(x, y, .9, .9, .8, DIM, dash="3 3", fo=0))
        lx_, ly_ = iso(x + .45, y + .45, 1.5)
        b.append(f'<g class="mv{" rm" if i == 3 else ""}" style="animation-delay:{i * 1.8:.1f}s">{cuboid(x, y, .9, .9, .8, OK, fo=.24)}'
                 f'{tag(lx_ - 52, ly_ - 12, f"obj_07 cup · t{i}", OK)}</g>')
    # timeline
    ty = ay + ah - 36
    b.append(t(ax + 22, ty + 5, "TIME", size=11.5, fill=DIM, ls=2))
    tx0, dt = ax + 110, 110
    b.append(f'<line x1="{tx0}" y1="{ty}" x2="{tx0 + 3 * dt + 18}" y2="{ty}" stroke="{LINE2}" stroke-width="1.5"/>')
    for i in range(4):
        b.append(f'<line x1="{tx0 + i * dt}" y1="{ty - 6}" x2="{tx0 + i * dt}" y2="{ty + 6}" stroke="{LINE2}" stroke-width="1.5"/>')
        b.append(t(tx0 + i * dt, ty + 22, f"t{i}", size=11.5, fill=DIM, anchor="middle"))
        b.append(f'<circle class="mv{" rm" if i == 3 else ""}" cx="{tx0 + i * dt}" cy="{ty}" r="7" fill="{OK}" style="animation-delay:{i * 1.8:.1f}s"/>')
    b.append(t(ax + aw - 22, ty + 5, "object identity persists", size=12, fill=MUTE, anchor="end"))
    # B: architecture
    bx, by, bw, bh = 716, 80, 456, 296
    b.append(panel(bx, by, bw, bh, "ARCHITECTURE"))
    layers = [("Sensors", "camera · depth · LiDAR · IMU"), ("Reconstruction", "geometry · mapping · localization"),
              ("Scene understanding", "objects · semantics · relations"), ("Temporal world model", "dynamic state · identity"),
              ("Spatial memory", "evidence · history · retrieval"), ("Reasoning", "spatial · physical · causal"),
              ("Interaction", "navigation · planning · robotics")]
    css += cycle_css("al", 7, 1.3, fade=0.1, shift=False)
    for i, (nm, sub) in enumerate(layers):
        y = by + 44 + i * 35
        b.append(f'<rect class="al{" rm" if i == 4 else ""}" x="{bx + 10}" y="{y}" width="{bw - 20}" height="30" rx="7" fill="{OK}" fill-opacity=".1" stroke="{OK}" stroke-opacity=".55" style="animation-delay:{i * 1.3:.1f}s"/>')
        b.append(t(bx + 22, y + 20, f"{i + 1:02d}", size=12, fill=DIM))
        b.append(t(bx + 50, y + 20, nm, cls="s", size=14, fill=TEXT, weight=700))
        b.append(t(bx + bw - 22, y + 20, sub, size=11.5, fill=MUTE, anchor="end"))
    # C: memory
    cx, cy, cw, ch = 716, 392, 456, 158
    b.append(panel(cx, cy, cw, ch, "WORLD MEMORY"))
    b.append(t(cx + cw - 18, cy + 28, "every fact carries its evidence", size=12.5, fill=DIM, anchor="end"))
    rows = [("cup", "moved t0 → t3", "measured", OK), ("door", "open", "estimated", INFO),
            ("lamp", "behind the shelf", "inferred", WARN), ("drawer", "contents", "unknown", DIM)]
    for i, (n_, st, ev, c) in enumerate(rows):
        y = cy + 42 + i * 27
        b.append(f'<rect x="{cx + 14}" y="{y}" width="{cw - 28}" height="22" rx="5" fill="{BG}" stroke="{LINE}"/>')
        b.append(f'<circle cx="{cx + 28}" cy="{y + 11}" r="3.5" fill="{c}"/>')
        b.append(t(cx + 40, y + 15.5, n_, size=12.5, fill=TEXT, weight=700))
        b.append(t(cx + 110, y + 15.5, st, size=12.5, fill=MUTE))
        b.append(t(cx + cw - 24, y + 15.5, ev, size=12, fill=c, anchor="end"))
    s_, h = strip(566, W, "PRINCIPLES", ["evidence before assumptions", "explicit uncertainty", "reversible updates",
                                        "measured geometry ≠ semantic inference", "local-first", "privacy-aware memory"])
    b.append(s_)
    return doc(W, 566 + h + 28, "".join(b),
               "ATLAS: an independent research initiative on persistent, evidence-grounded spatial intelligence. A 3D scene tracked "
               "over time with persistent object identity, measured versus inferred geometry, a seven-layer proposed architecture "
               "from sensors to interaction, and a world memory where every fact carries its evidence type.", css)


def big_cosmos():
    W, H = 1200, 500
    b = chrome(W, "cosmos", "modular intelligence infrastructure", "site live")
    hx, hy, hw, hh = 470, 214, 260, 124
    prods = ["Aira", "Echo", "enterprise apps", "research tools"]
    widths = [mw(p, 13) + 24 for p in prods]
    x = 600 - (sum(widths) + 10 * 3) / 2
    b.append(t(600, 96, "PRODUCTS THAT SHOULD NOT REBUILD THE SAME THING", size=12, fill=DIM, anchor="middle", ls=2))
    for p, w in zip(prods, widths):
        b.append(f'<rect x="{x:.0f}" y="112" width="{w:.0f}" height="30" rx="15" fill="{PANEL}" stroke="{LINE2}"/>')
        b.append(t(x + 12, 132, p, size=13, fill=TEXT))
        b.append(f'<path d="M{x + w / 2:.0f} 142C{x + w / 2:.0f} 180 600 176 600 {hy}" fill="none" stroke="{OK}" stroke-width="1.5" class="flow" opacity=".7"/>')
        x += w + 10
    systems = [("ToolOS", "CAN DO", "the safe doorway to capabilities", "v1.0.0", True),
               ("AgentOS", "ORGANIZE WORK", "TypeScript · Fastify · SQLite", "v0.2.0", True),
               ("ResearchOS", "INVESTIGATE", "the most mature system in Cosmos", "mature", True),
               ("EvalOS", "JUDGE QUALITY", "TypeScript · Fastify · SQLite", "built", True),
               ("MemoryOS", "PLANNED", "extracted from ResearchOS, behind its port", "planned", False),
               ("ModelOS", "PLANNED", "router with retry, fallback, circuit breaking", "planned", False)]
    cw, chh = 392, 84
    for i, (nm, kind, desc, st, built) in enumerate(systems):
        left = i < 3
        cx = 40 if left else W - 40 - cw
        cy = 164 + (i % 3) * 100
        col = OK if built else DIM
        da = "" if built else ' stroke-dasharray="5 5"'
        b.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{chh}" rx="12" fill="{PANEL}" stroke="{LINE2 if built else DIM}"{da}/>')
        b.append(t(cx + 20, cy + 26, kind, size=12, fill=col, ls=2, weight=700))
        b.append(t(cx + 19, cy + 52, nm, cls="s", size=23, fill=TEXT if built else MUTE, weight=800, ls=-.4))
        b.append(t(cx + 20, cy + 71, desc, size=12, fill=MUTE if built else DIM))
        c, w, h = chip(cx + cw - 18 - (mw(st, 11.5) + 16), cy + 14, st, size=11.5, color=col, stroke=col, fill=BG, pad=8)
        b.append(c)
        x1 = cx + cw if left else cx
        x2 = hx if left else hx + hw
        y1, y2 = cy + chh / 2, hy + hh / 2 + ((i % 3) - 1) * 26
        m = (x1 + x2) / 2
        if built:
            b.append(f'<path d="M{x1} {y1}C{m} {y1} {m} {y2} {x2} {y2}" fill="none" stroke="{OK}" stroke-width="1.6" class="flow"/>')
        else:
            b.append(f'<path d="M{x1} {y1}C{m} {y1} {m} {y2} {x2} {y2}" fill="none" stroke="{DIM}" stroke-width="1.4" stroke-dasharray="3 6"/>')
    b.append(f'<rect class="pulse" x="{hx - 8}" y="{hy - 8}" width="{hw + 16}" height="{hh + 16}" rx="20" fill="none" stroke="{OK}" stroke-opacity=".3"/>')
    b.append(f'<rect x="{hx}" y="{hy}" width="{hw}" height="{hh}" rx="14" fill="{PANEL2}" stroke="{OK}" stroke-width="1.5"/>')
    b.append(t(600, hy + 38, "COSMOS CORE", size=13, fill=OK, anchor="middle", ls=2.6, weight=700))
    b.append(t(600, hy + 70, "one coordination layer", cls="s", size=20, fill=TEXT, anchor="middle", weight=800))
    b.append(t(600, hy + 96, "clear boundaries, thin centre", size=12.5, fill=MUTE, anchor="middle"))
    b.append(t(600, H - 22, "the test: would two unrelated products both need this?", size=13.5, fill=MUTE, anchor="middle"))
    return doc(W, H, "".join(b),
               "CosmOS: a modular intelligence infrastructure platform. Products such as Aira and Echo connect to one coordination "
               "layer, Cosmos Core, which coordinates ToolOS (can do), AgentOS (organize work), ResearchOS (investigate) and EvalOS "
               "(judge quality). MemoryOS and ModelOS are planned as extractions from ResearchOS.")


def big_aira():
    W = 1200
    b = chrome(W, "aira", "one AI workspace across web, macOS and Windows", "v0.1.0 · macOS")
    ax, ay, aw, ah = 28, 80, 290, 400
    b.append(panel(ax, ay, aw, ah, "SURFACES"))
    surf = [("Chat", "streams; names the model used"), ("Code", "changes wait for approval"), ("Agents", "lead · research · review fleet"),
            ("Browser", "a real Chrome session"), ("Workspace", "routing · memory · MCP")]
    css = rows_cycle(b, "sf", ax, ay + 52, aw, 68, surf, slot=1.8, rm=1)
    # B: app
    bx, by, bw, bh = 334, 80, 452, 400
    b.append(panel(bx, by, bw, bh, "AGENTS"))
    b.append(t(bx + bw - 18, by + 28, "each with its own role and model", size=12.5, fill=DIM, anchor="end"))
    css += "@keyframes prog{0%{transform:scaleX(.04)}80%,100%{transform:scaleX(1)}}.prog{transform-box:fill-box;transform-origin:left;animation:prog 6s ease-in-out infinite}"
    for i, (nm, frac, st, c) in enumerate([("Lead", 1.0, "coordinating", OK), ("Research", .82, "running", INFO), ("Analyse", .55, "running", INFO), ("Review", .2, "queued", DIM)]):
        y = by + 48 + i * 34
        b.append(t(bx + 20, y + 15, nm, size=13.5, fill=TEXT, weight=700))
        b.append(f'<rect x="{bx + 106}" y="{y + 5}" width="220" height="10" rx="5" fill="{BG}" stroke="{LINE}"/>')
        b.append(f'<rect class="prog" x="{bx + 106}" y="{y + 5}" width="{220 * frac:.0f}" height="10" rx="5" fill="{c}" style="animation-delay:-{i * .7:.1f}s"/>')
        b.append(t(bx + bw - 20, y + 15, st, size=12, fill=c if c != DIM else MUTE, anchor="end"))
    dy = by + 198
    b.append(f'<rect x="{bx + 18}" y="{dy}" width="{bw - 36}" height="184" rx="12" fill="{BG}" stroke="{WARN}"/>')
    b.append(t(bx + 38, dy + 30, "APPROVAL REQUIRED", size=12, fill=WARN, ls=2, weight=700))
    b.append(t(bx + 38, dy + 60, "The coding agent wants to run a command", cls="s", size=16.5, fill=TEXT, weight=700))
    b.append(f'<rect x="{bx + 38}" y="{dy + 76}" width="{bw - 76}" height="38" rx="8" fill="{PANEL}" stroke="{LINE2}"/>')
    b.append(t(bx + 52, dy + 100, "$ npm test", size=14, fill=TEXT))
    css += (f"@keyframes appr{{0%,45%{{fill:{PANEL2};stroke:{LINE2}}}52%,92%{{fill:#14402E;stroke:{OK}}}100%{{fill:{PANEL2};stroke:{LINE2}}}}}.appr{{animation:appr 6s linear infinite}}"
            "@keyframes apprt{0%,52%{opacity:0}58%,92%{opacity:1}100%{opacity:0}}.apprt{animation:apprt 6s linear infinite}")
    b.append(f'<rect x="{bx + 38}" y="{dy + 130}" width="110" height="36" rx="8" fill="{PANEL2}" stroke="{LINE2}"/>')
    b.append(t(bx + 93, dy + 153, "Deny", cls="s", size=14.5, fill=MUTE, anchor="middle", weight=600))
    b.append(f'<rect class="appr" x="{bx + 158}" y="{dy + 130}" width="110" height="36" rx="8" fill="{PANEL2}" stroke="{LINE2}"/>')
    b.append(t(bx + 213, dy + 153, "Approve", cls="s", size=14.5, fill=TEXT, anchor="middle", weight=700))
    b.append(f'<g class="apprt rm">{check(bx + 290, dy + 148)}{t(bx + 304, dy + 153, "approved, running", size=12.5, fill=OK)}</g>')
    # C: gateway
    cx, cy, cw, ch = 802, 80, 370, 400
    b.append(panel(cx, cy, cw, ch, "GATEWAY"))
    gx, gy, gw, gh = cx + 40, cy + 142, cw - 80, 104
    for i, lab in enumerate(["WEB", "MACOS", "WINDOWS"]):
        x = cx + 18 + i * 114
        b.append(f'<rect x="{x}" y="{cy + 52}" width="106" height="34" rx="8" fill="{BG}" stroke="{LINE2}"/>{t(x + 53, cy + 74, lab, size=12.5, fill=TEXT, anchor="middle", ls=1)}')
        b.append(f'<path d="M{x + 53} {cy + 86}C{x + 53} {cy + 116} {cx + cw / 2} {cy + 112} {cx + cw / 2} {gy}" fill="none" stroke="{INFO}" stroke-width="1.5" class="flow"/>')
    b.append(f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" rx="12" fill="{PANEL2}" stroke="{OK}" stroke-width="1.5"/>')
    b.append(lock(gx + 34, gy + 34))
    b.append(t(gx + 62, gy + 38, "Model gateway", cls="s", size=17, fill=TEXT, weight=800))
    b.append(t(gx + 62, gy + 58, "provider keys stay here", size=12.5, fill=OK))
    b.append(t(gx + 20, gy + 86, "auth · routing · usage · memory · MCP", size=12, fill=MUTE))
    for i, lab in enumerate(["opencode", "openclaw", "Chrome", "Ollama"]):
        x = cx + 18 + i * 85
        b.append(f'<rect x="{x}" y="{cy + 300}" width="79" height="34" rx="8" fill="{BG}" stroke="{LINE2}"/>{t(x + 39.5, cy + 322, lab, size=12, fill=TEXT, anchor="middle")}')
        b.append(f'<path d="M{cx + cw / 2} {gy + gh}C{cx + cw / 2} {cy + 276} {x + 39.5} {cy + 270} {x + 39.5} {cy + 300}" fill="none" stroke="{OK}" stroke-width="1.5" class="flow"/>')
    b.append(t(cx + cw / 2, cy + 364, "local runtimes, supervised by the app", size=12.5, fill=MUTE, anchor="middle"))
    b.append(t(cx + cw / 2, cy + 384, "nothing in the demo recording is mocked", size=12, fill=DIM, anchor="middle"))
    s_, h = strip(496, W, "BOUNDARIES", ["keys never leave the gateway", "file, shell and tool actions need approval",
                                        "model routing per surface", "shared memory", "MCP endpoint for other tools"])
    b.append(s_)
    return doc(W, 496 + h + 28, "".join(b),
               "Aira: a full-stack AI workspace across web, macOS and Windows. Surfaces: Chat, Code, Agents, Browser, Workspace. "
               "An agent fleet with roles; commands and file changes wait for approval. Web and Tauri desktop shells connect to a "
               "server-side model gateway that holds provider keys and supervises local runtimes: opencode, openclaw, Chrome, Ollama.", css)


def big_studio():
    W = 1200
    b = chrome(W, "data science studio", "real AutoML, narrated but never invented", "live")
    css = ("@keyframes growx{0%{transform:scaleX(.05)}40%,88%{transform:scaleX(1)}100%{transform:scaleX(.05)}}"
           ".growx{transform-box:fill-box;transform-origin:left;animation:growx 7s ease-in-out infinite}")
    ax, ay, aw, ah = 28, 80, 364, 400
    b.append(panel(ax, ay, aw, ah, "MODEL SELECTION"))
    b.append(t(ax + aw - 18, ay + 28, "sample run", size=12.5, fill=DIM, anchor="end"))
    models = [("XGBoost", .91), ("Random Forest", .89), ("Gradient Boosting", .88), ("Logistic Regression", .84), ("SVM", .81)]
    for i, (m_, sc) in enumerate(models):
        y = ay + 50 + i * 52
        win = i == 0
        if win:
            b.append(f'<rect x="{ax + 10}" y="{y - 4}" width="{aw - 20}" height="48" rx="9" fill="{OK}" fill-opacity=".08" stroke="{OK}" stroke-opacity=".5"/>')
        b.append(t(ax + 22, y + 15, m_, size=13.5, fill=TEXT, weight=700 if win else None))
        b.append(f'<rect x="{ax + 22}" y="{y + 24}" width="270" height="10" rx="5" fill="{BG}" stroke="{LINE}"/>')
        b.append(f'<rect class="growx" x="{ax + 22}" y="{y + 24}" width="{270 * sc:.0f}" height="10" rx="5" fill="{OK if win else INFO}" opacity="{1 if win else .6}" style="animation-delay:{i * .12:.2f}s"/>')
        b.append(t(ax + aw - 22, y + 34, f"{sc:.2f}", size=13.5, fill=OK if win else MUTE, anchor="end", weight=700))
    x = ax + 18
    y = ay + ah - 52
    for i, st in enumerate(["ingest", "clean", "EDA", "train", "explain"]):
        c, w, h = chip(x, y, st, size=12, color=TEXT, fill=BG, pad=9)
        b.append(c)
        x += w
        if i < 4:
            b.append(f'<line x1="{x:.0f}" y1="{y + 13.5}" x2="{x + 12:.0f}" y2="{y + 13.5}" stroke="{OK}" stroke-width="1.8" class="flow"/>')
        x += 12
    # B: explain
    bx, by, bw, bh = 408, 80, 386, 400
    b.append(panel(bx, by, bw, bh, "EXPLAIN"))
    b.append(t(bx + bw - 18, by + 28, "SHAP feature impact", size=12.5, fill=DIM, anchor="end"))
    feats = [("tenure", 150, OK), ("monthly spend", 118, OK), ("region", -80, BAD), ("visits", 62, OK), ("age", -38, BAD)]
    for i, (f, v, c) in enumerate(feats):
        y = by + 50 + i * 25
        b.append(t(bx + 20, y + 12, f, size=12.5, fill=MUTE))
        b.append(f'<rect class="growx" x="{bx + 138}" y="{y}" width="{abs(v) * 1.45:.0f}" height="14" rx="3" fill="{c}" opacity=".85" style="animation-delay:{i * .1:.1f}s"/>')
    dy = by + 196
    b.append(f'<line x1="{bx + 18}" y1="{dy}" x2="{bx + bw - 18}" y2="{dy}" stroke="{LINE}"/>')
    b.append(t(bx + 18, dy + 28, "DRIFT", size=12.5, fill=DIM, ls=2))
    b.append(t(bx + bw - 18, dy + 28, "KS test: live vs training", size=12.5, fill=DIM, anchor="end"))

    def bell(mu, sd, amp, base):
        pts_ = []
        for i in range(61):
            xx = bx + 30 + i * (bw - 60) / 60
            yy = base - amp * math.exp(-((xx - mu) ** 2) / (2 * sd * sd))
            pts_.append(f"{xx:.1f} {yy:.1f}")
        return "M" + " L".join(pts_)

    base = dy + 164
    b.append(f'<line x1="{bx + 30}" y1="{base}" x2="{bx + bw - 30}" y2="{base}" stroke="{LINE2}" stroke-width="1.5"/>')
    b.append(f'<path d="{bell(bx + 150, 44, 104, base)}" fill="{INFO}" fill-opacity=".1" stroke="{INFO}" stroke-width="2"/>')
    css += "@keyframes shift{0%,15%{transform:translateX(-70px)}55%,90%{transform:translateX(0)}100%{transform:translateX(-70px)}}.shift{animation:shift 7s ease-in-out infinite}"
    css += "@keyframes dr{0%,50%{opacity:0}60%,90%{opacity:1}100%{opacity:0}}.dr{animation:dr 7s linear infinite}"
    b.append(f'<g clip-path="url(#dc)"><path class="shift" d="{bell(bx + 220, 50, 92, base)}" fill="{WARN}" fill-opacity=".1" stroke="{WARN}" stroke-width="2" stroke-dasharray="5 4"/></g>')
    b.append(t(bx + 30, base + 22, "training", size=12, fill=INFO))
    b.append(t(bx + 110, base + 22, "live", size=12, fill=WARN))
    c, w, h = chip(bx + bw - 18 - (mw("drift detected", 12) + 18), base + 6, "drift detected", size=12, color=WARN, stroke=WARN, fill=BG, pad=9, extra=' class="dr rm"')
    b.append(c)
    # C: narration
    cx, cy, cw, ch = 810, 80, 362, 400
    b.append(panel(cx, cy, cw, ch, "NARRATION"))
    b.append(t(cx + cw - 18, cy + 28, "Gemini explains only", size=12.5, fill=DIM, anchor="end"))
    b.append(f'<path d="M{cx + 30} {cy + 46}h{cw - 60}a12 12 0 0 1 12 12v74a12 12 0 0 1-12 12h-{cw - 96}l-18 16v-16h-18a12 12 0 0 1-12-12v-74a12 12 0 0 1 12-12z" fill="{BG}" stroke="{LINE2}"/>')
    for i, ln in enumerate(["XGBoost won on cross-validation.", "Tenure and monthly spend drive most", "predictions. Live data has drifted", "since training, so retrain soon."]):
        b.append(t(cx + 36, cy + 72 + i * 21, ln, cls="s", size=14.5, fill=TEXT))
    ry = cy + 186
    b.append(f'<rect x="{cx + 18}" y="{ry}" width="{cw - 36}" height="74" rx="10" fill="{PANEL2}" stroke="{OK}"/>')
    b.append(lock(cx + 44, ry + 30))
    b.append(t(cx + 68, ry + 31, "No numeric fields in its schema", cls="s", size=14.5, fill=TEXT, weight=700))
    b.append(t(cx + 68, ry + 52, "numbers come from the ML service", size=12, fill=OK))
    fy = cy + 292
    b.append(t(cx + 18, fy, "WHERE NUMBERS COME FROM", size=11.5, fill=DIM, ls=1.5))
    for i, (nm, sub, c) in enumerate([("React", "workspace", LINE2), ("Express", "orchestration", LINE2), ("FastAPI", "scikit-learn · XGBoost", OK)]):
        x = cx + 18 + i * 110
        w = 102 if i < 2 else 106
        b.append(f'<rect x="{x}" y="{fy + 14}" width="{w}" height="50" rx="8" fill="{BG}" stroke="{c}"/>')
        b.append(t(x + 10, fy + 35, nm, cls="s", size=14, fill=TEXT, weight=700))
        b.append(t(x + 10, fy + 52, sub if i < 2 else "ML service", size=11.5, fill=OK if i == 2 else MUTE))
        if i < 2:
            b.append(f'<line x1="{x + w}" y1="{fy + 39}" x2="{x + 110}" y2="{fy + 39}" stroke="{OK}" stroke-width="1.8" class="flow"/>')
    b.append(t(cx + 18, fy + 86, "template narration if Gemini is down", size=11.5, fill=DIM))
    # strip
    sy = 496
    s_, h = strip(sy, W, "ALSO", ["Beginner and Expert modes", "agentic reason → act → observe", "visual SQL builder",
                                 "hyperparameter tuning", "zero telemetry", "tested + CI"])
    b.append(s_)
    return doc(W, sy + h + 28, "".join(b),
               "Data Science Studio: a real AutoML workstation. Models are selected by cross-validation, explained with SHAP, and "
               "monitored for drift with KS tests, all computed by a Python FastAPI service running scikit-learn and XGBoost. "
               "Gemini only narrates: its response schema has no numeric fields.", css,
               defs='<clipPath id="dc"><rect x="426" y="276" width="350" height="166"/></clipPath>')


# ──────────────────────── PROJECT CARDS ─────────────────────────
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


def ill_helpin():
    b = []
    b.append(f'<path d="M36 300C120 268 150 214 236 204S400 250 470 214S540 172 564 168" fill="none" stroke="{INFO}" stroke-width="14" opacity=".1" stroke-linecap="round"/>')
    for d in ("M40 190H560", "M40 246H560", "M96 160V312", "M196 160V312", "M392 160V312", "M492 160V312", "M40 296L300 160", "M300 312L560 200"):
        b.append(f'<path d="{d}" stroke="{LINE}" stroke-width="1.5" fill="none"/>')
    for x, y, r_ in ((112, 204, 24), (474, 274, 22), (130, 284, 17), (508, 190, 16)):
        b.append(f'<circle cx="{x}" cy="{y}" r="{r_}" fill="{MUTE}" fill-opacity=".06" stroke="{LINE2}" stroke-dasharray="3 4"/><circle cx="{x}" cy="{y}" r="3" fill="{DIM}"/>')
    ax, ay, hx, hy = 300, 212, 214, 274
    css = ("@keyframes area{0%,100%{r:30;opacity:.9}50%{r:38;opacity:.4}}.area{animation:area 2.4s ease-in-out infinite}")
    css += cycle_css("hst", 3, 2.6, fade=0.1, shift=False)
    b.append(f'<circle class="area" cx="{ax}" cy="{ay}" r="30" fill="{WARN}" fill-opacity=".08" stroke="{WARN}" stroke-dasharray="4 4"/>')
    b.append(f'<line x1="{hx}" y1="{hy}" x2="{ax}" y2="{ay}" stroke="{OK}" stroke-width="1.5" class="flow"/>')
    b.append(f'<circle r="4" fill="{OK}"><animateMotion dur="2.6s" repeatCount="indefinite" path="M{hx} {hy}L{ax} {ay}"/></circle>')
    b.append(f'<circle cx="{ax}" cy="{ay}" r="6" fill="{WARN}"/>')
    b.append(f'<circle cx="{hx}" cy="{hy}" r="9" fill="{BG}" stroke="{OK}" stroke-width="1.5"/><circle cx="{hx}" cy="{hy}" r="4" fill="{OK}"/>')
    b.append(t(hx, hy + 26, "neighbour", size=11.5, fill=OK, anchor="middle"))
    states = [("asked: a letter I can't read", WARN), ("a neighbour offers help", INFO), ("solved · asker confirms · +karma", OK)]
    for i, (s_, c) in enumerate(states):
        w = mw(s_, 12) + 18
        b.append(f'<g class="hst{" rm" if i == 2 else ""}" style="animation-delay:{i * 2.6:.1f}s"><rect x="342" y="199" width="{w:.0f}" height="26" rx="13" fill="{BG}" stroke="{c}"/>'
                 f'{t(351, 216.5, s_, size=12, fill=c)}</g>')
    return "".join(b), css


CARDS = [
    ("talktual", "REAL-TIME VOICE", "Talktual", "Two people, two languages, one natural conversation.",
     "WebRTC · QR handshake · STT · translate · TTS", True, ill_talktual),
    ("transfer", "P2P TRANSFER", "Tata Dransfer", "Encrypted peer-to-peer files, calls and chat.",
     "WebRTC · direct-to-disk streaming · calls", True, ill_transfer),
    ("gita", "RETRIEVAL", "Gita.AI", "Grounded in all 701 verses, not in model memory.",
     "embeddings · RAG · multilingual · donated to ISKCON", False, ill_gita),
    ("helpin", "HYPERLOCAL", "HelpIn", "Neighbours solve real problems; the asker confirms.",
     "map-first PWA · Postgres · Web Push · Budapest", True, ill_helpin),
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
        "echo-family.svg": echo_family(),
        "sys-syntra.svg": big_syntra(), "sys-pluto.svg": big_pluto(), "sys-atlas.svg": big_atlas(),
        "sys-cosmos.svg": big_cosmos(), "sys-aira.svg": big_aira(), "sys-studio.svg": big_studio(), "toolkit.svg": toolkit(), "roles.svg": roles(), "footer.svg": footer(),
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
