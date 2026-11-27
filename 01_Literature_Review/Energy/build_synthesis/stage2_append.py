import os
import sys
import datetime
import shutil
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# Import data from test files
from test_e05 import e05_data
from test_e06 import e06_data
from test_e07 import e07_data
from test_e08 import e08_data
from test_e09 import e09_data

def append_stage2():
    master_path = "energy_datacentre_literature_synthesis_v1.xlsx"
    backup_path = "energy_datacentre_literature_synthesis_v1_stage2_backup.xlsx"
    
    # Save Stage 2 backup BEFORE modifying workbook (Hard Rule 4)
    shutil.copyfile(master_path, backup_path)
    print(f"Pre-stage backup saved: {backup_path}")
    
    wb = openpyxl.load_workbook(master_path)
    ws_extract = wb["Extraction"]
    ws_progress = wb["Progress_Log"]
    
    # Styles
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )
    inference_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    
    # Determine next row_id
    current_max_row = ws_extract.max_row
    # Current rows in Extraction = current_max_row - 1 (header)
    next_idx = current_max_row # e.g. 68 -> row 69, which is ROW-0068
    
    all_stage2_sources = [
        ("E05", e05_data),
        ("E06", e06_data),
        ("E07", e07_data),
        ("E08", e08_data),
        ("E09", e09_data)
    ]
    
    total_added = 0
    start_row_num = ws_extract.max_row + 1
    
    for paper_id, dataset in all_stage2_sources:
        print(f"Appending {paper_id}: {len(dataset)} rows...")
        for r in dataset:
            row_id_str = f"ROW-{next_idx:04d}"
            # Dataset row:
            # (paper_id, source_file, pdf_page, printed_page, page_flag, section, table_or_figure,
            #  variable_category, variable_name, value_as_printed, unit, year_or_period, geography,
            #  excerpt, paraphrase, statement_type, cited_from_other_source, author_caveat, tag)
            row_vals = [
                row_id_str, r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8],
                r[9], r[10], r[11], r[12], f'"{r[13]}"', r[14], r[15], r[16], r[17], r[18]
            ]
            ws_extract.append(row_vals)
            next_idx += 1
            total_added += 1
            
    end_row_num = ws_extract.max_row
    
    # Format newly added rows
    for row in ws_extract.iter_rows(min_row=start_row_num, max_row=end_row_num, min_col=1, max_col=ws_extract.max_column):
        for cell in row:
            cell.border = thin_border
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            if cell.value and ("[I]" in str(cell.value) or "derived [I]" in str(cell.value)):
                cell.fill = inference_fill

    # Update auto_filter ref
    ws_extract.auto_filter.ref = ws_extract.dimensions
    
    # Progress Log entry
    progress_entry = [
        "STAGE 2", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        f"Appended {total_added} code-verified rows for E05, E06, E07, E08, and E09 into Extraction sheet. Preserved water boundary (zero water rows extracted from E05/E08).",
        "E05 (16), E06 (20), E07 (18), E08 (18), E09 (18)", total_added,
        "None; all 90 candidate excerpts code-verified against exact PDF text prior to appending (100% pass rate).",
        backup_path
    ]
    ws_progress.append(progress_entry)
    
    # Format Progress_Log row
    p_last = ws_progress.max_row
    for cell in ws_progress[p_last]:
        cell.border = thin_border
        cell.alignment = Alignment(vertical="top", wrap_text=True)
    ws_progress.auto_filter.ref = ws_progress.dimensions
    
    wb.save(master_path)
    print(f"Stage 2 complete! Appended {total_added} rows. Master workbook updated: {master_path}")

if __name__ == '__main__':
    append_stage2()
