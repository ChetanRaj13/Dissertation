import json

with open(r"c:\Users\rajch\Desktop\SEM 7\Dissertation\DATA\new\verified_core_v2.json", "r", encoding="utf-8") as f:
    records = json.load(f)

ncr_ids = ["CORE24", "CORE25", "CORE61", "CORE62", "CORE63", "CORE64", "CORE65", "CORE66", "CORE67", "CORE68", "CORE69"]
ncr_recs = [r for r in records if r["id"] in ncr_ids]

total_ncr_op = sum(r["operational_mw"] for r in ncr_recs if r["operational_mw"] is not None)
print(f"Total Delhi NCR Operational MW in dataset: {total_ncr_op:.1f} MW")
print("Breakdown:")
for r in ncr_recs:
    print(f"  {r['id']}: {r['facility_name']} ({r['district']}) -> {r['operational_mw']} MW")

cushman_ncr_benchmark = 183.0
diff = round(total_ncr_op - cushman_ncr_benchmark, 1)
print(f"Cushman & Wakefield Benchmark: {cushman_ncr_benchmark} MW")
print(f"Difference: {diff} MW")
