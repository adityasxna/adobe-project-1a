import fitz  # PyMuPDF

def parse_pdf(pdf_path):
    """
    Extracts structured lines of text from a PDF, preserving essential metadata
    including font flags for bold/italic detection.
    """
    lines = []
    try:
        doc = fitz.open(pdf_path)
        for page_num, page in enumerate(doc, start=1):
            blocks = page.get_text("dict").get("blocks", [])
            for block in blocks:
                if block.get("type") == 0:  # Text blocks
                    for line in block.get("lines", []):
                        if not line.get("spans"):
                            continue
                        
                        first_span = line["spans"][0]
                        line_text = " ".join([s["text"] for s in line["spans"]]).strip()

                        if line_text:
                            lines.append({
                                "text": line_text,
                                "size": first_span["size"],
                                "font": first_span["font"],
                                "flags": first_span["flags"], # Flags for bold/italic
                                "page": page_num,
                                "bbox": line['bbox']  # Positional data (x0, y0, x1, y1)
                            })
    except Exception as e:
        print(f"Error parsing PDF {pdf_path}: {e}")
        return []
    
    return lines