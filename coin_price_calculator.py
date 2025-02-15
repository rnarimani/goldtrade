from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
from tabulate import tabulate
import colorama
from colorama import Fore, Style

colorama.init()

def get_crypto_gold_prices():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Get PAXG price from Mexc
        paxg_response = requests.get('https://www.mexc.com/open/api/v2/market/ticker?symbol=PAXG_USDT', headers=headers)
        paxg_data = paxg_response.json()['data'][0]
        paxg_price = float(paxg_data['last'])
        
        # Get XAUT price from Mexc
        xaut_response = requests.get('https://www.mexc.com/open/api/v2/market/ticker?symbol=XAUT_USDT', headers=headers)
        xaut_data = xaut_response.json()['data'][0]
        xaut_price = float(xaut_data['last'])
        
        print(f"Successfully got crypto prices - PAXG: ${paxg_price}, XAUT: ${xaut_price}")
        return {'paxg': paxg_price, 'xaut': xaut_price}
    except Exception as e:
        print(f"Error getting crypto gold prices: {str(e)}")
        print("Response content for debugging:")
        try:
            print("PAXG response:", paxg_response.text)
            print("XAUT response:", xaut_response.text)
        except:
            pass
        return {'paxg': 0, 'xaut': 0}

def get_prices():
    # Coin weights in grams
    FULL_COIN_WEIGHT = 8.133
    HALF_COIN_WEIGHT = 4.068
    QUARTER_COIN_WEIGHT = 2.034
    
    # Constants for gold price calculation
    GOLD_PURITY_18K = 0.750  # 18K gold is 75% pure
    GRAM_TO_OUNCE = 31.1035  # 1 ounce = 31.1035 grams
    
    try:
        # Setup Chrome options
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # Initialize the driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # First get local prices from bon-bast
        driver.get("https://bon-bast.com")
        wait = WebDriverWait(driver, 20)
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
        
        # Wait for dynamic content to load
        time.sleep(5)
        
        # Scroll down to make sure all content is loaded
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        def get_coin_price(coin_id):
            try:
                # Wait for the element to be present
                wait.until(EC.presence_of_element_located((By.ID, coin_id)))
                
                # Get the price element
                price_element = driver.find_element(By.ID, coin_id)
                price_text = price_element.text.strip()
                
                # Convert price text to integer (remove commas)
                price = int(''.join(filter(str.isdigit, price_text)))
                return price
            except Exception as e:
                print(f"Error getting price for {coin_id}: {str(e)}")
                return 0
        
        def get_usd_price():
            try:
                # Wait for the USD price element to be present
                wait.until(EC.presence_of_element_located((By.ID, "usd1")))
                
                # Get the USD sell price
                price_element = driver.find_element(By.ID, "usd1")
                price_text = price_element.text.strip()
                
                # Convert price text to integer (remove commas)
                price = int(''.join(filter(str.isdigit, price_text)))
                return price
            except Exception as e:
                print(f"Error getting USD price: {str(e)}")
                return 0
        
        def get_global_gold_price():
            try:
                # Wait for the gold price panel to be present
                wait.until(EC.presence_of_element_located((By.ID, "ounce_top")))
                
                # Get the gold price
                price_element = driver.find_element(By.ID, "ounce_top")
                price_text = price_element.text.strip()
                
                # Convert price text to float (remove commas)
                price = float(price_text.replace(',', ''))
                return price
            except Exception as e:
                print(f"Error getting global gold price: {str(e)}")
                return 0
        
        def get_gold_price():
            try:
                # Wait for the gold price element to be present
                wait.until(EC.presence_of_element_located((By.ID, "gol18")))
                
                # Get the gold price
                price_element = driver.find_element(By.ID, "gol18")
                price_text = price_element.text.strip()
                
                # Convert price text to integer (remove commas)
                price = int(''.join(filter(str.isdigit, price_text)))
                return price
            except Exception as e:
                print(f"Error getting gold price: {str(e)}")
                return 0
        
        # Get local prices from table
        local_prices = {
            'gold_per_gram': get_gold_price(),            # 18k gold per gram
            'full_coin': get_coin_price("emami1"),        # Emami coin
            'half_coin': get_coin_price("azadi1_2"),      # Half Azadi
            'quarter_coin': get_coin_price("azadi1_4"),   # Quarter Azadi
            'usd': get_usd_price(),
            'global_gold': get_global_gold_price()
        }
        
        # Calculate theoretical gold price
        theoretical_gold_gram = (local_prices['global_gold'] * local_prices['usd']) / GRAM_TO_OUNCE * GOLD_PURITY_18K
        gold_price_difference = ((local_prices['gold_per_gram'] - theoretical_gold_gram) / theoretical_gold_gram) * 100
        
        # Calculate coin bubbles
        full_coin_gold_value = local_prices['gold_per_gram'] * FULL_COIN_WEIGHT
        half_coin_gold_value = local_prices['gold_per_gram'] * HALF_COIN_WEIGHT
        quarter_coin_gold_value = local_prices['gold_per_gram'] * QUARTER_COIN_WEIGHT
        
        bubbles = {
            'full_coin': ((local_prices['full_coin'] - full_coin_gold_value) / full_coin_gold_value) * 100,
            'half_coin': ((local_prices['half_coin'] - half_coin_gold_value) / half_coin_gold_value) * 100,
            'quarter_coin': ((local_prices['quarter_coin'] - quarter_coin_gold_value) / quarter_coin_gold_value) * 100
        }
        
        # Return results instead of printing
        result = {
            'global_gold': local_prices['global_gold'],
            'usd': local_prices['usd'],
            'gold_per_gram': local_prices['gold_per_gram'],
            'full_coin': local_prices['full_coin'],
            'half_coin': local_prices['half_coin'],
            'quarter_coin': local_prices['quarter_coin'],
            'bubbles': bubbles,
            'gold_price_difference': gold_price_difference
        }
        
        # Get crypto gold prices
        crypto_prices = get_crypto_gold_prices()
        result['paxg'] = crypto_prices['paxg']
        result['xaut'] = crypto_prices['xaut']

        # Add investment options to result
        investment_options = [
            {
                'name': '18k Gold',
                'premium': gold_price_difference,
                'liquidity': 'High',
                'storage': 'Easy'
            },
            {
                'name': 'Full Coin',
                'premium': bubbles['full_coin'],
                'liquidity': 'Very High',
                'storage': 'Easy'
            },
            {
                'name': 'Half Coin',
                'premium': bubbles['half_coin'],
                'liquidity': 'High',
                'storage': 'Easy'
            },
            {
                'name': 'Quarter Coin',
                'premium': bubbles['quarter_coin'],
                'liquidity': 'Medium',
                'storage': 'Easy'
            },
            {
                'name': 'PAXG',
                'premium': ((crypto_prices['paxg'] - local_prices['global_gold']) / local_prices['global_gold']) * 100,
                'liquidity': 'Medium',
                'storage': 'Digital'
            },
            {
                'name': 'XAUT',
                'premium': ((crypto_prices['xaut'] - local_prices['global_gold']) / local_prices['global_gold']) * 100,
                'liquidity': 'Medium',
                'storage': 'Digital'
            }
        ]
        
        def get_best_investment():
            # Sort options by absolute premium value
            sorted_opts = sorted(investment_options, key=lambda x: abs(x['premium']))
            best_option = sorted_opts[0]
            
            # Generate timing advice
            if gold_price_difference < -5:
                timing = "Good time to buy! Gold price is below global price."
            else:
                timing = "Not an ideal time to buy. Consider waiting."
            
            # Generate detailed recommendation
            if abs(best_option['premium']) < 5:
                if best_option['name'] in ['PAXG', 'XAUT']:
                    recommendation = f"{best_option['name']} is the best option with minimal premium ({best_option['premium']:.1f}%). Digital gold offers global liquidity but requires crypto knowledge."
                elif best_option['name'] == '18k Gold':
                    recommendation = f"18k Gold is the best option with low premium ({best_option['premium']:.1f}%). Most liquid and divisible."
                else:
                    recommendation = f"{best_option['name']} has the lowest bubble ({best_option['premium']:.1f}%) among physical options."
            else:
                crypto_premiums = [opt['premium'] for opt in investment_options if opt['name'] in ['PAXG', 'XAUT']]
                if crypto_premiums and min(abs(p) for p in crypto_premiums) < 10:
                    recommendation = "Digital gold (PAXG/XAUT) might be safer due to lower premium, but requires crypto knowledge."
                elif gold_price_difference < min(bubbles.values()):
                    recommendation = "18k Gold is safest due to lower premium than coins."
                else:
                    recommendation = "All options have high premiums. Consider waiting for better prices."
            
            return timing, recommendation

        result['investment_options'] = investment_options
        timing_advice, investment_recommendation = get_best_investment()
        result['advice'] = timing_advice
        result['best_investment'] = investment_recommendation

        return result
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    prices = get_prices()
    if prices:
        # Market Overview Table
        market_headers = ["Indicator", "Value", "Change"]
        market_data = [
            ["Global Gold", f"${prices['global_gold']:,.2f}/oz", ""],
            ["PAXG", f"${prices['paxg']:,.2f}", f"{((prices['paxg'] - prices['global_gold']) / prices['global_gold']) * 100:+.2f}%"],
            ["XAUT", f"${prices['xaut']:,.2f}", f"{((prices['xaut'] - prices['global_gold']) / prices['global_gold']) * 100:+.2f}%"],
            ["USD/IRR", f"{prices['usd']:,} Tomans", ""],
            ["18k Gold", f"{prices['gold_per_gram']:,} Tomans/g", f"{prices['gold_price_difference']:+.1f}%"]
        ]
        
        # Coin Market Table
        coin_headers = ["Coin Type", "Price (Tomans)", "Bubble"]
        coin_data = [
            ["Full Coin (Emami)", f"{prices['full_coin']:,}", f"{prices['bubbles']['full_coin']:+.1f}%"],
            ["Half Coin", f"{prices['half_coin']:,}", f"{prices['bubbles']['half_coin']:+.1f}%"],
            ["Quarter Coin", f"{prices['quarter_coin']:,}", f"{prices['bubbles']['quarter_coin']:+.1f}%"]
        ]
        
        # Investment Options Table
        options = sorted(prices['investment_options'], key=lambda x: abs(x['premium']))
        investment_headers = ["Rank", "Type", "Premium", "Liquidity", "Storage", "Recommendation"]
        investment_data = []
        
        for i, option in enumerate(options, 1):
            premium = f"{option['premium']:+.1f}%"
            if abs(option['premium']) < 5:
                premium = Fore.GREEN + premium + Style.RESET_ALL
            elif abs(option['premium']) > 15:
                premium = Fore.RED + premium + Style.RESET_ALL
                
            recommendation = "✓" if i == 1 and abs(option['premium']) < 5 else ""
            
            investment_data.append([
                i,
                option['name'],
                premium,
                option['liquidity'],
                option['storage'],
                recommendation
            ])

        print(f"""
{Fore.CYAN}╔══════════════════ GOLD MARKET DASHBOARD ══════════════════╗{Style.RESET_ALL}

{Fore.YELLOW}Market Overview:{Style.RESET_ALL}
{tabulate(market_data, headers=market_headers, tablefmt="pretty")}

{Fore.YELLOW}Coin Market Status:{Style.RESET_ALL}
{tabulate(coin_data, headers=coin_headers, tablefmt="pretty")}

{Fore.YELLOW}Investment Options (Ranked):{Style.RESET_ALL}
{tabulate(investment_data, headers=investment_headers, tablefmt="pretty")}

{Fore.GREEN}Market Analysis:{Style.RESET_ALL}
• Timing: {prices['advice']}
• Best Choice: {prices['best_investment']}

{Fore.CYAN}╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
""")