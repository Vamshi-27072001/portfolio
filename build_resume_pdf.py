"""
Generate a 1-page PDF resume in the clean classic format from the reference.
Format: black/white, section headers in bold uppercase with horizontal rules,
role lines with right-aligned dates, indented bullets.
Run: python build_resume_pdf.py
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black
import os

OUT = "Vamshi_Yadav_Golla_Resume.pdf"

# ----- Simple palette: black + one subtle grey for rules -----
INK = black
GREY = HexColor("#000000")
RULE = HexColor("#000000")

# ----- Page -----
W, H = A4
LM = 15 * mm
RM = 15 * mm
TM = 14 * mm
BM = 12 * mm
CW = W - LM - RM

FONT = "Helvetica"
FONT_B = "Helvetica-Bold"
FONT_I = "Helvetica-Oblique"
FONT_BI = "Helvetica-BoldOblique"

c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("Vamshi Yadav Golla — Resume")
c.setAuthor("Vamshi Yadav Golla")
c.setSubject("AI Agent Engineer & Automation Architect")


def set_font(size, bold=False, italic=False):
    if bold and italic:
        c.setFont(FONT_BI, size)
    elif bold:
        c.setFont(FONT_B, size)
    elif italic:
        c.setFont(FONT_I, size)
    else:
        c.setFont(FONT, size)


def draw_wrapped(x, y, text, max_w, size=9.5, leading=11.5, bold=False, italic=False):
    set_font(size, bold, italic)
    c.setFillColor(INK)
    words = text.split()
    line = ""
    fn = FONT_B if bold else FONT_I if italic else FONT
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


def section_header(y, title):
    """Bold uppercase + full-width horizontal rule underneath."""
    y -= 4
    set_font(10, bold=True)
    c.setFillColor(INK)
    c.drawString(LM, y, title.upper())
    y -= 3
    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.line(LM, y, LM + CW, y)
    return y - 11


def role_header(y, left_bold, left_regular, date, left_italic_tail=""):
    """Role line: bold title + regular tail left; date right.
    If the italic tail would collide with the date, it wraps to line 2 in italic.
    """
    set_font(10, bold=True)
    c.setFillColor(INK)
    c.drawString(LM, y, left_bold)
    bw = c.stringWidth(left_bold, FONT_B, 10)
    # regular tail
    rw = 0
    if left_regular:
        set_font(10)
        c.drawString(LM + bw, y, left_regular)
        rw = c.stringWidth(left_regular, FONT, 10)
    # date right (always on first line)
    dw = 0
    if date:
        set_font(10)
        c.drawRightString(LM + CW, y, date)
        dw = c.stringWidth(date, FONT, 10)
    # italic parenthetical tail — inline if it fits, else next line
    if left_italic_tail:
        tail_text = " " + left_italic_tail
        set_font(10, italic=True)
        tail_w = c.stringWidth(tail_text, FONT_I, 10)
        first_line_used = bw + rw
        remaining = CW - first_line_used - dw - 8  # 8pt gap before date
        if tail_w <= remaining:
            c.drawString(LM + first_line_used, y, tail_text)
            return y - 12
        else:
            # wrap to second line
            y -= 12
            c.drawString(LM, y, left_italic_tail)
            return y - 11
    return y - 12


def bullet(y, text, indent=10, size=9.5, leading=11.5):
    """Indented bullet with a • mark."""
    set_font(size)
    c.setFillColor(INK)
    # bullet mark
    c.drawString(LM + 4, y, "\u2022")
    # body wrapped
    body_x = LM + indent + 6
    words = text.split()
    line = ""
    max_w = CW - (indent + 6)
    first = True
    for w in words:
        test = (line + " " + w).strip()
        if c.stringWidth(test, FONT, size) <= max_w:
            line = test
        else:
            c.drawString(body_x, y, line)
            y -= leading
            line = w
            first = False
    if line:
        c.drawString(body_x, y, line)
        y -= leading
    return y - 1


def skills_row(y, label, value, size=9.5, leading=12):
    """Label (bold): value — label sticks at top-left, value wraps."""
    set_font(size, bold=True)
    c.setFillColor(INK)
    c.drawString(LM, y, label + ":")
    lw = c.stringWidth(label + ":  ", FONT_B, size)
    set_font(size)
    words = value.split()
    line = ""
    max_w = CW - lw
    x = LM + lw
    first = True
    for w in words:
        test = (line + " " + w).strip()
        if c.stringWidth(test, FONT, size) <= max_w:
            line = test
        else:
            c.drawString(x, y, line)
            y -= leading
            line = w
            x = LM  # subsequent lines start at left margin
            max_w = CW
            first = False
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y


def cert_row(y, provider, detail, date):
    """Provider (bold): detail — date right-aligned."""
    set_font(9.5, bold=True)
    c.setFillColor(INK)
    c.drawString(LM, y, provider + ":")
    lw = c.stringWidth(provider + ":  ", FONT_B, 9.5)
    set_font(9.5)
    c.drawString(LM + lw, y, detail)
    set_font(9.5)
    c.drawRightString(LM + CW, y, date)
    return y - 12


# ================== HEADER ==================
y = H - TM

# Name — large, regular weight (not bold, matches reference)
set_font(22)
c.setFillColor(INK)
c.drawString(LM, y, "Vamshi Yadav Golla")
y -= 14

# Contact line — single line
set_font(8.8)
c.setFillColor(INK)
contact = ("London, UK  |  Phone: +44 7887 132 409  |  vamshiyadav2783@gmail.com  |  "
           "LinkedIn: linkedin.com/in/vamshi-yadav869  |  GitHub: github.com/Vamshi-27072001  |  "
           "Portfolio: vamshi-27072001.github.io/portfolio")
# If too long, shrink or wrap — check width
if c.stringWidth(contact, FONT, 8.8) > CW:
    # Render on two lines
    line1 = "London, UK  |  +44 7887 132 409  |  vamshiyadav2783@gmail.com  |  Portfolio: vamshi-27072001.github.io/portfolio"
    line2 = "LinkedIn: linkedin.com/in/vamshi-yadav869  |  GitHub: github.com/Vamshi-27072001"
    c.drawString(LM, y, line1)
    y -= 11
    c.drawString(LM, y, line2)
else:
    c.drawString(LM, y, contact)
y -= 6


# ================== SUMMARY ==================
y = section_header(y, "Summary")
y = draw_wrapped(
    LM, y,
    "AI Agent Engineer and MSc Computer Science graduate specialising in autonomous AI systems built on n8n, "
    "LangChain, and GPT-4o. Shipped three production AI agents delivering over £36,000/year in business impact, "
    "including a 99.98% cost-reduction customer-service chatbot and a zero-touch LinkedIn publishing pipeline. "
    "Dissertation delivered an ML-based GPS spoofing detection system at 99.95% accuracy. Seeking UK-based "
    "AI Engineer, Automation Engineer, or ML Engineer roles to apply technical depth and a delivery-focused "
    "mindset — Graduate Visa eligible.",
    CW, size=9.5, leading=12
)
y -= 2


# ================== EDUCATION ==================
y = section_header(y, "Education")
y = role_header(y,
                "MSc in Computer Science",
                " | University of East London | United Kingdom",
                "Oct 2024 – May 2026")
y = bullet(y,
           "Relevant Coursework: Software Engineering, Big Data Analytics, Artificial Intelligence and Machine Vision, Cloud Computing.")
y -= 2


# ================== TECHNICAL SKILLS ==================
y = section_header(y, "Technical Skills")
y = skills_row(y, "Programming & Tools",
               "Python (NumPy, Pandas, Matplotlib, Seaborn), SQL, Jupyter Notebook, Git / GitHub, VS Code, Linux, MATLAB")
y = skills_row(y, "AI Agents & LLMs",
               "LangChain, n8n, Prompt Engineering, Tool-First Routing, MCP, GPT-4o, GPT-4.1-mini, Claude API, OpenAI Vision / Images, OAuth2")
y = skills_row(y, "Machine Learning",
               "Scikit-learn, XGBoost, Random Forest, Logistic Regression, Neural Networks (CNN, RNN), NLP / TF-IDF, Feature Engineering, Time Series")
y = skills_row(y, "Data & Cloud",
               "PostgreSQL, Supabase, Google Sheets / Docs, Power BI, Tableau, AWS, Google Cloud, Telegram Bot API, LinkedIn REST API")
y -= 2


# ================== WORK EXPERIENCE ==================
y = section_header(y, "Work Experience")
y = role_header(y,
                "Cyber Security Intern",
                " | Lexnis Services Limited | Hertfordshire, UK",
                "Nov 2025 – Present")
for b in [
    "Analysed 10 UK vehicle tracking companies across 5 benchmarking criteria and mapped 15+ product features per provider, producing a decision-ready competitive matrix for leadership.",
    "Identified a gap in the UK security market supporting a £9,100/month operational model, feeding directly into the company's go-to-market strategy.",
    "Leveraged GPT-4 and Google tools to produce research reports that informed 3 major business decisions at 4\u00D7 analysis throughput.",
]:
    y = bullet(y, b)
y -= 2


# ================== PROJECTS ==================
y = section_header(y, "Projects")

# ---- 1: NSP ----
y = role_header(y,
                "NSP Cases – AI Email Enquiry Handler",
                "",
                "Apr 2026",
                left_italic_tail="(n8n + LangChain Agent, Production)")
for b in [
    "Engineered a 19-node n8n + LangChain workflow (GPT-4.1-mini) that replaces a human customer-service agent — Gmail to 7-tab knowledge base to HTML reply end-to-end in under 60 seconds, zero human intervention.",
    "Integrated GPT-4o Vision for multimodal enquiries (text + product drawings / images) with a Supabase PostgreSQL audit trail for regulatory traceability.",
]:
    y = bullet(y, b)

# ---- 2: Restaurant ----
y = role_header(y,
                "Restaurant AI Agent – Taco Bell UK",
                "",
                "Apr 2026",
                left_italic_tail="(LangChain Agent on Telegram, Production)")
for b in [
    "Deployed an 11-node LangChain agent on Telegram (GPT-4o-mini) serving 100+ menu items with full EU/UK allergen compliance, 24/7 at sub-2-second latency.",
    "Drove operating costs from £12,000/year to £36/year (99.98% reduction) via strict tool-first routing that guarantees zero hallucinations across menu, allergen, and nutrition queries.",
]:
    y = bullet(y, b)

# ---- 3: LinkedIn ----
y = role_header(y,
                "LinkedIn Post Manager – AI Content Engine",
                "",
                "Apr 2026",
                left_italic_tail="(Telegram-to-LinkedIn Automation)")
for b in [
    "Built a 13-node autonomous Telegram-to-LinkedIn publishing engine (GPT-4.1-mini + OpenAI Images API + LinkedIn ugcPosts API) eliminating every human touchpoint.",
    "Cut content creation time 98% (25 minutes to 30 seconds) and saved £24,000/year in outsourced social media costs at £0.01 per post.",
]:
    y = bullet(y, b)

# ---- 4: MSc Dissertation ----
y = role_header(y,
                "Machine Learning–Based GPS Spoofing Detection for Drone Delivery Systems",
                "",
                "Jun 2025 – Sep 2025",
                left_italic_tail="(MSc Dissertation)")
for b in [
    "Trained and optimised Random Forest and XGBoost classifiers to 99.95% and 99.90% accuracy on 62,000+ telemetry records, with false-positive rates under 0.05% — exceeding aviation safety thresholds.",
    "Deployed a Raspberry Pi-compatible real-time detection pipeline with autonomous countermeasures (hover, reroute, return-to-base) and validated against simulated spoofing attacks.",
]:
    y = bullet(y, b)
y -= 2


# ================== CERTIFICATIONS ==================
y = section_header(y, "Certifications")
y = cert_row(y, "AWS Academy", "Cloud Foundations", "March 2025")
y = cert_row(y, "MATLAB Onramps", "Machine Learning, Deep Learning (CNNs), Image Processing", "February 2025")


# ================== SAVE ==================
c.showPage()
c.save()
print(f"Saved: {OUT}  ({os.path.getsize(OUT)/1024:.1f} KB, 1 page)")
