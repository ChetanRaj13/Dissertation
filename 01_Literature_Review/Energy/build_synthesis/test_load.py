import os
import fitz
import re
from verifier import check_excerpt_on_page

# Let's inspect pages from E02
doc_e02 = fitz.open("2024 United States Data Center Energy Usage Report.pdf")
print("E02 loaded:", len(doc_e02), "pages")

# Let's inspect pages from E03
doc_e03 = fitz.open("Energy and AI - IEA.pdf")
print("E03 loaded:", len(doc_e03), "pages")

# Let's inspect pages from E04
doc_e04 = fitz.open("Artificial intelligence - Supply chain constraints and energy implications.pdf")
print("E04 loaded:", len(doc_e04), "pages")
