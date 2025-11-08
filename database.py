import os
import psycopg2
from dotenv import load_dotenv

# โหลด .env (จำเป็นสำหรับ DB)
load_dotenv() 

def get_db_connection():
    """(V-Refactor) ย้ายมาจาก app.py
    สร้างการเชื่อมต่อ PostgreSQL จากค่าใน .env"""
    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        port=os.environ['DB_PORT'],
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS']
    )
    return conn

def get_portfolio(user_id):
    """(V-Refactor) ดึงข้อมูลพอร์ตทั้งหมด (สำหรับ User นี้)"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT ticker, SUM(shares) as total_shares, 
               SUM(shares * cost_price) / SUM(shares) as avg_cost_thb
        FROM portfolio
        WHERE line_user_id = %s
        GROUP BY ticker ORDER BY ticker
        """, (user_id,)
    )
    rows = cur.fetchall()
    stocks = []
    for row in rows:
        stocks.append({
            'ticker': row[0],
            'shares': row[1],
            'cost_price_thb': row[2]
        })
    cur.close()
    conn.close()
    return stocks

def add_stock(user_id, ticker, shares, cost_price_thb):
    """(V-Refactor) เพิ่มหุ้น 1 รายการลง Database"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO portfolio (line_user_id, ticker, shares, cost_price) VALUES (%s, %s, %s, %s)",
            (user_id, ticker, shares, cost_price_thb)
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding stock to database: {e}")
        return False