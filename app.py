import os
from dotenv import load_dotenv
from flask import Flask, request, abort

# (ส่วน Import ของ LINE ยังเหมือนเดิม)
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    FlexMessage,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
import logic
from logic import handle_text_message

# Import Local Modules
# database.py - จัดการฐานข้อมูล SQLite
# logic.py - จัดการ Business Logic (ใช้ components)
#   ├── components/ - UI Components (Flex Messages)
#   │   ├── error_message.py - แสดงข้อผิดพลาดและข้อความทั่วไป
#   │   ├── stock_confirmation.py - แสดงการยืนยันการเพิ่มหุ้น
#   │   ├── stock_help.py - แสดงวิธีการใช้งาน
#   │   ├── stock_suggestion.py - แสดงคำแนะนำ Ticker
#   │   └── portfolio_view.py - แสดงพอร์ตโฟลิโอ
#   └── utils/ - Utility Functions
#       ├── stock_utils.py - จัดการเกี่ยวกับหุ้น
#       └── search_utils.py - ค้นหาและแนะนำ Ticker
import database
import logic

# --- 2. โหลดค่าตั้งค่าจาก .env ---
load_dotenv() 
app = Flask(__name__)

# ดึงค่ามาจาก .env
LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
LINE_CHANNEL_SECRET = os.environ['LINE_CHANNEL_SECRET']

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# --- (V-Refactor) ลบ get_db_connection() ออกไป (ย้ายไป database.py) ---

# --- 4. สร้างประตู /webhook (เหมือนเดิม) ---
@app.route("/webhook", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data()
    app.logger.info("Request body: " + body.decode('utf-8'))
    try:
        handler.handle(body.decode('utf-8'), signature)
    except InvalidSignatureError:
        print("!!! Signature ผิดพลาด ตรวจสอบ Secret Key ของคุณ !!!")
        abort(400)
    return 'OK'


# --- 5. ส่วนจัดการข้อความ ---
@handler.add(MessageEvent, message=TextMessageContent)
def handle_line_message(event):
    try:
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            
            # ส่งข้อความไปที่ Logic และรับการตอบกลับ
            reply_message = handle_text_message(event.source.user_id, event.message.text)
            
            # ตรวจสอบและแปลงให้เป็น list
            if reply_message:
                messages = []
                if isinstance(reply_message, (FlexMessage, TextMessage)):
                    messages.append(reply_message)
                elif isinstance(reply_message, list):
                    messages.extend(reply_message)
                    
                if messages:
                    line_bot_api.reply_message_with_http_info(
                        ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=messages
                        )
                    )
    except Exception as e:
        print(f"Error in handle_line_message: {e}")
        # สร้างข้อความ error แบบง่ายเมื่อเกิดข้อผิดพลาด
        error_message = TextMessage(text="ขออภัย เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง")
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[error_message]
                )
            )

# --- สั่งให้ Server เริ่มทำงาน ---
if __name__ == "__main__":
    print("...เซิร์ฟเวอร์ Stock Bot (Refactored) กำลังเริ่มทำงานที่ Port 5000...")
    app.run(port=5000, debug=True)