import urllib2
import math
import re
from bs4 import BeautifulSoup
from pprint import pprint
from threading import Thread
from collections import deque
import time
from ua import UserAgent
class GoogleSearch:
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8"
    SEARCH_URL = "https://google.com/search"
    RESULT_SELECTOR = ".srg h3.r a"
    TOTAL_SELECTOR = "#resultStats"
    RESULTS_PER_PAGE = 10
    DEFAULT_HEADERS = [
            ('User-Agent', USER_AGENT),
            ("Accept-Language", "en-US,en;q=0.5"),
        ]

    def search(self, query, num_results = 10, prefetch_pages = True, prefetch_threads = 10, language = "en"):
        searchResults = []
        pages = int(math.ceil(num_results / float(GoogleSearch.RESULTS_PER_PAGE)));
        fetcher_threads = deque([])
        total = None;
        ua = UserAgent()
        ua = ua.random()
        DEFAULT_HEADERS = [
            ('User-Agent', ua),
            ("Accept-Language", "en-US,en;q=0.5"),
        ]
        # print ua
        for i in range(pages) :
            start = i * GoogleSearch.RESULTS_PER_PAGE
            opener = urllib2.build_opener()
            opener.addheaders = GoogleSearch.DEFAULT_HEADERS
            response = opener.open(GoogleSearch.SEARCH_URL + "?q="+ urllib2.quote(query) + "&hl=" + language + ("" if start == 0 else ("&start=" + str(start))))
            soup = BeautifulSoup(response.read(), "lxml")
            response.close()
            if total is None:
                totalText = soup.select(GoogleSearch.TOTAL_SELECTOR)[0].children.next().encode('utf-8')
                total = long(re.sub("[',\. ]", "", re.search("(([0-9]+[',\. ])*[0-9]+)", totalText).group(1)))
                
            results = self.parseResults(soup.select(GoogleSearch.RESULT_SELECTOR))
            if len(searchResults) + len(results) > num_results:
                del results[num_results - len(searchResults):]
            searchResults += results
        return SearchResponse(searchResults, total);
    def parseResults(self, results):
        tStart = time.time()
        searchResults = [];
        for result in results:
            title = result.text
            searchResults.append(SearchResult(title))
        return searchResults
class SearchResponse:
    def __init__(self, results, total):
        self.results = results;
        self.total = total;

class SearchResult:
    def __init__(self, title):
        self.title = title
        self.__text = None
        self.__markup = None