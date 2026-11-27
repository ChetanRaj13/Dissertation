import os
import re
from PIL import Image
from bs4 import BeautifulSoup
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

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
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

def add_callout_box(doc, text, title=""):
    """Adds a stylish callout box for quotes or important takeaways."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.3)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=160)
    
    tc_pr = cell._element.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="1B365D"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''')
    tc_pr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    
    if title:
        run_t = p.add_run(title + "\n")
        run_t.bold = True
        run_t.font.name = "Calibri"
        run_t.font.size = Pt(10.5)
        run_t.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        
    parse_formatted_text_into_paragraph(p, text, default_italic=True, default_color=RGBColor(0x2D, 0x37, 0x48))
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)

def add_code_block(doc, code_str, lang="python"):
    """Adds a formatted code block in a shaded single-cell container."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.3)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=140)
    
    tc_pr = cell._element.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
            <w:left w:val="single" w:sz="18" w:space="0" w:color="3B82F6"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
        </w:tcBorders>
    ''')
    tc_pr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    
    lines = code_str.splitlines()
    for idx, line in enumerate(lines):
        run = p.add_run(line + ("\n" if idx < len(lines) - 1 else ""))
        run.font.name = "Consolas"
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
        
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(3)

def add_output_block(doc, output_str):
    """Adds a formatted notebook output block."""
    if not output_str.strip():
        return
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.3)
    set_cell_background(cell, "FAFAFA")
    set_cell_margins(cell, top=100, bottom=100, left=160, right=140)
    
    tc_pr = cell._element.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="E5E7EB"/>
            <w:left w:val="single" w:sz="12" w:space="0" w:color="9CA3AF"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="E5E7EB"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="E5E7EB"/>
        </w:tcBorders>
    ''')
    tc_pr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.line_spacing = 1.05
    
    lines = output_str.splitlines()
    for idx, line in enumerate(lines):
        run = p.add_run(line + ("\n" if idx < len(lines) - 1 else ""))
        run.font.name = "Consolas"
        run.font.size = Pt(8.0)
        run.font.color.rgb = RGBColor(0x4B, 0x55, 0x63)
        
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(3)

