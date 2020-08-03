# Instagram posts's comments parser

## Script's aim

It's simple script for scrapping first level comments for single post

## How to use it

### Installation

You should have python 3.7 or higher on your pc.

For install requirements use `pip install -r requirements.txt`. I recommend use virtual virtual environments.

### How to run

For run script use ` python insta_comment_parser.py --post {post_shortcode} `

All script's params:

1. `--post` - instagram post's shortcode
2. `--skip_author` - skip author's comments
3. `--xlsx_file_name` - file name
4. `--enable_debug` - enable debug logs