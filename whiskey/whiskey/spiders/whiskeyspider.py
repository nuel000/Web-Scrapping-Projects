import scrapy
import requests

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
class WhiskeyspiderSpider(scrapy.Spider):
    name = "whiskeyspider"
    allowed_domains = ["whiskyshop.com"]
    start_urls = ["https://www.whiskyshop.com/scotch-whisky/all?item_availability=In+Stock"]



    def parse(self, response):
        products = response.css('div.product-item-info')
        for item in products:
            try:
                
                yield{
                    'product_id' : item.css("a::attr(data-id)").get(),
                    'product_name': item.css("a::attr(data-name)").get(),
                    'product_price' : item.css("a::attr(data-price)").get(),
                    'product_link' : item.css("a::attr(href)").get(),
                    'image_url' : item.css('img::attr(src)').get(),
                    }
            except:
                yield{

                    'product_id' : item.css("a::attr(data-id)").get(),
                    'product_name': item.css("a::attr(data-name)").get(),
                    'product_price' : 'sold out',
                    'product_link' : item.css("a::attr(href)").get(),
                    'image_url' : item.css('img::attr(src)').get(),
                }
                


        next_page_url =response.css("a[title=Next]::attr(href)").get()
        if next_page_url is not None:
            yield response.follow(next_page_url, callback = self.parse)