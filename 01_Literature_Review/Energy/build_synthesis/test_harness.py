import fitz
import re
from verifier import check_excerpt_on_page

# Helper to check a list of rows
def test_rows(rows_list, name):
    passed = 0
    failed = []
    for idx, r in enumerate(rows_list):
        # r = (paper_id, file, page, printed_page, flag, sec, tbl, cat, var, val, unit, yr, geo, excerpt, paraphrase, stype, cited, caveat, tag)
        pdf = r[1]
        pg = r[2]
        exc = r[13]
        ok, msg = check_excerpt_on_page(pdf, pg, exc)
        if ok:
            passed += 1
        else:
            failed.append((idx + 1, r[0], pg, exc, msg))
    print(f"[{name}] Total: {len(rows_list)} | Passed: {passed} | Failed: {len(failed)}")
    for f in failed:
        print(f"  FAILED row {f[0]} ({f[1]} p.{f[2]}): {f[3]} -> {f[4]}")
    return len(failed) == 0

print("Test harness loaded.")
