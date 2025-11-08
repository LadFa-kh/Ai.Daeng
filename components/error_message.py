from linebot.v3.messaging import (
    FlexMessage,
    FlexBubble,
    FlexBox,
    FlexText,
    FlexButton,
    MessageAction
)

def build_error_bubble(title_th, message_en):
    """สร้าง Flex Message สำหรับแสดงข้อผิดพลาด"""
    bubble = FlexBubble(
        body=FlexBox(
            layout='vertical',
            background_color='#FFFFFF',
            padding_all='lg',
            contents=[
                # Icon และหัวข้อ
                FlexBox(
                    layout='horizontal',
                    background_color='#FFE9E9',
                    padding_all='lg',
                    corner_radius='lg',
                    contents=[
                        FlexText(
                            text='⚠️',
                            size='xl',
                            flex=1
                        ),
                        FlexBox(
                            layout='vertical',
                            flex=5,
                            contents=[
                                FlexText(
                                    text='เกิดข้อผิดพลาด',
                                    weight='bold',
                                    size='xl',
                                    color='#DC3545'
                                ),
                            ]
                        )
                    ]
                ),
                # ข้อความแสดงข้อผิดพลาด
                FlexBox(
                    layout='vertical',
                    margin='lg',
                    spacing='sm',
                    contents=[
                        # ข้อความภาษาไทย
                        FlexText(
                            text=title_th,
                            size='md',
                            color='#111111',
                            wrap=True
                        ),
                        # ข้อความภาษาอังกฤษ
                        FlexText(
                            text=message_en,
                            size='sm',
                            color='#888888',
                            wrap=True
                        )
                    ]
                ),
                # ปุ่มดูวิธีการใช้งาน
                FlexButton(
                    style='primary',
                    color='#DC3545',
                    margin='lg',
                    action=MessageAction(
                        label='ยกเลิกการทำรายการ',
                        text='ยกเลิก'
                    )
                )
            ]
        )
    )
    
    return FlexMessage(
        alt_text='เกิดข้อผิดพลาด',
        contents=bubble
    )

def build_simple_message_bubble(title, message):
    """สร้าง Flex Message สำหรับข้อความทั่วไป"""
    bubble = FlexBubble(
        body=FlexBox(
            layout='vertical',
            contents=[
                FlexText(
                    text=title,
                    weight='bold',
                    size='lg',
                    color='#111111'
                ),
                FlexText(
                    text=message,
                    size='md',
                    color='#666666',
                    margin='md',
                    wrap=True
                )
            ]
        )
    )
    return FlexMessage(
        alt_text=title,
        contents=bubble
    )