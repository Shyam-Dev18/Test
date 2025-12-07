import os
import sys
import logging
from yt_dlp import YoutubeDL

# --- Configuration ---
# 1. Hardcoded video URL to test (use a publicly available video for initial tests)
VIDEO_URL = "https://www.youtube.com/watch?v=s78np22i9W8"  # Rickroll for testing!

# 2. Environment variable name where your cookie file path is stored
# Koyeb Secrets often set environment variables; e.g., COOKIE_FILE_PATH='/path/to/cookies.txt'
COOKIE_ENV_VAR = "COOKIE_FILE_PATH"

# 3. Output file path (Note: Koyeb uses ephemeral storage, this file will be lost after the process ends)
OUTPUT_TEMPLATE = 'downloaded_video.%(ext)s'

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def download_video_with_cookies():
    """Attempts to download the video using yt-dlp, reading cookies from the specified file."""
    
    # 1. Check for cookie file path environment variable
    cookie_file = os.environ.get(COOKIE_ENV_VAR)
    
    if not cookie_file:
        logging.error(f"❌ FAILED: Required environment variable '{COOKIE_ENV_VAR}' not found.")
        logging.info("Attempting download WITHOUT cookies.")
        # Continue without cookies if the path is missing
        ydl_opts = {'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
                    'outtmpl': OUTPUT_TEMPLATE}
    else:
        # 2. Verify the cookie file exists
        if not os.path.exists(cookie_file):
            logging.error(f"❌ FAILED: Cookie file not found at path: {cookie_file}")
            logging.info("Attempting download WITHOUT cookies.")
            ydl_opts = {'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
                        'outtmpl': OUTPUT_TEMPLATE}
        else:
            logging.info(f"🍪 SUCCESS: Using cookie file found at: {cookie_file}")
            # 3. Configure yt-dlp options
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]/bestvideo',
                'outtmpl': OUTPUT_TEMPLATE,
                'cookiefile': cookie_file,  # Use the path from the environment variable
                'noplaylist': True,
                'logger': logging.getLogger(), # Use the standard logger
                'quiet': False, # Make sure errors are printed
                'verbose': True # Detailed logging for better debugging on Koyeb
            }

    logging.info(f"Attempting to download video from: {VIDEO_URL}")

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([VIDEO_URL])
        
        logging.info("✅ SUCCESS: Video download attempt completed.")
        logging.info(f"Check logs for file saved as: {OUTPUT_TEMPLATE}")
        return True

    except Exception as e:
        logging.error(f"❌ FAILED: An error occurred during download.")
        # Log the full error message
        logging.error(e, exc_info=True)
        return False

if __name__ == "__main__":
    if not download_video_with_cookies():
        # Exit with a non-zero code to signal failure in a deployment environment
        sys.exit(1)