def parse_formatted_text_into_paragraph(paragraph, text, default_bold=False, default_italic=False, default_color=None, default_font_size=None):
    """
    Parses inline markdown like **bold**, *italic**, `code`, [links](url), and equations
    into formatted docx runs.
    """
    pattern = re.compile(
        r'(\*\*\*(.+?)\*\*\*|___(.+?)___|'
        r'\*\*(.+?)\*\*|__(.+?)__|'
        r'\*(.+?)\*|_(.+?)_|'
        r'`([^`]+)`|'
        r'\$([^$]+)\$|'
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
        elif full_match.startswith('$'):
            # Math notation like $N=33$
            content = match.group(9)
            run = paragraph.add_run(content)
            run.font.name = "Calibri"
            run.italic = True
            if default_color: run.font.color.rgb = default_color
            if default_font_size: run.font.size = default_font_size
        elif full_match.startswith('['):
            link_text = match.group(10)
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

def calculate_smart_col_widths(matrix, total_width_inches=6.3):
    """Computes intelligent proportional column widths for tables."""
    num_cols = max(len(r) for r in matrix)
    if num_cols == 0:
        return []
        
    # Calculate max text length per column
    max_lens = [0] * num_cols
    for row in matrix:
        for c_idx in range(num_cols):
            val = row[c_idx] if c_idx < len(row) else ""
            max_lens[c_idx] = max(max_lens[c_idx], len(str(val)))
            
    # Check if col 0 is index column (short numbers / empty header)
    weights = []
    for c_idx in range(num_cols):
        l = max(max_lens[c_idx], 3)
        if c_idx == 0 and (matrix[0][0] == "" or matrix[0][0] == "#" or max_lens[0] <= 4):
            weights.append(1.0) # Fixed small weight for index col
        else:
            # Sqrt scale helps balance very wide text columns vs short columns
            weights.append(max(2.0, (l ** 0.65)))
            
    total_weight = sum(weights)
    widths = [Inches(total_width_inches * (w / total_weight)) for w in weights]
    return widths

def convert_html_table_to_docx(doc, html_str):
    """Converts an HTML table into a styled Word table."""
    soup = BeautifulSoup(html_str, 'html.parser')
    table_tag = soup.find('table')
    if not table_tag:
        return
        
    rows = table_tag.find_all('tr')
    if not rows:
        return
        
    matrix = []
    is_header_row = []
    
    for tr in rows:
        cells = tr.find_all(['th', 'td'])
        row_data = [c.get_text().strip() for c in cells]
        matrix.append(row_data)
        is_header = len(tr.find_all('th')) > len(tr.find_all('td'))
        is_header_row.append(is_header)
        
    if not matrix:
        return
        
    num_rows = len(matrix)
    num_cols = max(len(r) for r in matrix)
    if num_cols == 0:
        return
        
    table = doc.add_table(rows=num_rows, cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    set_table_borders(table, color="CBD5E0", sz="4")
    col_widths = calculate_smart_col_widths(matrix, total_width_inches=6.3)
    
    for r_idx, row_data in enumerate(matrix):
        row = table.rows[r_idx]
        tr_pr = row._element.get_or_add_trPr()
        tr_pr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        if r_idx == 0 or is_header_row[r_idx]:
            tr_pr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
            
        is_hdr = (r_idx == 0) or is_header_row[r_idx]
        bg_color = "1B365D" if is_hdr else ("F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
        
        for c_idx in range(num_cols):
            cell = row.cells[c_idx]
            if c_idx < len(col_widths):
                cell.width = col_widths[c_idx]
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            
            val = row_data[c_idx] if c_idx < len(row_data) else ""
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.05
            
            if is_hdr:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.add_run(val)
                run.font.name = "Calibri"
                run.bold = True
                run.font.size = Pt(9.0)
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            else:
                if c_idx == 0 and (matrix[0][0] == "" or val.isdigit()):
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.add_run(val)
                run.font.name = "Calibri"
                run.font.size = Pt(8.5)
                run.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)
                
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)

def convert_md_table_to_docx(doc, table_lines):
    """Converts markdown table lines into a styled Word table."""
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
    col_widths = calculate_smart_col_widths(parsed_rows, total_width_inches=6.3)
    
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
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            
            val = row_data[c_idx] if c_idx < len(row_data) else ""
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.05
            
            if is_hdr:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.add_run(val)
                run.font.name = "Calibri"
                run.bold = True
                run.font.size = Pt(9.0)
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            else:
                parse_formatted_text_into_paragraph(p, val, default_font_size=Pt(8.5), default_color=RGBColor(0x1F, 0x29, 0x37))
                
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)

def add_image_to_doc(doc, img_rel_path, base_dir, alt_text=""):
    """Embeds an image into docx with proper dimension scaling and centering."""
    full_path = os.path.normpath(os.path.join(base_dir, img_rel_path))
    if not os.path.exists(full_path):
        print(f"Warning: image file not found: {full_path}")
        p = doc.add_paragraph()
        p.add_run(f"[Missing Image: {img_rel_path}]").bold = True
        return
        
    try:
        with Image.open(full_path) as img:
            w_px, h_px = img.size
            aspect = h_px / w_px
            
        max_w = 6.2  # Max width in inches
        max_h = 7.0  # Max height in inches
        
        target_w = max_w
        target_h = target_w * aspect
        if target_h > max_h:
            target_h = max_h
            target_w = target_h / aspect
            
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = False
        
        run = p.add_run()
        run.add_picture(full_path, width=Inches(target_w), height=Inches(target_h))
        
    except Exception as e:
        print(f"Error adding image {full_path}: {e}")
        p = doc.add_paragraph()
        p.add_run(f"[Error loading image: {img_rel_path} - {e}]").bold = True

