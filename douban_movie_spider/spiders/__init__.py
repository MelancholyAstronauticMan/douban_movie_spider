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
            item["link"] = current_url#��������ҳ��ַ
            item["title"]=response.xpath('//*[@id="content"]/h1/span[1]').extract()#��Ӱ����
            item["year"]=response.xpath('//*[@id="content"]/h1/span[2]').extract()#��Ӱ���
            item["info"]=response.xpath('//*[@id="info"]').extract()#ӰƬ������Ϣ
            item["related_info"]=response.xpath('//*[@id="content"]/div[2]/div[1]/div[3]').extract()#���
            yield item

        for url in response.xpath('//a/@href').extract():
            # response.urljoin(url)  �������·��
            # dont_filter=False  ȥ��
            yield scrapy.Request(response.urljoin(url), callback=self.parse,dont_filter=False)