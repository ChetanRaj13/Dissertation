import fitz
import re
import unicodedata

def normalize_text(text):
    if not text:
        return ""
    text = unicodedata.normalize('NFKD', text)
    # Soft hyphen handling: discretionary hyphen at line break
    text = re.sub(r'\xad\s*\n\s*', '', text)
    text = text.replace('\xad', '')
    # Quote normalization
    text = text.replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'")
    text = text.replace("''", '"')
    text = text.replace('—', '-').replace('–', '-')
    # Drop capitals
    text = re.sub(r'\b([A-Z])\s*\n\s*([a-z]+)\b', r'\1\2', text)
    # Remove hyphen at line breaks ONLY between alphabetic words: word-\nword -> wordword
    text = re.sub(r'([a-zA-Z]+)-\s*\n\s*([a-zA-Z]+)', r'\1\2', text)
    # Number hyphen at line break: 2014-\n2016 -> 2014-2016
    text = re.sub(r'(\d+)\s*-\s*\n\s*(\d+)', r'\1-\2', text)
    # Handle closing parenthesis hyphen: (GPU)-\naccelerated -> (gpu)- accelerated
    text = re.sub(r'\)-\s*\n\s*', r')- ', text)
    # Replace all newlines and multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()

def check_excerpt_on_page(pdf_path, page_num_1indexed, excerpt):
    clean_excerpt = excerpt.strip('"\'' )
    words = clean_excerpt.split()
    if len(words) > 25:
        return False, f"Excerpt exceeds 25 words ({len(words)} words)"
    
    doc = fitz.open(pdf_path)
    if page_num_1indexed < 1 or page_num_1indexed > len(doc):
        return False, f"Page {page_num_1indexed} out of range (1-{len(doc)})"
    
    page = doc[page_num_1indexed - 1]
    page_text = page.get_text()
    
    norm_page = normalize_text(page_text)
    norm_excerpt = normalize_text(clean_excerpt)
    
    if norm_excerpt in norm_page:
        return True, "Found"
    else:
        return False, f"Not found on page {page_num_1indexed}"

print("Verifier updated.")
