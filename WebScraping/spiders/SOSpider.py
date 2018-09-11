# -*- coding: utf-8 -*-
import scrapy

class SospiderSpider(scrapy.Spider):
    name = 'SOSpider'
    allowed_domains = ['stackoverflow.com']
    start_urls = ['https://stackoverflow.com/questions/tagged/python?sort=votes&pageSize=50']

    def parse(self, response):
        #quest_sums = response.xpath('//div[@class="question-summary"]')

        question_links = response.xpath('//div[@class="question-summary"]//a[@class="question-hyperlink"]')

        for qlinks in question_links:
            # can use extract() just for safety use extract_first so spider can continue to run
            rel_l = qlinks.xpath('./@href').extract_first()
            abs_l = response.urljoin(rel_l)

            yield scrapy.Request(abs_l, callback = self.parse_question_page)

    def parse_question_page(self, response):

        quest_sect = response.xpath('//div[@class="inner-content clearfix"]')

        print(quest_sect)
        print('\n')

        q_title = quest_sect.xpath('.//div[@id="question-header"]//a[@class="question-hyperlink"]/text()').extract_first()
        q_votes = quest_sect.xpath('.//div[@class="question"]//*[@itemprop="upvoteCount"]/text()').extract_first()
        q_tags = quest_sect.xpath('.//div[@class="question"]//div[@class="post-taglist"]//a')

        tags = []

        for tag in q_tags:
            tags.append(tag.xpath('.//text()').extract_first())


        yield { 'Q_Title': q_title,
                'Q_Votes': q_votes,
                'tags': tags }
