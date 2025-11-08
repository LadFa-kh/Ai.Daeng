import yfinance as yf
import requests
from urllib.parse import urlparse

def get_exchange_rate():
    """ดึงอัตราแลกเปลี่ยน USD/THB จาก Yahoo Finance"""
    try:
        thb = yf.Ticker("THB=X")
        rate = thb.info.get('regularMarketPrice', None)
        if rate:
            return rate
    except Exception as e:
        print(f"Error getting exchange rate: {e}")
    return 35.0  # ค่า default ถ้าไม่สามารถดึงข้อมูลได้

def validate_ticker(ticker):
    """
    ตรวจสอบ Ticker กับ yfinance ว่า "มีจริง" หรือไม่
    Return: (True, info_dict) หรือ (False, None)
    """
    try:
        if not ticker:
            return (False, None)
            
        stock = yf.Ticker(ticker)
        
        # ใช้ basic info method แทนการเข้าถึง info dictionary
        try:
            price = stock.info.get('regularMarketPrice')
            symbol = stock.info.get('symbol')
            quote_type = stock.info.get('quoteType')
            
            # รองรับประเภทสินทรัพย์ต่างๆ
            supported_types = {
                'EQUITY': 'หุ้น',
                'CRYPTOCURRENCY': 'คริปโตเคอร์เรนซี',
                'ETF': 'กองทุน ETF',
                'CURRENCY': 'สกุลเงิน',
                'INDEX': 'ดัชนี'
            }
            
            if price and symbol and quote_type in supported_types:
                info = stock.info.copy()
                info['asset_type'] = supported_types.get(quote_type, quote_type)
                return (True, info)
            return (False, None)
            
        except Exception as e:
            print(f"Error getting ticker info: {e}")
            return (False, None)
            
    except Exception as e:
        print(f"Error validating ticker {ticker}: {e}")
        return (False, None)

def get_logo_url(ticker_symbol, website_url=None, asset_type='หุ้น'):
    """พยายามหา Logo URL จาก Clearbit API (ฟรี) หรือใช้ Icon ตามประเภทสินทรัพย์"""
    try:
        # สี theme สำหรับแต่ละประเภทสินทรัพย์ (fallback)
        asset_colors = {
            'หุ้น': {'bg': 'E8F5E9', 'fg': '2E7D32'},
            'คริปโตเคอร์เรนซี': {'bg': 'FFF3E0', 'fg': 'E65100'},
            'กองทุน ETF': {'bg': 'E3F2FD', 'fg': '1565C0'},
            'สกุลเงิน': {'bg': 'F3E5F5', 'fg': '6A1B9A'},
            'ดัชนี': {'bg': 'ECEFF1', 'fg': '263238'}
        }
        
        # 1. เช็คประเภทสินทรัพย์พิเศษก่อน
        if asset_type == 'คริปโตเคอร์เรนซี':
            # ดึงสัญลักษณ์ crypto (เช่น BTC จาก BTC-USD)
            crypto_symbol = ticker_symbol.split('-')[0].lower()
            try:
                response = requests.get(f"https://cryptoicons.org/api/icon/{crypto_symbol}/200", timeout=2)
                if response.status_code == 200:
                    return f"https://cryptoicons.org/api/icon/{crypto_symbol}/200"
            except:
                pass

        # 2. เช็ค Bitcoin-related tickers
        btc_keywords = ['BTC', 'GBTC', 'BITCOIN']
        if any(keyword in ticker_symbol.upper() for keyword in btc_keywords):
            try:
                response = requests.get("https://cryptoicons.org/api/icon/btc/200", timeout=2)
                if response.status_code == 200:
                    return "https://cryptoicons.org/api/icon/btc/200"
            except:
                pass

        # 3. Yahoo Finance API สำหรับหุ้นและ ETF
        if asset_type in ['หุ้น', 'กองทุน ETF']:
            try:
                stock = yf.Ticker(ticker_symbol)
                if 'logo_url' in stock.info and stock.info['logo_url']:
                    return stock.info['logo_url']
            except:
                pass

        # 4. เช็ค currency pairs
        if '=' in ticker_symbol and ticker_symbol.endswith('=X'):
            currency_code = ticker_symbol.split('=')[0][:3]
            return f"https://placehold.co/100x100/F3E5F5/6A1B9A?text={currency_code}"

        # 5. เช็ค special indices
        index_patterns = {
            '^GSPC': 'S&P',
            'SPX': 'SPX',
            'SPXL': 'SPX',
            'SPXU': 'SPX',
            'SPY': 'SPY',
            '^DJI': 'DOW',
            '^IXIC': 'NDQ'
        }
        if ticker_symbol in index_patterns:
            return f"https://placehold.co/100x100/1565C0/FFFFFF?text={index_patterns[ticker_symbol]}"

        # 6. ลอง Clearbit ถ้ามี website
        if website_url:
            try:
                domain = urlparse(website_url).netloc.replace('www.', '')
                logo_api_url = f"https://logo.clearbit.com/{domain}"
                response = requests.get(logo_api_url, timeout=2)
                if response.status_code == 200:
                    return logo_api_url
            except:
                pass

        # 7. Fallback: ใช้ placeholder ตามประเภทสินทรัพย์
        colors = asset_colors.get(asset_type, {'bg': 'EFEFEF', 'fg': '555555'})
        display_text = ticker_symbol

        # ปรับข้อความที่แสดงตามประเภท
        if asset_type == 'กองทุน ETF':
            display_text = 'ETF'
        elif len(ticker_symbol) > 4:
            display_text = ticker_symbol[:4]

        return f"https://placehold.co/100x100/{colors['bg']}/{colors['fg']}?text={display_text}"

    except Exception as e:
        print(f"Error getting logo for {ticker_symbol}: {e}")
        # Final fallback: ใช้อักษรตัวแรกของ ticker
        return f"https://placehold.co/100x100/EFEFEF/555555?text={ticker_symbol[0]}"

    except Exception:
         # (Fallback) ถ้า "พัง" ทุกอย่าง -> สร้าง Placeholder
        first_char = ticker_symbol[0]
        return f"https://placehold.co/100x100/EFEFEF/555555?text={first_char}"