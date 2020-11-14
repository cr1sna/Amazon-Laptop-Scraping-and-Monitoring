import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from laptop_price_scraper import LaptoppriceSpider
from utils import get_past_data, save_data, send_notification

MESSAGE_TEMPLATE = 'Price Change detected\nASIN:{}\nOld Price:{}\t\tNew Price:{}'

if __name__ == "__main__":
    
    amazon_data = []
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(LaptoppriceSpider, amazon_data)
    process.start() 

    curr_df = pd.DataFrame(amazon_data)


    old_data =  get_past_data()
    
    if len(old_data)!=0:
        for i in range(len(curr_df)):
            price = curr_df['price'].iloc[i]
            asin = curr_df['asin'].iloc[i]
            

            old_price = old_data[old_data['asin']==asin]['price'].iloc[0]
            if old_price!=price:
                message = MESSAGE_TEMPLATE.format(asin,old_price,price)
                print(message)
                send_notification(message)

    save_data(curr_df)
