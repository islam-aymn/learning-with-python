import scrapy


class IetfSpider(scrapy.Spider):
    name = "ietf"
    allowed_domains = ["pythonscraping.com"]
    start_urls = ["http://pythonscraping.com/linkedin/ietf.html"]

    def parse(self, response, **kwargs):

        title = response.xpath("//span[@class='title']/text()").get()
        phone = response.xpath("//span[@class='phone']/text()").get()
        return {"title": title, "phone": phone}
