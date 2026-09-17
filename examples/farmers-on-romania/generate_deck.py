"""Emit a standalone HTML deck: one file per slide, no build step, no framework.

Parameterised from generate_s3_deck.py (RLM Test Cafe Session 3).

    python3 generate_deck.py

Reads  slides/slideNN.body.html   (zero-padded fragments, plain HTML)
Writes deck/slide1.html … slideN.html   (1-indexed, NOT zero-padded)
       deck/index.html                  (meta-refresh to slide1.html)
       SPEAKER_NOTES.md                 (sibling of deck/)

Fill SLIDE_TITLES and SPEAKER_NOTES below. A missing body renders a visible
placeholder slide rather than failing, so the deck is always navigable.
"""

import os

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

HERE = os.path.dirname(os.path.abspath(__file__))

DECK_TITLE = "Farmers in Romania"
SUBTITLE = "One country, two agricultures, three official answers"
PAGE_TITLE = "Farmers in Romania - By the Numbers, and Against Them"  # browser tab + index.html
BYLINE = "**Romanian Agriculture - By the Numbers, and Against Them** | built with the html-deck skill"

# Two free-text lines under the byline in SPEAKER_NOTES.md. Keep or empty them.
NOTES_INTRO = [
    "Navigation: arrow keys, space, or PageUp/PageDown. `deck/index.html` opens slide 1.",
    "Structure: slides 2-6. Money, output, volatility, trade: 7-10. Where it breaks down: 11-12. Scope and close: 13-14.",
    "",
    "Every figure carries its source and year. Sources: Eurostat, European Commission DG AGRI, EU CAP Network, INS Romania.",
]

TOTAL_SLIDES = 14  # fix this BEFORE writing bodies; it lands in every slide three times

OUTPUT_DIR = os.path.join(HERE, "deck")
BODIES_DIR = os.path.join(HERE, "slides")
NOTES_PATH = os.path.join(os.path.dirname(OUTPUT_DIR), "SPEAKER_NOTES.md")

