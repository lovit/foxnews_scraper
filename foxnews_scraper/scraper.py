import json
import time
import requests
from .parser import parse_page

url_base = 'https://www.foxnews.com/search-results/search?q={}&ss=fn&sort=latest&type=story&min_date={}&max_date={}&start={}'
request_base = 'https://api.foxnews.com/v1/content/search?q={}&fields=date,description,title,url,image,type,taxonomy&sort=latest&section.path=fnc&type=article&min_date={}&max_date={}&start={}&callback=angular.callbacks._0&cb=2019117193'

def yield_articles_from_search_result(query, begin_date, end_date, max_num, sleep=1.5):
    docs, num_found = get_info_from_search_page(query, begin_date, end_date, 0)
    if max_num <= num_found:
        docs = docs[:max_num]

    def yield_loop(docs):
        for doc in docs:
            url = doc.get('url', '')
            if not url:
                continue
            json_obj = parse_page(url)
            doc['author'] = json_obj['author']
            doc['headline'] = json_obj['headline']
            doc['content'] = json_obj['content']
            yield doc
            time.sleep(sleep)

    for doc in yield_loop(docs):
        yield doc
    for start in range(10, max_num, 10):
        docs, _ = get_info_from_search_page(query, begin_date, end_date, start)
        for doc in yield_loop(docs):
            yield doc

def get_info_from_search_page(query, begin_date, end_date, start):
    def parse_info(doc):
        date = doc.get('date', '')
        description = doc.get('description', '')
        category = [taxo.get('adTag', '') for taxo in doc.get('taxonomy', [])]
        category = [c for c in category if c]
        category = ', '.join(category) if category else ''
        title = doc.get('title', '')
        url = doc.get('url', [''])
        if isinstance(url, list):
            url = url[0]

        return {'date': date, 'description': description, 'category': category, 'title': title, 'url': url}

    url = url_base.format(query, begin_date, end_date, start)
    request_url = request_base.format(query, begin_date, end_date, start)
    headers = {
        'Referer': url,
        'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    r = requests.get(request_url, headers=headers)
    # len('angular.callbacks._0(') = 21, last character is ')'
    response = json.loads(r.text[21:-1])
    num_found = response.get('response', {}).get('numFound', 0)
    docs = [parse_info(doc) for doc in response.get('response', {}).get('docs', [])]
    return docs, num_found
