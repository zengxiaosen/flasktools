# -*- coding: utf-8 -*-
import datetime
import json

import scrapy
import re
from scrapy.http import Request
from urllib.parse import urljoin
from scrapy.loader import ItemLoader
from ArticleSpider.utils.common import get_md5
from ArticleSpider.items import ArticleItemLoader, JobBoleArticleItem


class JobboleSpider(scrapy.Spider):

    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1, 获取文章列表中的文章url并交给scrapy下载后并进行解析
        2, 获取下一页的url并交给scrapy进行下载,下载完成后交给parse
        :param response:
        :return:
        """
        # #archive
        post_nodes = response.css(" .floated-thumb .post-thumb a")
        print(post_nodes)
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=urljoin(response.url, post_url), meta={"front_image_url": image_url}, callback=self.parse_detail)
            # print('--')
            # print(response.url)
            # print(post_url)
            # print(parse.urljoin(response.url, post_url))

        # 提取下一页并交给scrapy进行下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):


        # 提取文章的具体字段
        # re_selector = response.xpath("/html/body/div[3]/div[3]/div[1]/div[1]/h1")
        # re2_selector = response.xpath('//*[@id="post-110287"]/div[1]/h1/text()')
        # re3_selector = response.xpath('//div[@class="entry-header"]/h1/text()')
        # print(re_selector)
        # print(re2_selector)
        # print(re3_selector.extract()[0])
        # title = re3_selector.extract()[0]
        # create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace("·", "").strip()
        # print(create_date)
        # re4_selector = response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()")
        # praise_nums = re4_selector.extract()[0]
        # print(praise_nums)
        # re5_selector = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0]
        # print(re5_selector)
        # print('--')
        # match_re = re.match(".*?(\d+).*", re5_selector)
        # fav_nums = 0
        # if match_re:
        #     fav_nums = match_re.group(1)
        # print(fav_nums)
        # comments_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()
        # match_re = re.match(".*?(\d+).*", fav_nums)
        # if match_re:
        #     comments_nums = match_re.group(1)
        # print("comment_nums:" + comments_nums)
        # content = response.xpath("//div[@class='entry']").extract()[0]
        # print(content)
        # tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith('评论')]
        # tags = ",".join(tag_list)
        # print(tag_list)

        # print("css selector ---")
        # 通过css选择器提取字段
        # 文章封面图
        # front_image_url = response.meta.get("front_image_url", "")
        # title = response.css(".entry-header h1::text").extract()[0]
        # create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace("·", "").strip()
        # praise_nums = response.css(".vote-post-up h10::text").extract()[0]
        # fav_nums = response.css("span.bookmark-btn::text").extract()[0]
        # match_re = re.match(".*?(\d+).*", fav_nums)
        # if match_re:
        #     fav_nums = int(match_re.group(1))
        # else:
        #     fav_nums = 0
        #
        # comments_nums = response.css("a[href='#article-comment'] span::text").extract()[0]
        # match_re = re.match(".*?(\d+).*", comments_nums)
        # if match_re:
        #     comments_nums = int(match_re.group(1))
        # else:
        #     comments_nums = 0
        #
        # content = response.css("div.entry").extract()[0]
        # tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith('评论')]
        # tags = ",".join(tag_list)
        # # print(title)
        # # print(create_date)
        # # print(praise_nums)
        # # print(fav_nums)
        # # print(comments_nums)
        # # print(content)
        # # print(tags)
        # article_item = JobBoleArticleItem()
        # article_item["url_object_id"] = get_md5(response.url)
        # article_item["title"] = title
        # article_item["url"] = response.url
        # try:
        #     create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()
        # article_item["create_date"] = create_date
        # article_item["front_image_url"] = [front_image_url]
        # article_item["praise_nums"] = praise_nums
        # article_item["comment_nums"] = comments_nums
        # article_item["fav_nums"] = fav_nums
        # article_item["tags"] = tags
        # article_item["content"] = content

        # item loader
        front_image_url = response.meta.get("front_image_url", "")
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("fav_nums", "span.bookmark-btn::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")
        article_item = item_loader.load_item()

        yield article_item

        #pass


