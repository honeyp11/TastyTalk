import re
from datetime import datetime
from typing import List, Dict
from fpdf import FPDF

def sanitize_latin1(text: str) -> str:
    """
    Sanitizes unicode / emojis for standard FPDF Latin-1 font compatibility.
    """
    if not text:
        return ""
    replacements = {
        '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"',
        '\u2013': '-', '\u2014': '-',
        '\u2022': '*', '\u2026': '...',
        '\u00a0': ' ', '\u200b': '',
        '🥑': '[Nutri]', '🥗': '[Diet]', '👤': '[User]',
        '🎯': '[Goal]', '🔥': '[Cal]', '📋': '[Plan]',
        '⚖️': '[Macro]', '🍳': '[Cook]', '💡': '[Tip]',
        '🍽️': '[Meal]', '📊': '[Stats]', '🛒': '[Grocery]',
        '⏱️': '[Time]', '💊': '[Health]', '⚡': '[Energy]'
    }
    for orig, rep in replacements.items():
        text = text.replace(orig, rep)
    return text.encode('latin-1', 'replace').decode('latin-1')

def render_markdown_section_to_pdf(pdf: FPDF, markdown_text: str):
    """
    Parses and renders Markdown text into beautifully structured PDF elements:
    headings, tables, bullet points, and clean paragraphs.
    """
    lines = markdown_text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            pdf.ln(2)
            i += 1
            continue

        # Check for Markdown Table (| Col 1 | Col 2 |)
        if line.startswith('|') and line.endswith('|') and '|' in line[1:-1]:
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|') and lines[i].strip().endswith('|'):
                t_row = lines[i].strip()
                # Skip separator row (| --- | --- |)
                if not re.match(r'^\|[\s\-:|]+\|$', t_row):
                    cols = [c.strip() for c in t_row.split('|')[1:-1]]
                    table_lines.append(cols)
                i += 1
            
            if table_lines:
                pdf.ln(2)
                num_cols = max(len(row) for row in table_lines)
                if num_cols > 0:
                    avail_width = 180
                    col_width = avail_width / num_cols
                    
                    # Table Header row
                    pdf.set_font('Helvetica', 'B', 8.5)
                    pdf.set_fill_color(225, 245, 235) # Soft Mint
                    pdf.set_text_color(5, 120, 80)
                    pdf.set_draw_color(180, 220, 200)
                    for col in table_lines[0]:
                        pdf.cell(col_width, 6.5, sanitize_latin1(col[:30]), border=1, fill=True, align='C')
                    pdf.ln()

                    # Table Data rows
                    pdf.set_font('Helvetica', size=8)
                    pdf.set_text_color(40, 40, 40)
                    fill = False
                    for row in table_lines[1:]:
                        pdf.set_fill_color(248, 252, 250) if fill else pdf.set_fill_color(255, 255, 255)
                        for c_idx in range(num_cols):
                            val = row[c_idx] if c_idx < len(row) else ""
                            pdf.cell(col_width, 5.5, sanitize_latin1(val[:35]), border=1, fill=fill)
                        pdf.ln()
                        fill = not fill
                pdf.ln(3)
            continue

        # Check for Headings
        if line.startswith('### '):
            pdf.ln(3)
            pdf.set_font('Helvetica', 'B', 10.5)
            pdf.set_text_color(5, 150, 105) # Emerald Green
            clean_head = re.sub(r'[*#]', '', line).strip()
            pdf.cell(0, 6, sanitize_latin1(clean_head), new_x='LMARGIN', new_y='NEXT')
            pdf.ln(1)
            i += 1
            continue
        elif line.startswith('## '):
            pdf.ln(4)
            pdf.set_font('Helvetica', 'B', 11.5)
            pdf.set_text_color(16, 185, 129)
            clean_head = re.sub(r'[*#]', '', line).strip()
            pdf.cell(0, 7, sanitize_latin1(clean_head), new_x='LMARGIN', new_y='NEXT')
            pdf.ln(1)
            i += 1
            continue

        # Check for Bullet Points (* or - or •)
        if line.startswith('* ') or line.startswith('- ') or line.startswith('• '):
            bullet_body = line[2:].strip()
            clean_body = re.sub(r'\*\*(.*?)\*\*', r'\1', bullet_body)
            pdf.set_font('Helvetica', 'B', 9)
            pdf.set_text_color(16, 185, 129)
            pdf.cell(5, 5, '-', new_x='RIGHT')
            pdf.set_font('Helvetica', size=9)
            pdf.set_text_color(40, 40, 40)
            pdf.multi_cell(0, 5, sanitize_latin1(clean_body))
            pdf.ln(1)
            i += 1
            continue

        # Normal Paragraph Line
        clean_text = re.sub(r'\*\*(.*?)\*\*', r'\1', line)
        pdf.set_font('Helvetica', size=9)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 5, sanitize_latin1(clean_text))
        pdf.ln(1)
        i += 1

