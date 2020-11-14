import scrapy
import pandas as pd
import csv
import urllib.parse



class LaptoppriceSpider(scrapy.Spider):
   
    def __init__(self,amazon_data):
        self.amazon_data = amazon_data
        self.name = 'laptopPrice'
        self.API = 'e0dcc1b878721fc0e57c91cc84c173ba'
        self.custom_settings ={
                    # 'CONCURRENT_REQUESTS': 50,
                    'RETRY_TIMES': 50,

        }



    def start_requests(self):
        # self.API = 'e0dcc1b878721fc0e57c91cc84c173ba'
        # URLs from the google spreadsheets
        input_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTxuF4Z1COoBrs0TzVwXcdgqtDRWTgTHu98j7xK3PtnXBJYgmjioKTgMmWq5gw0wonEgc8ghjmcPCIW/pub?gid=0&single=true&output=csv'
        df = pd.read_csv(input_url)
        urls = df['url'].tolist()
        for url in urls:
            print(url)
            payload = {'api_key': self.API, 'url': url}
        # scraperapi 
            proxy_url = 'http://api.scraperapi.com/?' + urllib.parse.urlencode(payload)

            yield scrapy.Request(
                url=proxy_url,
                callback=self.parse
            )
    
   
    def parse(self, response):
        product_asin = response.xpath('//tr[contains(.,"ASIN")]/td/text()').get('').strip()
        product_price = response.css('#priceblock_ourprice::text').get('').strip()
        if product_asin=='' or product_price =='':
            yield scrapy.Request(
                url=response.url,
                dont_filter=True,
                callback=self.parse
            )
        else:
            self.amazon_data.append({
                
                'asin': product_asin,
                'price': product_price
            })
            print({
                
                'asin': product_asin,
                'price': product_price
            })
            
        