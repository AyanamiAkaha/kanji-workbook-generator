#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MeCab
import jaconv

def furigana(text):
    mecab = MeCab.Tagger("-Ochasen")
    mecab.parse('')
    node = mecab.parseToNode(text)
    parsed = []
    idx = 0
    while node:
        surface = node.surface
        features = node.feature.split(",")
        feature_idx = 7
        if len(features) <= 7:
            feature_idx = len(features) - 1
        print("%d. %s: %s" % (idx, surface, jaconv.kata2hira(features[feature_idx])))
        node = node.next
        idx = idx + 1

if __name__ == '__main__':
    furigana("プロデューサーの丘野塔也さんが「人の指とか入ってたら面白くない？」")