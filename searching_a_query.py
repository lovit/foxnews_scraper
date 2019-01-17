import argparse
import json
import os
from foxnews_scraper import yield_articles_from_search_result

def save(json_obj, directory):
    date = json_obj.get('date', '')[:10]
    urlpart = json_obj['url'].split('/')[-1]
    filepath = '{}/{}_{}.json'.format(directory, date, urlpart)
    with open(filepath, 'w', encoding='utf-8') as fp:
        json.dump(json_obj, fp, indent=2, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=str, default='./output', help='Output directory')
    parser.add_argument('--begin_date', type=str, default='2019-01-01', help='yyyy-mm-dd form')
    parser.add_argument('--end_date', type=str, default='2019-01-10', help='yyyy-mm-dd form')
    parser.add_argument('--sleep', type=float, default=2, help='Sleep time for each submission (post)')
    parser.add_argument('--max_num', type=int, default=15, help='Number of scrapped articles')
    parser.add_argument('--query', type=str, default='korea', help='Number of scrapped articles')

    args = parser.parse_args()
    directory = args.directory
    begin_date = args.begin_date
    end_date = args.end_date
    sleep = args.sleep
    max_num = args.max_num
    query = args.query

    # check output directory
    directory += '/%s' % query
    if not os.path.exists(directory):
        os.makedirs(directory)

    for article in yield_articles_from_search_result(query, begin_date, end_date, max_num, sleep):
        save(article, directory)
        print('scraped {}'.format(article.get('url'), ''))

if __name__ == '__main__':
    main()