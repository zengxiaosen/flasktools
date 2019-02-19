import os

from scrapy.cmdline import execute
import sys
# sys.path.append("/root/PycharmProjects/flasktools/SpiderUsingScrapy/ArticleSpider")
print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy", "crawl", "jobbole"])
execute(["scrapy", "crawl", "zhihu"])