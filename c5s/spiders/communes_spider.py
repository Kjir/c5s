import scrapy
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors import LinkExtractor
from c5s.items import Article


class CommuneSpider(scrapy.contrib.spiders.CrawlSpider):
    name = "communes"
    allowed_domains = ["beppegrillo.it"]
    start_urls = ["http://www.beppegrillo.it/listeciviche/liste/jesi/"]
    rules = (
        Rule(
            LinkExtractor("listeciviche/liste/jesi/\d+/\d+/.*\.html"),
            'parse_article'
        ),
    )

    def parse_article(self, response):
        article = Article()
        article['url'] = response.url
        article['date'] = response.css("abbr.published::text").extract()
        article['title'] = response.css("h2.entry-title::text").extract()
        article['author'] = response.css("span.author a::text").extract()
        city = response.css("span.entryCity::text").extract()[0]
        self.log("City is %s" % city)
        c = response.css(".asset-body *::text").extract()
        i = 0
        for l in c:
            i += 1
            if l == city:
                break
        article['content'] = "\n".join(c[i:])
        return article
