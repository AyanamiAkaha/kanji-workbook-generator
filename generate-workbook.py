#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import *
import MeCab
import jaconv

def split_furigana(text):
    mecab = MeCab.Tagger("-Ochasen")
    mecab.parse('')
    node = mecab.parseToNode(text)
    parsed = []
    while node:
        surface = node.surface
        features = node.feature.split(",")
        furigana = "" # in case there's no furigana
        if len(features) > 7:
            furigana = jaconv.kata2hira(features[7])
        parsed.append((surface, furigana))
        node = node.next
    return parsed

class WorkbookGenerator:
    def __init__(self, jp_fname, kanji_fname, output_fname, font_size=30, char_margin=2, page_size=A4, page_margin_x=50, page_margin_y=100):
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
        pdfmetrics.registerFont(TTFont('Noto Sans JP', 'static/NotoSansJP-Regular.ttf'))

        self.x = self.page_margin_x
        self.y = self.page_size[1] - self.page_margin_y

        self.pdf = canvas.Canvas(output_fname, pagesize=self.page_size)
        self.japanese_text = open(jp_fname, 'r').read()
        if self.japanese_text[self.japanese_text.__len__() - 1] == '\n':
            self.japanese_text = self.japanese_text[:-1]
        self.kanji_list = open(kanji_fname, 'r').read()
        if self.kanji_list[self.kanji_list.__len__() - 1] == '\n':
            self.kanji_list = self.kanji_list[:-1]

        self.kanji_stats = {}
        for char in self.kanji_list:
            self.kanji_stats[char] = 0
        for char in self.japanese_text:
            if char in self.kanji_list:
                self.kanji_stats[char] += 1
        
        self.kanji_count = 0
        for count in self.kanji_stats.values():
            if count > 0:
                self.kanji_count += 1

        self.start_page()
    
    def start_page(self):
        self.pdf.setFont('Noto Sans JP', self.furigana_size)
        self.pdf.drawString(self.page_margin_x, self.page_size[1] - self.page_margin_y/2, "%d of %d kanji" % (self.kanji_count, self.kanji_list.__len__()))
        self.pdf.drawCentredString(self.page_size[0] - self.page_margin_x, self.page_margin_y/2, self.pdf.getPageNumber().__str__())
        self.pdf.setFont('Noto Sans JP', self.font_size)
        self.x = self.page_margin_x
        self.y = self.page_size[1] - self.page_margin_y

    def count_boxes(self, text):
        count = 0
        for char in text:
            if char in self.kanji_list:
                count += 1
        return count

    def furigana_offset(self, text):
        total_chars = text.__len__()
        boxes = self.count_boxes(text)
        chars = total_chars - boxes
        return (chars * self.font_size + boxes*(self.box_size + 2*self.char_margin))/2

    def check_margins(self):
        if self.x > self.page_size[0] - self.page_margin_x:
            self.x = self.page_margin_x
            self.y -= self.box_size + self.furigana_size + 3*self.char_margin
        if self.y < self.page_margin_y:
            self.pdf.showPage()
            self.start_page()

    def write_text(self, text):
        tokenized = split_furigana(text)
        for pair in tokenized:
            jp = pair[0]
            if pair.__len__() > 1 and self.count_boxes(jp) > 0:
                self.pdf.setFont('Noto Sans JP', self.furigana_size)
                furigana_y = self.y + self.font_size + self.box_font_diff + self.char_margin;
                self.pdf.drawCentredString(self.x + self.furigana_offset(pair[0]), furigana_y, pair[1])
                self.pdf.setFont('Noto Sans JP', self.font_size)
            for char in jp:
                if char in self.kanji_list:
                    self.pdf.setFillColor(colors.white)
                    self.pdf.rect(self.x + self.char_margin, self.y - self.box_font_diff - 1, self.box_size, self.box_size, fill=True, stroke=True)
                    self.pdf.setFillColor(colors.black)
                    self.x += self.box_size + self.char_margin
                else:
                    self.pdf.drawCentredString(self.x + self.box_size / 2, self.y, char)
                    self.x += self.font_size + self.char_margin
                self.check_margins()
        
    def create_workbook(self):
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

PAGE_SIZES = {
    'A0': A0,
    'A1': A1,
    'A2': A2,
    'A3': A3,
    'A4': A4,
    'A5': A5,
    'A6': A6,
    'A7': A7,
    'A8': A8,
    'A9': A9,
    'A10': A10,
    'B0': B0,
    'B1': B1,
    'B2': B2,
    'B3': B3,
    'B4': B4,
    'B5': B5,
    'B6': B6,
    'B7': B7,
    'B8': B8,
    'B9': B9,
    'B10': B10,
    'C0': C0,
    'C1': C1,
    'C2': C2,
    'C3': C3,
    'C4': C4,
    'C5': C5,
    'C6': C6,
    'C7': C7,
    'C8': C8,
    'C9': C9,
    'C10': C10,
    'LETTER': LETTER,
    'LEGAL': LEGAL,
    'ELEVENSEVENTEEN': ELEVENSEVENTEEN,
    'JUNIOR_LEGAL': JUNIOR_LEGAL,
    'HALF_LETTER': HALF_LETTER,
    'GOV_LETTER': GOV_LETTER,
    'GOV_LEGAL': GOV_LEGAL,
    'TABLOID': TABLOID,
    'LEDGER': LEDGER
}

def main():
    parser = argparse.ArgumentParser(description='Generate a workbook for Japanese kanji practice.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('-j', '--japanese-text', metavar='japanese_text', type=str, help='file with japanese text to be used in the workbook', required=True)
    parser.add_argument('-k', '--kanji-list', metavar='kanji_list', type=str, help='file with the list of kanji to be used in the workbook', required=True)
    parser.add_argument('-o', '--output-file', metavar='output_file', type=str, help='Output file name', required=True)
    parser.add_argument('--font-size', metavar='font_size', type=int, help='Font size', default=30)
    parser.add_argument('--char-margin', metavar='char_margin', type=int, help='Character margin', default=2)
    parser.add_argument('--page-size', metavar='page_size', type=str, help='Page size', default='A4', choices=PAGE_SIZES.keys())
    parser.add_argument('--page-margin-x', metavar='page_margin_x', type=int, help='Page margin x', default=50)
    parser.add_argument('--page-margin-y', metavar='page_margin_y', type=int, help='Page margin y', default=100)
    args = parser.parse_args()

    page_size = PAGE_SIZES[args.page_size]

    generator = WorkbookGenerator(args.japanese_text, args.kanji_list, args.output_file, font_size=args.font_size, char_margin=args.char_margin, page_size=page_size, page_margin_x=args.page_margin_x, page_margin_y=args.page_margin_y)
    generator.create_workbook()

if __name__ == "__main__":
    main()