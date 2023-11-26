Simple script for generating kanji workbooks. Requires mecab:

```
sudo apt-get install libmecab-dev mecab mecab-ipadic-utf8
sudo -H pip3 install mecab-python3
sudo -H pip3 install jaconv
```

you also need to set MECABRC env variable to correct mecab rc,
a default one is installed under /etc/mecabrc:

```
export MECABRC=/etc/mecabrc
```