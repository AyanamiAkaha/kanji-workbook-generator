#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import math

from workbook import WorkbookGenerator, SentenceFinder, WorkbookMode, PAGE_SIZES

def main():
    parser = argparse.ArgumentParser(description='Generate a workbook for Japanese kanji practice.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('-j', '--japanese-text', metavar='japanese_text', type=str, help='file with japanese text to be used in the workbook', required=True)
    parser.add_argument('-k', '--kanji-list', metavar='kanji_list', type=str, help='file with the list of kanji to be used in the workbook', required=True)
    parser.add_argument('-o', '--output-file', metavar='output_file', type=str, help='Output file name', required=True)
    parser.add_argument('--font-size', metavar='font_size', type=int, help='Font size', default=14)
    parser.add_argument('--char-margin', metavar='char_margin', type=int, help='Character margin', default=2)
    parser.add_argument('--page-size', metavar='page_size', type=str, help='Page size', default='A4', choices=PAGE_SIZES.keys())
    parser.add_argument('--page-margin-x', metavar='page_margin_x', type=int, help='Page margin x', default=50)
    parser.add_argument('--page-margin-y', metavar='page_margin_y', type=int, help='Page margin y', default=50)
    parser.add_argument('--limit', metavar='limit', type=int, help='Limit of kanji per workbook', default=math.inf)
    mode = parser.add_mutually_exclusive_group(required=False)
    mode.add_argument('--sentences', action='store_true', help='Use sentences instead of words')
    mode.add_argument('--words', action='store_true', help='Use words instead of sentences')
    parser.add_argument('--randomize', action='store_true', help='Randomize sentences or words')
    args = parser.parse_args()

    if args.randomize and not (args.sentences or args.words):
        parser.error('Randomize is supported only for sentences or words')
    
    kanji_list = open(args.kanji_list, 'r').read()
    if kanji_list[kanji_list.__len__() - 1] == '\n':
        kanji_list = kanji_list[:-1]

    text =  open(args.japanese_text, 'r').read()
    if text[text.__len__() - 1] == '\n':
        text = text[:-1]

    if args.sentences:
        parser = SentenceFinder(text, kanji_list, limit=args.limit, randomize=args.randomize)
        parser.find_sentences()
        text = '\n'.join(map(lambda v: "　%d.　%s" % (v[0], v[1]), enumerate(parser.sentences)))
    elif args.words:
        parser = SentenceFinder(text, kanji_list, limit=args.limit)
        parser.find_words()
        text = '\n'.join(parser.words)

    page_size = PAGE_SIZES[args.page_size]

    generator = WorkbookGenerator(
        text,
        kanji_list,
        args.output_file,
        font_size=args.font_size,
        char_margin=args.char_margin,
        page_size=page_size,
        page_margin_x=args.page_margin_x,
        page_margin_y=args.page_margin_y,
        limit=args.limit,
    )
    generator.create_workbook()
    answers_fname = args.output_file.replace('.pdf', '_answers.pdf')
    answers = WorkbookGenerator(
        text,
        kanji_list,
        answers_fname,
        font_size=args.font_size,
        char_margin=args.char_margin,
        page_size=page_size,
        page_margin_x=args.page_margin_x,
        page_margin_y=args.page_margin_y,
        limit=args.limit,
        mode=WorkbookMode.ANSWERS,
    )
    answers.create_workbook()

if __name__ == "__main__":
    main()