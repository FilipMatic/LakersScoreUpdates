#!/usr/bin/env python
from Foundation import NSUserNotification
from Foundation import NSUserNotificationCenter
from Foundation import NSUserNotificationDefaultSoundName
from optparse import OptionParser
from requests import get
from contextlib import closing
from bs4 import BeautifulSoup

def main():
    get_data() # while true this

def get_data():
    # post_notification()
    raw_html = get_html('https://www.google.com/search?q=womens+world+cup&oq=womens+world+cup&aqs=chrome..69i57j0l5.2667j1j1&sourceid=chrome&ie=UTF-8')

    if raw_html is not None:
        html = BeautifulSoup(raw_html, 'html.parser')
        # print(type(html))
        # print(html)
        # idk = html.find(class_='ellipsisize kno-fb-ctx')
        idk = html.find_all('div')[300]
        idk2 = html.find(class_='ellipsisize kno-fb-ctx')
        print(idk2)

def post_notification():
    parser = OptionParser(usage='%prog -t TITLE -m MESSAGE')
    parser.add_option('-t', '--title', action='store', default='Q3 - 4:22')
    parser.add_option('-m', '--message', action='store', default='Lakers: 100\nX: 0')
    parser.add_option('--no-sound', action='store_false', default=True, dest='sound')

    options, args = parser.parse_args()

    notification = NSUserNotification.alloc().init()
    notification.setTitle_(options.title)
    notification.setInformativeText_(options.message)
    if options.sound:
        notification.setSoundName_(NSUserNotificationDefaultSoundName)

    center = NSUserNotificationCenter.defaultUserNotificationCenter()
    center.deliverNotification_(notification)

def get_html(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_response_html(resp):
                #print(resp.content)
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_response_html(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 and content_type is not None and content_type.find('html') > -1)

def log_error(e):
    print(e)

if __name__ == '__main__':
    main()