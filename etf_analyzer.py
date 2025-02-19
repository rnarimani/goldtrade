import requests
from bs4 import BeautifulSoup
import pandas as pd
import coin_price_calculator as cpc
import streamlit as st
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import chrome_config


class GoldETFAnalyzer:
    def __init__(self):
        # اطلاعات پایه صندوق‌های طلا
        self.gold_etf_info = {
            'طلا': {  # لوتوس
                'name': 'صندوق سرمایه پشتوانه لوتوس',
                'gold_weight': 0.01,  # هر واحد معادل 0.01 گرم طلای 24 عیار
                'gold_purity': 1.000  # طلای 24 عیار
            },
            'عیار': {  # کیان
                'name': 'صندوق طلای کیان',
                'gold_weight': 0.01,
                'gold_purity': 1.000
            },
            'مفید': {
                'name': 'صندوق سرمایه گذاری پشتوانه طلای مفید',
                'gold_weight': 0.01,
                'gold_purity': 1.000
            },
            'زر': {  # زرافشان
                'name': 'صندوق پشتوانه سکه طلای زرافشان امید ایرانیان',
                'gold_weight': 0.01,
                'gold_purity': 1.000
            },
            'کزر': {  # کیمیای زرین
                'name': 'صندوق سرمایه گذاری طلای کیمیای زرین کاردان',
                'gold_weight': 0.01,
                'gold_purity': 1.000
            },
            'صبا': {
                'name': 'صندوق سرمایه گذاری مبتنی بر طلای صبا',
                'gold_weight': 0.01,
                'gold_purity': 1.000
            },
            'زرفام': {
                'name': 'صندوق سرمایه گذاری مبتنی بر طلای زرفام آشنا',
                'gold_weight': 0.01,
                'gold_purity': 1.000
            },
            'زرین': {
                'name': 'صندوق سرمایه گذاری زرین آگاه',
                'gold_weight': 0.01,
                'gold_purity': 1.000
            },
            'تابان': {
                'name': 'صندوق سرمایه گذاری تابان تمدن',
                'gold_weight': 0.01,
                'gold_purity': 1.000
            },
            'زاگرس': {
                'name': 'صندوق سرمایه گذاری زاگرس',
                'gold_weight': 0.01,
                'gold_purity': 1.000
            },
            'آلتون': {
                'name': 'صندوق سرمایه گذاری آسمان آلتون',
                'gold_weight': 0.01,
                'gold_purity': 1.000
            }
        }
        self.gold_etfs = {}  # این دیکشنری با اطلاعات صندوق‌ها پر خواهد شد
        self.get_all_gold_etfs()
    
    def get_all_gold_etfs(self):
        """دریافت لیست همه صندوق‌های طلا از tradersarena"""
        try:
            print("Getting ETF list from tradersarena...")
            
            # استفاده از تنظیمات مشترک Chrome و headers
            driver = chrome_config.get_chrome_driver()
            headers = chrome_config.get_headers()
            
            try:
                driver.get('https://tradersarena.ir/industries/68f')
                
                # افزایش زمان انتظار
                wait = WebDriverWait(driver, 60)  # افزایش به 60 ثانیه
                table = wait.until(EC.presence_of_element_located((By.ID, 'navTable')))
                time.sleep(10)  # افزایش به 10 ثانیه
                
                # پیدا کردن ردیف‌های جدول
                rows = table.find_elements(By.TAG_NAME, 'tr')
                print(f"Found {len(rows)} rows")
                
                for row in rows[1:]:
                    try:
                        cols = row.find_elements(By.TAG_NAME, 'td')
                        if len(cols) >= 6:
                            symbol_element = cols[0].find_element(By.TAG_NAME, 'a')
                            symbol = symbol_element.text.strip()
                            
                            if symbol and symbol not in ['حداقل', 'حداکثر']:
                                self.gold_etfs[symbol] = {
                                    'name': symbol_element.get_attribute('href').split('/')[-1],
                                    'gold_weight': 0.01,
                                    'gold_purity': 1.000
                                }
                                print(f"Added ETF: {symbol}")
                                
                    except Exception as e:
                        print(f"Error parsing row: {str(e)}")
                        continue
                
            finally:
                driver.quit()
                
            print(f"Total gold ETFs found: {len(self.gold_etfs)}")
            
        except Exception as e:
            print(f"Error getting ETF list: {str(e)}")
            # اگر خطا رخ داد، از لیست پیش‌فرض استفاده کنیم
            self.gold_etfs = self.gold_etf_info
    
    def convert_volume(self, volume_text):
        """تبدیل متن حجم معاملات به عدد"""
        try:
            print(f"Converting volume: '{volume_text}'")  # Debug
            
            if not volume_text or volume_text == '-':
                return 0
                
            # حذف همه فاصله‌ها و کاماها
            volume_text = volume_text.replace(',', '').replace(' ', '')
            
            # تبدیل B به میلیارد
            if 'B' in volume_text:
                number = float(volume_text.replace('B', ''))
                result = int(number * 1000000000)
                print(f"Converted B: {volume_text} -> {result}")
                return result
                
            # تبدیل K به هزار
            if 'K' in volume_text:
                number = float(volume_text.replace('K', ''))
                result = int(number * 1000)
                print(f"Converted K: {volume_text} -> {result}")
                return result
                
            # تبدیل M به میلیون
            if 'M' in volume_text:
                number = float(volume_text.replace('M', ''))
                result = int(number * 1000000)
                print(f"Converted M: {volume_text} -> {result}")
                return result
                
            # اگر عدد ساده باشد
            result = int(float(volume_text))
            print(f"Converted plain: {volume_text} -> {result}")
            return result
            
        except (ValueError, TypeError) as e:
            print(f"Error converting volume '{volume_text}': {str(e)}")
            return 0

    def test_volume_conversion(self):
        """تست تبدیل حجم معاملات"""
        test_cases = [
            "19.4 M",
            "980.3 K",
            "4.8 M",
            "2.8 M",
            "3.5 M"
        ]
        
        print("\nTesting volume conversion:")
        for test in test_cases:
            result = self.convert_volume(test)
            print(f"Input: {test} -> Output: {result:,}")
            
    def clean_number(self, text):
        """تمیز کردن متن عددی از کاما، فاصله و پسوندها"""
        if not text or text == '-':
            return None
            
        # حذف کاما و فاصله
        text = text.replace(',', '').replace(' ', '').strip()
        
        try:
            # حذف پسوندها
            for suffix in ['B', 'M', 'K']:
                if suffix in text:
                    number = float(text.replace(suffix, ''))
                    if suffix == 'B':
                        return str(number * 1000000000)
                    elif suffix == 'M':
                        return str(number * 1000000)
                    elif suffix == 'K':
                        return str(number * 1000)
            
            return text
            
        except Exception as e:
            print(f"Error cleaning number '{text}': {str(e)}")
            return None
        
    def get_market_data(self):
        """دریافت اطلاعات صندوق‌ها از tradersarena با استفاده از selenium"""
        try:
            print("\nGetting market data from tradersarena...")
            
            driver = chrome_config.get_chrome_driver()
            
            try:
                driver.get('https://tradersarena.ir/industries/68f')
                
                # صبر برای لود شدن جدول
                wait = WebDriverWait(driver, 60)
                
                # صبر برای لود شدن کل صفحه
                wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                time.sleep(3)
                
                # صبر برای لود شدن جدول
                table = wait.until(EC.presence_of_element_located((By.ID, 'industriesTable')))
                time.sleep(3)
                
                # صبر برای لود شدن محتوای جدول
                wait.until(EC.presence_of_element_located((By.XPATH, "//table[@id='industriesTable']//tbody//tr[1]//td[1]//a")))
                time.sleep(3)
                
                # پیدا کردن ردیف‌ها
                rows = table.find_elements(By.XPATH, ".//tbody//tr[not(@id='minrow') and not(@id='maxrow')]")
                
                if len(rows) <= 0:
                    raise Exception("No rows found in table")
                    
                print(f"Found {len(rows)} rows")
                
                etf_data = {}
                
                for row in rows:
                    try:
                        # صبر برای لود شدن هر ردیف
                        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'td')))
                        cells = row.find_elements(By.TAG_NAME, 'td')
                        
                        if len(cells) < 10 or not cells[0].find_elements(By.TAG_NAME, 'a'):
                            continue
                            
                        symbol = cells[0].find_element(By.TAG_NAME, 'a').text.strip()
                        name = cells[0].find_element(By.TAG_NAME, 'a').get_attribute('title') or symbol
                        volume_text = cells[1].text.strip()
                        price_text = cells[3].text.strip()  # قیمت آخرین معامله
                        nav_text = cells[4].text.strip()  # NAV
                        bubble_text = cells[5].text.strip().replace('%', '')  # حباب
                        
                        print(f"Processing row - Symbol: {symbol}, Volume: {volume_text}, Price: {price_text}, NAV: {nav_text}")
                        
                        if symbol and symbol not in ['حداقل', 'حداکثر']:
                            volume = self.convert_volume(volume_text)
                            
                            # تمیز کردن اعداد
                            price_text = self.clean_number(price_text)
                            nav_text = self.clean_number(nav_text)
                            
                            if nav_text and price_text:
                                try:
                                    price = float(price_text)
                                    nav = float(nav_text)
                                    bubble = float(bubble_text) if bubble_text and bubble_text != '-' else 0
                                    
                                    if nav > 0 and price > 0:  # اطمینان از معتبر بودن اعداد
                                        etf_data[symbol] = {
                                            'name': name,
                                            'price': price * 10,
                                            'nav': nav * 10,
                                            'bubble': bubble,
                                            'volume': volume
                                        }
                                        print(f"Added data for {symbol}: Price={price:,}, NAV={nav:,}, Volume={volume:,}")
                                    else:
                                        print(f"Invalid numbers for {symbol}: Price={price}, NAV={nav}")
                                    
                                except ValueError as e:
                                    print(f"Error converting numbers for {symbol}: {str(e)}, Raw Price: '{price_text}', Raw NAV: '{nav_text}'")
                                    continue
                                
                    except Exception as e:
                        print(f"Error parsing row: {str(e)}")
                        continue
                
                if not etf_data:
                    raise Exception("No ETF data could be extracted")
                    
            finally:
                driver.quit()
                
            return etf_data
            
        except Exception as e:
            print(f"Error getting market data: {str(e)}")
            return {}

    def calculate_gold_value(self, gold_prices):
        """محاسبه حباب صندوق‌ها با استفاده از NAV"""
        try:
            market_data = self.get_market_data()
            if not market_data:
                return None
            
            print("\nProcessing market data:")  # Debug
            for symbol, data in market_data.items():
                print(f"{symbol}: Volume={data['volume']:,}, Name={data['name']}")  # Debug
            
            etf_data = {}
            for symbol, data in market_data.items():
                if data['nav'] > 0:  # فقط صندوق‌های فعال
                    etf_data[symbol] = {
                        'name': data['name'],
                        'price': data['price'],
                        'gold_value': data['nav'],
                        'bubble': data['bubble'],
                        'volume': data['volume']
                    }
                    print(f"Added to etf_data: {symbol} with volume {data['volume']:,}")  # Debug
            
            return etf_data
            
        except Exception as e:
            print(f"Error calculating values: {str(e)}")
            return None
    
    @st.cache_data(ttl=300)
    def get_market_price(self, symbol):
        try:
            # استفاده از headers مشترک
            headers = chrome_config.get_headers()
            
            url = f"http://cdn.tsetmc.com/api/Instrument/GetInstrumentPriceData/{symbol}"
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data and 'closingPriceData' in data:
                    return float(data['closingPriceData']['finalPrice'])
            
            return 0
            
        except Exception as e:
            print(f"Error getting market price for {symbol}: {str(e)}")
            return 0
    
    @st.cache_data(ttl=300)
    def get_trading_volume(self, symbol):
        try:
            # استفاده از headers مشترک
            headers = chrome_config.get_headers()
            
            url = f"http://cdn.tsetmc.com/api/Instrument/GetInstrumentPriceData/{symbol}"
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data and 'closingPriceData' in data:
                    return int(data['closingPriceData']['volume'])
            
            return 0
            
        except Exception as e:
            print(f"Error getting volume for {symbol}: {str(e)}")
            return 0
    
    def get_analysis(self):
        """تحلیل جامع صندوق‌های طلا"""
        # دریافت قیمت‌های طلا
        gold_prices = cpc.get_prices()
        if not gold_prices:
            return None
        
        # محاسبه ارزش و حباب صندوق‌ها
        etf_data = self.calculate_gold_value(gold_prices)
        if not etf_data:
            return None
        
        # یافتن بهترین گزینه‌ها
        analysis = {
            'lowest_bubble': min(etf_data.items(), key=lambda x: x[1]['bubble']),
            'highest_volume': max(etf_data.items(), key=lambda x: x[1]['volume']),
            'all_funds': etf_data
        }
        
        # تولید توصیه‌ها
        recommendations = self.get_recommendations(etf_data)
        
        analysis['recommendations'] = recommendations
        analysis['market_stats'] = {
            'avg_bubble': sum(data['bubble'] for data in etf_data.values()) / len(etf_data),
            'std_bubble': (sum((data['bubble'] - sum(data['bubble'] for data in etf_data.values()) / len(etf_data)) ** 2 for data in etf_data.values()) / len(etf_data)) ** 0.5,
            'avg_volume': sum(data['volume'] for data in etf_data.values()) / len(etf_data)
        }
        return analysis

    def get_recommendations(self, funds_data):
        """Generate investment recommendations based on analysis"""
        recommendations = []
        
        # Find funds with low bubble
        low_bubble_funds = [
            (symbol, data) for symbol, data in funds_data.items() 
            if data['bubble'] < 2
        ]
        if low_bubble_funds:
            symbols = ', '.join(symbol for symbol, _ in low_bubble_funds)
            recommendations.append(
                f"{symbols} have minimal bubble (<2%). Good options for investment."
            )
        
        # Find funds with high volume
        high_volume_funds = [
            (symbol, data) for symbol, data in funds_data.items()
            if data['volume'] > 1000000
        ]
        if high_volume_funds:
            symbols = ', '.join(symbol for symbol, _ in high_volume_funds)
            recommendations.append(
                f"{symbols} have high trading volume. Better liquidity for large trades."
            )
        
        # Warning for high bubble funds
        high_bubble_funds = [
            (symbol, data) for symbol, data in funds_data.items()
            if data['bubble'] > 5
        ]
        if high_bubble_funds:
            symbols = ', '.join(symbol for symbol, _ in high_bubble_funds)
            recommendations.append(
                f"Caution: {symbols} have high bubble (>5%). Consider waiting for better prices."
            )
        
        # Warning for low volume funds
        low_volume_funds = [
            (symbol, data) for symbol, data in funds_data.items()
            if data['volume'] < 100000
        ]
        if low_volume_funds:
            symbols = ', '.join(symbol for symbol, _ in low_volume_funds)
            recommendations.append(
                f"Note: {symbols} have low trading volume. May be difficult to trade large amounts."
            )
        
        return recommendations

    def print_analysis(self):
        """Print formatted analysis"""
        analysis = self.get_analysis()
        if not analysis:
            return
            
        print("\n=== Gold ETF Analysis ===")
        print("\nFund Prices and Premiums:")
        for symbol, data in analysis['all_funds'].items():
            print(f"{symbol} ({data['name']})")
            print(f"  Price: {data['price']:,.0f}")
            print(f"  Gold Value: {data['gold_value']:,.0f}")
            print(f"  Bubble: {data['bubble']:+.1f}%")
            print(f"  Volume: {data['volume']:,}")
            
        print("\nRecommendations:")
        for rec in analysis['recommendations']:
            print(f"• {rec}")

