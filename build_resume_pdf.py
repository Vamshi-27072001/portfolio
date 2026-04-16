"""
Generate a clean 1-page PDF resume: Vamshi_Yadav_Golla_Resume.pdf
4 flagship projects only, 2 tight bullets each, generous whitespace.
Run: python build_resume_pdf.py
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import os

OUT = "Vamshi_Yadav_Golla_Resume.pdf"

# ----- Palette (matches portfolio) -----
INK = HexColor("#0F172A")      # primary text / names / bold
INK2 = HexColor("#334155")     # body text
MUTED = HexColor("#64748B")    # dates, subtle meta
ACCENT = HexColor("#6366F1")   # section headers, bullets, highlights
RULE = HexColor("#E2E8F0")     # section underlines

# ----- Page -----
W, H = A4
MARGIN_X = 16 * mm
MARGIN_TOP = 14 * mm
CONTENT_W = W - 2 * MARGIN_X

FONT = "Helvetica"
FONT_B = "Helvetica-Bold"
FONT_I = "Helvetica-Oblique"

c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("Vamshi Yadav Golla — Resume")
c.setAuthor("Vamshi Yadav Golla")
c.setSubject("AI Agent Engineer & Automation Architect")

y = H - MARGIN_TOP


def set_font(size, bold=False, italic=False):
    if bold and italic:
        c.setFont("Helvetica-BoldOblique", size)
    elif bold:
        c.setFont(FONT_B, size)
    elif italic:
        c.setFont(FONT_I, size)
    else:
        c.setFont(FONT, size)


def draw_wrapped(x, y, text, max_w, size, leading, color=INK2, bold=False):
    set_font(size, bold)
    c.setFillColor(color)
    words = text.split()
    line = ""
    fn = FONT_B if bold else FONT
    for w in words:
        test = (line + " " + w).strip()
        if c.stringWidth(test, fn, size) <= max_w:
            line = test
        else:
            c.drawString(x, y, line)
            y -= leading
            line = w
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y


def inline(x, y, segments, max_w, size=9, leading=11.5, base_color=INK2, bold_color=INK):
    """Render mixed bold/regular inline runs with wrapping."""
    tokens = []
    for text, bold in segments:
        parts = text.split(" ")
        for i, p in enumerate(parts):
            if i > 0:
                tokens.append((" ", bold))
            if p:
                tokens.append((p, bold))
    line, line_w = [], 0
    for tok, bold in tokens:
        fn = FONT_B if bold else FONT
        tw = c.stringWidth(tok, fn, size)
        if line_w + tw <= max_w:
            line.append((tok, bold, tw))
            line_w += tw
        else:
            cx = x
            for t, b, w_ in line:
                c.setFont(FONT_B if b else FONT, size)
                c.setFillColor(bold_color if b else base_color)
                c.drawString(cx, y, t)
                cx += w_
            y -= leading
            if tok.strip() == "":
                line, line_w = [], 0
            else:
                line, line_w = [(tok, bold, tw)], tw
    if line:
        cx = x
        for t, b, w_ in line:
            c.setFont(FONT_B if b else FONT, size)
            c.setFillColor(bold_color if b else base_color)
            c.drawString(cx, y, t)
            cx += w_
        y -= leading
    return y


def section(y, title):
    """Section header: small caps + thin accent rule."""
    y -= 4
    set_font(8.6, bold=True)
    c.setFillColor(ACCENT)
    c.drawString(MARGIN_X, y, title.upper())
    # Tracked letter-spacing via manual redraw isn't needed — keep simple
    y -= 3
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.line(MARGIN_X, y, MARGIN_X + CONTENT_W, y)
    return y - 9


def role_line(y, role, org_meta, date):
    """Role (bold, dark) left · date (muted) right · org/meta underneath."""
    set_font(9.4, bold=True)
    c.setFillColor(INK)
    c.drawString(MARGIN_X, y, role)
    if date:
        set_font(8.2)
        c.setFillColor(MUTED)
        c.drawRightString(MARGIN_X + CONTENT_W, y, date)
    y -= 11
    set_font(8.4)
    c.setFillColor(INK2)
    c.drawString(MARGIN_X, y, org_meta)
    return y - 10


def bullet(y, segments, indent=10, size=8.8, leading=11):
    """Bullet with accent mark + mixed bold/regular wrapped body."""
    set_font(size)
    c.setFillColor(ACCENT)
    c.drawString(MARGIN_X + 1, y, "\u2022")
    return inline(MARGIN_X + indent, y, segments, CONTENT_W - indent, size=size, leading=leading) - 2


def stack_line(y, stack):
    set_font(7.6, italic=True)
    c.setFillColor(MUTED)
    label = "Stack:"
    label_w = c.stringWidth(label + " ", FONT_I, 7.6)
    c.drawString(MARGIN_X + 10, y, label)
    set_font(7.6)
    c.drawString(MARGIN_X + 10 + label_w, y, stack)
    return y - 12


# ================== HEADER ==================
set_font(22, bold=True)
c.setFillColor(INK)
c.drawString(MARGIN_X, y, "Vamshi Yadav Golla")
set_font(9.4, bold=True)
c.setFillColor(ACCENT)
c.drawRightString(MARGIN_X + CONTENT_W, y + 3, "AI Agent Engineer & Automation Architect")
y -= 14

# Contact line (two logical groups separated by middots)
set_font(8.2)
c.setFillColor(INK2)
contact = ("London, UK  \u2022  Vamshiyadav2783@gmail.com  \u2022  +44 7887 132 409  \u2022  "
           "linkedin.com/in/vamshi-yadav869  \u2022  github.com/Vamshi-27072001  \u2022  "
           "vamshi-27072001.github.io/portfolio")
c.drawString(MARGIN_X, y, contact)
y -= 7
c.setStrokeColor(INK)
c.setLineWidth(1.3)
c.line(MARGIN_X, y, MARGIN_X + CONTENT_W, y)
y -= 10

# ================== SUMMARY ==================
y = section(y, "Summary")
y = inline(
    MARGIN_X, y,
    [
        ("AI Agent Engineer", True),
        (" specialising in autonomous AI systems on ", False),
        ("n8n, LangChain, and GPT-4o", True),
        (". Shipped ", False),
        ("3 production AI agents", True),
        (" delivering ", False),
        ("£36K+/year business impact", True),
        (", including a ", False),
        ("99.98% cost-reduction chatbot", True),
        (" and a zero-touch LinkedIn publishing pipeline. MSc Computer Science (UEL). Interviewing for UK AI Engineer / Automation / ML roles — Graduate Visa eligible.", False),
    ],
    CONTENT_W, size=9, leading=11.5
)
y -= 2

# ================== EXPERIENCE ==================
y = section(y, "Experience")
y = role_line(y, "Cyber Security Intern", "Lexnis Services Limited — Hertfordshire, UK", "Nov 2025 – Present")
for seg in [
    [("Analysed 10 UK vehicle tracking companies across 5 benchmarking criteria", True),
     (" and mapped 15+ product features per provider to produce a decision-ready competitive matrix.", False)],
    [("Identified a market gap supporting a £9,100/month operational model", True),
     (", feeding directly into the company's go-to-market strategy.", False)],
    [("Leveraged GPT-4 and Google tools", True),
     (" to produce research reports that informed 3 major business decisions at 4\u00D7 analysis throughput.", False)],
]:
    y = bullet(y, seg)
y -= 4

# ================== PROJECTS ==================
y = section(y, "Flagship Projects")

# ---- 1 ---- NSP
y = role_line(y, "NSP Cases — AI Email Enquiry Handler",
              "Autonomous customer-service pipeline  \u2022  Production",
              "Apr 2026")
for seg in [
    [("Engineered a 19-node n8n + LangChain workflow", True),
     (" that replaces a human customer-service agent — Gmail \u2192 7-tab knowledge base \u2192 HTML reply end-to-end in ", False),
     ("under 60 seconds, zero human intervention", True), (".", False)],
    [("Integrated GPT-4o Vision for multimodal enquiries", True),
     (" (text + product drawings/images) with a Supabase PostgreSQL audit trail for regulatory traceability.", False)],
]:
    y = bullet(y, seg)
y = stack_line(y, "n8n \u00B7 LangChain \u00B7 GPT-4.1-mini \u00B7 GPT-4o Vision \u00B7 Gmail OAuth2 \u00B7 Supabase PostgreSQL")

# ---- 2 ---- Restaurant
y = role_line(y, "Restaurant AI Agent — Taco Bell UK",
              "Zero-hallucination chatbot  \u2022  Production",
              "Apr 2026")
for seg in [
    [("Deployed an 11-node LangChain agent on Telegram (GPT-4o-mini)", True),
     (" serving 100+ menu items with full EU/UK allergen compliance, ", False),
     ("24/7 at sub-2-second latency", True), (".", False)],
    [("Drove operating costs from £12,000/year to £36/year (99.98% reduction)", True),
     (" via strict tool-first routing that guarantees zero hallucinations.", False)],
]:
    y = bullet(y, seg)
y = stack_line(y, "n8n \u00B7 LangChain \u00B7 GPT-4o-mini \u00B7 Telegram Bot \u00B7 Google Sheets / Docs \u00B7 PostgreSQL")

# ---- 3 ---- LinkedIn
y = role_line(y, "LinkedIn Post Manager — AI Content Engine",
              "Telegram-to-LinkedIn publishing  \u2022  Production",
              "Apr 2026")
for seg in [
    [("Built a 13-node autonomous Telegram-to-LinkedIn publishing engine", True),
     (" (GPT-4.1-mini + OpenAI Images API + LinkedIn ugcPosts) eliminating every human touchpoint.", False)],
    [("Cut content creation time 98% (25 min \u2192 30 sec)", True),
     (", saving ", False),
     ("£24,000/year in outsourced social costs", True),
     (" at £0.01 per post.", False)],
]:
    y = bullet(y, seg)
y = stack_line(y, "n8n \u00B7 LangChain \u00B7 GPT-4.1-mini \u00B7 OpenAI Images API \u00B7 LinkedIn REST \u00B7 OAuth2")

# ---- 4 ---- MSc Dissertation
y = role_line(y, "ML-Based GPS Spoofing Detection for Drone Delivery",
              "MSc Dissertation  \u2022  University of East London",
              "Jun – Sep 2025")
for seg in [
    [("Trained Random Forest & XGBoost classifiers to 99.95% / 99.90% accuracy", True),
     (" on 62,000+ telemetry records with a ", False),
     ("false-positive rate under 0.05%", True),
     (" — exceeding aviation safety thresholds.", False)],
    [("Deployed a real-time detection pipeline on Raspberry Pi", True),
     (" with autonomous countermeasures (hover, reroute, return-to-base); validated against simulated spoofing attacks.", False)],
]:
    y = bullet(y, seg)
y = stack_line(y, "Python \u00B7 Scikit-learn \u00B7 XGBoost \u00B7 Random Forest \u00B7 Pandas \u00B7 NumPy \u00B7 Raspberry Pi")
y -= 2

# ================== SKILLS ==================
y = section(y, "Technical Skills")
for label, val in [
    ("AI Agents",   "LangChain \u00B7 n8n \u00B7 Agent Architecture \u00B7 Prompt Engineering \u00B7 Tool-First Routing \u00B7 MCP"),
    ("LLMs & APIs", "GPT-4o \u00B7 GPT-4.1-mini \u00B7 Claude API \u00B7 OpenAI Vision / Images \u00B7 REST \u00B7 OAuth2"),
    ("Integrations","Telegram Bot \u00B7 LinkedIn REST \u00B7 Gmail \u00B7 Google Sheets / Docs \u00B7 Supabase"),
    ("ML & Data",   "Python \u00B7 Scikit-learn \u00B7 XGBoost \u00B7 Random Forest \u00B7 NLP \u00B7 PostgreSQL \u00B7 Power BI \u00B7 Tableau \u00B7 AWS \u00B7 GCP"),
]:
    set_font(8.6, bold=True)
    c.setFillColor(INK)
    lw = c.stringWidth(label + ":  ", FONT_B, 8.6)
    c.drawString(MARGIN_X, y, label + ":")
    set_font(8.6)
    c.setFillColor(INK2)
    c.drawString(MARGIN_X + lw, y, val)
    y -= 11.5
y -= 3

# ================== EDUCATION & CERTS ==================
y = section(y, "Education & Certifications")
set_font(9.4, bold=True)
c.setFillColor(INK)
c.drawString(MARGIN_X, y, "MSc Computer Science")
set_font(8.8)
c.setFillColor(INK2)
role_w = c.stringWidth("MSc Computer Science   ", FONT_B, 9.4)
c.drawString(MARGIN_X + role_w, y, "University of East London — London, UK")
y -= 11
set_font(8, italic=True)
c.setFillColor(MUTED)
c.drawString(MARGIN_X, y, "Focus: AI systems, automation, applied machine learning. Dissertation: ML-based GPS spoofing detection (99.95% accuracy).")
y -= 13

set_font(8.6, bold=True)
c.setFillColor(INK)
c.drawString(MARGIN_X, y, "Certifications:")
cert_x = MARGIN_X + c.stringWidth("Certifications:  ", FONT_B, 8.6)
set_font(8.6)
c.setFillColor(INK2)
c.drawString(cert_x, y, "AWS Academy Cloud Foundations  \u00B7  MATLAB Onramps (ML, Deep Learning, Image Processing)")

# ================== SAVE ==================
c.showPage()
c.save()
print(f"Saved: {OUT}  ({os.path.getsize(OUT)/1024:.1f} KB, 1 page)")
