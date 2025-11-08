from linebot.v3.messaging import (
    TextMessage,
    FlexMessage,
    FlexBubble,
    FlexBox,
    FlexText
)

# Import จาก Python Standard Library
import time

# Import จาก Third-party Libraries
import yfinance as yf

# Import Components (UI)
from components.error_message import build_error_bubble, build_simple_message_bubble
from components.stock_confirmation import build_add_stock_confirmation_bubble
from components.stock_help import build_help_add_stock_bubble
from components.stock_suggestion import build_suggestion_bubble
from components.portfolio_view import build_view_portfolio_bubble
from components.stock_input_bubble import build_shares_input_bubble, build_price_input_bubble

# Import Utils (Functions)
from utils.stock_utils import validate_ticker, get_logo_url, get_exchange_rate
from utils.search_utils import search_similar_tickers

# Import Local Modules
import database

# ================================================================
# 🏛️ คลาส UserState: จัดการสถานะผู้ใช้งาน
# ================================================================
class UserState:
    def __init__(self):
        self.states = {}  # Dict เก็บสถานะของแต่ละ user_id

    def set_state(self, user_id, state, data=None):
        self.states[user_id] = {
            'state': state,
            'data': data,
            'timestamp': time.time()
        }

    def get_state(self, user_id):
        state_data = self.states.get(user_id)
        if state_data and time.time() - state_data['timestamp'] < 300:  # หมดอายุใน 5 นาที
            return state_data
        self.states.pop(user_id, None)
        return None

    def clear_state(self, user_id):
        self.states.pop(user_id, None)

# สร้าง global instance
user_states = UserState()

# ================================================================
# 📈 ฟังก์ชันจัดการ Ticker
# ================================================================
def validate_ticker_and_suggest(ticker):
    """
    ฟังก์ชันหลักในการตรวจสอบ Ticker
    Return: (status, data)
    - ("valid", info) -> Ticker ถูกต้อง
    - ("suggest", suggestions_list) -> Ticker ผิด แต่มีคำแนะนำ
    - ("invalid", None) -> Ticker ผิด และไม่มีคำแนะนำ
    """
    is_valid, info = validate_ticker(ticker)
    
    # 1. ถ้า Ticker "ถูกต้อง"
    if is_valid:
        return ("valid", info)
        
    # 2. ถ้า Ticker "ผิด" -> พยายาม "หาคำแนะนำ"
    suggestions = []
    
    # 2.1 ค้นหาด้วย Yahoo Finance Search API
    similar_tickers = search_similar_tickers(ticker)
    suggestions.extend(similar_tickers)
    
    # 2.2 ลองเติม Suffix (ถ้าไม่มี '.')
    if "." not in ticker:
        common_suffixes = ['.BK', '.SS', '.SZ']
        for suffix in common_suffixes:
            suggested_ticker = f"{ticker}{suffix}"
            is_valid_suggestion, _ = validate_ticker(suggested_ticker)
            if is_valid_suggestion:
                suggestions.append(suggested_ticker)
    
    # 3. สรุปผล
    if suggestions:
        # ลบ duplicates และจัดเรียง
        suggestions = sorted(list(set(suggestions)))
        return ("suggest", suggestions)
    else:
        return ("invalid", None)

