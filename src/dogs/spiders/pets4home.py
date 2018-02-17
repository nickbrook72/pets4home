# -*- coding: utf-8 -*-
import scrapy


class Pets4homeSpider(scrapy.Spider):
    name = 'pets4home'
    allowed_domains = ['pets4homes.co.uk']
    start_urls = ['https://www.pets4homes.co.uk/search/?type_id=3&results=20&sort=datenew&page=1']

    def parse(self, response):
        for div_listing in response.css("div.profilelisting"):
            categories = div_listing.css('div.categories')

            price = div_listing.css('div.listingprice::text').extract_first()
            if price:
                price = price[1:].replace(',','')
            yield {
                'title': div_listing.css('h2.headline a::text').extract_first(),
                'location': div_listing.css('div.location b::text').extract_first().strip(),
                'breed': categories.css('a:nth-child(3)::text').extract_first(),
                'description': div_listing.css('.description::text').extract_first(),
                'price': price
            }

            next_page = response.css('div.paginate').xpath("//a[contains(., '»')]/@href").extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield response.follow(next_page, callback=self.parse)