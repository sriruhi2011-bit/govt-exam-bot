# google_drive_uploader.py
# Uploads reports to Google Drive automatically

import os
import json
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from config.settings import DATA_DIR, EXCEL_DIR, FILTERED_NEWS_DIR, QUIZ_DIR
from config.logger import setup_logger

logger = setup_logger("drive_uploader")


class GoogleDriveUploader:
    """
    Uploads files to Google Drive after each bot run.
    
    Setup required:
    1. Create Google Cloud Project
    2. Enable Google Drive API
    3. Create Service Account and download JSON key file
    4. Share a folder with service account email
    5. Add FOLDER_ID and SERVICE_ACCOUNT_FILE to secrets
    """
    
    def __init__(self):
        from config.settings import GDRIVE_FOLDER_ID, GDRIVE_SERVICE_ACCOUNT_FILE
        
        self.folder_id = GDRIVE_FOLDER_ID
        # Check for env override (GitHub Actions)
        if os.environ.get('GDRIVE_FOLDER_ID'):
            self.folder_id = os.environ.get('GDRIVE_FOLDER_ID')
        
        self.credentials_file = GDRIVE_SERVICE_ACCOUNT_FILE
        # Check for env override (GitHub Actions)
        if os.environ.get('GDRIVE_SERVICE_ACCOUNT_FILE'):
            self.credentials_file = os.environ.get('GDRIVE_SERVICE_ACCOUNT_FILE')
        
        self.credentials = None
        self.service = None
    
    def authenticate(self):
        """Authenticate with Google Drive using service account"""
        try:
            logger.info(f"Folder ID: {self.folder_id}")
            logger.info(f"Credentials file: {self.credentials_file}")
            
            if not self.credentials_file or not self.folder_id:
                logger.warning("Google Drive not configured - skipping upload")
                return False
            
            # Check if credentials file exists
            if not os.path.exists(self.credentials_file):
                logger.warning(f"Service account file not found: {self.credentials_file}")
                return False
            
            # Debug: show file size
            file_size = os.path.getsize(self.credentials_file)
            logger.info(f"Service account file size: {file_size} bytes")
            
            self.credentials = service_account.Credentials.from_service_account_file(
                self.credentials_file,
                scopes=['https://www.googleapis.com/auth/drive.file']
            )
            
            self.service = build('drive', 'v3', credentials=self.credentials)
            logger.info("Authenticated with Google Drive")
            return True
            
        except Exception as e:
            logger.error(f"Google Drive authentication failed: {e}")
            return False
    
    def upload_file(self, file_path, file_name=None):
        """Upload a single file to Google Drive"""
        if not self.service:
            return False
        
        try:
            if not os.path.exists(file_path):
                logger.warning(f"File not found: {file_path}")
                return False
            
            if file_name is None:
                file_name = os.path.basename(file_path)
            
            # Add date prefix for organization
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            drive_file_name = f"{today}_{file_name}"
            
            # Upload file
            media = MediaFileUpload(file_path, resumable=True)
            
            file_metadata = {
                'name': drive_file_name,
                'parents': [self.folder_id]
            }
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name'
            ).execute()
            
            logger.info(f"Uploaded {drive_file_name} to Google Drive (ID: {file.get('id')})")
            return True
            
        except Exception as e:
            logger.error(f"Upload failed: {e}")
            return False
    
    def upload_all_reports(self):
        """Upload all daily reports to Google Drive"""
        if not self.authenticate():
            logger.warning("Skipping Google Drive upload - not authenticated")
            return False
        
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        uploaded = 0
        failed = 0
        
        # Upload Excel daily report
        excel_file = os.path.join(EXCEL_DIR, f"daily_report_{today}.xlsx")
        if self.upload_file(excel_file):
            uploaded += 1
        else:
            failed += 1
        
        # Upload filtered news
        filtered_file = os.path.join(FILTERED_NEWS_DIR, f"filtered_{today}.json")
        if self.upload_file(filtered_file):
            uploaded += 1
        else:
            failed += 1
        
        # Upload quiz
        quiz_file = os.path.join(QUIZ_DIR, f"quiz_{today}.json")
        if self.upload_file(quiz_file):
            uploaded += 1
        else:
            failed += 1
        
        # Upload master database
        master_file = os.path.join(EXCEL_DIR, "master_database.xlsx")
        if self.upload_file(master_file):
            uploaded += 1
        else:
            failed += 1
        
        logger.info(f"Google Drive upload complete: {uploaded} uploaded, {failed} failed")
        return uploaded > 0


# Standalone test
if __name__ == "__main__":
    print("Testing Google Drive upload...")
    uploader = GoogleDriveUploader()
    result = uploader.upload_all_reports()
    if result:
        print("✅ Upload successful!")
    else:
        print("❌ Upload failed - check configuration")