def export_session_as_pdf(
    messages: List[Dict],
    goal: str = "",
    preference: str = "",
    calorie_target: int = 2000
) -> bytes:
    """
    Generates a beautifully formatted, magazine-grade PDF nutrition report with
    structured tables, styled message cards, and proper typography.
    """
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    class TastyTalkPDF(FPDF):
        def header(self):
            # Emerald Banner Header
            self.set_fill_color(16, 185, 129)
            self.rect(0, 0, 210, 12, 'F')
            self.set_y(2)
            self.set_font('Helvetica', 'B', 9)
            self.set_text_color(255, 255, 255)
            self.cell(0, 8, 'TASTYTALK - PERSONALIZED NUTRITION ARCHITECTURE & DIET REPORT', align='C')
            self.ln(12)
            
        def footer(self):
            self.set_y(-14)
            self.set_font('Helvetica', 'I', 8)
            self.set_text_color(140, 140, 140)
            self.cell(0, 10, f'Page {self.page_no()} | Engineered by TastyTalk AI Nutritionist', align='C')

    pdf = TastyTalkPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=16)

    # 1. Title Area
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 9, 'Personalized Dietary & Consultation Record', new_x='LMARGIN', new_y='NEXT')

    pdf.set_font('Helvetica', size=9.5)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 5, f'Generated on: {now_str}  |  Official TastyTalk Clinical Summary', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(4)

    # 2. Structured Metadata Grid Box
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(226, 232, 240)
    pdf.rect(10, pdf.get_y(), 190, 18, 'DF')
    start_y = pdf.get_y() + 2

    # Column 1: Health Goal
    pdf.set_xy(14, start_y)
    pdf.set_font('Helvetica', 'B', 7.5)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(55, 4, 'PRIMARY HEALTH GOAL', new_x='LMARGIN', new_y='NEXT')
    pdf.set_x(14)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(16, 185, 129)
    pdf.cell(55, 6, sanitize_latin1(goal or 'Healthy Living'), new_x='LMARGIN', new_y='NEXT')

    # Column 2: Dietary Preference
    pdf.set_xy(75, start_y)
    pdf.set_font('Helvetica', 'B', 7.5)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(55, 4, 'DIET PREFERENCE', new_x='LMARGIN', new_y='NEXT')
    pdf.set_x(75)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(55, 6, sanitize_latin1(preference or 'Standard'), new_x='LMARGIN', new_y='NEXT')

    # Column 3: Calorie Budget
    pdf.set_xy(138, start_y)
    pdf.set_font('Helvetica', 'B', 7.5)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(55, 4, 'DAILY CALORIE BUDGET', new_x='LMARGIN', new_y='NEXT')
    pdf.set_x(138)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(217, 119, 6)
    pdf.cell(55, 6, f"{calorie_target} kcal / day", new_x='LMARGIN', new_y='NEXT')

    pdf.set_y(start_y + 18)
    pdf.ln(6)

    # 3. Render Messages in Clean Structured Cards
    if not messages:
        pdf.set_font('Helvetica', 'I', 10)
        pdf.set_text_color(120, 120, 120)
        pdf.cell(0, 10, 'No consultation messages recorded in this session.', align='C')
    else:
        for turn_idx, msg in enumerate(messages, 1):
            is_user = (msg["role"] == "user")
            content = msg.get("content", "").strip()

            if is_user:
                # User Query Pill Box
                pdf.set_fill_color(241, 245, 249)
                pdf.set_draw_color(203, 213, 225)
                pdf.set_font('Helvetica', 'B', 9)
                pdf.set_text_color(30, 41, 59)
                pdf.cell(0, 6.5, sanitize_latin1(f"  [QUESTION #{turn_idx}] USER INQUIRY"), border=1, fill=True, new_x='LMARGIN', new_y='NEXT')
                pdf.set_font('Helvetica', size=9.5)
                pdf.set_text_color(51, 65, 85)
                clean_q = re.sub(r'[*#]', '', content)
                pdf.ln(1)
                pdf.multi_cell(0, 5, sanitize_latin1(clean_q))
                pdf.ln(4)
            else:
                # TastyTalk Recommendation Header
                pdf.set_fill_color(236, 253, 245)
                pdf.set_draw_color(167, 243, 208)
                pdf.set_font('Helvetica', 'B', 9.5)
                pdf.set_text_color(5, 150, 105)
                pdf.cell(0, 7, sanitize_latin1("  [GUIDANCE] TASTYTALK NUTRITION & RECIPE ARCHITECTURE"), border=1, fill=True, new_x='LMARGIN', new_y='NEXT')
                pdf.ln(2)

                # Render Structured Markdown (Headings, Tables, Lists)
                render_markdown_section_to_pdf(pdf, content)

                # Section End Divider
                pdf.set_draw_color(226, 232, 240)
                pdf.set_line_width(0.3)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(6)

    return bytes(pdf.output())

