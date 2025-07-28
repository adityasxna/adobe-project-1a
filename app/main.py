import os
from pdf_parser import parse_pdf
from heading_detector import analyze_and_find_headings
from output_generator import save_to_json

def process_all_pdfs():
    input_dir = "/app/input"
    output_dir = "/app/output"
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            print(f"Processing {filename}...")
            pdf_path = os.path.join(input_dir, filename)
            lines = parse_pdf(pdf_path)
            result = analyze_and_find_headings(lines)
            output_filename = f"{os.path.splitext(filename)[0]}.json"
            output_path = os.path.join(output_dir, output_filename)
            save_to_json(result, output_path)

if __name__ == '__main__':
    process_all_pdfs()