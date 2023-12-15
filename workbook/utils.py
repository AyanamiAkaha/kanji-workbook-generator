import re
import MeCab
import jaconv

whitespace = re.compile(r'\s+', re.UNICODE)

def split_furigana(text: str) -> list[tuple[str, str]]: # list of (kanji, furigana)
    mecab = MeCab.Tagger('-Ochasen')
    mecab.parse('')
    node = mecab.parseToNode(text)
    parsed = []
    while node:
        surface = node.surface
        features = node.feature.split(',')
        furigana = '' # in case there's no furigana
        if len(features) > 7:
            furigana = jaconv.kata2hira(features[7])
        parsed.append((surface, furigana))
        node = node.next
    return parsed

def strip_white(text: str) -> str:
    return re.sub(whitespace, '', text)
