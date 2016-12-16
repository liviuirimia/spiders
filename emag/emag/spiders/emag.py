from __future__ import absolute_import
import scrapy
from emag.items import EmagItem

base_url = 'http://wwww.emag.ro'


class EmagSpider(scrapy.Spider):
    name = "emag"

    def start_requests(self):
        url = 'http://www.emag.ro/laptopuri/c'

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        def extract_css(query):
            return response.css(query).extract()

        nume = extract_css(".middle-container a::attr(title)")
        link = extract_css(".middle-container a::attr(href)")
        pret = extract_css(".pret-produs-listing .price-over .money-int::text")

        for x in xrange(len(nume)):
            yield EmagItem(produs=nume[x], pret=pret[x], link=base_url+link[x])

        next_page = response.css("a+.emg-icon-holder::attr(href)").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
