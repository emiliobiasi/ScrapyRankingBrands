import json

import scrapy



def urls_brands():
    name = 'blogspider'
    start_urls = ['https://www.rankingthebrands.com/The-Brands-and-their-Rankings.aspx?catFilter=0&nameFilter=W']
    return start_urls


def write_results(brands, gbin, websites, countries):
    sorted_brands = sorted(brands, key=lambda d: d['brand_name'])
    i = 0
    for brand in sorted_brands:
        brand_name = brand['brand_name']
        brand['gbin'] = gbin[i]
        brand['website'] = websites[i]
        brand['country'] = countries[i]
        i+=1
        

    jsonstring = json.dumps(sorted_brands)
    with open('marcas.json', 'w') as output_file:
        output_file.write(jsonstring)


class BrandsSpider(scrapy.Spider):
    name = 'brands'
    start_urls = urls_brands()
    brands = list()
    details_link = []
    names = []
    gbin = list()
    websites = list()
    countries = list()

    def parse(self, response):
        for title in response.css('.rankingName'):
            brand_to_write = title.css('::text').get()
            self.brands.append({'brand_name': brand_to_write})
            yield {'title': title.css('::text').get()}

        for link in response.css('a::attr(href)').getall():
            if link.startswith('Brand-detail.aspx?brandID='):
                self.details_link.append('https://www.rankingthebrands.com/' + link)

        
        for link in self.details_link:
            yield scrapy.Request(link, callback=self.parse_details)

        print(self.brands)
        print(self.details_link)
        print(self.countries)

    def parse_details(self, response):
        for c in response.css('div.brandInfoRow'):
            g = c.css('span#ctl00_mainContent_LBLGBIN::text').get()
            website = c.css('a[rel="nofollow"]::text').get()
            country = c.css('span#ctl00_mainContent_LBCountryOfOrigin::text').get()
            if g != None:
                self.gbin.append(g)
                print(g)
            if country != None:
                self.countries.append(country)
                print(country)
            if website != None and website != 'http://www.GBIN.info':
                self.websites.append(website)
                print(website)
            

        print(self.gbin)
        print(self.countries)
        print(self.websites)
            

        #for c in response.css('.element .style'):
            #name = c.css('#ctl00_mainContent_LBBrandName::text').get()
            #if name != None:
                #self.names.append(name)
                #print(name)
 
        #print(self.countries)
        #print(self.name)

    

    def close(self, reason):
        write_results(self.brands, self.gbin, self.websites, self.countries)
