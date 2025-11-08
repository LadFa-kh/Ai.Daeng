from linebot.v3.messaging import (
    FlexMessage,
    FlexBubble,
    FlexBox,
    FlexText,
    FlexButton,
    FlexSeparator,
    MessageAction
)

def build_help_add_stock_bubble():
    """สร้าง Flex Message แสดงวิธีการเพิ่มหุ้น"""
    bubble = FlexBubble(
        body=FlexBox(
            layout='vertical',
            background_color='#FFFFFF',
            padding_all='lg',
            contents=[
                # หัวข้อ
                FlexBox(
                    layout='horizontal',
                    background_color='#1DB446',
                    padding_all='lg',
                    corner_radius='lg',
                    contents=[
                        FlexText(
                            text='📈',
                            size='xl',
                            color='#FFFFFF',
                            flex=1
                        ),
                        FlexBox(
                            layout='vertical',
                            flex=5,
                            contents=[
                                FlexText(
                                    text='วิธีเพิ่มหุ้นในพอร์ต',
                                    weight='bold',
                                    size='xl',
                                    color='#FFFFFF'
                                ),
                                FlexText(
                                    text='Add Stock to Portfolio',
                                    size='sm',
                                    color='#FFFFFF'
                                )
                            ]
                        )
                    ]
                ),
                # รูปแบบคำสั่ง
                FlexBox(
                    layout='vertical',
                    margin='lg',
                    padding_all='lg',
                    background_color='#F5F5F5',
                    corner_radius='lg',
                    contents=[
                        FlexText(
                            text='รูปแบบคำสั่ง',
                            weight='bold',
                            size='md',
                            color='#111111'
                        ),
                        FlexText(
                            text='[TICKER] [จำนวนหุ้น] [ราคาต่อหุ้น]',
                            size='sm',
                            color='#111111',
                            margin='md'
                        )
                    ]
                ),
                # ตัวอย่าง
                FlexBox(
                    layout='vertical',
                    margin='lg',
                    contents=[
                        FlexText(
                            text='📝 ตัวอย่างการเพิ่มหุ้นแบบที่ 1',
                            weight='bold',
                            color='#111111',
                            size='md'
                        ),
                        # ตัวอย่าง US Stock
                        FlexBox(
                            layout='vertical',
                            margin='md',
                            contents=[
                                FlexBox(
                                    layout='vertical',
                                    background_color='#EDF7ED',
                                    corner_radius='md',
                                    padding_all='md',
                                    contents=[
                                        FlexText(
                                            text='หุ้นต่างประเทศ 🌎',
                                            weight='bold',
                                            color='#1DB446',
                                            size='sm'
                                        ),
                                        FlexText(
                                            text='NVDA 10 35000',
                                            color='#1DB446',
                                            size='md',
                                            margin='sm'
                                        ),
                                        FlexText(
                                            text='ซื้อ NVIDIA 10 หุ้น ราคา 35,000 บาท/หุ้น',
                                            color='#666666',
                                            size='xs',
                                            margin='sm',
                                            wrap=True
                                        )
                                    ]
                                ),
                                FlexButton(
                                    style='primary',
                                    color='#1DB446',
                                    action=MessageAction(
                                        label='เพิ่ม NVIDIA ➜',
                                        text='NVDA'
                                    ),
                                    height='sm',
                                    margin='sm'
                                )
                            ]
                        ),
                        # ตัวอย่าง Thai Stock
                        FlexBox(
                            layout='vertical',
                            margin='lg',
                            contents=[
                                FlexBox(
                                    layout='vertical',
                                    background_color='#EDF7ED',
                                    corner_radius='md',
                                    padding_all='md',
                                    contents=[
                                        FlexText(
                                            text='หุ้นไทย 🇹🇭',
                                            weight='bold',
                                            color='#1DB446',
                                            size='sm'
                                        ),
                                        FlexText(
                                            text='PTT.BK 100 35',
                                            color='#1DB446',
                                            size='md',
                                            margin='sm'
                                        ),
                                        FlexText(
                                            text='ซื้อ PTT 100 หุ้น ราคา 35 บาท/หุ้น',
                                            color='#666666',
                                            size='xs',
                                            margin='sm',
                                            wrap=True
                                        )
                                    ]
                                ),
                                FlexButton(
                                    style='primary',
                                    color='#1DB446',
                                    action=MessageAction(
                                        label='เพิ่ม PTT ➜',
                                        text='PTT.BK'
                                    ),
                                    height='sm',
                                    margin='sm'
                                )
                            ]
                        )
                    ]
                ),
                # แสดงขั้นตอนการเพิ่มหุ้น
                FlexBox(
                    layout='vertical',
                    margin='lg',
                    background_color='#E3F2FD',
                    corner_radius='md',
                    padding_all='md',
                    contents=[
                        FlexText(
                            text='📋 ขั้นตอนการเพิ่มหุ้นแบบที่ 2',
                            weight='bold',
                            color='#1565C0',
                            size='sm'
                        ),
                        FlexBox(
                            layout='vertical',
                            margin='sm',
                            spacing='sm',
                            contents=[
                                FlexText(
                                    text='1️⃣ พิมพ์ชื่อหุ้น เช่น NVDA หรือ PTT.BK',
                                    color='#1565C0',
                                    size='xs',
                                    wrap=True
                                ),
                                FlexText(
                                    text='2️⃣ ระบุจำนวนหุ้นที่ต้องการ เช่น 0.1 หรือ 10',
                                    color='#1565C0',
                                    size='xs',
                                    wrap=True
                                ),
                                FlexText(
                                    text='3️⃣ ใส่ราคาต่อหุ้น (บาท) เช่น 10 หรือ 100',
                                    color='#1565C0',
                                    size='xs',
                                    wrap=True
                                )
                            ]
                        )
                    ]
                ),
                # Tips
                FlexBox(
                    layout='vertical',
                    margin='lg',
                    background_color='#FFF3CD',
                    corner_radius='md',
                    padding_all='md',
                    contents=[
                        FlexText(
                            text='💡 คำแนะนำ',
                            weight='bold',
                            color='#856404',
                            size='sm'
                        ),
                        FlexText(
                            text='• หุ้นไทยต้องเติม .BK (เช่น PTT.BK)\n• หุ้น US ไม่ต้องเติมอะไร (เช่น AAPL)\n• ใส่ราคาเป็นสกุลเงินบาทเท่านั้น',
                            color='#856404',
                            size='xs',
                            wrap=True,
                            margin='sm'
                        )
                    ]
                )
            ]
        )
    )
    
    return FlexMessage(
        alt_text='วิธีการเพิ่มหุ้น',
        contents=bubble
    )