def main():
    """اجرای مستقل تحلیل صندوق‌های طلا"""
    try:
        print("تحلیل صندوق‌های طلا")
        print("-" * 50)
        
        analyzer = GoldETFAnalyzer()
        analysis = analyzer.get_analysis()
        
        if analysis and analysis['all_funds']:
            # نمایش جدول اطلاعات صندوق‌ها
            print("\nاطلاعات صندوق‌های طلا:")
            print("{:<10} {:<40} {:>15} {:>15} {:>10} {:>15}".format(
                "نماد", "نام صندوق", "قیمت (تومان)", "NAV (تومان)", "حباب %", "حجم معاملات"
            ))
            print("-" * 105)
            
            for symbol, data in analysis['all_funds'].items():
                print("{:<10} {:<40} {:>15,.0f} {:>15,.0f} {:>10.1f} {:>15,}".format(
                    symbol,
                    data['name'],
                    data['price'] / 10,  # تبدیل به تومان
                    data['gold_value'] / 10,
                    data['bubble'],
                    data['volume']
                ))
            
            # نمایش توصیه‌ها
            if analysis['recommendations']:
                print("\nتوصیه‌های سرمایه‌گذاری:")
                for rec in analysis['recommendations']:
                    print(f"• {rec}")
            else:
                print("\nدر حال حاضر همه صندوق‌ها در محدوده قیمتی منطقی معامله می‌شوند.")
            
            # نمایش بهترین گزینه‌ها
            lowest_bubble = analysis['lowest_bubble']
            highest_volume = analysis['highest_volume']
            
            print("\nبهترین گزینه‌ها:")
            print(f"• کمترین حباب: {lowest_bubble[0]} با {lowest_bubble[1]['bubble']:.1f}% حباب")
            print(f"• بیشترین حجم معامله: {highest_volume[0]} با {highest_volume[1]['volume']:,} واحد")
            
        else:
            print("خطا در دریافت اطلاعات صندوق‌ها")
            
    except Exception as e:
        print(f"خطا در اجرای برنامه: {str(e)}")

if __name__ == "__main__":
    main() 