COLOR_BG = "#192b37"
COLOR_ACCENT = "#ff5640"
COLOR_ROI = "#FFD700"
COLOR_SUCCESS = "#2ecc71"
COLOR_WARN = "#e74c3c"
COLOR_MUTED = "#8fa3b0"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- 1. CSS & Head ---
# NOTE: plain string, not an f-string. The colour literals are written out so that
# Tailwind/CSS braces can never collide with f-string interpolation. __PAGE_TITLE__
# is substituted with .replace() for the same reason.
# These are the same bytes as assets/boilerplate.html; this file is the source of truth.
html_head = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>__PAGE_TITLE__</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;600;700&family=Fira+Code&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #192b37;
            --accent-color: #ff5640;
            --roi-color: #FFD700;
            --success-color: #2ecc71;
            --warn-color: #e74c3c;
            --glass: rgba(255, 255, 255, 0.05);
        }
        body {
            background-color: var(--bg-color);
            color: white;
            font-family: 'IBM Plex Sans', sans-serif;
            overflow: hidden;
            margin: 0;
        }
        @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-10px); } 100% { transform: translateY(0px); } }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes pulse { 0%,100% { opacity: 0.6; } 50% { opacity: 1; } }
        @keyframes rotateGlow { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        @keyframes dataFlow { 0% { left: 0%; opacity:0; } 10% { opacity:1; } 90% { opacity:1; } 100% { left: 100%; opacity:0; } }

        .animate-float { animation: float 6s ease-in-out infinite; }
        .animate-entry { animation: fadeIn 0.8s ease-out forwards; opacity: 0; }
        .animate-pulse { animation: pulse 2s ease-in-out infinite; }
        .delay-1 { animation-delay: 0.2s; }
        .delay-2 { animation-delay: 0.4s; }
        .delay-3 { animation-delay: 0.6s; }
        .delay-4 { animation-delay: 0.8s; }

        .glass-panel {
            background: var(--glass);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            border-left: 4px solid var(--accent-color);
        }
        .glass-panel-alt {
            background: var(--glass);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            border-left: 4px solid var(--roi-color);
        }
        .glass-panel-success {
            background: var(--glass);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            border-left: 4px solid var(--success-color);
        }
        .glass-panel-warn {
            background: var(--glass);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            border-left: 4px solid var(--warn-color);
        }
        .code-block {
            font-family: 'Fira Code', monospace;
            background: #0d161c;
            border-radius: 8px;
            border: 1px solid #333;
        }
        .nav-btn {
            transition: all 0.3s;
            opacity: 0.5;
        }
        .nav-btn:hover { opacity: 1; transform: scale(1.1); color: var(--accent-color); }

        .badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.85em;
            display: inline-block;
        }
        .badge-accent { background: var(--accent-color); color: white; }
        .badge-success { background: var(--success-color); color: white; }
        .badge-roi { background: var(--roi-color); color: var(--bg-color); }
        .badge-warn { background: var(--warn-color); color: white; }

        .mcp-packet {
            position: absolute;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: var(--accent-color);
            box-shadow: 0 0 15px var(--accent-color);
            animation: dataFlow 3s linear infinite;
            z-index: 8;
        }

        .chev { transition: transform 0.2s ease; }
        .card-press { transition: transform .06s ease; }
        .card-press:active { transform: scale(0.98); }

        .stamp {
            position: absolute;
            transform: rotate(-11deg);
            border: 3px solid var(--warn-color);
            color: var(--warn-color);
            font-weight: 700;
            letter-spacing: 0.18em;
            padding: 6px 18px;
            border-radius: 6px;
            background: rgba(25,43,55,0.72);
            white-space: nowrap;
        }

        /* ---- PRINT / PDF EXPORT -------------------------------------------------
           Chrome does NOT paint the canvas background in print: without the
           html/body rule below the whole deck prints WHITE. print-color-adjust
           must be forced on everything, and .animate-entry starts at opacity 0
           so it has to be frozen or slides render mid-fade. */
        .print-only { display: none; }
        @media print {
            @page { size: 1920px 1080px; margin: 0; }
            html, body {
                background: #192b37 !important;
                background-color: #192b37 !important;
                width: 1920px; height: 1080px;
                overflow: hidden !important;
            }
            *, *::before, *::after {
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }
            .animate-entry {
                animation: none !important;
                opacity: 1 !important;
                transform: none !important;
            }
            .animate-float, .animate-pulse, .mcp-packet { animation: none !important; }
            .h-screen { height: 1080px !important; }
            .w-screen { width: 1920px !important; }
            .print-hide { display: none !important; }
            .print-only { display: block !important; }
        }
    </style>
</head>
<body>
""".replace("__PAGE_TITLE__", PAGE_TITLE)


# --- 2. Shared layout helpers ---
# TOTAL_SLIDES lands in the emitted HTML three times per slide: the forward-link
# guard, the counter, and the End key target. Change the count -> re-emit ALL slides.

def get_nav(slide_id):
    prev_link = f"slide{slide_id - 1}.html" if slide_id > 1 else "#"
    next_link = f"slide{slide_id + 1}.html" if slide_id < TOTAL_SLIDES else "#"
    return f"""
    <div class="absolute bottom-6 right-8 flex items-center gap-6 z-50">
        <span class="text-sm opacity-40 font-mono">SLIDE {slide_id:02d} / {TOTAL_SLIDES}</span>
        <a href="{prev_link}" class="nav-btn text-2xl"><i class="fas fa-chevron-left"></i></a>
        <a href="{next_link}" class="nav-btn text-2xl"><i class="fas fa-chevron-right"></i></a>
    </div>
    <script>
      var PREV = "{prev_link}", NEXT = "{next_link}";
      document.addEventListener('keydown', function (e) {{
        if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
          if (NEXT !== '#') {{ e.preventDefault(); location.href = NEXT; }}
        }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
          if (PREV !== '#') {{ e.preventDefault(); location.href = PREV; }}
        }} else if (e.key === 'Home') {{
          location.href = 'slide1.html';
        }} else if (e.key === 'End') {{
          location.href = 'slide{TOTAL_SLIDES}.html';
        }}
      }});
    </script>
    """


# --- 3. SLIDE BODIES ---
# Each slide's body lives in slides/slideNN.body.html as plain HTML with literal
# colour values. Keeping them out of this file is the one deliberate departure
# from Session 2's generator: the bodies contain inline <svg> and CSS braces, and
# an f-string would need every one of them escaped. The emitted deck is identical.

def load_body(slide_id):
    path = os.path.join(BODIES_DIR, f"slide{slide_id:02d}.body.html")
    if not os.path.exists(path):
        return (f"<div class='h-screen w-screen flex items-center justify-center'>"
                f"<h1 class='text-4xl opacity-40'>Slide {slide_id} &mdash; not written yet</h1></div>")
    with open(path, encoding="utf-8") as f:
        return f.read()


# --- 4. TITLES & SPEAKER NOTES ---
# Shape:
#   SLIDE_TITLES = {1: "Short title", 2: "...", ...}
#   SPEAKER_NOTES = {1: """
#   Prose, wrapped at ~110 columns. Plain text, no markdown.
#   Never write a literal "--": it is illegal inside an HTML comment. notes_comment()
#   collapses it to "-" defensively, which silently rewrites your em dashes.
#   """, ...}
# One entry per slide, 1..TOTAL_SLIDES. Missing keys emit an empty section.

