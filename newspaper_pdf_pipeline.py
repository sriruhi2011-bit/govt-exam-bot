# newspaper_pdf_pipeline.py
"""
Newspaper Study Material Pipeline for The Hindu & Prajavani.
Extracts real, fresh news from the last 24 hours, strictly filters for exam relevance,
and dynamically synthesizes bilingual civil services study materials:
- The Hindu: Template 4 (Nordic Amber Focus) -> The_Hindu_<YYYY-MM-DD>.pdf
- Prajavani: Template 3 (KPSC Royal Crimson) -> Prajavani_<YYYY-MM-DD>.pdf
Format: Both English & Kannada in each PDF (English first, then Kannada).
"""

import os
import sys
import json
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Tuple

from config.settings import DATA_DIR
from config.logger import setup_logger
from pdf_engine import PDFEngine
from news_pdf_synthesizer import DailyNewsPDFSynthesizer

logger = setup_logger("newspaper_pipeline")
PDF_DIR = os.path.join(DATA_DIR, "pdfs")
os.makedirs(PDF_DIR, exist_ok=True)


class NewspaperPDFPipeline:
    def __init__(self):
        self.engine = PDFEngine()
        self.synthesizer = DailyNewsPDFSynthesizer()
        self.ist_offset = timezone(timedelta(hours=5, minutes=30))

    def get_today_str(self) -> str:
        return datetime.now(self.ist_offset).strftime("%Y-%m-%d")

    def get_formatted_date(self) -> str:
        return datetime.now(self.ist_offset).strftime("%A, %d %B %Y")

    # ════════════════════════════════════════════════════
    # 1. THE HINDU GENERATOR (Template 4: Nordic Amber Focus)
    # ════════════════════════════════════════════════════
    def generate_the_hindu_pdf(self, date_str: str = None) -> str:
        """
        Dynamically generates The Hindu bilingual study PDF using
        real news stories published in the last 24 hours.
        """
        if not date_str:
            date_str = self.get_today_str()

        formatted_date = self.get_formatted_date()
        filename = f"The_Hindu_{date_str}.pdf"
        output_path = os.path.join(PDF_DIR, filename)

        logger.info(f"Synthesizing dynamic 24-hour news context for The Hindu ({date_str})...")
        context = self.synthesizer.synthesize_the_hindu_content(formatted_date)

        html = self.engine.render_html("the_hindu_nordic.html", context)
        self.engine.generate_pdf_from_html(html, output_path)
        logger.info(f"Successfully generated dynamic The Hindu PDF: {output_path}")
        return output_path

    # ════════════════════════════════════════════════════
    # 2. PRAJAVANI GENERATOR (Template 3: KPSC Royal Crimson)
    # ════════════════════════════════════════════════════
    def generate_prajavani_pdf(self, date_str: str = None) -> str:
        """
        Dynamically generates Prajavani Karnataka & National bilingual study PDF
        using real news stories published in the last 24 hours.
        """
        if not date_str:
            date_str = self.get_today_str()

        formatted_date = self.get_formatted_date()
        filename = f"Prajavani_{date_str}.pdf"
        output_path = os.path.join(PDF_DIR, filename)

        logger.info(f"Synthesizing dynamic 24-hour news context for Prajavani ({date_str})...")
        context = self.synthesizer.synthesize_prajavani_content(formatted_date)

        html = self.engine.render_html("prajavani_crimson.html", context)
        self.engine.generate_pdf_from_html(html, output_path)
        logger.info(f"Successfully generated dynamic Prajavani PDF: {output_path}")
        return output_path

    def run_daily_generation(self) -> Tuple[str, str]:
        today = self.get_today_str()
        print(f"Generating dynamic daily 24h news study PDFs for {today}...")
        hindu_pdf = self.generate_the_hindu_pdf(today)
        prajavani_pdf = self.generate_prajavani_pdf(today)
        return hindu_pdf, prajavani_pdf


if __name__ == "__main__":
    pipeline = NewspaperPDFPipeline()
    h, p = pipeline.run_daily_generation()
    print(f"Generated fresh dynamic PDFs:\nHindu: {h}\nPrajavani: {p}")
