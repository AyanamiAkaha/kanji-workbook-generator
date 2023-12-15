#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from enum import Enum
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import *

from .utils import split_furigana, strip_white

class WorkbookMode(Enum):
    EXERCISES = 1
    ANSWERS = 2

class WorkbookGenerator:
    def __init__(
            self,
            text: str,
            kanji_list: str,
            output_fname: str,
            font_size: int = 14,
            char_margin: int = 2,
            page_size: tuple = A4,
            page_margin_x: int = 50,
            page_margin_y: int = 50,
            limit: int = math.inf,
            mode: WorkbookMode = WorkbookMode.EXERCISES,
    ) -> None:
        self.japanese_text = text
        self.kanji_list = strip_white(kanji_list)
        self.limit = limit
        self.output_fname = output_fname
        self.page_size = page_size
        self.page_margin_x = page_margin_x
        self.page_margin_y = page_margin_y
        self.box_size = font_size * 1.25
        self.font_size = font_size
        self.box_font_diff = (self.box_size - self.font_size) / 2
        self.char_margin = char_margin
        self.furigana_size = font_size / 3
        self.paragraph_margin = self.furigana_size
        self.mode = mode
        pdfmetrics.registerFont(TTFont('Noto Sans JP', 'static/NotoSansJP-Regular.ttf'))

        self.x = self.page_margin_x
        self.y = self.page_size[1] - self.page_margin_y

        self.pdf = canvas.Canvas(output_fname, pagesize=self.page_size)

        self.kanji_stats = {char: 0 for char in self.kanji_list}
        self.kanji_counts = {char: 0 for char in self.kanji_list}
        for char in self.japanese_text:
            if char in self.kanji_list:
                self.kanji_stats[char] += 1

        self.kanji_count = 0
        for count in self.kanji_stats.values():
            if count > 0:
                self.kanji_count += 1

        self.start_page()

    def start_page(self) -> None:
        self.pdf.setFont('Noto Sans JP', self.furigana_size)
        self.pdf.drawString(self.page_margin_x, self.page_size[1] - self.page_margin_y/2, "%d of %d kanji" % (self.kanji_count, self.kanji_list.__len__()))
        self.pdf.drawCentredString(self.page_size[0] - self.page_margin_x, self.page_margin_y/2, self.pdf.getPageNumber().__str__())
        self.pdf.setFont('Noto Sans JP', self.font_size)
        self.x = self.page_margin_x
        self.y = self.page_size[1] - self.page_margin_y

    def count_boxes(self, text: str) -> int:
        count = 0
        for char in text:
            if self.need_kanji(char):
                count += 1
        return count

    def furigana_offset(self, text: str) -> int:
        total_chars = text.__len__()
        boxes = self.count_boxes(text)
        chars = total_chars - boxes
        return (chars * self.font_size + boxes*(self.box_size + 2*self.char_margin))/2

    def check_margins(self) -> None:
        if self.x > self.page_size[0] - self.page_margin_x:
            self.x = self.page_margin_x
            self.y -= self.box_size + self.furigana_size + 3*self.char_margin
        if self.y < self.page_margin_y:
            self.pdf.showPage()
            self.start_page()
    
    def need_kanji(self, kanji: str) -> bool:
        return kanji in self.kanji_stats and self.kanji_counts[kanji] < self.limit

    def write_text(self, text: str) -> None:
        tokenized = split_furigana(text)
        for pair in tokenized:
            jp = pair[0]
            if pair.__len__() > 1 and self.count_boxes(jp) > 0:
                self.pdf.setFont('Noto Sans JP', self.furigana_size)
                furigana_y = self.y + self.font_size + self.box_font_diff + self.char_margin;
                self.pdf.drawCentredString(self.x + self.furigana_offset(pair[0]), furigana_y, pair[1])
                self.pdf.setFont('Noto Sans JP', self.font_size)
            for char in jp:
                if self.need_kanji(char):
                    if self.mode == WorkbookMode.EXERCISES:
                        self.pdf.setFillColor(colors.white)
                        self.pdf.rect(self.x + self.char_margin, self.y - self.box_font_diff - 1, self.box_size, self.box_size, fill=True, stroke=True)
                        self.pdf.setFillColor(colors.black)
                        self.x += self.box_size + self.char_margin
                        self.kanji_counts[char] += 1
                    else:
                        self.pdf.setFillColor(colors.red)
                        self.pdf.drawCentredString(self.x + self.box_size / 2, self.y, char)
                        self.x += self.box_size + self.char_margin
                        self.pdf.setFillColor(colors.black)
                else:
                    self.pdf.drawCentredString(self.x + self.box_size / 2, self.y, char)
                    self.x += self.font_size + self.char_margin
                self.check_margins()

    def create_workbook(self) -> None:
        lines = self.japanese_text.split('\n')
        for idx, l in enumerate(lines):
            if l != '':
                self.write_text(l)
            if idx <= lines.__len__() - 1:
                self.x = self.page_margin_x
                self.y -= self.box_size + self.furigana_size + 3*self.char_margin + self.paragraph_margin
                self.check_margins()
        self.pdf.save()
        missing_kanji = ""
        print("Kanji stats:\n")
        for kanji, count in sorted(self.kanji_stats.items(), key=lambda x: x[1], reverse=True):
            if count == 0:
                missing_kanji += kanji
            else:
                print("%s: %d" % (kanji, count))
        print("\nMissing kanji: %d" % missing_kanji.__len__())
        print(missing_kanji)
        print("\nWorkbook saved to %s" % self.output_fname)