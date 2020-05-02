import requests
from lxml import html
import pandas as pd
import threading
from queue import Queue


# This project is in process.
class scraper:
    # todo
    # Lag keybinds, og UI
    # Specific virker ikke skikkelig
    # Lag funksjon for å søke direkte etter tekst

    def __init__(self):
        self.url = None
        self.page = None
        self.links = []
        self.tree = None
        self.counter = 0
        self.grab = False
        self.tables = None
        self.specific = None
        self.get_tables = False
        self.threads = []
        self.get_text = False
        self.keyword = None
        self.checked = []
        self.other = {
            'links': []
        }
        self.queue = Queue()

    def __call__(self, url=None, specific=None, keyword=None, grab=False):
        if url is not None:
            self.url = url
        if specific is not None:
            self.specific = specific
        if grab:
            self.grab = True
        else:
            self.grab = False
        self.__update__()

    def __update__(self):
        try:
            self.page = requests.get(self.url, timeout=5)
            self.tree = html.fromstring(self.page.content)
            self.__hrefs__()
            # self.__base_link__()
            self.checked.append(self.url)
        except:
            pass

    def __base_link__(self):
        try:
            self.base_url = (str(self.url).split('//')[1]).split('/')[0]
        except:
            pass

    def __hrefs__(self):
        try:
            for href in self.tree.iterlinks():
                if 'http' in href[2]:
                    if not href[2] in self.other['links']:
                        if self.specific in href[2]:
                            if self.grab:
                                self.links.append(href[2])
                            elif not self.grab:
                                self.__setitem__('links', href[2])
                                self.counter += 1
                        elif self.specific is None:
                            self.__setitem__('link', href)
                            self.counter += 1
                        else:
                            pass
            if self.grab:
                return self.grab
        except:
            pass

    def __tables__(self):
        try:
            self.tables = pd.read_html(self.page.content)
        except:
            self.tables = None

    def __delitem__(self, sub_name, value):
        for x, z in self.other[sub_name]:
            if z == value:
                self.other[sub_name].pop(x)

    def __setitem__(self, key, value):
        if key in self.other:
            self.other[key].append(value)
        else:
            self.other[key] = [value]

    def __threadscraping__(self):
        while True:
            try:
                self.__call__(url=self.url)
                break
            except:
                break

    def __crawl__(self):
        counter = 0
        while True:
            stats = {
                'Links found': self.counter,
                'Links searched': counter,
                'Open threads': self.queue.qsize()
            }
            if self.counter - 1 > counter:
                if not self.queue.full():
                    try:
                        self.url = self.other['links'][counter]
                        t = threading.Thread(target=self.__threadscraping__())
                        self.queue.put(t)
                        self.threads.append(t)
                        print(stats)
                        print(self.url)
                        counter += 1
                    except:
                        pass

    def to_excel(self, filename=None, index=0):
        if filename:
            if '.xlsx' not in filename:
                filename += '.xlsx'
        df = pd.DataFrame(data=self.tables[index])
        df.to_excel(filename)
