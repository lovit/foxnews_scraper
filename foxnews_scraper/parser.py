def parse_headline(soup):
    h1 = soup.select('h1[class=headline]')
    if not h1:
        return ''
    return h1[0].text.strip()

def parse_author(soup):
    a = soup.select('div[class^=article-meta] a')
    names = [ai.text.strip() for ai in a if '/person/' in ai.attrs.get('href', '')]
    if not names:
        return ''
    return ', '.join(names)

def parse_date(soup):
    time = soup.select('div[class=article-date] time')
    if not time:
        return ''
    return time[0].text.strip()

def parse_content(soup):
    phrases = soup.select('div[class=article-body] p')
    if not phrases:
        return ''
    return '\n'.join(p.text.strip() for p in phrases).strip()

def parse_category(soup):
    div = soup.select('div[class=eyebrow]')
    if not div:
        return ''
    return div[0].text

def parse_page(url):
    """
    Argument
    --------
    url : str
        URL of news article

    Returns
    -------
    dict format information. keys are [headline, author, date, content, category, url, scraped_at]
    """

    soup = get_soup(url)
    return {
        'headline': parse_headline(soup),
        'author': parse_author(soup),
        'date': parse_date(soup),
        'content': parse_content(soup),
        'category': parse_category(soup),
        'url': url,
        'scraped_at': now(),
    }