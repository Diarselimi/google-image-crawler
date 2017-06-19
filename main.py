import sys
import re
from contextlib import closing
from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait


def get_page(url):

    try:
        with closing(Firefox()) as browser:
            browser.get(url)
            page_source = browser.page_source
            return page_source

    except:
        return ""


def get_all_links(page):
    urls = re.findall('\"data:image/jpeg.+\"', page)
    output = []
    for url in urls:
        res = re.search("(?P<url>data:image/jpeg;base64[^\s]+)(?:\"|\">|\"])", url)
        if res:
            res = re.sub(r'\\u003d', '=', res.group('url'))
            output.append(res)
    return output


def crawl_web(seed):
    return get_all_links(get_page(seed))

if len(sys.argv) != 3:
    print("Enter path as first parameter and keyword as second.")
    exit()


app_path = sys.argv[1]
book_title = sys.argv[2]
book_title_splited = book_title.split(' ')
book_slug = '-'.join(book_title_splited) + ".txt"
url = "https://www.google.com/search?newwindow=1&site=&tbm=isch&source=hp&biw=1366&bih=672&q=" + '+'.join(book_title_splited)

urls = crawl_web(url)
for url in urls:
    with open(app_path + book_slug, 'a') as file:
        file.write(url + '\n')
