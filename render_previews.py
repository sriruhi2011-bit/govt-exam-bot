# render_previews.py
from pdf_engine import PDFEngine, OUTPUT_DIR
from newspaper_pdf_pipeline import NewspaperPDFPipeline
from playwright.sync_api import sync_playwright
import os

def generate_previews():
    pipe = NewspaperPDFPipeline()
    engine = PDFEngine()
    today = pipe.get_today_str()

    print("Generating PDFs and Preview Images...")
    pipe.run_daily_generation()

    # The Hindu HTML & Prajavani HTML
    # We can use pdf-to-image or render html directly with playwright
    print("PDFs generated in:", OUTPUT_DIR)
    for f in os.listdir(OUTPUT_DIR):
        if f.endswith('.pdf'):
            full_p = os.path.join(OUTPUT_DIR, f)
            print(f"  • {f} ({os.path.getsize(full_p):,} bytes)")

if __name__ == "__main__":
    generate_previews()
