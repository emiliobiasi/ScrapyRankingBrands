import json

import scrapy


def urls_brands():
    name = 'blogspider'
    start_urls = ['https://www.rankingthebrands.com/The-Brands-and-their-Rankings.aspx?catFilter=0&nameFilter=W']
    return start_urls


def write_results(brands):
    sorted_brands = sorted(brands, key=lambda d: d['brand_name'])
    jsonstring = json.dumps(sorted_brands)
    output_file = open('marcas.json', 'w')
    output_file.write(jsonstring)
    output_file.close()


class BrandsSpider(scrapy.Spider):
    name = 'brands'
    start_urls = urls_brands()
    brands = []
    details_link = []
    images = []

    def parse(self, response):
        for title in response.css('.rankingName'):
            brand_to_write = title.css('::text').get()
            self.brands.append({'brand_name': brand_to_write})
            yield {'title': title.css('::text').get()}

        for link in response.css('a::attr(href)').getall():
            if link.startswith('Brand-detail.aspx?brandID='):
                self.details_link.append('https://www.rankingthebrands.com/' + link)

        for link in self.details_link:
            for img in response.css('img::attr(src)').getall():
                if img.startswith('logos/'):
                    self.images.append(img)

        print(self.brands)
        print(self.details_link)
        print(self.images)


    def close(self, reason):
        write_results(self.brands)
