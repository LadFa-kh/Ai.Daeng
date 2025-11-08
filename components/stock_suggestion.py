from linebot.v3.messaging import (
    FlexMessage,
    FlexBubble,
    FlexBox,
    FlexText,
    FlexImage,
    FlexButton,
    FlexSeparator,
    MessageAction
)
from utils.stock_utils import validate_ticker, get_logo_url
import yfinance as yf

def build_suggestion_bubble(original_ticker, suggestions_list):
    """สร้าง Flex Message "คุณหมายถึง...?" พร้อม logo"""
    suggestions_boxes = []
    
    # วนลูปผ่าน symbols
    for symbol in suggestions_list:
        # ดึงข้อมูลเพิ่มเติมสำหรับแต่ละ symbol
        is_valid, info = validate_ticker(symbol)
        if not is_valid:
            continue
            
        # ดึงข้อมูลที่จำเป็น
        name = info.get('shortName', info.get('longName', ''))
        exchange = info.get('exchange', '')
        price = info.get('regularMarketPrice', 0)
        currency = info.get('currency', '')
        website_url = info.get('website')
        asset_type = info.get('asset_type', 'หุ้น')
        logo_url = get_logo_url(symbol, website_url, asset_type)
        
        # สร้าง price text
        price_text = f"{price:,.2f} {currency}" if price else "N/A"
        
        suggestion_box = FlexBox(
            layout='horizontal',
            margin='sm',
            action=MessageAction(
                label=f'เลือก {symbol}',
                text=symbol
            ),
            contents=[
                # Logo box
                FlexBox(
                    layout='vertical',
                    width='40px',
                    height='40px',
                    corner_radius='xxl',
                    background_color='#FFFFFF',
                    contents=[
                        FlexImage(
                            url=logo_url,
                            size='full',
                            aspect_mode='cover',
                            aspect_ratio='1:1'
                        )
                    ]
                ),
                # Info box
                FlexBox(
                    layout='vertical',
                    margin='sm',
                    spacing='xs',
                    flex=5,
                    contents=[
                        FlexText(
                            text=symbol,
                            size='md',
                            color='#111111',
                            weight='bold'
                        ),
                        FlexText(
                            text=name,
                            size='xs',
                            color='#888888',
                            wrap=True
                        ),
                        FlexText(
                            text=price_text,
                            size='xs',
                            color='#aaaaaa'
                        )
                    ]
                )
            ]
        )
        suggestions_boxes.append(suggestion_box)
    
    bubble = FlexBubble(
        body=FlexBox(
            layout='vertical',
            spacing='md',
            contents=[
                FlexText(
                    text='TICKER NOT FOUND',
                    weight='bold',
                    color='#FF0000',
                    size='sm'
                ),
                FlexText(
                    text=f"ไม่พบ '{original_ticker}'",
                    weight='bold',
                    size='xl',
                    margin='md',
                    wrap=True
                ),
                FlexText(
                    text="Ticker นี้ไม่มีอยู่จริงในระบบของเรา",
                    color="#AAAAAA",
                    size="sm",
                    wrap=True
                ),
                FlexSeparator(margin='lg'),
                FlexBox(
                    layout='vertical',
                    margin='lg',
                    spacing='sm',
                    contents=[
                        FlexText(
                            text="คุณหมายถึง Ticker นี้หรือไม่? (คลิกเพื่อเลือก)",
                            size="sm",
                            color="#555555"
                        ),
                        *suggestions_boxes,
                        FlexSeparator(margin='md'),
                        FlexButton(
                            action=MessageAction(
                                label="❌ ยกเลิก",
                                text="ยกเลิก"
                            ),
                            style="secondary",
                            height="sm",
                            margin="md"
                        ),
                        FlexText(
                            text="กรุณาลองพิมพ์คำสั่งใหม่อีกครั้ง ด้วย Ticker ที่ถูกต้อง",
                            color="#AAAAAA",
                            size="xs",
                            wrap=True,
                            margin="md"
                        )
                    ]
                )
            ]
        )
    )
    
    return FlexMessage(
        alt_text=f"ไม่พบ Ticker {original_ticker}",
        contents=bubble
    )