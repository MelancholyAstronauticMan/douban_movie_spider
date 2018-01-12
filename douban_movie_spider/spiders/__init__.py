# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
from douban_movie_spider.items import DoubanMovieSpiderItem

class InitSpider(scrapy.Spider):
    name = "douban_movie"
    allowed_domains = ["movie.douban.com"]
    start_urls = [
        "https://movie.douban.com/"
    ]

    def parse(self, response):
        current_url=response.url
        if(current_url.startswith("https://movie.douban.com/subject")):
            item=DoubanMovieSpiderItem()
            item["link"] = current_url#豆瓣详情页地址
            item["title"]=response.xpath('//*[@id="content"]/h1/span[1]').extract()#电影名称
            item["year"]=response.xpath('//*[@id="content"]/h1/span[2]').extract()#电影年份
            item["info"]=response.xpath('//*[@id="info"]').extract()#影片基本信息
            item["related_info"]=response.xpath('//*[@id="content"]/div[2]/div[1]/div[3]').extract()#简介
            yield item

        for url in response.xpath('//a/@href').extract():
            # response.urljoin(url)  处理相对路径
            # dont_filter=False  去重
            yield scrapy.Request(response.urljoin(url), callback=self.parse,dont_filter=False)