# ================================================================
# 🎯 ฟังก์ชัน Handle Messages หลัก
# ================================================================
def handle_text_message(user_id, message):
    """ฟังก์ชันหลักในการ handle text message จาก LINE"""
    # เช็ค state ก่อน (ถ้ามี state แสดงว่าอยู่ระหว่างการทำ flow อะไรสักอย่าง)
    state_data = user_states.get_state(user_id)
    if state_data:
        state = state_data['state']
        data = state_data.get('data', {})
        
        if message.lower() == "ยกเลิก":
            user_states.clear_state(user_id)
            return build_simple_message_bubble(
                "ยกเลิกการทำรายการ",
                "คุณได้ยกเลิกการทำรายการแล้ว"
            )
        
        if state == 'waiting_shares':
            try:
                shares = float(message)
                if shares <= 0:
                    return build_error_bubble(
                        "จำนวนหุ้นต้องมากกว่า 0",
                        "Please enter a positive number."
                    )
                
                # เก็บจำนวนหุ้นและรอราคา
                user_states.set_state(user_id, 'waiting_price', {
                    'ticker': data['ticker'],
                    'shares': shares
                })
                return build_price_input_bubble(data['ticker'])
            except ValueError:
                return build_error_bubble(
                    "กรุณาระบุจำนวนหุ้นที่มีเป็นตัวเลข เช่น 10",
                    "Please enter a valid number."
                )
                
        elif state == 'waiting_price':
            try:
                price = float(message)
                if price <= 0:
                    return build_error_bubble(
                        "ราคาต้องมากกว่า 0",
                        "Please enter a positive price."
                    )
                # เพิ่มหุ้นเข้าพอร์ต
                user_states.clear_state(user_id)
                return handle_add_stock_simple(user_id, f"{data['ticker']} {data['shares']} {price}")
            except ValueError:
                return build_error_bubble(
                    "กรุณาระบุราคาเป็นตัวเลข เช่น 100",
                    "Please enter a valid price."
                )
    
    # เช็คว่าเป็น ticker เดี่ยวๆ จาก FlexLineMessage หรือไม่
    if len(message.split()) == 1:
        if message.isupper():  # ถ้าเป็นตัวพิมพ์ใหญ่ทั้งหมด (เช่น NVDA, PTT.BK)
            ticker = message
            status, data = validate_ticker_and_suggest(ticker)
            if status == "valid":
                user_states.set_state(user_id, 'waiting_shares', {'ticker': ticker})
                return build_shares_input_bubble(ticker)
            elif status == "suggest":
                return build_suggestion_bubble(ticker, data)
            else:
                return build_error_bubble(
                    "Ticker ไม่ถูกต้อง",
                    f"ไม่พบ ticker '{ticker}' ในระบบ"
                )
    
    # เช็คว่าเป็นคำสั่งพิเศษหรือไม่
    command = message.lower()
    if command == "ดูพอร์ต" or command == "portfolio":
        return handle_view_portfolio(user_id)
    elif command == "ช่วยเหลือ" or command == "help":
        return build_help_add_stock_bubble()
        
    # ถ้าไม่ใช่คำสั่งพิเศษ ลองแยก format ticker จำนวน ราคา
    if len(message.split()) == 3:  # Format: TICKER SHARES PRICE
        return handle_add_stock_simple(user_id, message)
        
    # ถ้าไม่ตรงเงื่อนไขไหนเลย -> ส่งข้อความช่วยเหลือ
    return build_help_add_stock_bubble()

# ================================================================
# 🛠️ ฟังก์ชัน Handle งานเฉพาะ
# ================================================================
def handle_add_stock_simple(user_id, message):
    """เพิ่มหุ้นเข้าพอร์ต (Format: TICKER SHARES PRICE)"""
    try:
        # แยก components
        ticker, shares_str, cost_str = message.split()
        ticker = ticker.strip().upper()
        
        # ตรวจสอบ ticker
        is_valid, info = validate_ticker(ticker)
        if not is_valid:
            return build_error_bubble(
                "Ticker ไม่ถูกต้อง",
                f"ไม่พบ ticker '{ticker}' ในระบบ"
            )
            
        # แปลงค่าจำนวนและราคา
        try:
            shares = float(shares_str)
            cost_price_thb = float(cost_str)
        except ValueError:
            return build_error_bubble(
                "รูปแบบไม่ถูกต้อง",
                "กรุณาระบุจำนวนและราคาเป็นตัวเลข"
            )
            
        # ตรวจสอบค่าที่รับมา
        if shares <= 0:
            return build_error_bubble(
                "จำนวนหุ้นต้องมากกว่า 0",
                "Please enter a positive number."
            )
            
        if cost_price_thb <= 0:
            return build_error_bubble(
                "ราคาต้องมากกว่า 0",
                "Please enter a positive price."
            )
            
        # บันทึกลงฐานข้อมูล
        website_url = info.get('website')
        logo_url = get_logo_url(ticker, website_url)
        
        db_success = database.add_stock(
            user_id=user_id,
            ticker=ticker,
            shares=shares,
            cost_price_thb=cost_price_thb
        )
        
        if not db_success:
            return build_error_bubble(
                "เกิดข้อผิดพลาด",
                "ไม่สามารถบันทึกข้อมูลได้ กรุณาลองใหม่อีกครั้ง"
            )
            
        # ส่งข้อความยืนยัน
        asset_type = info.get('asset_type', 'หุ้น')
        return build_add_stock_confirmation_bubble(
            ticker=ticker,
            shares=shares,
            cost_price_thb=cost_price_thb,
            logo_url=logo_url,
            asset_type=asset_type
        )
        
    except Exception as e:
        print(f"Error in handle_add_stock: {e}")
        return build_error_bubble(
            "เกิดข้อผิดพลาด",
            "กรุณาลองใหม่อีกครั้ง"
        )
        
