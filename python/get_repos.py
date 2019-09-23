import scrapy


class GitHubSpider(scrapy.Spider):
    name = 'github_spider'
    start_urls = ['https://github.com/search?o=desc&q=followers%3A%3E%3D38000&s=updated&type=Repositories']

    def parse(self, response):
       """ Main function that parses downloaded pages """
       # Print what the spider is doing
       print(response.url)
       # Get all the <a> tags
       a_selectors = response.xpath('//ul[@class="repo-list"]/li//h3/a/@href').extract()
       print('############################################')
       print(a_selectors)
       # Loop on each tag
       #for li in a_selectors:
       ## Extract the link text
       #     href = li.xpath("/h3/a/#href").extract_first()
       ##    # Extract the link href
       ##    link = selector.xpath("@href").extract_first()
       ##    # Create a new Request object
       ##    #request = response.follow(link, callback=self.parse)
       ##    # Return it thanks to a generator
       next_page_url = response.xpath('//a[@class="next_page"]/@href').extract_first()
       next_page_url = response.urljoin(next_page_url)
       yield scrapy.Request(url = next_page_url, callback = self.parse)


    