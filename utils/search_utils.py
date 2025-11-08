import time
import requests
from difflib import SequenceMatcher
import time
import requests

def search_similar_tickers(query):
    """ค้นหา tickers ที่คล้ายกับคำที่ให้มาแบบละเอียด"""
    try:
        similar_tickers = []
        seen = set()
        query_upper = query.upper()
        
        # 1. ค้นหาครั้งแรกด้วย keyword ต้นฉบับ
        first_results = _search_yahoo_finance(query)
        for ticker in first_results:
            if ticker not in seen:
                similar_tickers.append(ticker)
                seen.add(ticker)
        
        # 2. หน่วงเวลาเล็กน้อย
        time.sleep(0.5)
        
        # 3. ค้นหาด้วยตัวอักษร 3 ตัวแรก
        if len(query) >= 3:
            prefix_results = _search_yahoo_finance(query[:3])
            for ticker in prefix_results:
                if ticker not in seen:
                    similar_tickers.append(ticker)
                    seen.add(ticker)
        
        # 4. จัดเรียงตามความคล้ายคลึง
        return _sort_by_similarity(similar_tickers, query_upper)
        
    except Exception as e:
        print(f"Error searching similar tickers: {e}")
        return []

def _search_yahoo_finance(term):
    """ค้นหาผ่าน Yahoo Finance API"""
    try:
        url = "https://query2.finance.yahoo.com/v1/finance/search"
        params = {
            'q': term,
            'quotesCount': 20,
            'newsCount': 0,
            'enableFuzzyQuery': True,
            'lang': 'en-US',
            'region': 'US'
        }
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        
        results = []
        if 'quotes' in data:
            for quote in data['quotes']:
                if 'symbol' in quote:
                    results.append(quote['symbol'])
        
        return results
        
    except Exception as e:
        print(f"Error in Yahoo Finance search: {e}")
        return []

def _sort_by_similarity(tickers, query):
    """จัดเรียงตามความคล้ายคลึงโดยใช้หลายวิธี"""
    def get_similarity_score(ticker):
        # 1. ถ้าตรงกันทั้งหมด
        if ticker == query:
            return 1.0
            
        # 2. ใช้ sequence matcher
        ratio = SequenceMatcher(None, query, ticker).ratio()
        
        # 3. ให้คะแนนพิเศษสำหรับ prefix match
        if ticker.startswith(query):
            ratio += 0.2
        
        # 4. ให้คะแนนพิเศษสำหรับการมีตัวอักษรที่ตรงกัน
        common_chars = set(query) & set(ticker)
        char_ratio = len(common_chars) / max(len(query), len(ticker))
        
        # 5. ให้คะแนนพิเศษสำหรับความยาวที่ใกล้เคียงกัน
        len_diff = abs(len(query) - len(ticker))
        len_penalty = 1 / (1 + len_diff)
        
        # รวมคะแนน
        final_score = (ratio + char_ratio + len_penalty) / 3
        return final_score
    
    # จัดเรียงและจำกัดจำนวน
    sorted_tickers = sorted(tickers, key=get_similarity_score, reverse=True)
    return sorted_tickers[:5]