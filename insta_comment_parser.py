import argparse
import logging
from xlsxwriter import Workbook
from instaloader import Instaloader, Post


def parse_args():
    parser = argparse.ArgumentParser(description='Instgram comment parser')
    parser.add_argument('--post', type=str, required=True,
                        help="post id")
    parser.add_argument('--skip_author', type=bool, default=True,
                        help="get image directory, delault='test_photos'")
    parser.add_argument('--xlsx_file_name', type=str, default='comments.xlsx',
                        help="Excel file name")
    parser.add_argument('--enable_debug', type=bool, default=True,
                        help="Logging enable")
    args = parser.parse_args()
    return args.post, args.skip_author, args.xlsx_file_name, args.enable_debug


def get_comments(post, skip_author):
    L = Instaloader()
    post = Post.from_shortcode(L.context, post)
    owner_username = post.owner_username
    comments = []
    for comment in post.get_comments():
        if skip_author and owner_username == comment.owner.username:
            continue
        comments.append({
            'username': comment.owner.username,
            'created_at': str(comment.created_at_utc),
            'text': comment.text})
    logging.info(f'Downloaded {len(comments)} comments')
    return comments


def write_comments_to_xlsx(xlsx_file_name, comments):
    workbook = Workbook(xlsx_file_name)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    worksheet.set_column('A:A', 55)
    worksheet.set_column('B:B', 25)
    worksheet.set_column('C:C', 100)
    cell_format = workbook.add_format()
    # cell_format.set_text_wrap()
    col = 0
    for comment_number, comment in enumerate(comments):
        row = comment_number
        worksheet.write_url(
            row, col,     f"https://www.instagram.com/{comment['username']}", bold)
        worksheet.write(row, col + 1, comment['created_at'])
        worksheet.write(row, col + 2, comment['text'], cell_format)
    workbook.close()
    logging.info(f'Saved {len(comments)} comments to {xlsx_file_name}')


def main():
    post, skip_author, xlsx_file_name, enable_debug = parse_args()
    if enable_debug:
        logging.basicConfig(level=logging.INFO)
    comments = get_comments(post, skip_author)
    write_comments_to_xlsx(xlsx_file_name, comments)


if __name__ == "__main__":
    main()
