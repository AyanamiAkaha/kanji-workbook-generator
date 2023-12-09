#!/usr/bin/env python3

import re

import argparse
import MeCab

class SentenceFinder:
    """
    Finds sentences for each kanji from the list in given text.
    """
    def __init__(self, text, kanji_list):
        self.mecab = MeCab.Tagger("-Owakati")
        self.kanji_list = kanji_list
        self.text = text
        self.sentence_counts = {ch: 0 for ch in kanji_list}
        self.sentences = []
        self.word_counts = {ch: 0 for ch in kanji_list}
        self.words = []

    def find_words(self):
        """
        Finds words for each kanji from the list in given text.
        """
        for word in self.mecab.parse(self.text).split():
            found = False
            for kanji in self.kanji_list:
                if kanji in word:
                    self.word_counts[kanji] += 1
                    found = True
            if found:
                self.words.append(word.strip())

    def find_sentences(self):
        """
        Finds sentences for each kanji from the list in given text.
        """
        regex = re.compile("[^。.\n\r]*[。.\n\r]")
        for sentence in regex.findall(self.text):
            found = False
            if re.compile("[。.\n\r]").match(sentence):
                continue
            for kanji in self.kanji_list:
                if self.sentence_counts[kanji] > 10:
                    continue
                if kanji in sentence:
                    self.sentence_counts[kanji] += 1
                    found = True
            if found:
                self.sentences.append(sentence.strip())


def main():
    parser = argparse.ArgumentParser(description="Split text into sentences.")
    parser.add_argument("-t", "--text", metavar="text", type=str, help="file with text to be split", required=True)
    parser.add_argument("-k", "--kanji-list", metavar="kanji_list", type=str, help="file with the list of kanji to be used in the workbook", required=True)
    args = parser.parse_args()

    text = ""
    with open(args.text, "r") as f:
        text = f.read()
    kanji_list = ""
    with open(args.kanji_list, "r") as f:
        kanji_list = f.read()
    kanji_list = kanji_list.replace("\n", "")
    kanji_list = kanji_list.replace("\r", "")
    parser = SentenceFinder(text, kanji_list)
    parser.find_sentences()

    for kanji, count in sorted(parser.sentence_counts.items(), key=lambda x: x[1], reverse=True):
        print("%s: %d" % (kanji, count))

    print("\nSentences:")
    for sentence in parser.sentences:
        print(sentence)

if __name__ == "__main__":
    main()
