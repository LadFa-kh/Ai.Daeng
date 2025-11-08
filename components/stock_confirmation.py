import yfinance as yf
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

def build_add_stock_confirmation_bubble(ticker, shares, cost_price_thb, logo_url, asset_type='หุ้น'):
    """สร้าง Flex Message สำหรับการยืนยันการเพิ่มหุ้น"""
    bubble = FlexBubble(
        body=FlexBox(
            layout='vertical',
            spacing='md',
            contents=[
                FlexBox(
                    layout='horizontal',
                    spacing='md',
                    contents=[
                        FlexImage(
                            url=logo_url,
                            size='xs',
                            aspect_mode='cover',
                            aspect_ratio='1:1',
                            flex=1,
                            background_color="#FFFFFF",
                            border_radius="100px"
                        ),
                        FlexBox(
                            layout='vertical',
                            contents=[
                                FlexText(
                                    text=f'{asset_type.upper()} ADDED',
                                    weight='bold',
                                    color='#1DB446',
                                    size='sm'
                                ),
                                FlexText(
                                    text=ticker,
                                    weight='bold',
                                    size='xl'
                                )
                            ],
                            flex=5
                        )
                    ]
                ),
                FlexSeparator(margin='lg'),
                FlexBox(
                    layout='vertical',
                    margin='lg',
                    spacing='sm',
                    contents=[
                        FlexBox(
                            layout='horizontal',
                            contents=[
                                FlexText(text='Shares', size='sm', color='#555555'),
                                FlexText(text=f"{shares:,.2f}", size='sm', color='#111111', align='end')
                            ]
                        ),
                        FlexBox(
                            layout='horizontal',
                            contents=[
                                FlexText(text='Cost Price', size='sm', color='#555555'),
                                FlexText(text=f"{cost_price_thb:,.2f} THB", size='sm', color='#111111', align='end')
                            ]
                        ),
                        FlexBox(
                            layout='horizontal',
                            contents=[
                                FlexText(text='ต้นทุนรวม', size='sm', color='#555555'),
                                FlexText(text=f"{shares * cost_price_thb:,.2f} THB", size='sm', color='#111111', align='end')
                            ]
                        )
                    ]
                ),
                FlexSeparator(margin='lg'),
                FlexButton(
                    style='primary',
                    color='#1DB446',
                    margin='md',
                    action=MessageAction(
                        label='ดูพอร์ตทั้งหมด',
                        text='ดูพอร์ต'
                    )
                )
            ]
        )
    )
    
    return FlexMessage(
        alt_text=f'บันทึก {ticker} เรียบร้อย',
        contents=bubble
    )