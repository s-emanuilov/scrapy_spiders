# -*- coding: utf-8 -*-
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import Spider
from scrapy.http import Request
import re


class EStoresSpider(Spider):
    name = 'e_stores'
    download_timeout = 12

    def start_requests(self):
        with open('/Users/Mac/Projects/scraper_8m/scraper_8m/sites.txt', 'r') as f:
            for url in f.readlines():
                url = url.strip()
                if not url.startswith('http'):
                    url = "http://" + url
                yield Request(url, callback=self.parse_site, errback=self.handle_error)

    def parse_site(self, response):
        url = response.url

        e_store = 0

        try:
            meta_title = response.xpath('//title/text()').extract_first().lower()
        except AttributeError:
            meta_title = "None"

        try:
            meta_description = response.xpath('//meta[@name="description"]/@content').extract_first().lower()
        except AttributeError:
            meta_description = "None"

        needles_meta_top = [u"онлайн магазин"]
        needles_meta_low = [u"купете", u"магазин", u"цени"]

        for needle in needles_meta_top:
            if needle in meta_title:
                e_store += 2
            if needle in meta_description:
                e_store += 2

        for needle in needles_meta_low:
            if needle in meta_title:
                e_store += 1
            if needle in meta_description:
                e_store += 0.5

        # Check if prices marked with itemprop
        prices = response.xpath('//*[@itemprop="price"]').extract()

        if (len(prices) > 0):
            e_store += 2

        try:
            body = response.xpath('//body').extract_first().lower()
        except AttributeError:
            body = "None"

        needles_body_top = [u"количка", u"кошница", u"добави в количката", u"добави в кошницата"]
        needles_popular_cms = ["catalog/view/theme/", "wp-content/plugins/woocommerce/"]
        needles_body_middle = [u"поръчай онлайн", u"купи онлайн"]
        needles_body_low = [u"лв.", u"лева", u"купете", u"купи", u"вход", u"регистрация", u"поръчай"]

        for needle in needles_body_top:
            if needle in body:
                e_store += 1

        for needle in needles_popular_cms:
            if needle in body:
                e_store += 1.5

        for needle in needles_body_middle:
            if needle in body:
                e_store += 0.5

        for needle in needles_body_low:
            if needle in body:
                e_store += 0.15

        email = re.findall(r'[\w\.-]+@[\w\.-]+', response.body)

        try:
            email_1 = email[0]
        except IndexError:
            email_1 = "none"

        try:
            email_2 = email[1]
        except IndexError:
            email_2 = "none"

        yield {
            "url": url,
            "e_store": e_store,
            "email_1": email_1,
            "email_2": email_2,
        }

    def handle_error(self, failure):
        url = failure.request.url

        yield {
            "url": url,
            "e_store": 'error_parsing',
            "email_1": 'error_parsing',
            "email_2": 'error_parsing',
        }
