# excel_saver.py
# Works WITHOUT pandas — uses only openpyxl

import os
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime

from config.settings import EXCEL_DIR
from config.logger import setup_logger

logger = setup_logger("excel")


class ExcelSaver:

    def __init__(self):
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.daily_file = os.path.join(EXCEL_DIR, f"daily_report_{self.today}.xlsx")
        self.master_file = os.path.join(EXCEL_DIR, "master_database.xlsx")

        self.header_font = Font(bold=True, color="FFFFFF", size=11)
        self.header_fill = PatternFill(start_color="2F5496", end_color="2F5496", fill_type="solid")
        self.border = Border(
            left=Side(style='thin'), right=Side(style='thin'),
            top=Side(style='thin'), bottom=Side(style='thin')
        )

    def _write_sheet(self, wb, sheet_name, headers, rows):
        if sheet_name in wb.sheetnames:
            del wb[sheet_name]
        ws = wb.create_sheet(sheet_name)

        for col, h in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=h)
            cell.font = self.header_font
            cell.fill = self.header_fill
            cell.alignment = Alignment(horizontal='center', wrap_text=True)
            cell.border = self.border

        for row_idx, row_data in enumerate(rows, 2):
            for col_idx, value in enumerate(row_data, 1):
                cell = ws.cell(row=row_idx, column=col_idx, value=str(value) if value else "")
                cell.border = self.border
                cell.alignment = Alignment(wrap_text=True)

        for col in range(1, len(headers) + 1):
            max_len = len(str(headers[col - 1]))
            for row in range(2, len(rows) + 2):
                val = ws.cell(row=row, column=col).value
                if val:
                    max_len = max(max_len, min(len(str(val)), 50))
            ws.column_dimensions[get_column_letter(col)].width = max_len + 2

        return ws

    def _ensure_daily_file(self):
        if not os.path.exists(self.daily_file):
            wb = Workbook()
            wb.remove(wb.active)
            wb.save(self.daily_file)

    def save_scraped_news(self, articles):
        logger.info(f"Saving {len(articles)} scraped articles to Excel...")
        self._ensure_daily_file()

        headers = ['S.No', 'Date', 'Scraped At', 'Source', 'Title', 'Link', 'Content Length']
        rows = []
        for i, a in enumerate(articles, 1):
            rows.append([
                i, a.get('date', self.today), a.get('scraped_at', self.timestamp),
                a.get('source', ''), a.get('title', ''), a.get('link', ''),
                len(a.get('content', ''))
            ])

        wb = load_workbook(self.daily_file)
        self._write_sheet(wb, 'Raw News', headers, rows)
        wb.save(self.daily_file)
        logger.info(f"   Saved to: {self.daily_file}")

    def save_filtered_news(self, filtered_articles, stats):
        logger.info(f"Saving {len(filtered_articles)} filtered articles...")

        headers = ['S.No', 'Date', 'Filtered At', 'Category', 'Importance',
                    'Title', 'Source', 'Summary', 'Key Facts', 'Link']
        rows = []
        for i, a in enumerate(filtered_articles, 1):
            ev = a.get('evaluation', {})
            rows.append([
                i, a.get('date', self.today), a.get('filtered_at', self.timestamp),
                ev.get('category', ''), ev.get('importance', 0),
                a.get('title', ''), a.get('source', ''),
                ev.get('one_line_summary', ''),
                ', '.join(ev.get('key_facts', [])), a.get('link', '')
            ])

        wb = load_workbook(self.daily_file)
        self._write_sheet(wb, 'Filtered News', headers, rows)

        stat_headers = ['Metric', 'Value', 'Timestamp']
        stat_rows = [
            ['Date', self.today, self.timestamp],
            ['Total Scraped', stats.get('total', 0), ''],
            ['Keyword Passed', stats.get('keyword_passed', 0), ''],
            ['Keyword Skipped', stats.get('keyword_skipped', 0), ''],
            ['AI Relevant', stats.get('ai_relevant', 0), ''],
            ['AI Not Relevant', stats.get('ai_not_relevant', 0), ''],
            ['AI Errors', stats.get('ai_errors', 0), ''],
            ['Final Selected', stats.get('final_selected', 0), ''],
        ]
        self._write_sheet(wb, 'Statistics', stat_headers, stat_rows)
        wb.save(self.daily_file)

    def save_posts(self, post_data):
        if not post_data:
            return
        logger.info(f"Saving {len(post_data)} posts to Excel...")

        headers = list(post_data[0].keys())
        rows = [[p.get(h, '') for h in headers] for p in post_data]

        wb = load_workbook(self.daily_file)
        self._write_sheet(wb, 'Generated Posts', headers, rows)
        wb.save(self.daily_file)

    def save_quiz(self, questions):
        logger.info(f"Saving {len(questions)} quiz questions to Excel...")

        headers = ['Q.No', 'Date', 'Time', 'Category', 'Question',
                    'Option A', 'Option B', 'Option C', 'Option D',
                    'Answer', 'Explanation', 'Source Article']
        rows = []
        for q in questions:
            rows.append([
                q.get('question_number', ''), q.get('date', self.today),
                q.get('generated_at', self.timestamp), q.get('category', ''),
                q.get('question', ''), q.get('option_a', ''),
                q.get('option_b', ''), q.get('option_c', ''),
                q.get('option_d', ''), q.get('correct_answer', ''),
                q.get('explanation', ''), q.get('source_article', ''),
            ])

        wb = load_workbook(self.daily_file)
        self._write_sheet(wb, 'Quiz Questions', headers, rows)
        wb.save(self.daily_file)

    def save_posting_log(self, post_type, status, details=""):
        wb = load_workbook(self.daily_file)

        if 'Posting Log' not in wb.sheetnames:
            ws = wb.create_sheet('Posting Log')
            for col, h in enumerate(['Date', 'Time', 'Type', 'Status', 'Details'], 1):
                cell = ws.cell(row=1, column=col, value=h)
                cell.font = self.header_font
                cell.fill = self.header_fill
                cell.border = self.border
        else:
            ws = wb['Posting Log']

        next_row = ws.max_row + 1
        values = [self.today, datetime.now().strftime("%H:%M:%S"),
                  post_type, status, details]
        for col, val in enumerate(values, 1):
            cell = ws.cell(row=next_row, column=col, value=val)
            cell.border = self.border
        wb.save(self.daily_file)

    def update_master(self, filtered_articles, questions):
        logger.info("Updating master database...")

        if os.path.exists(self.master_file):
            wb = load_workbook(self.master_file)
        else:
            wb = Workbook()
            wb.remove(wb.active)

        # All News sheet
        if 'All News' not in wb.sheetnames:
            ws = wb.create_sheet('All News')
            news_headers = ['Date', 'Time', 'Category', 'Importance',
                            'Title', 'Source', 'Summary', 'Key Facts', 'Link']
            for col, h in enumerate(news_headers, 1):
                cell = ws.cell(row=1, column=col, value=h)
                cell.font = self.header_font
                cell.fill = self.header_fill
                cell.border = self.border
        else:
            ws = wb['All News']

        for a in filtered_articles:
            ev = a.get('evaluation', {})
            next_row = ws.max_row + 1
            values = [
                a.get('date', self.today), a.get('filtered_at', self.timestamp),
                ev.get('category', ''), ev.get('importance', 0),
                a.get('title', ''), a.get('source', ''),
                ev.get('one_line_summary', ''),
                ', '.join(ev.get('key_facts', [])), a.get('link', '')
            ]
            for col, val in enumerate(values, 1):
                cell = ws.cell(row=next_row, column=col, value=str(val))
                cell.border = self.border

        # All Quiz sheet
        if 'All Quiz' not in wb.sheetnames:
            ws2 = wb.create_sheet('All Quiz')
            quiz_headers = ['Date', 'Time', 'Category', 'Question',
                            'A', 'B', 'C', 'D', 'Answer', 'Explanation']
            for col, h in enumerate(quiz_headers, 1):
                cell = ws2.cell(row=1, column=col, value=h)
                cell.font = self.header_font
                cell.fill = self.header_fill
                cell.border = self.border
        else:
            ws2 = wb['All Quiz']

        for q in questions:
            next_row = ws2.max_row + 1
            values = [
                q.get('date', self.today), q.get('generated_at', ''),
                q.get('category', ''), q.get('question', ''),
                q.get('option_a', ''), q.get('option_b', ''),
                q.get('option_c', ''), q.get('option_d', ''),
                q.get('correct_answer', ''), q.get('explanation', '')
            ]
            for col, val in enumerate(values, 1):
                cell = ws2.cell(row=next_row, column=col, value=str(val))
                cell.border = self.border

        wb.save(self.master_file)
        logger.info(f"   Master DB updated")