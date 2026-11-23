# pdf_engine.py
"""
High-Fidelity PDF Study Material Engine.
Renders Jinja2 HTML/CSS templates into pixel-perfect 2-column A4 study material PDFs
with full Indic (Kannada) typography, custom callouts, traps, and exam styling.
"""

import os
import sys
import jinja2
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional

from config.logger import setup_logger

logger = setup_logger("pdf_engine")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "pdfs")


class PDFEngine:
    def __init__(self):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(TEMPLATES_DIR),
            autoescape=jinja2.select_autoescape(["html", "xml"])
        )

    def render_html(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render a Jinja2 template with the given context."""
        template = self.jinja_env.get_template(template_name)
        return template.render(**context)

    def generate_pdf_from_html(self, html_content: str, output_path: str) -> str:
        """
        Converts HTML string to a vector PDF using Playwright Chromium with full
        Google Fonts and HarfBuzz Kannada ligature shaping.
        """
        from playwright.sync_api import sync_playwright

        temp_html_path = os.path.join(OUTPUT_DIR, f"_temp_{os.getpid()}.html")
        try:
            with open(temp_html_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            abs_html_uri = f"file:///{os.path.abspath(temp_html_path).replace(os.sep, '/')}"

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()

                # Navigate and wait for external fonts (Lora, Noto Sans Kannada) to finish loading
                page.goto(abs_html_uri, wait_until="networkidle")
                page.wait_for_timeout(500)  # Brief buffer for font rendering

                page.pdf(
                    path=output_path,
                    format="A4",
                    print_background=True,
                    prefer_css_page_size=True,
                    margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
                )
                browser.close()

            logger.info(f"Successfully generated PDF: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            raise e
        finally:
            if os.path.exists(temp_html_path):
                try:
                    os.remove(temp_html_path)
                except Exception:
                    pass

    def generate_english_pdf(self, context: Dict[str, Any], filename: Optional[str] = None) -> str:
        """Generates English 'The Civils Vault' style Prelims + Mains + MCQ PDF"""
        ist_offset = timezone(timedelta(hours=5, minutes=30))
        today_str = datetime.now(ist_offset).strftime("%Y-%m-%d")

        if not filename:
            filename = f"CivilsVault_Analysis_{today_str}.pdf"
        output_path = os.path.join(OUTPUT_DIR, filename)

        html = self.render_html("civils_vault_en.html", context)
        return self.generate_pdf_from_html(html, output_path)

    def generate_kannada_pdf(self, context: Dict[str, Any], filename: Optional[str] = None) -> str:
        """Generates Kannada 'KPSCinsights' style Prajavani/Deccan Herald PDF"""
        ist_offset = timezone(timedelta(hours=5, minutes=30))
        today_str = datetime.now(ist_offset).strftime("%Y-%m-%d")

        if not filename:
            filename = f"KPSCinsights_Prajavani_{today_str}.pdf"
        output_path = os.path.join(OUTPUT_DIR, filename)

        html = self.render_html("kpsc_insights_kn.html", context)
        return self.generate_pdf_from_html(html, output_path)
