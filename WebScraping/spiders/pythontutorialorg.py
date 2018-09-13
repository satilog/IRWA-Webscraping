# -*- coding: utf-8 -*-
import scrapy


class PythontutorialorgSpider(scrapy.Spider):
    name = 'pythontutorialorg'
    allowed_domains = ['python.org']
    start_urls = ['https://docs.python.org/3/tutorial/index.html']

    def parse(self, response):
        chapters = response.xpath('//div[@class="toctree-wrapper compound"]//li[@class="toctree-l1"]/a')

        for chap in chapters:
            link = chap.xpath('.//@href').extract_first()
            abs_link = response.urljoin(link)

            yield scrapy.Request(abs_link, callback=self.parse_lesson)


    def parse_lesson(self, response):
        main = response.xpath('//div[@class="body"]/div[@class="section"]')
        l2_sect = main.xpath('./div[@class="section"]')

        main_title = main.xpath('./h1/text()').extract_first()
        main_desc = main.xpath('./p//text()').extract()
        main_code = main.xpath('./div[@class="highlight-python3 notranslate"]//text()').extract()

        # Looping through level 2 sections.
        if(len(l2_sect) != 0):
            for l2 in l2_sect:
                l3_sect = l2.xpath('./div[@class="section"]')

                l2_title = l2.xpath('./h2/text()').extract_first()
                l2_desc = l2.xpath('./p//text()').extract()
                l2_code = l2.xpath('./div[@class="highlight-python3 notranslate"]//text()').extract()

                if(len(l3_sect) != 0):
                    for l3 in l3_sect:
                        l3_title = l3.xpath('./h3/text()').extract_first()
                        l3_desc = l3.xpath('./p//text()').extract()
                        l3_code = l3.xpath('./div[@class="highlight-python3 notranslate"]//text()').extract()

                        yield { 'URL': response.url,
                                'Language': 'Python',
                                'M_Title': main_title,
                                'M_Desc': main_desc,
                                'M_Code': main_code,
                                'L2_Title': l2_title,
                                'L2_Desc': l2_desc,
                                'L2_Code': l2_code,
                                'L3_Title': l3_title,
                                'L3_Desc': l3_desc,
                                'L3_Code': l3_code
                                }
                else:
                    yield { 'URL': response.url,
                            'Language': 'Python',
                            'M_Title': main_title,
                            'M_Desc': main_desc,
                            'M_Code': main_code,
                            'L2_Title': l2_title,
                            'L2_Desc': l2_desc,
                            'L2_Code': l2_code,
                            'L3_Title': '',
                            'L3_Desc': [],
                            'L3_Code': []
                            }
        else:
            yield { 'URL': response.url,
                    'Language': 'Python',
                    'M_Title': main_title,
                    'M_Desc': main_desc,
                    'M_Code': main_code,
                    'L2_Title': '',
                    'L2_Desc': [],
                    'L2_Code': [],
                    'L3_Title': '',
                    'L3_Desc': [],
                    'L3_Code': []
                    }