def handle_view_portfolio(user_id):
    """ดูพอร์ตการลงทุนทั้งหมด"""
    try:
        # ดึงข้อมูลจากฐานข้อมูล
        portfolio = database.get_portfolio(user_id)
        if not portfolio:
            return build_simple_message_bubble(
                "ยังไม่มีสินทรัพย์",
                "คุณยังไม่มีสินทรัพย์ในพอร์ต\nลองเพิ่มสินทรัพย์ตัวแรกดูสิ! 💪"
            )
            
        stock_data_list = []
        total_pl_thb = 0
        total_cost_thb = 0
        
        fx_rate = get_exchange_rate()  # ดึงอัตราแลกเปลี่ยนล่าสุดจาก Yahoo Finance
        
        # คำนวณมูลค่าพอร์ตแต่ละตัว
        for item in portfolio:
            try:
                ticker = item['ticker']
                shares = item['shares']
                avg_cost = item['cost_price_thb']
                
                # ดึงข้อมูลปัจจุบัน
                stock = yf.Ticker(ticker)
                current_price = stock.info.get('regularMarketPrice', 0)
                if stock.info.get('currency') == 'USD':
                    current_price = current_price * fx_rate
                    
                # คำนวณ P/L
                cost_price_thb = avg_cost
                pl_thb = (current_price - cost_price_thb) * shares
                pl_percent = (pl_thb / (cost_price_thb * shares)) * 100
                total_pl_thb += pl_thb
                total_cost_thb += (cost_price_thb * shares)
                
                # ดึงข้อมูล logo และ asset type
                website_url = stock.info.get('website')
                quote_type = stock.info.get('quoteType', '').lower()
                
                # กำหนด asset_type ตามประเภทของสินทรัพย์
                if quote_type == 'cryptocurrency':
                    asset_type = 'คริปโตเคอร์เรนซี'
                elif quote_type == 'etf':
                    asset_type = 'กองทุน ETF'
                elif quote_type == 'index':
                    asset_type = 'ดัชนี'
                elif '=' in ticker and ticker.endswith('=X'):
                    asset_type = 'สกุลเงิน'
                else:
                    asset_type = 'หุ้น'
                    
                logo_url = get_logo_url(ticker, website_url, asset_type)
                
                stock_data = {
                    'ticker': ticker,
                    'total_shares': shares,
                    'current_price': current_price,
                    'avg_cost_thb': cost_price_thb,
                    'pl_thb': pl_thb,
                    'pl_percent': pl_percent,
                    'pl_color': '#1DB446' if pl_thb >= 0 else '#DC3545',
                    'logo_url': logo_url
                }
                stock_data_list.append(stock_data)
                print(f"Successfully processed {ticker} with P/L: {pl_thb:,.2f} THB")
            
            except Exception as e:
                print(f"Error processing {ticker}: {e}")
                continue
            
        # คำนวณผลรวมทั้งหมด
        total_pl_percent = (total_pl_thb / total_cost_thb) * 100 if total_cost_thb > 0 else 0.0
        total_pl_usd = total_pl_thb / fx_rate
        main_color = "#1DB446" if total_pl_thb >= 0 else "#FF0000"
        
        totals = {
            "total_pl_thb": total_pl_thb,
            "total_pl_usd": total_pl_usd,
            "total_pl_percent": total_pl_percent,
            "main_color": main_color
        }
        
        print(f"Portfolio summary:")
        print(f"- Total P/L THB: {total_pl_thb:,.2f}")
        print(f"- Total P/L USD: {total_pl_usd:,.2f}")
        print(f"- Total P/L %: {total_pl_percent:,.2f}%")
        
        try:
            result = build_view_portfolio_bubble(fx_rate, stock_data_list, totals)
            print("Successfully built portfolio view")
            return result
        except Exception as view_error:
            print(f"Error building portfolio view: {view_error}")
            return build_simple_message_bubble(
                "เกิดข้อผิดพลาด",
                "ไม่สามารถแสดงผลพอร์ตได้\nกรุณาลองใหม่อีกครั้ง"
            )

    except Exception as e:
        print(f"Unexpected error in handle_view_portfolio: {e}")
        return build_simple_message_bubble(
            "เกิดข้อผิดพลาด",
            "ไม่สามารถดึงข้อมูลพอร์ตได้\nกรุณาลองใหม่อีกครั้ง"
        )