import json

import scrapy

from bd import bd


def urls_brands():
    start_urls = ['https://www.rankingthebrands.com/The-Brands-and-their-Rankings.aspx?catFilter=0&nameFilter=W']

    # realizei apenas a captura de uma letra por conta do tempo de execução que daria captando todas as marcas,
    # porem ficaria desta forma:

    # base_url = 'https://www.rankingthebrands.com/The-Brands-and-their-Rankings.aspx?catFilter=0&nameFilter='
    # alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # urls = list()
    # for c in alphabet:
    #     urls.append(base_url + c)
    # return urls

    return start_urls


def write_results(names, images, gbin, websites, countries):
    brands = []
    for i in range(len(names)):
        brand = {
            'brand_name': names[i],
            'image': images[i],
            'gbin': gbin[i],
            'website': websites[i],
            'country': countries[i]
        }
        brands.append(brand)

    jsonstring = json.dumps(brands)
    with open('marcas.json', 'w') as output_file:
        output_file.write(jsonstring)
    bd()


class BrandsSpider(scrapy.Spider):
    name = 'brands'
    start_urls = urls_brands()
    details_link = []
    names = list()
    gbin = list()
    websites = list()
    countries = list()
    images = list()

    def parse(self, response):
        for link in response.css('a::attr(href)').getall():
            if link.startswith('Brand-detail.aspx?brandID='):
                self.details_link.append('https://www.rankingthebrands.com/' + link)

        for link in self.details_link:
            yield scrapy.Request(link, callback=self.parse_details)

        print(self.details_link)

    def parse_details(self, response):

        for c in response.css('.brandContainer'):
            img = c.css('img::attr(src)').get()
            name = c.css('span#ctl00_mainContent_LBBrandName::text').get()
            self.images.append('https://www.rankingthebrands.com/' + str(img))

            if name is not None:
                self.names.append(name)

        for c in response.css('div.brandInfoRow'):
            g = c.css('span#ctl00_mainContent_LBLGBIN::text').get()
            website = c.css('a[rel="nofollow"]::text').get()
            country = c.css('span#ctl00_mainContent_LBCountryOfOrigin::text').get()
            if g is not None:
                self.gbin.append(g)

            if country is not None:
                self.countries.append(country)

            if website is not None and website != 'http://www.GBIN.info':
                self.websites.append(website)

    def close(self, reason):
        write_results(self.names, self.images, self.gbin, self.websites, self.countries)
