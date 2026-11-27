import os
import re
from PIL import Image
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Set background color of a table cell."""
    tc_pr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    """Set cell padding (in dxa: 20 dxa = 1 pt)."""
    tc_pr = cell._element.get_or_add_tcPr()
    tc_mar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tc_pr.append(tc_mar)

def set_table_borders(table, color="CBD5E0", sz="4", val="single"):
    """Set elegant subtle borders for a table."""
    tbl_pr = table._element.xpath('w:tblPr')
    if tbl_pr:
        borders = parse_xml(f'''
            <w:tblBorders {nsdecls("w")}>
                <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:left w:val="none"/>
                <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:right w:val="none"/>
                <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:insideV w:val="none"/>
            </w:tblBorders>
        ''')
        tbl_pr[0].append(borders)

def parse_formatted_text_into_paragraph(paragraph, text, default_bold=False, default_italic=False, default_color=None, default_font_size=None):
    """
    Parses inline markdown formatting into formatted docx runs without modifying any text.
    """
    pattern = re.compile(
        r'(\*\*\*(.+?)\*\*\*|___(.+?)___|'
        r'\*\*(.+?)\*\*|__(.+?)__|'
        r'\*(.+?)\*|_(.+?)_|'
        r'`([^`]+)`|'
        r'\[([^\]]+)\]\(([^)]+)\))'
    )
    
    last_idx = 0
    for match in pattern.finditer(text):
        start, end = match.span()
        if start > last_idx:
            plain_part = text[last_idx:start]
            run = paragraph.add_run(plain_part)
            run.font.name = "Calibri"
            if default_bold: run.bold = True
            if default_italic: run.italic = True
            if default_color: run.font.color.rgb = default_color
            if default_font_size: run.font.size = default_font_size
            
        full_match = match.group(0)
        
        if full_match.startswith('***') or full_match.startswith('___'):
            content = match.group(2) or match.group(3)
            run = paragraph.add_run(content)
            run.font.name = "Calibri"
            run.bold = True
            run.italic = True
            if default_color: run.font.color.rgb = default_color
            if default_font_size: run.font.size = default_font_size
        elif full_match.startswith('**') or full_match.startswith('__'):
            content = match.group(4) or match.group(5)
            run = paragraph.add_run(content)
            run.font.name = "Calibri"
            run.bold = True
            if default_italic: run.italic = True
            if default_color: run.font.color.rgb = default_color
            if default_font_size: run.font.size = default_font_size
        elif full_match.startswith('*') or full_match.startswith('_'):
            content = match.group(6) or match.group(7)
            run = paragraph.add_run(content)
            run.font.name = "Calibri"
            run.italic = True
            if default_bold: run.bold = True
            if default_color: run.font.color.rgb = default_color
            if default_font_size: run.font.size = default_font_size
        elif full_match.startswith('`'):
            content = match.group(8)
            run = paragraph.add_run(content)
            run.font.name = "Consolas"
            run.font.size = Pt(9.0)
            run.font.color.rgb = RGBColor(0x99, 0x1B, 0x1B)
        elif full_match.startswith('['):
            link_text = match.group(9)
            run = paragraph.add_run(link_text)
            run.font.name = "Calibri"
            run.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)
            run.underline = True
            if default_font_size: run.font.size = default_font_size
            
        last_idx = end
        
    if last_idx < len(text):
        plain_part = text[last_idx:]
        run = paragraph.add_run(plain_part)
        run.font.name = "Calibri"
        if default_bold: run.bold = True
        if default_italic: run.italic = True
        if default_color: run.font.color.rgb = default_color
        if default_font_size: run.font.size = default_font_size

def convert_md_table_to_docx(doc, table_lines):
    """Converts markdown table lines into an academic Word table with smart column widths."""
    parsed_rows = []
    for line in table_lines:
        line_s = line.strip()
        if not line_s or re.match(r'^\|[\s:\-]+(\|[\s:\-]+)+\|$', line_s):
            continue
        cells = [c.strip() for c in line_s.strip('|').split('|')]
        parsed_rows.append(cells)
        
    if not parsed_rows:
        return
        
    num_rows = len(parsed_rows)
    num_cols = max(len(r) for r in parsed_rows)
    if num_cols == 0:
        return
        
    table = doc.add_table(rows=num_rows, cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    set_table_borders(table, color="CBD5E0", sz="4")
    
    # Custom widths for this 3-column table
    # Col 1 (Search Focus): 2.4 in, Col 2 (Records Found): 1.5 in, Col 3 (What It Represents): 2.4 in
    col_widths = [Inches(2.4), Inches(1.5), Inches(2.4)]
    
    for r_idx, row_data in enumerate(parsed_rows):
        row = table.rows[r_idx]
        tr_pr = row._element.get_or_add_trPr()
        tr_pr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        if r_idx == 0:
            tr_pr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
            
        is_hdr = (r_idx == 0)
        bg_color = "1B365D" if is_hdr else ("F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
        
        for c_idx in range(num_cols):
            cell = row.cells[c_idx]
            if c_idx < len(col_widths):
                cell.width = col_widths[c_idx]
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            
            val = row_data[c_idx] if c_idx < len(row_data) else ""
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.10
            
            if is_hdr:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.add_run(val)
                run.font.name = "Calibri"
                run.bold = True
                run.font.size = Pt(9.5)
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            else:
                if c_idx == 1:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                parse_formatted_text_into_paragraph(p, val, default_font_size=Pt(9.0), default_color=RGBColor(0x1F, 0x29, 0x37))
                
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)

def add_image_to_doc(doc, img_rel_path, base_dir):
    """Embeds an image into docx with proper dimension scaling and centering."""
    full_path = os.path.normpath(os.path.join(base_dir, img_rel_path))
    if not os.path.exists(full_path):
        print(f"Warning: image file not found: {full_path}")
        p = doc.add_paragraph()
        p.add_run(f"[Image File Not Found: {img_rel_path}]").bold = True
        return
        
    try:
        with Image.open(full_path) as img:
            w_px, h_px = img.size
            aspect = h_px / w_px
            
        max_w = 6.2  # Max width in inches
        max_h = 6.8  # Max height in inches
        
        target_w = max_w
        target_h = target_w * aspect
        if target_h > max_h:
            target_h = max_h
            target_w = target_h / aspect
            
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(10)
        p.paragraph_format.keep_with_next = False
        
        run = p.add_run()
        run.add_picture(full_path, width=Inches(target_w), height=Inches(target_h))
        
    except Exception as e:
        print(f"Error adding image {full_path}: {e}")
        p = doc.add_paragraph()
        p.add_run(f"[Error loading image: {img_rel_path} - {e}]").bold = True

def convert_report():
    report_md_path = r'c:\Users\rajch\Desktop\SEM 7\Dissertation\Data\BIBLIO\bibliometric_analysis_report.md'
    base_dir = os.path.dirname(report_md_path)
    out_docx_path = r'c:\Users\rajch\Desktop\SEM 7\Dissertation\Data\BIBLIO\bibliometric_analysis_report.docx'
    
    print(f"Reading markdown from: {report_md_path}")
    with open(report_md_path, 'r', encoding='utf-8') as f:
        text = f.read()
        
    doc = docx.Document()
    
    # Page setup
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        s.page_width = Inches(8.5)
        s.page_height = Inches(11.0)
        
        header = s.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Bibliometric Gap Analysis Report | Executive Summary")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(0x9C, 0xA3, 0xAF)
        
        footer = s.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Dissertation: Assessing Energy & Grid Sustainability of India's AI Data Center Expansion")
        frun.font.name = "Calibri"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(0x9C, 0xA3, 0xAF)

    # Map of suggested images to image paths
    # 1. overlapping circles -> four_themes_intersection.png
    # 2. bar chart of six record counts -> bibliometric_gap_analysis_85_0.png
    # 3. density map (Section 2.9) -> bibliometric_gap_analysis_101_0.png
    # 4. keyword network graph (Section 2.10) -> bibliometric_gap_analysis_103_0.png
    # 5. cumulative growth chart (Section 2.12) -> bibliometric_gap_analysis_107_0.png
    # 6. radar/maturity comparison chart (Section 2.13) -> bibliometric_gap_analysis_109_0.png
    
    lines = text.splitlines()
    n = len(lines)
    i = 0
    
    while i < n:
        line = lines[i]
        stripped = line.strip()
        
        if not stripped:
            i += 1
            continue
            
        # Heading 1
        if stripped.startswith('# '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(stripped[2:].strip())
            run.font.name = "Calibri"
            run.font.size = Pt(20)
            run.bold = True
            run.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
            i += 1
            continue
            
        # Heading 2
        if stripped.startswith('## '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(14)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(stripped[3:].strip())
            run.font.name = "Calibri"
            run.font.size = Pt(13)
            run.bold = True
            run.italic = True
            run.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)
            i += 1
            continue
            
        # Heading 3
        if stripped.startswith('### '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(5)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(stripped[4:].strip())
            run.font.name = "Calibri"
            run.font.size = Pt(12)
            run.bold = True
            run.font.color.rgb = RGBColor(0x2C, 0x52, 0x82)
            i += 1
            continue
            
        # Markdown Table
        if stripped.startswith('|') and stripped.endswith('|'):
            table_lines = [line]
            i += 1
            while i < n and lines[i].strip().startswith('|') and lines[i].strip().endswith('|'):
                table_lines.append(lines[i])
                i += 1
            convert_md_table_to_docx(doc, table_lines)
            continue
            
        # Bullet list items
        if stripped.startswith('- ') or stripped.startswith('* '):
            item_text = stripped[2:].strip()
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.left_indent = Inches(0.25)
            parse_formatted_text_into_paragraph(p, item_text, default_color=RGBColor(0x22, 0x22, 0x22), default_font_size=Pt(10.5))
            i += 1
            continue
            
        # Check for suggested image placeholders
        # We keep the placeholder text EXACTLY as written, and then insert the image directly below it!
        is_suggested_img = False
        img_to_add = None
        
        if 'overlapping circles' in stripped:
            img_to_add = 'bibliometric_gap_analysis_files/four_themes_intersection.png'
            is_suggested_img = True
        elif 'bar chart of these six record counts' in stripped:
            img_to_add = 'bibliometric_gap_analysis_files/bibliometric_gap_analysis_85_0.png'
            is_suggested_img = True
        elif 'density map from this step' in stripped or 'Section 2.9' in stripped:
            img_to_add = 'bibliometric_gap_analysis_files/bibliometric_gap_analysis_101_0.png'
            is_suggested_img = True
        elif 'keyword network graph' in stripped or 'Section 2.10' in stripped:
            img_to_add = 'bibliometric_gap_analysis_files/bibliometric_gap_analysis_103_0.png'
            is_suggested_img = True
        elif 'cumulative growth chart' in stripped or 'Section 2.12' in stripped:
            img_to_add = 'bibliometric_gap_analysis_files/bibliometric_gap_analysis_107_0.png'
            is_suggested_img = True
        elif 'radar/maturity comparison chart' in stripped or 'Section 2.13' in stripped:
            img_to_add = 'bibliometric_gap_analysis_files/bibliometric_gap_analysis_109_0.png'
            is_suggested_img = True
            
        # Regular paragraph (including placeholder text)
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.15
        
        parse_formatted_text_into_paragraph(p, stripped, default_color=RGBColor(0x22, 0x22, 0x22), default_font_size=Pt(10.5))
        
        # If this paragraph was a suggested image prompt, insert the corresponding image right below!
        if is_suggested_img and img_to_add:
            add_image_to_doc(doc, img_to_add, base_dir)
            
        i += 1
        
    print(f"Saving report docx to: {out_docx_path}")
    doc.save(out_docx_path)
    file_size = os.path.getsize(out_docx_path)
    print(f"Successfully generated {out_docx_path} ({file_size:,} bytes)!")

if __name__ == "__main__":
    convert_report()
