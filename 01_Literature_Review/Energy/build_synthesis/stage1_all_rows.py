import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verifier import check_excerpt_on_page
from prepare_stage1_rows import e01_data
from test_e02 import e02_data
from test_e03_e04 import e03_data, e04_data

# Combine all rows
all_stage1_rows = []
row_idx = 1

# E01
for r in e01_data:
    row_dict = {
        'row_id': f"ROW-{row_idx:04d}",
        'paper_id': r[0],
        'source_file': r[1],
        'pdf_page': r[2],
        'printed_page': r[3],
        'page_flag': r[4],
        'section': r[5],
        'table_or_figure': r[6],
        'variable_category': r[7],
        'variable_name': r[8],
        'value_as_printed': r[9],
        'unit': r[10],
        'year_or_period': r[11],
        'geography': r[12],
        'excerpt': f'"{r[13]}"',
        'paraphrase': r[14],
        'statement_type': r[15],
        'cited_from_other_source': r[16],
        'author_caveat': r[17],
        'tag': r[18]
    }
    all_stage1_rows.append(row_dict)
    row_idx += 1

# E02
for r in e02_data:
    row_dict = {
        'row_id': f"ROW-{row_idx:04d}",
        'paper_id': r[0],
        'source_file': r[1],
        'pdf_page': r[2],
        'printed_page': r[3],
        'page_flag': r[4],
        'section': r[5],
        'table_or_figure': r[6],
        'variable_category': r[7],
        'variable_name': r[8],
        'value_as_printed': r[9],
        'unit': r[10],
        'year_or_period': r[11],
        'geography': r[12],
        'excerpt': f'"{r[13]}"',
        'paraphrase': r[14],
        'statement_type': r[15],
        'cited_from_other_source': r[16],
        'author_caveat': r[17],
        'tag': r[18]
    }
    all_stage1_rows.append(row_dict)
    row_idx += 1

# E03
for r in e03_data:
    row_dict = {
        'row_id': f"ROW-{row_idx:04d}",
        'paper_id': r[0],
        'source_file': r[1],
        'pdf_page': r[2],
        'printed_page': r[3],
        'page_flag': r[4],
        'section': r[5],
        'table_or_figure': r[6],
        'variable_category': r[7],
        'variable_name': r[8],
        'value_as_printed': r[9],
        'unit': r[10],
        'year_or_period': r[11],
        'geography': r[12],
        'excerpt': f'"{r[13]}"',
        'paraphrase': r[14],
        'statement_type': r[15],
        'cited_from_other_source': r[16],
        'author_caveat': r[17],
        'tag': r[18]
    }
    all_stage1_rows.append(row_dict)
    row_idx += 1

# E04
for r in e04_data:
    row_dict = {
        'row_id': f"ROW-{row_idx:04d}",
        'paper_id': r[0],
        'source_file': r[1],
        'pdf_page': r[2],
        'printed_page': r[3],
        'page_flag': r[4],
        'section': r[5],
        'table_or_figure': r[6],
        'variable_category': r[7],
        'variable_name': r[8],
        'value_as_printed': r[9],
        'unit': r[10],
        'year_or_period': r[11],
        'geography': r[12],
        'excerpt': f'"{r[13]}"',
        'paraphrase': r[14],
        'statement_type': r[15],
        'cited_from_other_source': r[16],
        'author_caveat': r[17],
        'tag': r[18]
    }
    all_stage1_rows.append(row_dict)
    row_idx += 1

if __name__ == '__main__':
    print(f"Total Stage 1 rows: {len(all_stage1_rows)}")
    failed = 0
    for row in all_stage1_rows:
        ok, msg = check_excerpt_on_page(row['source_file'], row['pdf_page'], row['excerpt'])
        if not ok:
            print(f"FAILED {row['row_id']} ({row['paper_id']} p.{row['pdf_page']}): {row['excerpt'][:40]}... -> {msg}")
            failed += 1
    print(f"Verification complete. Total: {len(all_stage1_rows)} | Passed: {len(all_stage1_rows)-failed} | Failed: {failed}")
