# dropbox_uploader.py
# Upload daily reports to Dropbox

import os
import json
from datetime import datetime
from config.settings import (
    DROPBOX_ACCESS_TOKEN, DATA_DIR, EXCEL_DIR, FILTERED_NEWS_DIR, QUIZ_DIR
)
from config.logger import setup_logger

logger = setup_logger("dropbox_uploader")


class DropboxUploader:
    """
    Uploads daily reports to Dropbox.
    
    Setup:
    1. Go to https://www.dropbox.com/developers/apps
    2. Create an app (Scoped access)
    3. Generate access token
    4. Add to GitHub secrets as DROPBOX_ACCESS_TOKEN
    """
    
    def __init__(self):
        self.access_token = DROPBOX_ACCESS_TOKEN
        self.base_path = ""  # Root of your Dropbox folder
        self.enabled = bool(self.access_token and self.access_token != 'PASTE_HERE')
        
    def upload_file(self, local_path, dropbox_path):
        """Upload a single file to Dropbox"""
        if not self.enabled:
            logger.warning("Dropbox not configured - skipping upload")
            return False
            
        try:
            import dropbox
            dbx = dropbox.Dropbox(self.access_token)
            
            with open(local_path, 'rb') as f:
                content = f.read()
            
            result = dbx.files_upload(
                content, 
                f"{self.base_path}/{dropbox_path}",
                mode=dropbox.files.WriteMode.overwrite
            )
            logger.info(f"Uploaded: {dropbox_path}")
            return True
            
        except Exception as e:
            logger.error(f"Upload failed: {e}")
            return False
    
    def upload_folder(self, local_folder, dropbox_folder):
        """Upload all files in a folder to Dropbox"""
        if not self.enabled or not os.path.exists(local_folder):
            return 0
            
        uploaded = 0
        for root, dirs, files in os.walk(local_folder):
            for file in files:
                if file.endswith(('.json', '.xlsx', '.log')):
                    local_path = os.path.join(root, file)
                    relative_path = os.path.relpath(local_path, local_folder)
                    dropbox_path = f"{dropbox_folder}/{relative_path}"
                    
                    if self.upload_file(local_path, dropbox_path):
                        uploaded += 1
        return uploaded
    
    def upload_all_reports(self):
        """Upload all daily reports to Dropbox"""
        if not self.enabled:
            logger.warning("Dropbox not configured - skipping")
            return 0
            
        today = datetime.now().strftime('%Y-%m-%d')
        total_uploaded = 0
        
        # Upload Excel reports
        logger.info("Uploading Excel reports...")
        total_uploaded += self.upload_folder(EXCEL_DIR, f"excel_reports/{today}")
        
        # Upload filtered news
        logger.info("Uploading filtered news...")
        total_uploaded += self.upload_folder(FILTERED_NEWS_DIR, f"filtered_news/{today}")
        
        # Upload quizzes
        logger.info("Uploading quizzes...")
        total_uploaded += self.upload_folder(QUIZ_DIR, f"quizzes/{today}")
        
        logger.info(f"Dropbox upload complete: {total_uploaded} files")
        return total_uploaded


if __name__ == "__main__":
    uploader = DropboxUploader()
    if uploader.enabled:
        print("Uploading to Dropbox...")
        count = uploader.upload_all_reports()
        print(f"Done! Uploaded {count} files.")
    else:
        print("Dropbox not configured. Set DROPBOX_ACCESS_TOKEN in config/settings.py")