def export_session_as_markdown(
    messages: List[Dict],
    goal: str = "",
    preference: str = "",
    calorie_target: int = 2000
) -> str:
    """
    Generates a structured, clean GitHub-flavored Markdown report.
    """
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    md = "# 🥑 TastyTalk — Personalized Nutrition & Consultation Report\n\n"
    md += f"> **Generated:** {now_str}  \n"
    md += f"> **Health Goal:** {goal or 'Healthy Living'} | **Diet:** {preference or 'Standard'} | **Daily Budget:** {calorie_target} kcal  \n\n"
    md += "---\n\n"
    
    if not messages:
        md += "_No consultation messages recorded in this session._\n"
        return md
        
    for i, msg in enumerate(messages, 1):
        if msg["role"] == "user":
            md += f"## 👤 User Consultation (#{i})\n\n"
            md += f"{msg['content'].strip()}\n\n"
        else:
            md += f"## 🥑 TastyTalk Guidance\n\n"
            md += f"{msg['content'].strip()}\n\n"
        md += "---\n\n"
        
    return md

def export_session_as_text(
    messages: List[Dict],
    goal: str = "",
    preference: str = "",
    calorie_target: int = 2000
) -> str:
    """
    Generates an executive ASCII formatted Plaintext (.txt) consultation report.
    """
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    sep = "=" * 74
    sub_sep = "-" * 74
    
    lines = [
        sep,
        "          TASTYTALK — PERSONALIZED NUTRITION ARCHITECTURE REPORT",
        sep,
        f"Generated: {now_str}",
        f"Goal: {goal or 'General Health'}  |  Diet: {preference or 'Standard'}  |  Target: {calorie_target} kcal",
        sep,
        ""
    ]
    
    if not messages:
        lines.append("No consultation messages recorded in this session.")
    else:
        for idx, msg in enumerate(messages, 1):
            if msg["role"] == "user":
                lines.append(f"[QUERY #{idx}] USER INQUIRY:")
                lines.append(sub_sep)
                clean_q = re.sub(r'[*#]', '', msg["content"].strip())
                lines.append(clean_q)
            else:
                lines.append(f"[GUIDANCE #{idx}] TASTYTALK NUTRITION & RECIPE ARCHITECTURE:")
                lines.append(sub_sep)
                clean_ans = re.sub(r'\*\*(.*?)\*\*', r'\1', msg["content"].strip())
                lines.append(clean_ans)
            lines.append("")
            lines.append(sep)
            lines.append("")
            
    return "\n".join(lines)
