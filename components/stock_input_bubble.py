from linebot.v3.messaging import (
    FlexMessage,
    FlexBubble,
    FlexBox,
    FlexText,
    FlexButton,
    FlexSeparator,
    FlexImage,
    MessageAction
)

from utils.stock_utils import validate_ticker, get_logo_url

def build_shares_input_bubble(ticker):
    """สร้าง Flex Message สำหรับถามจำนวนหุ้น"""
    # ดึงข้อมูลหุ้น
    is_valid, info = validate_ticker(ticker)
    if is_valid:
        website_url = info.get('website')
        quote_type = info.get('quoteType', '').lower()
        name = info.get('shortName', info.get('longName', ''))
        
        # กำหนด asset_type
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
    else:
        logo_url = get_logo_url(ticker)
        name = ""

    return FlexMessage(
        alt_text=f"โปรดระบุจำนวน {ticker}",
        contents=FlexBubble(
            body=FlexBox(
                layout='vertical',
                contents=[
                    FlexBox(
                        layout='horizontal',
                        contents=[
                            FlexImage(
                                url=logo_url,
                                size='sm',
                                align='start',
                                margin='md',
                                aspect_ratio='1:1',
                                aspect_mode='cover'
                            ),
                            FlexBox(
                                layout='vertical',
                                contents=[
                                    FlexText(
                                        text=ticker,
                                        size='md',
                                        weight='bold'
                                    ),
                                    FlexText(
                                        text=name,
                                        size='xs',
                                        color='#888888',
                                        wrap=True
                                    ),
                                    FlexText(
                                        text=f'โปรดระบุจำนวนหุ้น {ticker} ที่มี',
                                        size='sm',
                                        wrap=True,
                                        margin='md'
                                    )
                                ],
                                flex=4,
                                margin='md'
                            )
                        ]
                    ),
                    FlexSeparator(margin='md'),
                    FlexButton(
                        action=MessageAction(
                            label="❌ ยกเลิก",
                            text="ยกเลิก"
                        ),
                        style="secondary",
                        height="sm",
                        margin="md"
                    )
                ]
            )
        )
    )

def build_price_input_bubble(ticker):
    """สร้าง Flex Message สำหรับถามราคาต่อหุ้น"""
    # ดึงข้อมูลหุ้น
    is_valid, info = validate_ticker(ticker)
    if is_valid:
        website_url = info.get('website')
        quote_type = info.get('quoteType', '').lower()
        name = info.get('shortName', info.get('longName', ''))
        
        # กำหนด asset_type
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
    else:
        logo_url = get_logo_url(ticker)
        name = ""

    return FlexMessage(
        alt_text=f"โปรดระบุราคาต่อหุ้น {ticker}",
        contents=FlexBubble(
            body=FlexBox(
                layout='vertical',
                contents=[
                    FlexBox(
                        layout='horizontal',
                        contents=[
                            FlexImage(
                                url=logo_url,
                                size='sm',
                                align='start',
                                margin='md',
                                aspect_ratio='1:1',
                                aspect_mode='cover'
                            ),
                            FlexBox(
                                layout='vertical',
                                contents=[
                                    FlexText(
                                        text=ticker,
                                        size='md',
                                        weight='bold'
                                    ),
                                    FlexText(
                                        text=name,
                                        size='xs',
                                        color='#888888',
                                        wrap=True
                                    ),
                                    FlexText(
                                        text=f'โปรดระบุราคาต่อหุ้น {ticker} (บาท)',
                                        size='sm',
                                        wrap=True,
                                        margin='md'
                                    )
                                ],
                                flex=4,
                                margin='md'
                            )
                        ]
                    ),
                    FlexSeparator(margin='md'),
                    FlexButton(
                        action=MessageAction(
                            label="❌ ยกเลิก",
                            text="ยกเลิก"
                        ),
                        style="secondary",
                        height="sm",
                        margin="md"
                    )
                ]
            )
        )
    )