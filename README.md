# install

Simple script for generating kanji workbooks. Requires mecab:

```
sudo apt-get install libmecab-dev mecab mecab-ipadic-utf8
```

you also need to set MECABRC env variable to correct mecab rc,
a default one is installed under /etc/mecabrc:

```
export MECABRC=/etc/mecabrc
```

To install dependencies:

```
virtualenv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

# usage

```
usage: generate-workbook.py [-h] [-v] -j japanese_text -k kanji_list -o output_file [--font-size font_size] [--char-margin char_margin]
                            [--page-size page_size] [--page-margin-x page_margin_x] [--page-margin-y page_margin_y]

Generate a workbook for Japanese kanji practice.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -j japanese_text, --japanese-text japanese_text
                        file with japanese text to be used in the workbook
  -k kanji_list, --kanji-list kanji_list
                        file with the list of kanji to be used in the workbook
  -o output_file, --output-file output_file
                        Output file name
  --font-size font_size
                        Font size
  --char-margin char_margin
                        Character margin
  --page-size page_size
                        Page size
  --page-margin-x page_margin_x
                        Page margin x
  --page-margin-y page_margin_y
                        Page margin y
```

# known issues

- ~~It seems furigana module does not handle jinmeiyou kanji correctly. For
example texts with 也 will crash the application.~~ (fixed)
