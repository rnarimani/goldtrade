from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

def get_chrome_driver():
    """تنظیمات مشترک Chrome برای همه فایل‌ها"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument(f'--user-data-dir=/tmp/chrome-data-{os.getpid()}')
    chrome_options.binary_location = "/usr/bin/chromium"
    
    # استفاده از selenium-manager
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(300)  # افزایش timeout به 5 دقیقه
    
    return driver

def get_headers():
    """تنظیمات مشترک headers برای درخواست‌ها"""
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    } 