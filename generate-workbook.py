#!/usr/bin/env python3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from furigana.furigana import split_furigana

def count_boxes(japanese_text, kanji_list):
    count = 0
    for char in japanese_text:
        if char in kanji_list:
            count += 1
    return count

def furigana_offset(japanese_text, kanji_list, font_size, box_size, margin):
    total_chars = japanese_text.__len__()
    boxes = count_boxes(japanese_text, kanji_list)
    chars = total_chars - boxes
    return (chars * font_size + boxes*(box_size + 2*margin))/2

def create_workbook(japanese_text, kanji_list, output_file):
    x, y = 50, 700
    box_size = 40
    font_size = 30;
    box_font_diff = (box_size - font_size) / 2
    margin = 2
    furigana_size = 10

    pdfmetrics.registerFont(TTFont('Noto Sans JP', 'static/NotoSansJP-Regular.ttf'))
    pdf = canvas.Canvas(output_file, pagesize=letter)
    pdf.setFont('Noto Sans JP', font_size)

    tokenized = split_furigana(japanese_text)

    for pair in tokenized:
        jp = pair[0]

        if pair.__len__() > 1 and count_boxes(jp, kanji_list) > 0:
            pdf.setFont('Noto Sans JP', furigana_size)
            pdf.drawCentredString(x + furigana_offset(pair[0], kanji_list, font_size, box_size, margin), y + font_size + box_font_diff + margin, pair[1])
            pdf.setFont('Noto Sans JP', font_size)

        for char in jp:
            if char in kanji_list:
                pdf.setFillColor(colors.white)
                pdf.rect(x + margin, y - box_font_diff - 1, box_size, box_size, fill=True, stroke=True)
                pdf.setFillColor(colors.black)
                x += box_size + margin
            else:
                pdf.drawCentredString(x + box_size / 2, y, char)
                x += font_size + margin

            if x > 550:  # Move to the next line after reaching the end of the line
                x = 50
                y -= box_size + furigana_size + 3*margin

    pdf.save()

# Example usage:
japanese_text = "あさ、わたしは学校へいきます。友達と あそびます。ランチは おにぎりと みずです。学校のあと、図書館で ほんを よみます。かえりに、おかあさんが たべものを つくります。ねるとき、ねこと いっしょに ねます。たのしい いちにちでした。"
kanji_list = ["校", "友", "館", "図", "書", "館", "母", "食", "寝", "猫", "一", "日"]
output_file = "workbook.pdf"

create_workbook(japanese_text, kanji_list, output_file)