from linebot.v3.messaging import (
    FlexMessage,
    FlexBubble,
    FlexBox,
    FlexText,
    FlexImage,
    FlexSeparator
)

def build_view_portfolio_bubble(fx_rate, stock_data_list, totals):
    """สร้าง Flex Message สำหรับแสดงข้อมูลพอร์ตโฟลิโอ"""
    stock_cards_contents = []
    for stock in stock_data_list:
        # คำนวณ Volume และ Market Price
        volume = stock['total_shares']
        
        # ตรวจสอบว่าราคาปัจจุบันใช้งานได้หรือไม่
        try:
            current_price = stock['current_price']
            market_value = volume * current_price * fx_rate
            market_value_display = f"{market_value:,.2f} THB"
        except:
            current_price = "N/A"
            market_value_display = "N/A"
        
        stock_box = FlexBox(
            layout="vertical",
            margin="lg",
            contents=[
                FlexBox(
                    layout="horizontal",
                    contents=[
                        FlexBox(
                            layout='vertical',
                            width='40px',
                            height='40px',
                            corner_radius='xxl',
                            background_color='#FFFFFF',
                            contents=[
                                FlexImage(
                                    url=stock['logo_url'],
                                    size='full',
                                    aspect_mode='cover',
                                    aspect_ratio='1:1'
                                )
                            ]
                        ),
                        FlexBox(
                            layout="vertical",
                            margin="sm",
                            flex=4,
                            contents=[
                                FlexBox(
                                    layout="horizontal",
                                    contents=[
                                        FlexText(
                                            text=stock['ticker'],
                                            weight="bold",
                                            size="lg",
                                            color="#111111",
                                            flex=2
                                        )
                                    ]
                                ),
                                FlexText(
                                    text=f"{volume:,.0f} Shares",
                                    size="xs",
                                    color="#888888"
                                ),
                                FlexText(
                                    text=f"Value: {market_value_display}",
                                    size="xs",
                                    color="#888888"
                                )
                            ]
                        ),
                        FlexBox(
                            layout="vertical",
                            flex=3,
                            contents=[
                                FlexText(
                                    text=f"{stock['pl_percent']:+.2f}%",
                                    weight="bold",
                                    size="md",
                                    color=stock['pl_color'],
                                    align="end"
                                ),
                                FlexText(
                                    text=f"{stock['pl_thb']:+,.2f} THB",
                                    size="xs",
                                    color=stock['pl_color'],
                                    align="end"
                                )
                            ]
                        )
                    ]
                ),
                FlexBox(
                    layout="horizontal",
                    margin="md",
                    contents=[
                        FlexBox(
                            layout="vertical",
                            flex=1,
                            contents=[
                                FlexText(
                                    text="Cost",
                                    size="xs",
                                    color="#AAAAAA"
                                ),
                                FlexText(
                                    text=f"{stock['avg_cost_thb']:,.2f} THB",
                                    size="sm",
                                    color="#555555",
                                    weight="bold"
                                )
                            ]
                        ),
                        FlexBox(
                            layout="vertical",
                            flex=1,
                            spacing="none",
                            contents=[
                                FlexBox(
                                    layout="horizontal",
                                    contents=[
                                        FlexBox(
                                            layout="horizontal",
                                            width="80px",
                                            contents=[
                                                FlexText(
                                                    text="Market",
                                                    size="xs",
                                                    color="#AAAAAA",
                                                    align="center",
                                                    flex=1
                                                )
                                            ]
                                        )
                                    ],
                                    justifyContent="flex-end"
                                ),
                                FlexBox(
                                    layout="horizontal",
                                    contents=[
                                        FlexText(
                                            text=f"{current_price} THB",
                                            size="sm",
                                            color="#555555",
                                            weight="bold",
                                            align="end",
                                            flex=1
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
        stock_cards_contents.append(stock_box)
        if stock != stock_data_list[-1]:
            stock_cards_contents.append(FlexSeparator())

    # สร้าง bubble
    bubble = FlexBubble(
        body=FlexBox(
            layout="vertical",
            contents=[
                # ส่วนบนแสดง Total P/L
                FlexBox(
                    layout="vertical",
                    margin="none",
                    background_color="#F5F5F5",
                    corner_radius="lg",
                    padding_all="lg",
                    contents=[
                        FlexText(
                            text="📝 PORTFOLIO SUMMARY",
                            weight="bold",
                            color="#1DB446",
                            size="sm"
                        ),
                        FlexText(
                            text=f"💸{totals['total_pl_thb']:+,.2f} THB ({totals['total_pl_percent']:+.2f}%)",
                            weight="bold",
                            size="md",
                            color=totals['main_color'],
                            margin="md"
                        ),
                        FlexText(
                            text=f"💲{totals['total_pl_usd']:+,.2f} USD ({totals['total_pl_percent']:+.2f}%)",
                            weight="bold",
                            size="sm",
                            margin="sm"
                        ),
                        FlexText(
                            text=f"💱 1 USD = {fx_rate:,.2f} THB",
                            size="xs",
                            color="#888888",
                            margin="sm"
                        )
                    ]
                ),
                # รายการหุ้น
                FlexBox(
                    layout="vertical",
                    margin="lg",
                    spacing="sm",
                    contents=stock_cards_contents
                )
            ]
        )
    )

    try:
        return FlexMessage(
            alt_text=f"Portfolio Summary: {totals['total_pl_thb']:+,.2f} THB",
            contents=bubble
        )
    except Exception as e:
        print(f"Error creating portfolio view: {e}")
        return FlexMessage(
            alt_text="Portfolio Error",
            contents=FlexBubble(
                body=FlexBox(
                    layout="vertical",
                    contents=[
                        FlexText(
                            text="เกิดข้อผิดพลาดในการแสดงพอร์ต",
                            weight="bold",
                            size="md",
                            color="#FF0000"
                        )
                    ]
                )
            )
        )