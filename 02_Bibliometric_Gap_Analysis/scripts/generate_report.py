import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_report():
    doc = Document()

    # Configure Margins (A4 standard: 1 inch / 25.4mm)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)

    # Color Palette Constants
    COLOR_NAVY = RGBColor(26, 54, 93)      # #1A365D - Title / Primary Heading
    COLOR_SLATE = RGBColor(43, 108, 176)   # #2B6CB0 - Sub-headings
    COLOR_CHARCOAL = RGBColor(45, 55, 72)  # #2D3748 - Subsections / H3
    COLOR_BODY = RGBColor(45, 55, 72)      # #2D3748 - Body Text
    COLOR_MUTED = RGBColor(100, 116, 139)  # #64748B - Metadata / Footnotes
    COLOR_CALLOUT_BORDER = "1E3A8A"
    COLOR_CALLOUT_BG = "F1F5F9"
    COLOR_HEADER_BG = "1A365D"
    COLOR_ZEBRA_BG = "F8FAFC"
    COLOR_BORDER = "CBD5E1"

    # Style Helpers
    def style_run(run, font_name="Calibri", size_pt=11, bold=False, italic=False, color=COLOR_BODY):
        run.font.name = font_name
        run.font.size = Pt(size_pt)
        run.bold = bold
        run.italic = italic
        run.font.color.rgb = color

    def add_title(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        style_run(run, font_name="Calibri", size_pt=22, bold=True, color=COLOR_NAVY)
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(12)
        run = p.add_run(text)
        style_run(run, font_name="Calibri", size_pt=12.5, italic=True, color=COLOR_SLATE)
        return p

    def add_metadata_box(meta_dict):
        table = doc.add_table(rows=len(meta_dict), cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        col_widths = [Inches(1.8), Inches(4.4)]
        for i, (k, v) in enumerate(meta_dict.items()):
            row = table.rows[i]
            
            c0 = row.cells[0]
            c0.width = col_widths[0]
            p0 = c0.paragraphs[0]
            p0.paragraph_format.space_before = Pt(2)
            p0.paragraph_format.space_after = Pt(2)
            r0 = p0.add_run(k)
            style_run(r0, font_name="Calibri", size_pt=9.5, bold=True, color=COLOR_NAVY)

            c1 = row.cells[1]
            c1.width = col_widths[1]
            p1 = c1.paragraphs[0]
            p1.paragraph_format.space_before = Pt(2)
            p1.paragraph_format.space_after = Pt(2)
            r1 = p1.add_run(v)
            style_run(r1, font_name="Calibri", size_pt=9.5, color=COLOR_CHARCOAL)

            for cell in (c0, c1):
                set_cell_background(cell, "F8FAFC")
                set_cell_margins(cell, top=60, bottom=60, left=100, right=100)

        set_table_borders(table, color="E2E8F0", sz="4", val="single")
        
        spacer = doc.add_paragraph()
        spacer.paragraph_format.space_before = Pt(4)
        spacer.paragraph_format.space_after = Pt(6)

    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        style_run(run, font_name="Calibri", size_pt=14, bold=True, color=COLOR_NAVY)
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        style_run(run, font_name="Calibri", size_pt=12, bold=True, color=COLOR_SLATE)
        return p

    def add_paragraph(text, bold_prefix="", space_after=5):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            style_run(r_pre, font_name="Calibri", size_pt=10.5, bold=True, color=COLOR_CHARCOAL)
        run = p.add_run(text)
        style_run(run, font_name="Calibri", size_pt=10.5, color=COLOR_BODY)
        return p

    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            style_run(r_pre, font_name="Calibri", size_pt=10.5, bold=True, color=COLOR_CHARCOAL)
        run = p.add_run(text)
        style_run(run, font_name="Calibri", size_pt=10.5, color=COLOR_BODY)
        return p

    def add_callout(text, bold_title="Key Takeaway: "):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        cell = table.rows[0].cells[0]
        cell.width = Inches(6.27)
        set_cell_background(cell, COLOR_CALLOUT_BG)
        set_cell_margins(cell, top=120, bottom=120, left=180, right=180)

        # Thick left border
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="none"/>
                <w:left w:val="single" w:sz="24" w:space="0" w:color="{COLOR_CALLOUT_BORDER}"/>
                <w:bottom w:val="none"/>
                <w:right w:val="none"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)

        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        if bold_title:
            r_bold = p.add_run(bold_title)
            style_run(r_bold, font_name="Calibri", size_pt=10.5, bold=True, color=COLOR_NAVY)
        run = p.add_run(text)
        style_run(run, font_name="Calibri", size_pt=10.5, italic=True, color=COLOR_CHARCOAL)

        spacer = doc.add_paragraph()
        spacer.paragraph_format.space_before = Pt(2)
        spacer.paragraph_format.space_after = Pt(4)

    def add_figure(image_path, caption_title, caption_desc, width_in=6.0):
        if not os.path.exists(image_path):
            print(f"Warning: image path does not exist: {image_path}")
            return
        
        # Image paragraph
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(3)
        p_img.paragraph_format.keep_with_next = True
        run = p_img.add_run()
        run.add_picture(image_path, width=Inches(width_in))

        # Caption paragraph
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(12)
        
        r_title = p_cap.add_run(caption_title + " ")
        style_run(r_title, font_name="Calibri", size_pt=9.5, bold=True, color=COLOR_NAVY)
        
        r_desc = p_cap.add_run(caption_desc)
        style_run(r_desc, font_name="Calibri", size_pt=9.5, italic=True, color=COLOR_MUTED)

    def set_cell_background(cell, fill_hex):
        shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shading_elm)

    def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            node = OxmlElement(f'w:{m}')
            node.set(qn('w:w'), str(val))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    def set_table_borders(table, color="CBD5E1", sz="4", val="single"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(f'''
            <w:tblBorders {nsdecls("w")}>
                <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:left w:val="none"/>
                <w:right w:val="none"/>
                <w:insideV w:val="none"/>
            </w:tblBorders>
        ''')
        tblPr.append(borders)

    # -------------------------------------------------------------
    # DOCUMENT CONTENT GENERATION
    # -------------------------------------------------------------

    # Document Header
    add_title("Bibliometric Analysis & Literature Gap Assessment")
    add_subtitle("Evaluating the Scholarly Landscape on the Energy, Grid, and Resource Sustainability of India's AI Data Center Expansion")

    # Metadata Overview
    add_metadata_box({
        "Research Inquiry:": "Can India's renewable energy capacity and grid infrastructure sustainably meet the surging electricity, thermal, and water demands of AI hyperscale data center expansion?",
        "Empirical Corpus:": "Lens.org Scholarly Database — 6 Structured Comparative Queries (11,622 Unique Records)",
        "Core Methodology:": "Cross-Corpus Overlap Analysis, Publication Recency Velocity, Keyword Co-Occurrence Networks, White-Space Density Modeling, and Multi-Dimensional Maturity Profiling.",
        "Status / Scope:": "Empirical Pre-Study & Literature Justification Report for Dissertation"
    })

    # Section 1: Executive Purpose
    add_heading_1("1. Executive Purpose & Research Justification")
    add_paragraph(
        "As India accelerates its digital infrastructure initiatives, the explosive growth of artificial intelligence (AI) "
        "and generative AI workloads has triggered an unprecedented surge in computational power requirements. Hyperscale "
        "data center clusters demand uninterrupted, high-density electricity alongside intensive cooling and water resources. "
        "This dissertation investigates whether India's regional power grids, planned renewable energy integration, and "
        "industrial procurement frameworks can sustainably absorb this rapid expansion without compromising local grid reliability "
        "or environmental mandates."
    )
    add_paragraph(
        "Before designing empirical grid models or evaluating procurement policies, it is essential to determine whether this "
        "problem has been comprehensively addressed in existing scholarship. A rigorous bibliometric audit offers an objective, "
        "data-driven methodology to map the research landscape, measure thematic concentration, and substantiate the presence "
        "of a structural knowledge gap."
    )
    add_callout(
        "This report empirically confirms that peer-reviewed scholarship directly addressing the intersection of AI data centers, "
        "Indian power grid sustainability, and local resource constraints remains critically sparse, establishing an urgent, "
        "defensible foundation for the dissertation.",
        bold_title="Core Assessment: "
    )

    # Section 2: Data Architecture & Methodological Design
    add_heading_1("2. Data Architecture & Methodological Framework")
    add_paragraph(
        "To establish a defensible baseline, six structured queries were constructed and executed on the Lens.org global scholarly database. "
        "Rather than relying on an isolated search, this comparative architecture benchmarks the core inquiry against adjacent, "
        "well-established disciplines upon which the dissertation builds."
    )

    # Table 1: Query Architecture Table
    query_data = [
        ["Query", "Thematic Scope & Query Strategy", "Corpus Size", "Year Span", "Analytical Role in Dissertation"],
        ["A", "AI + Data Centers + India + Energy", "27", "2020–2026", "Core Inquiry (Headline Gap Target)"],
        ["B", "Global AI + Data Centers + Energy", "1,000*", "2009–2026", "Global Methodological Benchmark"],
        ["C", "Data Centers + Energy + India (General)", "71", "2002–2026", "Historical Pre-AI Infrastructure Baseline"],
        ["D", "AI + Macro Grid Systems & Demand", "10,750", "1987–2026", "Macro Grid Context (AI applied to power)"],
        ["E", "Renewables + Industrial PPAs + India", "103", "2005–2026", "Market & Regulatory Policy Template"],
        ["F", "Data Centers + Water / Cooling + India", "29", "1969–2026", "Physical Resource & Thermal Constraint"]
    ]

    t1 = doc.add_table(rows=len(query_data), cols=5)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    t1.autofit = False
    col_w1 = [Inches(0.6), Inches(2.3), Inches(0.8), Inches(0.9), Inches(1.67)]

    for row_idx, row in enumerate(t1.rows):
        for col_idx, cell in enumerate(row.cells):
            cell.width = col_w1[col_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            val = query_data[row_idx][col_idx]
            
            if row_idx == 0:
                set_cell_background(cell, COLOR_HEADER_BG)
                run = p.add_run(val)
                style_run(run, font_name="Calibri", size_pt=9.5, bold=True, color=RGBColor(255, 255, 255))
            else:
                bg = COLOR_ZEBRA_BG if row_idx % 2 == 1 else "FFFFFF"
                set_cell_background(cell, bg)
                run = p.add_run(val)
                is_bold = (col_idx == 0)
                style_run(run, font_name="Calibri", size_pt=9.0, bold=is_bold, color=COLOR_CHARCOAL)
            
            set_cell_margins(cell, top=70, bottom=70, left=90, right=90)

    set_table_borders(t1, color=COLOR_BORDER, sz="4", val="single")

    p_note = doc.add_paragraph()
    p_note.paragraph_format.space_before = Pt(3)
    p_note.paragraph_format.space_after = Pt(8)
    r_note = p_note.add_run("*Note: Query B reached the Lens.org export ceiling of 1,000 records; global literature volume is substantially higher.")
    style_run(r_note, font_name="Calibri", size_pt=8.5, italic=True, color=COLOR_MUTED)

    add_paragraph("The analytical pipeline integrates five complementary bibliometric evaluation techniques:")
    add_bullet("Evaluates aggregate publication volumes to determine absolute scholarly attention across domains.", bold_prefix="1. Volumetric Asymmetry Analysis: ")
    add_bullet("Tracks unique Lens ID intersections across queries to detect disciplinary silos and cross-pollination.", bold_prefix="2. Cross-Corpus Overlap Mapping: ")
    add_bullet("Measures the proportion of publications generated within 2024–2026 to distinguish mature fields from nascent frontiers.", bold_prefix="3. Recency Velocity Profiling: ")
    add_bullet("Quantifies bridging edges and lexical clusters across a 50-keyword co-occurrence graph to identify thematic divides.", bold_prefix="4. Semantic & Network Modeling: ")
    add_bullet("Scores individual corpora across volume, recency, citations, geographic diversity, and venue concentration.", bold_prefix="5. Multi-Dimensional Maturity Indexing: ")

    # Section 3: Detailed Findings
    add_heading_1("3. Detailed Empirical Findings")

    # 3.1 Volume Asymmetry
    add_heading_2("3.1 Volumetric Asymmetry: Extreme Scarcity at the Core Intersection")
    add_paragraph(
        "A quantitative assessment of search volumes reveals a dramatic structural imbalance across the six investigated domains. "
        "Macro-level research exploring AI applications in electricity systems (Query D) encompasses an extensive body of 10,750 publications. "
        "Similarly, global research dedicated to AI data center energy management (Query B) is robust and expansive, easily saturating "
        "the 1,000-record export threshold. In stark contrast, Query A—representing the primary focus of this dissertation—yields "
        "a total of only 27 publications across the entire historical record."
    )
    add_paragraph(
        "This corresponds to an asymmetry ratio of approximately 400 to 1 between generalized power-system AI scholarship and "
        "India-specific AI data center energy research. Scholarly output is abundant in the broader technical disciplines; "
        "however, literature positioned precisely at their convergence remains nearly unpopulated."
    )

    # Insert Figure 1
    add_figure(
        "bibliometric_gap_analysis_files/bibliometric_gap_analysis_25_1.png",
        "Figure 1.",
        "Comparative publication volume across all six Lens.org queries (logarithmic scale), highlighting the extreme volumetric deficit in Query A (27 papers) and Query F (29 papers)."
    )

    # 3.2 Citation Impact & Thematic Drift
    add_heading_2("3.2 Low Citation Impact and Substantive Thematic Drift in Core Records")
    add_paragraph(
        "Beyond nominal publication counts, an in-depth content and citation audit of the 27 records in Query A confirms substantial "
        "thematic dispersion and low academic penetration. Across all 27 papers, the corpus has garnered an aggregate of 52 citations, "
        "yielding a mean citation rate of 1.93 per document and a median of zero. Over 55% of the documents have never received a single citation, "
        "and none has been cited within patent literature."
    )
    add_paragraph(
        "Crucially, granular inspection reveals that few of these records directly investigate the grid or infrastructural impacts of "
        "generative AI data centers. The most-cited document (17 citations) investigates shifts in residential electricity demand during "
        "COVID-19 lockdowns. Remaining entries examine generalized smart-city security protocols, algorithmic financial trading systems, "
        "or municipal IoT routing. Consequently, the actual volume of peer-reviewed empirical work addressing the electricity constraints "
        "of hyperscale AI infrastructure in India is effectively close to zero."
    )

    # 3.3 Overlap Matrix
    add_heading_2("3.3 Cross-Corpus Overlap: Disconnected Disciplinary Silos")
    add_paragraph(
        "An analysis of pairwise record intersections demonstrates that current research operates in isolated methodological silos. "
        "Three distinct patterns emerge from the overlap matrix:"
    )
    add_bullet(
        "Of the 27 papers in Query A, 22 are directly subsumed within Query C (general Indian data centers). Adding 'AI' keywords filters "
        "out legacy infrastructure papers but yields an extremely thin residual rather than a specialized, independent literature.",
        bold_prefix="Core Corpus Subsumption: "
    )
    add_bullet(
        "Query A shares only 6 publications with global data center energy scholarship (Query B) and 10 with macro-grid AI research (Query D). "
        "Global methodologies are rarely contextualized within Indian grid realities.",
        bold_prefix="Disconnection from Global Methodologies: "
    )
    add_bullet(
        "Global data center energy (Query B) and macro-grid AI (Query D) share 311 overlapping publications. Conversely, Indian industrial "
        "renewable energy research (Query E) shares only 2 papers with Query B and 1 with Query D. Technical compute engineering and Indian "
        "power procurement frameworks proceed along completely parallel tracks.",
        bold_prefix="Entrenched Global vs. National Divide: "
    )

    # Insert Figure 2
    add_figure(
        "bibliometric_gap_analysis_files/bibliometric_gap_analysis_26_1.png",
        "Figure 2.",
        "Pairwise scholarly record overlap matrix (Lens ID intersections), illustrating the dense cross-citation among global domains and the structural isolation of Indian corporate renewable energy research."
    )

    # 3.4 Recency Dynamics
    add_heading_2("3.4 Publication Recency Dynamics: An Emerging, Unconsolidated Frontier")
    add_paragraph(
        "Temporal distribution analysis demonstrates that scholarly engagement with the core inquiry is of very recent origin. "
        "Query A exhibits a mean publication year of 2024.7, with 81.5% of its total output (22 of 27 papers) appearing between 2024 and 2026. "
        "This represents the highest recency velocity among all evaluated queries. Query F (water and cooling constraints) exhibits a 79.3% recency share, "
        "followed by Query B at 75.3% and Query C at 71.8%."
    )
    add_paragraph(
        "In contrast, Query E (industrial renewable energy and corporate PPAs in India) constitutes a mature historical field, with a mean publication "
        "year of 2020.6 and only 31.1% of output originating from the last three years. This disparity underscores that while the regulatory mechanisms "
        "for industrial green power procurement have been studied for over two decades, their application to the dynamic, continuous load profiles of "
        "AI data centers represents an unexamined contemporary frontier."
    )

    # Insert Figure 3
    add_figure(
        "bibliometric_gap_analysis_files/bibliometric_gap_analysis_31_1.png",
        "Figure 3.",
        "Recency velocity across search queries, defined as the percentage of publications generated within the 2024–2026 window, demonstrating the nascent status of Query A."
    )

    # 3.5 Adjacent Literatures
    add_heading_2("3.5 Adjacent Literatures: Methodological Value but Divergent Orientations")
    add_paragraph(
        "While adjacent research domains cannot substitute for direct empirical investigation, they provide indispensable theoretical and "
        "methodological building blocks for the dissertation:"
    )
    add_bullet(
        "Encompassing 123,455 citations (11.48 citations per paper), this corpus addresses 'AI applied to optimize the grid' (e.g., solar irradiance "
        "forecasting, smart meter analytics, transmission fault detection). The dissertation inverts this dynamic, analyzing the grid's capacity to absorb "
        "massive AI-driven load growth.",
        bold_prefix="Macro Grid AI (Query D): "
    )
    add_bullet(
        "Comprising 5,359 citations and 124 patent citations, this literature provides established engineering models for workload consolidation, "
        "carbon-aware dynamic task scheduling, and server thermal management, which can be adapted to Indian conditions.",
        bold_prefix="Global AI Data Center Energy (Query B): "
    )
    add_bullet(
        "Exhibiting an average of 10.27 citations per paper, this body of work establishes the legal and tariff mechanisms governing open-access "
        "wheeling, green energy tariffs, and corporate PPAs in India, though historically focused on heavy industries such as steel and cement.",
        bold_prefix="Industrial Renewable Energy in India (Query E): "
    )
    add_bullet(
        "Encompassing 71 papers and 138 citations, this corpus focuses on legacy enterprise server rooms and power reliability, preceding modern "
        "high-density GPU acceleration architectures.",
        bold_prefix="Pre-AI Indian Data Center Research (Query C): "
    )

    # 3.6 Water & Thermal
    add_heading_2("3.6 The Water and Cooling Nexus: A Critical Second-Order Vulnerability")
    add_paragraph(
        "Query F captures only 29 publications investigating data centers, cooling methodologies, and water constraints in the Indian context. "
        "Highly cited papers within this set date primarily from 2003 to 2014 and examine generic thermodynamics rather than regional Indian "
        "hydrological stress. Given that hyperscale evaporative cooling systems require millions of liters of potable water daily, and primary data "
        "center hubs (e.g., Navi Mumbai, Chennai, Bengaluru) face acute water stress, the literature leaves a vital second-order resource bottleneck "
        "almost entirely unaddressed."
    )

    # 3.7 Lexical & Topic Modeling
    add_heading_2("3.7 Semantic Bifurcation: Lexical and Topic Network Analysis")
    add_paragraph(
        "Comparative vocabulary extraction and network analysis reveal an epistemological divide between computing and energy literature. "
        "While Query A and Query B share general high-level terms (e.g., 'artificial intelligence', 'machine learning', 'energy consumption'), "
        "specialized data center engineering terms ('cloud computing', 'green computing', 'distributed computing', 'energy management') "
        "are prevalent in global literature but absent from India-specific corpora."
    )
    add_paragraph(
        "A network graph constructed from the 50 most frequent keywords contains 91 intra-cluster links among energy/grid terms and 27 intra-cluster "
        "links among AI/computing terms. The 112 bridging edges that connect the two clusters route exclusively through broad, uninformative nodes "
        "such as 'energy consumption' and 'machine learning'. There is no cohesive, high-density cluster integrating AI training workloads with "
        "Indian power system constraints. Non-Negative Matrix Factorization (NMF) topic modeling reinforces this separation, resolving the corpus into "
        "isolated themes (e.g., solar forecasting, grid fault detection, data center thermal optimization) without producing an integrated topic for "
        "national AI infrastructure energy sustainability."
    )

    # Insert Figure 4
    add_figure(
        "bibliometric_gap_analysis_files/bibliometric_gap_analysis_34_1.png",
        "Figure 4.",
        "Keyword co-occurrence network graph (top 50 terms), showing the dual-cluster topology between AI/computing concepts and power/grid concepts, linked only by generic intermediate nodes."
    )

    # 3.8 White-Space Map
    add_heading_2("3.8 Paper-Level White-Space Density Modeling")
    add_paragraph(
        "To rigorously test whether relevant literature exists outside the predefined query classifications, all 11,622 unique papers in the "
        "combined corpus were scored on two orthogonal term frequencies: (1) AI and data center computational concepts, and (2) Indian power grid "
        "and renewable energy concepts. Documents achieving a score of 2 or higher in both dimensions were classified as occupying the target intersection."
    )
    add_paragraph(
        "This automated classification flagged 1,344 documents (11.56% of the corpus). However, qualitative validation reveals that this overlap "
        "is largely a lexical artifact. Flagged papers primarily comprise generic climate-forecasting code repositories, mathematical optimization "
        "surveys, or broad policy commentaries that mention both vocabularies without investigating the core problem. The authentic, domain-specific "
        "scholarly body remains strictly bounded within the vicinity of Query A's 27 papers."
    )

    # Insert Figure 5
    add_figure(
        "bibliometric_gap_analysis_files/bibliometric_gap_analysis_33_1.png",
        "Figure 5.",
        "Paper-level white-space density map of all 11,622 unique records, illustrating that the high-density intersection is populated by superficial keyword co-occurrences rather than dedicated investigative research."
    )

    # 3.9 Multi-Dimensional Maturity Scores
    add_heading_2("3.9 Multi-Dimensional Maturity Scoring")
    add_paragraph(
        "To synthesize structural characteristics across datasets, each query was evaluated across five standardized indices (scaled 0.0 to 1.0): "
        "Volume, Citation Impact, Recency, Geographic Diversity, and Venue Concentration."
    )
    add_paragraph(
        "Query D dominates across Volume (1.00) and Geographic Diversity (1.00). Query B displays strong Volume (0.74) and Geographic Diversity (0.70). "
        "In contrast, Query A demonstrates severe structural weaknesses, recording the lowest Citation Impact (0.08), low Volume (0.36), and limited "
        "Geographic Diversity (0.25). Its singular high index is Recency (0.81), confirming its status as an emergent, unconsolidated niche. "
        "Query F exhibits the lowest Geographic Diversity (0.15), and Query E records the lowest Recency (0.31)."
    )

    # Insert Figure 6
    add_figure(
        "bibliometric_gap_analysis_files/bibliometric_gap_analysis_37_1.png",
        "Figure 6.",
        "Multi-dimensional literature maturity radar profile, contrasting the well-developed profiles of global queries (D, B) against the highly constrained, recency-dominated footprint of Query A."
    )

    # Section 4: Scorecard Table
    add_heading_1("4. Literature Gap Synthesis Scorecard")
    add_paragraph("The synthesized evaluation of the six research domains is summarized in the matrix below:")

    scorecard_data = [
        ["Thematic Domain & Query", "Volume", "Literature Maturity", "Strategic Contribution to Dissertation"],
        ["Core Intersection: AI Data Centers + India + Energy (A)", "27", "Extremely Scarce / Nascent", "Defines the primary research gap and core investigative target."],
        ["Global AI Data Center Power Management (B)", "1,000+", "Mature & Fast-Growing", "Provides computational modeling methods and workload scheduling frameworks."],
        ["Pre-AI Indian Data Center Energy (C)", "71", "Sparse / Legacy Focus", "Establishes baseline power reliability data; precedes generative AI architectures."],
        ["AI in Macro Power & Grid Systems (D)", "10,750", "Vast & Established", "Provides technical context on grid integration and AI-driven load forecasting."],
        ["Industrial Renewables & Open-Access PPAs in India (E)", "103", "Moderate / Stable", "Provides legal, tariff, and regulatory procurement models for corporate clean power."],
        ["Data Center Water & Thermal Cooling in India (F)", "29", "Near-Zero / Outdated", "Identifies a critical second-order resource constraint alongside electricity."]
    ]

    t2 = doc.add_table(rows=len(scorecard_data), cols=4)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t2.autofit = False
    col_w2 = [Inches(1.8), Inches(0.7), Inches(1.5), Inches(2.27)]

    for row_idx, row in enumerate(t2.rows):
        for col_idx, cell in enumerate(row.cells):
            cell.width = col_w2[col_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            val = scorecard_data[row_idx][col_idx]
            
            if row_idx == 0:
                set_cell_background(cell, COLOR_HEADER_BG)
                run = p.add_run(val)
                style_run(run, font_name="Calibri", size_pt=9.5, bold=True, color=RGBColor(255, 255, 255))
            else:
                bg = COLOR_ZEBRA_BG if row_idx % 2 == 1 else "FFFFFF"
                set_cell_background(cell, bg)
                run = p.add_run(val)
                is_bold = (col_idx == 0)
                style_run(run, font_name="Calibri", size_pt=9.0, bold=is_bold, color=COLOR_CHARCOAL)
            
            set_cell_margins(cell, top=70, bottom=70, left=90, right=90)

    set_table_borders(t2, color=COLOR_BORDER, sz="4", val="single")

    # Section 5: Interpretations & Gap Statement
    add_heading_1("5. Core Interpretations & Definitive Gap Statement")
    add_paragraph(
        "Synthesizing the empirical evidence from the volumetric, citation, network, and maturity analyses leads to three principal conclusions:"
    )
    add_bullet(
        "Direct peer-reviewed coverage of India's AI data center power sustainability is confined to fewer than thirty loosely related publications, "
        "characterized by near-zero citation impact and substantial thematic drift.",
        bold_prefix="1. Absolute Literature Scarcity: "
    )
    add_bullet(
        "The gap is driven not by an absence of foundational knowledge, but by disciplinary fragmentation. Advanced computational modeling of AI loads "
        "and robust Indian renewable procurement frameworks exist as mature, independent bodies of literature that have never been integrated.",
        bold_prefix="2. Disciplinary Disconnection: "
    )
    add_bullet(
        "Cooling architectures and regional water stress represent an acute, unstudied vulnerability that compounds the electrical grid constraint.",
        bold_prefix="3. The Overlooked Thermal-Water Constraint: "
    )

    add_callout(
        "\"While global scholarship provides advanced engineering models for AI data center energy management, and Indian power-sector "
        "literature offers established frameworks for industrial renewable procurement, existing research fails to reflect India's regional "
        "grid realities, green tariff structures, and thermal-water constraints; consequently, no integrated empirical assessment currently "
        "evaluates whether India's power system and renewable capacity can sustainably support the projected expansion of hyperscale AI data centers.\"",
        bold_title="Definitive Literature Gap Statement: "
    )

    # Section 6: Limitations
    add_heading_1("6. Methodological Limitations & Boundary Conditions")
    add_paragraph("To maintain analytical rigor, four methodological constraints must be acknowledged:")
    add_bullet(
        "The analysis relies exclusively on academic literature indexed in Lens.org. Non-peer-reviewed industry whitepapers (e.g., CBRE, JLL, CEA reports) "
        "actively discuss data center expansion but are excluded to maintain focus on formal scholarly gaps.",
        bold_prefix="Database Indexing Boundary: "
    )
    add_bullet(
        "Query B was capped at 1,000 records due to platform export restrictions, understating the absolute volume of global computer science literature.",
        bold_prefix="Export Ceilings: "
    )
    add_bullet(
        "A substantial proportion of records lack explicit institutional country tags (82.3% in Query B, 73.8% in Query D), introducing minor uncertainty "
        "into geographic diversity metrics.",
        bold_prefix="Metadata Incompleteness: "
    )
    add_bullet(
        "Lexical scoring captures keyword frequency rather than deep semantic comprehension, necessitating manual qualitative validation.",
        bold_prefix="Lexical Keyword Filtering: "
    )

    # Section 7: Conclusion
    add_heading_1("7. Strategic Conclusion & Dissertation Trajectory")
    add_paragraph(
        "The bibliometric evidence compiled in this report establishes an unassailable justification for the proposed dissertation. "
        "The research space at the confluence of artificial intelligence workloads, Indian renewable energy integration, and regional grid stability "
        "is both exceptionally sparse and structurally disconnected. By synthesizing global computational energy models with Indian power-market "
        "mechanisms and water-cooling constraints, this dissertation directly bridges a documented, high-impact void in contemporary energy policy "
        "and sustainability scholarship."
    )

    # Save Document
    out_file = "Bibliometric_Analysis_Report.docx"
    doc.save(out_file)
    print(f"Successfully generated humanized document: {out_file} (Size: {os.path.getsize(out_file)} bytes)")

if __name__ == "__main__":
    create_report()
