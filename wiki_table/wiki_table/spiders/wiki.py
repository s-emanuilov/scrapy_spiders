# -*- coding: utf-8 -*-
import scrapy


class WikiSpider(scrapy.Spider):
    name = "wiki"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = (
        'https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population',
    )

    def parse(self, response):
        table = response.xpath('//table')[3]
        trs = table.xpath('.//tr')[1:]
        for tr in trs:
            rank = tr.xpath('.//td[1]/text()').extract_first()
            city = tr.xpath('.//td[2]//text()').extract_first()
            state = tr.xpath('.//td[3]//text()').extract()[-1]

            yield {'rank': rank,
                   'city': city,
                   'state': state}