SLIDE_TITLES = {
    1: "Title",
    2: "The headline - a third of Europe's farms",
    3: "Two agricultures, one country",
    4: "The average farm is a lie",
    5: "Who is actually farming",
    6: "The hinge - three official answers",
    7: "The money - CAP 2023-2027",
    8: "What the land produces",
    9: "The volatility - a 63% collapse",
    10: "Raw out, processed in",
    11: "Where this framing is wrong",
    12: "When the sources disagree",
    13: "What this deck does not cover",
    14: "Close - ask which number they mean",
}

SPEAKER_NOTES = {}


# --- 5. GENERATE HTML FILES ---

def notes_comment(slide_id):
    body = SPEAKER_NOTES.get(slide_id, "").replace("--", "-")
    return f"<!--\nSPEAKER NOTES - SLIDE {slide_id:02d}: {SLIDE_TITLES.get(slide_id, '')}\n\n{body}\n-->\n"


def generate_slides():
    print(f"Generating: {DECK_TITLE} - {SUBTITLE}")
    print(f"Total slides: {TOTAL_SLIDES}")
    print(f"Output directory: {OUTPUT_DIR}")

    for i in range(1, TOTAL_SLIDES + 1):
        html = html_head + notes_comment(i) + load_body(i) + get_nav(i) + "</body></html>"
        with open(os.path.join(OUTPUT_DIR, f"slide{i}.html"), "w", encoding="utf-8") as f:
            f.write(html)

    index_html = ('<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0;url=slide1.html">'
                  f'<title>{PAGE_TITLE}</title></head><body></body></html>')
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    # speaker notes, one file, same source as the embedded comments
    lines = [
        f"# {DECK_TITLE}: {SUBTITLE}",
        "",
        BYLINE,
        "",
    ]
    for line in NOTES_INTRO:
        lines.append(line)
        lines.append("")
    lines.append("---")
    lines.append("")
    for i in range(1, TOTAL_SLIDES + 1):
        lines.append(f"## Slide {i:02d} - {SLIDE_TITLES.get(i, '')}")
        lines.append("")
        lines.append(SPEAKER_NOTES.get(i, "").strip())
        lines.append("")
        lines.append("---")
        lines.append("")
    with open(NOTES_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\nSuccess! {TOTAL_SLIDES} slides + index.html in: {OUTPUT_DIR}")
    print(f"Speaker notes: {NOTES_PATH}")
    for i in range(1, TOTAL_SLIDES + 1):
        print(f"  Slide {i:2d}: {SLIDE_TITLES.get(i, '')}")
    print(f"\nOpen {os.path.join(OUTPUT_DIR, 'slide1.html')} in your browser. Arrow keys / space to navigate.")


if __name__ == "__main__":
    generate_slides()
