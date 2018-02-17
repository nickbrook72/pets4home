# -*- coding: utf-8 -*-
import logging
from urllib.parse import urlparse, parse_qs, urlsplit

import scrapy

FOLLOW_PAGINATE = True

fetched_urls = set()


class Pets4homeSpider(scrapy.Spider):
    name = 'pets4home'
    allowed_domains = ['pets4homes.co.uk']
    start_urls = ['https://www.pets4homes.co.uk/search/?type_id=3&advert_type=1']

    def parse(self, response):
        # fetch all breeds first
        breeds = response.css('select#petbreed option::attr(value)').extract()
        for breed_id in breeds:
            if breed_id:
                for sort in ["datenew", "dateold", "creatednew", "createdold", "pricelow", "pricehigh"]:
                    url = 'https://www.pets4homes.co.uk/search/?type_id=3&advert_type=1&sort={sort}&breed_id={breed_id}'\
                       .format(breed_id=breed_id, sort=sort)
                    yield response.follow(url, self.parse_result_page)


    def parse_result_page(self, response):
        listings = response.css("div.profilelisting")

        unique_listings = 0
        for div_listing in listings:

            url = div_listing.css('h2.headline a::attr(href)').extract_first()
            if url not in fetched_urls:
                unique_listings += 1
                categories = div_listing.css('div.categories')

                price = div_listing.css('div.listingprice::text').extract_first()
                loc = div_listing.css('div.location b::text').extract_first()
                if loc:
                    loc = loc.strip()
                if price:
                    price = price[1:].replace(',','')
                yield {
                    'url': url,
                    'title': div_listing.css('h2.headline a::text').extract_first(),
                    'location': loc,
                    'breed': categories.css('a:nth-child(3)::text').extract_first(),
                    'description': div_listing.css('.description::text').extract_first(),
                    'price': price
                }
                fetched_urls.add(url)

        if FOLLOW_PAGINATE:
            next_page = response.css('div.paginate').xpath("//a[contains(., '»')]/@href").extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield response.follow(next_page, callback=self.parse_result_page)

        # else:
        #     if unique_listings == num_listings:
        #         url = urlsplit(response.request.url)
        #         next_page = int(parse_qs(url.query)['page'][0]) + 1
        #
        #         if next_page < 1000:
        #             next_page_url = 'https://www.pets4homes.co.uk/search/?type_id=3&advert_type=1&results=20&sort=datenew&page={}'.format(next_page)
        #             yield response.follow(next_page_url, callback=self.parse)
        #     else:
        #         logging.info("Terminated spider due to dups")