def main():
    md_path = r'c:\Users\rajch\Desktop\SEM 7\Dissertation\Data\BIBLIO\bibliometric_gap_analysis.md'
    base_dir = os.path.dirname(md_path)
    out_docx_path = r'c:\Users\rajch\Desktop\SEM 7\Dissertation\Data\BIBLIO\bibliometric_gap_analysis.docx'
    
    print(f"Reading markdown from: {md_path}")
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()
        
    doc = docx.Document()
    
    # Page setup - Margins 1 inch, standard Letter / A4
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
        hrun = hp.add_run("Bibliometric Gap Analysis | Dissertation")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(0x9C, 0xA3, 0xAF)
        
        footer = s.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("India AI Data Center Grid Sustainability Assessment")
        frun.font.name = "Calibri"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(0x9C, 0xA3, 0xAF)
        
    lines = text.splitlines()
    n = len(lines)
    i = 0
    blocks = []
    
    while i < n:
        line = lines[i]
        stripped = line.strip()
        
        if not stripped:
            i += 1
            continue
            
        if stripped.startswith('```'):
            lang = stripped[3:].strip()
            code_lines = []
            i += 1
            while i < n and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            if i < n and lines[i].strip().startswith('```'):
                i += 1
            blocks.append(('code', lang, '\n'.join(code_lines)))
            continue
            
        if stripped.startswith('<div') or stripped.startswith('<table'):
            html_lines = [line]
            i += 1
            while i < n:
                html_lines.append(lines[i])
                if '</table>' in lines[i] or '</div>' in lines[i]:
                    full_html = '\n'.join(html_lines)
                    if full_html.count('<table') <= full_html.count('</table>') and full_html.count('<div') <= full_html.count('</div>'):
                        i += 1
                        break
                i += 1
            blocks.append(('html', '\n'.join(html_lines)))
            continue
            
        if stripped.startswith('![') and '](' in stripped and stripped.endswith(')'):
            m = re.match(r'!\[(.*?)\]\((.*?)\)', stripped)
            if m:
                blocks.append(('image', m.group(1), m.group(2)))
            else:
                blocks.append(('p', stripped))
            i += 1
            continue
            
        if stripped.startswith('#'):
            m = re.match(r'^(#+)\s*(.*)$', stripped)
            if m:
                blocks.append(('heading', len(m.group(1)), m.group(2)))
            else:
                blocks.append(('p', stripped))
            i += 1
            continue
            
        if stripped in ('---', '***', '___'):
            blocks.append(('hr', ''))
            i += 1
            continue
            
        if stripped.startswith('|') and stripped.endswith('|'):
            table_lines = [line]
            i += 1
            while i < n and lines[i].strip().startswith('|') and lines[i].strip().endswith('|'):
                table_lines.append(lines[i])
                i += 1
            blocks.append(('md_table', table_lines))
            continue
            
        if re.match(r'^\s*[-*+]\s+', line):
            indent = len(line) - len(line.lstrip())
            blocks.append(('ul', indent, re.sub(r'^\s*[-*+]\s+', '', line)))
            i += 1
            continue
            
        if re.match(r'^\s*\d+\.\s+', line):
            indent = len(line) - len(line.lstrip())
            blocks.append(('ol', indent, re.sub(r'^\s*\d+\.\s+', '', line)))
            i += 1
            continue
            
        if stripped.startswith('>'):
            quote_lines = [re.sub(r'^>\s*', '', stripped)]
            i += 1
            while i < n and lines[i].strip().startswith('>'):
                quote_lines.append(re.sub(r'^>\s*', '', lines[i].strip()))
                i += 1
            blocks.append(('quote', '\n'.join(quote_lines)))
            continue
            
        if line.startswith('    ') and not line.strip().startswith(('1.', '2.', '3.', '-', '*')):
            out_lines = [line[4:]]
            i += 1
            while i < n and (lines[i].startswith('    ') or not lines[i].strip()):
                if lines[i].strip():
                    out_lines.append(lines[i][4:] if lines[i].startswith('    ') else lines[i])
                else:
                    out_lines.append('')
                i += 1
            blocks.append(('output', '\n'.join(out_lines).strip('\n')))
            continue
            
        # Standard paragraph
        p_lines = [line]
        i += 1
        while i < n and lines[i].strip() and not lines[i].strip().startswith(('```', '<div', '<table', '#', '---', '***', '![', '|', '>', '- ', '* ', '+ ')) and not re.match(r'^\s*\d+\.\s+', lines[i]) and not lines[i].startswith('    '):
            p_lines.append(lines[i])
            i += 1
        blocks.append(('p', '\n'.join(p_lines)))
        
    print(f"Total parsed blocks: {len(blocks)}. Building Word Document...")
    
    for b_idx, block in enumerate(blocks):
        b_type = block[0]
        
        if b_type == 'heading':
            level, h_text = block[1], block[2]
            p = doc.add_paragraph()
            p.paragraph_format.keep_with_next = True
            
            if level == 1:
                p.paragraph_format.space_before = Pt(20)
                p.paragraph_format.space_after = Pt(6)
                run = p.add_run(h_text)
                run.font.name = "Calibri"
                run.font.size = Pt(18)
                run.bold = True
                run.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
            elif level == 2:
                p.paragraph_format.space_before = Pt(15)
                p.paragraph_format.space_after = Pt(4)
                run = p.add_run(h_text)
                run.font.name = "Calibri"
                run.font.size = Pt(13.5)
                run.bold = True
                run.font.color.rgb = RGBColor(0x2C, 0x52, 0x82)
            elif level == 3:
                p.paragraph_format.space_before = Pt(11)
                p.paragraph_format.space_after = Pt(3)
                run = p.add_run(h_text)
                run.font.name = "Calibri"
                run.font.size = Pt(11.5)
                run.bold = True
                run.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)
            else:
                p.paragraph_format.space_before = Pt(8)
                p.paragraph_format.space_after = Pt(2)
                run = p.add_run(h_text)
                run.font.name = "Calibri"
                run.font.size = Pt(10.5)
                run.bold = True
                run.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)
                
        elif b_type == 'p':
            p_text = block[1]
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15
            parse_formatted_text_into_paragraph(p, p_text, default_color=RGBColor(0x22, 0x22, 0x22), default_font_size=Pt(10.0))
            
        elif b_type == 'ul':
            indent, item_text = block[1], block[2]
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            if indent >= 4:
                p.paragraph_format.left_indent = Inches(0.5)
            else:
                p.paragraph_format.left_indent = Inches(0.25)
            parse_formatted_text_into_paragraph(p, item_text, default_color=RGBColor(0x22, 0x22, 0x22), default_font_size=Pt(10.0))
            
        elif b_type == 'ol':
            indent, item_text = block[1], block[2]
            p = doc.add_paragraph(style='List Number')
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            if indent >= 4:
                p.paragraph_format.left_indent = Inches(0.5)
            else:
                p.paragraph_format.left_indent = Inches(0.25)
            parse_formatted_text_into_paragraph(p, item_text, default_color=RGBColor(0x22, 0x22, 0x22), default_font_size=Pt(10.0))
            
        elif b_type == 'code':
            lang, code_str = block[1], block[2]
            add_code_block(doc, code_str, lang=lang)
            
        elif b_type == 'output':
            out_str = block[1]
            add_output_block(doc, out_str)
            
        elif b_type == 'html':
            html_str = block[1]
            convert_html_table_to_docx(doc, html_str)
            
        elif b_type == 'md_table':
            table_lines = block[1]
            convert_md_table_to_docx(doc, table_lines)
            
        elif b_type == 'image':
            alt_text, img_rel_path = block[1], block[2]
            add_image_to_doc(doc, img_rel_path, base_dir, alt_text=alt_text)
            
        elif b_type == 'quote':
            q_text = block[1]
            add_callout_box(doc, q_text)
            
        elif b_type == 'hr':
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
            pBdr = parse_xml(f'''
                <w:pBdr {nsdecls("w")}>
                    <w:bottom w:val="single" w:sz="6" w:space="1" w:color="CBD5E0"/>
                </w:pBdr>
            ''')
            p._p.get_or_add_pPr().append(pBdr)
            
    print(f"Saving document to: {out_docx_path}")
    doc.save(out_docx_path)
    file_size = os.path.getsize(out_docx_path)
    print(f"Successfully generated {out_docx_path} ({file_size:,} bytes)!")

if __name__ == "__main__":
    main()
