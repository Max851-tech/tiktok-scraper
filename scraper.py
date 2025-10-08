"""
TikTok Video Information Scraper
Using yt-dlp for reliable data extraction
"""

import csv
import os
import json
from datetime import datetime
from typing import List, Dict
import logging
import subprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TikTokScraper:
    """
    TikTok scraper class using yt-dlp for reliable extraction
    """
    
    def __init__(self, username: str, output_dir: str = "data", max_videos: int = 10):
        """
        Initialize the scraper
        
        Args:
            username: TikTok username to scrape
            output_dir: Directory to save CSV files
            max_videos: Maximum number of videos to scrape
        """
        self.username = username
        self.output_dir = output_dir
        self.max_videos = max_videos
        self.base_url = f"https://www.tiktok.com/@{username}"
        self._ensure_output_directory()
        
    def _ensure_output_directory(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logger.info(f"Created output directory: {self.output_dir}")
    
    def scrape_videos(self) -> List[Dict]:
        """
        Scrape video information from TikTok account using yt-dlp
        
        Returns:
            List of dictionaries containing video information
        """
        logger.info(f"Starting scrape for user: {self.username}")
        videos = []
        
        try:
            # yt-dlp command to extract video information
            cmd = [
                'yt-dlp',
                '--dump-json',
                '--playlist-end', str(self.max_videos),
                '--no-download',
                '--no-warnings',
                self.base_url
            ]
            
            logger.info(f"Executing yt-dlp for {self.base_url}")
            logger.info("This may take a few minutes...")
            
            # Run yt-dlp and capture output
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode != 0:
                logger.error(f"yt-dlp error: {result.stderr}")
                raise Exception(f"yt-dlp failed with return code {result.returncode}")
            
            # Parse JSON output (one JSON object per line)
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                    
                try:
                    video_info = json.loads(line)
                    
                    # Extract relevant information
                    video_data = {
                        "url": video_info.get('webpage_url', ''),
                        "description": video_info.get('description', 'No description')[:200],
                        "thumbnail": video_info.get('thumbnail', ''),
                        "views": video_info.get('view_count', 0),
                        "likes": video_info.get('like_count', 0),
                        "comments": video_info.get('comment_count', 0)
                    }
                    
                    videos.append(video_data)
                    logger.info(f"✓ Extracted video {len(videos)}: {video_data['url'][:50]}...")
                    
                    if len(videos) >= self.max_videos:
                        break
                        
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse JSON line: {e}")
                    continue
            
            logger.info(f"Successfully retrieved {len(videos)} videos")
            
        except subprocess.TimeoutExpired:
            logger.error("yt-dlp timed out after 5 minutes")
            raise
        except Exception as e:
            logger.error(f"Error during scraping: {str(e)}")
            raise
        
        return videos
    
    def export_to_csv(self, videos: List[Dict]) -> str:
        """
        Export video data to CSV file
        
        Args:
            videos: List of video dictionaries
            
        Returns:
            Path to the created CSV file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.username}_{timestamp}.csv"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['url', 'description', 'thumbnail', 'views', 'likes', 'comments']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                writer.writerows(videos)
                
            logger.info(f"Data exported successfully to: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error exporting to CSV: {str(e)}")
            raise
    
    def run(self) -> str:
        """
        Execute the complete scraping and export process
        
        Returns:
            Path to the created CSV file
        """
        logger.info("=" * 50)
        logger.info("TikTok Scraper Started (using yt-dlp)")
        logger.info("=" * 50)
        
        videos = self.scrape_videos()
        
        if not videos:
            logger.warning("No videos were scraped. Check if the username is correct.")
            videos = []
        
        filepath = self.export_to_csv(videos)
        
        logger.info("=" * 50)
        logger.info("Scraping completed!")
        logger.info(f"Total videos: {len(videos)}")
        logger.info(f"Output file: {filepath}")
        logger.info("=" * 50)
        
        return filepath


def main():
    """Main entry point"""
    # Configuration
    USERNAME = os.getenv("TIKTOK_USERNAME", "hugodecrypte")
    MAX_VIDEOS = int(os.getenv("MAX_VIDEOS", "10"))
    
    try:
        scraper = TikTokScraper(username=USERNAME, max_videos=MAX_VIDEOS)
        scraper.run()
        
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
