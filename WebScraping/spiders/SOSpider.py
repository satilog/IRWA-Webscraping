# -*- coding: utf-8 -*-
import scrapy
# from bs4 import BeautifulSoup

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

        next_page_link = response.xpath('//div[@class="pager fl"]//a[@rel="next"]/@href').extract_first()

        if(len(next_page_link) != 0):
            abs_n_l = response.urljoin(next_page_link)
            yield scrapy.Request(abs_n_l)


    def parse_question_page(self, response):

        quest_sect = response.xpath('//div[@class="inner-content clearfix"]')

        #print(quest_sect)
        #print('\n')

        # Obtaining Questions
        q_title = quest_sect.xpath('.//div[@id="question-header"]//a[@class="question-hyperlink"]/text()').extract_first()
        q_votes = quest_sect.xpath('.//div[@class="question"]//*[@itemprop="upvoteCount"]/text()').extract_first()
        q_tags = quest_sect.xpath('.//div[@class="question"]//div[@class="post-taglist grid gs4 gsy fd-column"]//a')
        q_cont = ((''.join(quest_sect.xpath('.//div[@class="question"]//div[@class="post-text"]//text()').extract())).replace('\n',' ')).replace('\r',' ')

        # Obtaining Tags
        taglist = []
        for tag in q_tags:
            taglist.append(tag.xpath('.//text()').extract_first())

        print(taglist)

        # Obtaining Answers
        a_aa_sect = quest_sect.xpath('.//div[@class="answer accepted-answer"]')
        a_o_sect = quest_sect.xpath('.//div[@class="answer"]')

        # Accepted Answer
        #acc_ans = []
        if len(a_aa_sect) != 0:
            aa_votes = a_aa_sect.xpath('.//*[@itemprop="upvoteCount"]/text()').extract_first()
            aa_cont = ((''.join(a_aa_sect.xpath('.//div[@class="post-text"]//text()').extract())).replace('\n',' ')).replace('\r',' ')

            yield { 'URL': response.url,
                    'Language': "Python",
                    'Q_Title': q_title,
                    'Q_Votes': q_votes,
                    'Q_Content': q_cont,
                    'Tags': taglist,
                    'A_Votes': aa_votes,
                    'A_Content': aa_cont,
                    'isAccepted': "Yes"}

        # Other Answers
        #oth_ans = []
        if len(a_o_sect) != 0:
            for o_ans in a_o_sect:
                oa_votes = o_ans.xpath('.//*[@itemprop="upvoteCount"]/text()').extract_first()
                oa_cont = ((''.join(o_ans.xpath('.//div[@class="post-text"]//text()').extract())).replace('\n',' ')).replace('\r',' ') # list of the description

                yield { 'URL': response.url,
                        'Language': "Python",
                        'Q_Title': q_title,
                        'Q_Votes': q_votes,
                        'Q_Content': q_cont,
                        'Tags': taglist,
                        'A_Votes': oa_votes,
                        'A_Content': oa_cont,
                        'isAccepted': "No"}
