"""
Generate a tight 1-page PDF resume: Vamshi_Yadav_Golla_Resume.pdf
Matches the portfolio styling. Designed to fit on a single A4 page.
Run: python build_resume_pdf.py
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
import os

OUT = "Vamshi_Yadav_Golla_Resume.pdf"

# Colors (match portfolio palette)
INK = HexColor("#0F172A")
INK2 = HexColor("#334155")
MUTED = HexColor("#64748B")
ACCENT = HexColor("#6366F1")
RULE = HexColor("#E2E8F0")

# Page geometry
W, H = A4
MARGIN_X = 14 * mm
MARGIN_TOP = 12 * mm
MARGIN_BOTTOM = 10 * mm
CONTENT_W = W - 2 * MARGIN_X

# Fonts (use built-in Helvetica — universal)
FONT = "Helvetica"
FONT_B = "Helvetica-Bold"
FONT_I = "Helvetica-Oblique"

c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("Vamshi Yadav Golla — Resume")
c.setAuthor("Vamshi Yadav Golla")

y = H - MARGIN_TOP


def set_font(size, bold=False, italic=False):
    f = FONT
    if bold and italic:
        f = "Helvetica-BoldOblique"
    elif bold:
        f = FONT_B
    elif italic:
        f = FONT_I
    c.setFont(f, size)


def draw_wrapped(x, y, text, max_w, size, leading, color=INK2, bold=False, italic=False):
    """Draw text wrapped to max_w, return new y."""
    set_font(size, bold, italic)
    c.setFillColor(color)
    words = text.split()
    line = ""
    for w in words:
        test = (line + " " + w).strip()
        if c.stringWidth(test, FONT_B if bold else FONT, size) <= max_w:
            line = test
        else:
            c.drawString(x, y, line)
            y -= leading
            line = w
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_bold_inline(x, y, segments, max_w, size=8.2, leading=10.2):
    """segments: list of (text, bold) — renders inline with bold parts mixed in."""
    # Tokenize into words keeping bold flag
    tokens = []
    for text, bold in segments:
        parts = text.split(" ")
        for i, p in enumerate(parts):
            if i > 0:
                tokens.append((" ", bold))  # space carries bold flag of trailing text (doesn't matter)
            if p:
                tokens.append((p, bold))
    # Build lines respecting max width
    line = []  # list of (text, bold, width)
    line_w = 0
    c.setFillColor(INK2)
    for tok, bold in tokens:
        fn = FONT_B if bold else FONT
        w = c.stringWidth(tok, fn, size)
        if line_w + w <= max_w:
            line.append((tok, bold, w))
            line_w += w
        else:
            # flush line
            cx = x
            for t, b, tw in line:
                c.setFont(FONT_B if b else FONT, size)
                c.setFillColor(INK if b else INK2)
                c.drawString(cx, y, t)
                cx += tw
            y -= leading
            # new line — skip leading spaces
            if tok.strip() == "":
                line, line_w = [], 0
            else:
                line = [(tok, bold, w)]
                line_w = w
    if line:
        cx = x
        for t, b, tw in line:
            c.setFont(FONT_B if b else FONT, size)
            c.setFillColor(INK if b else INK2)
            c.drawString(cx, y, t)
            cx += tw
        y -= leading
    return y


def section_header(y, title):
    """Render a section header with a bottom rule."""
    set_font(8.4, bold=True)
    c.setFillColor(ACCENT)
    c.drawString(MARGIN_X, y, title.upper())
    # Rule under the text
    y -= 2
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.line(MARGIN_X, y, MARGIN_X + CONTENT_W, y)
    return y - 7


def role_line(y, role, org, date):
    """Role + date on one line, org underneath."""
    set_font(9, bold=True)
    c.setFillColor(INK)
    c.drawString(MARGIN_X, y, role)
    # date right-aligned
    if date:
        set_font(7.8)
        c.setFillColor(MUTED)
        c.drawRightString(MARGIN_X + CONTENT_W, y, date)
    y -= 10.5
    set_font(8, italic=False)
    c.setFillColor(INK2)
    c.drawString(MARGIN_X, y, org)
    return y - 9


def bullet(y, segments, bullet_char="\u2022", indent=9, size=8.2, leading=10.2):
    """Render a bullet with bold inline support."""
    # Bullet mark
    set_font(size, bold=False)
    c.setFillColor(ACCENT)
    c.drawString(MARGIN_X + 2, y, bullet_char)
    # Body (wrapped, with bold)
    new_y = draw_bold_inline(MARGIN_X + indent, y, segments, CONTENT_W - indent, size=size, leading=leading)
    return new_y - 1


def stack_line(y, stack, link=None):
    set_font(7.4)
    c.setFillColor(MUTED)
    full = f"Stack: {stack}" + (f"   |   {link}" if link else "")
    # keep on one line if possible; else wrap
    if c.stringWidth(full, FONT, 7.4) <= CONTENT_W:
        c.drawString(MARGIN_X, y, full)
        return y - 9.5
    else:
        return draw_wrapped(MARGIN_X, y, full, CONTENT_W, 7.4, 9, color=MUTED)


# ============ HEADER ============
set_font(22, bold=True)
c.setFillColor(INK)
c.drawString(MARGIN_X, y, "Vamshi Yadav Golla")
# Right-side: title
set_font(9.2, bold=True)
c.setFillColor(ACCENT)
c.drawRightString(MARGIN_X + CONTENT_W, y + 2, "AI Agent Engineer & Automation Architect")
y -= 13

# Contact line
set_font(7.8)
c.setFillColor(INK2)
contact = "London, UK  \u2022  Vamshiyadav2783@gmail.com  \u2022  +44 7887 132 409  \u2022  linkedin.com/in/vamshi-yadav869  \u2022  github.com/Vamshi-27072001  \u2022  vamshi-27072001.github.io/portfolio"
c.drawString(MARGIN_X, y, contact)
y -= 5
# Header rule
c.setStrokeColor(INK)
c.setLineWidth(1.2)
c.line(MARGIN_X, y, MARGIN_X + CONTENT_W, y)
y -= 8

# ============ SUMMARY ============
y = section_header(y, "Professional Summary")
y = draw_bold_inline(
    MARGIN_X, y,
    [
        ("AI Agent Engineer", True),
        (" specialising in autonomous AI systems on ", False),
        ("n8n, LangChain, and GPT-4o", True),
        (". Shipped ", False),
        ("6 production projects", True),
        (" delivering ", False),
        ("£36K+/year business impact", True),
        (" — including a ", False),
        ("99.98% cost-reduction chatbot", True),
        (", a zero-touch LinkedIn publishing pipeline, and an ML GPS-spoofing detector at ", False),
        ("99.95% accuracy", True),
        (". MSc Computer Science (UEL). Interviewing for UK AI Engineer / Automation / ML roles — Graduate Visa eligible.", False),
    ],
    CONTENT_W, size=8.4, leading=10.4
)
y -= 2

# ============ EXPERIENCE ============
y = section_header(y, "Professional Experience")
y = role_line(y, "Cyber Security Intern", "Lexnis Services Limited — Hertfordshire, UK", "Nov 2025 – Present")
for seg in [
    [("Conducted market analysis of 10 UK vehicle tracking companies", True), (" across 5 benchmarking criteria; produced a decision-ready competitive matrix.", False)],
    [("Mapped 15+ product features per provider", True), (" and recommended best-fit GPS tracking solutions by customer segment.", False)],
    [("Identified a market gap supporting a £9,100/month operational model", True), (" feeding directly into go-to-market strategy.", False)],
    [("Used AI tools (GPT-4, Google suite) to produce research reports", True), (" that informed 3 major business decisions at 4\u00D7 analysis throughput.", False)],
]:
    y = bullet(y, seg)
y -= 1

# ============ PROJECTS ============
y = section_header(y, "Flagship Projects")

# Project 1
y = role_line(y, "NSP Cases — AI Email Enquiry Handler", "Autonomous customer-service pipeline  \u2022  Production", "Apr 2026")
for seg in [
    [("Engineered a 19-node n8n workflow replacing a human customer-service agent", True), (" — Gmail to knowledge-base to HTML reply end-to-end in ", False), ("under 60 seconds, zero human intervention", True), (".", False)],
    [("Integrated GPT-4o Vision for multimodal enquiries", True), (" — auto-analyses product drawings/images, removing the #1 friction in technical sales.", False)],
]:
    y = bullet(y, seg)
y = stack_line(y, "n8n \u00B7 LangChain \u00B7 GPT-4.1-mini \u00B7 GPT-4o Vision \u00B7 Gmail OAuth2 \u00B7 Supabase", "github.com/Vamshi27072001/NSP-email-enquiry")

# Project 2
y = role_line(y, "Restaurant AI Agent — Taco Bell UK", "Zero-hallucination chatbot  \u2022  Production", "Apr 2026")
for seg in [
    [("Deployed an 11-node LangChain agent on Telegram (GPT-4o-mini)", True), (" — menu, allergen, nutrition ", False), ("24/7 at sub-2-second latency", True), (".", False)],
    [("Drove operating costs from £12,000/yr to £36/yr (99.98% reduction)", True), (" with full EU/UK allergen compliance across 100+ items.", False)],
]:
    y = bullet(y, seg)
y = stack_line(y, "n8n \u00B7 LangChain \u00B7 GPT-4o-mini \u00B7 Telegram \u00B7 Google Sheets \u00B7 PostgreSQL", "github.com/Vamshi-27072001/restaurant-ai-agent")

# Project 3
y = role_line(y, "LinkedIn Post Manager — AI Content Engine", "Telegram-to-LinkedIn automation  \u2022  Production", "Apr 2026")
for seg in [
    [("Built a 13-node autonomous Telegram-to-LinkedIn publishing engine", True), (" (GPT-4.1-mini + OpenAI Images + LinkedIn ugcPosts API) eliminating every human touchpoint.", False)],
    [("Cut content creation time 98% (25 min \u2192 30 sec)", True), (" and saved ", False), ("£24,000/year in outsourced social costs", True), (" at £0.01 per post.", False)],
]:
    y = bullet(y, seg)
y = stack_line(y, "n8n \u00B7 LangChain \u00B7 GPT-4.1-mini \u00B7 OpenAI Images API \u00B7 LinkedIn REST \u00B7 OAuth2", "github.com/Vamshi-27072001/telegram-linkedin-agent")

# Project 4
y = role_line(y, "ML-Based GPS Spoofing Detection for Drone Delivery", "MSc Dissertation  \u2022  University of East London", "Jun – Sep 2025")
for seg in [
    [("Trained Random Forest & XGBoost classifiers to 99.95% / 99.90% accuracy", True), (" on 62,000+ telemetry records; false-positive rate <0.05%.", False)],
    [("Deployed real-time detection on Raspberry Pi", True), (" with autonomous countermeasures (hover, reroute, return-to-base).", False)],
]:
    y = bullet(y, seg)
y = stack_line(y, "Python \u00B7 Scikit-learn \u00B7 XGBoost \u00B7 Random Forest \u00B7 Pandas \u00B7 Raspberry Pi")

# Projects 5 + 6 — compact single line
set_font(9, bold=True)
c.setFillColor(INK)
c.drawString(MARGIN_X, y, "Disaster Tweet NLP Classifier")
set_font(7.8)
c.setFillColor(MUTED)
c.drawRightString(MARGIN_X + CONTENT_W, y, "Kaggle \u2022 2025")
y -= 10
y = bullet(y, [("87% accuracy NLP pipeline", True), (" (TF-IDF + Logistic Regression) on 7,000+ tweets — +15% over baseline; recovered 90% of missing geolocation data for geospatial analysis.", False)])

set_font(9, bold=True)
c.setFillColor(INK)
c.drawString(MARGIN_X, y, "Zomato Dataset Analysis & Consumer Insights")
set_font(7.8)
c.setFillColor(MUTED)
c.drawRightString(MARGIN_X + CONTENT_W, y, "Feb 2025")
y -= 10
y = bullet(y, [("Quantified 65% online delivery adoption and a 10–15% ratings uplift", True), (" from digital presence; sentiment analysis across thousands of reviews surfaced top 3 operational rating drivers.", False)])
y -= 2

# ============ SKILLS ============
y = section_header(y, "Technical Skills")
skills = [
    ("AI Agents", "LangChain \u00B7 n8n \u00B7 Agent Architecture \u00B7 Prompt Engineering \u00B7 Tool-First Routing \u00B7 MCP"),
    ("LLMs & APIs", "GPT-4o \u00B7 GPT-4.1-mini \u00B7 Claude API \u00B7 OpenAI Vision / Images \u00B7 REST \u00B7 OAuth2"),
    ("Integrations", "Telegram Bot \u00B7 LinkedIn REST \u00B7 Gmail \u00B7 Google Sheets/Docs \u00B7 Supabase"),
    ("ML / Data", "Python \u00B7 Scikit-learn \u00B7 XGBoost \u00B7 Random Forest \u00B7 NLP / TF-IDF \u00B7 CNN / RNN \u00B7 PostgreSQL \u00B7 Power BI \u00B7 Tableau \u00B7 AWS \u00B7 GCP"),
]
for label, val in skills:
    set_font(8, bold=True)
    c.setFillColor(INK)
    label_w = c.stringWidth(label + ": ", FONT_B, 8)
    c.drawString(MARGIN_X, y, label + ":")
    y = draw_wrapped(MARGIN_X + label_w, y, val, CONTENT_W - label_w, 8, 10, color=INK2)
    y -= 0

# ============ EDUCATION + CERTS ============
y = section_header(y, "Education & Certifications")
set_font(8.8, bold=True)
c.setFillColor(INK)
c.drawString(MARGIN_X, y, "MSc Computer Science — University of East London, London, UK")
y -= 9.5
set_font(7.8, italic=True)
c.setFillColor(MUTED)
c.drawString(MARGIN_X, y, "Focus: AI systems, automation, applied ML. Dissertation: ML-based GPS spoofing detection (99.95% accuracy).")
y -= 11
# Certs as one line
set_font(8, bold=True)
c.setFillColor(INK)
c.drawString(MARGIN_X, y, "Certifications:")
cert_x = MARGIN_X + c.stringWidth("Certifications: ", FONT_B, 8)
set_font(8)
c.setFillColor(INK2)
c.drawString(cert_x, y, "AWS Academy Cloud Foundations  \u00B7  MATLAB Onramps (ML, Deep Learning, Image Processing)")

# ============ SAVE ============
c.showPage()
c.save()
print(f"Saved: {OUT}  ({os.path.getsize(OUT)/1024:.1f} KB, 1 page)")
