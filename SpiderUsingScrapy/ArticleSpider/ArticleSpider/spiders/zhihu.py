import json
import re

from PIL import Image
import scrapy
from scrapy import Request
from selenium.webdriver.chrome.options import Options
from urllib import parse
from scrapy.loader import ItemLoader

from ArticleSpider.items import ZhihuQuestionItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com/']

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhihu.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }

    def parse(self, response):
        print("--------------------------")
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url,  url) for url in all_urls]
        all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)

        for url in all_urls:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                print(url)
                request_url = match_obj.group(1)
                question_id = match_obj.group(2)
                print(request_url, question_id)
                yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_question)
        pass

    def parse_question(self, response):

        if "QuestionHeader-title" in response.text:
            print("latest version")
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
            if match_obj:
                question_id = int(match_obj.group(2))
            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            item_loader.add_css("title", "h1.QuestionHeader-title::text")
            item_loader.add_css("content", ".QuestionHeader-detail")
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)
            # TODO tomorrow
        else:
            print("old version , please switch to latest version")
        pass

    def start_requests(self):
        from selenium import webdriver
        import time
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-infobars')
        # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        # 驱动路径
        path = '/usr/bin/chromedriver'
        # 创建浏览器对象
        browser = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
        browser.get("https://www.zhihu.com/signin")
        # browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("13533401988")
        # browser.find_element_by_css_selector(".SignFlow-password input").send_keys("qazwsxedcrf123")
        browser.find_element_by_xpath('//button[@class="Button Button--plain"]').click()

        # browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()
        # test
        time.sleep(20)
        Cookies = browser.get_cookies()
        print("Cookies: ")
        print(Cookies)
        cookie_dict = {}
        import pickle
        for cookie in Cookies:
            f = open('/home/aonezeng/cookies/zhihu/' + cookie['name'] + '.zhihu', 'wb')
            pickle.dump(cookie, f)
            f.close()
            cookie_dict[cookie['name']] = cookie['value']
        browser.close()
        return [scrapy.Request(url=self.start_urls[0], dont_filter=True, headers=self.headers, cookies=cookie_dict)]
        # yield scrapy.Request(url=self.start_urls[0], callback=self.parse)


    def after_login(self):
        print("after login")
        pass

















        # response_text = response.text
        # match_obj = re.match('.*name="_xsrf" value="(.*?)".*', response_text, re.DOTALL)
        # _xsrf = ''
        # if match_obj:
        #     print(match_obj.group(1))
        #     _xsrf = match_obj.group(1)
        # if _xsrf:
        #     post_data = {
        #         "_xsrf": _xsrf,
        #         "phone_num": '13533401988',
        #         "password": 'qazwsxedcrf123',
        #         "captcha": "",
        #
        #     }
        #     import time
        #     t = str(int(time.time() * 1000))
        #     captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login&lang=cn".format(t)
        #     yield scrapy.Request(captcha_url, headers=self.headers, meta={"post_data": post_data},
        #                          callback=self.login_after_captcha)  # 重点

    def login_after_captcha(self, response):
        with open("captcha.gif", "wb") as f:
            f.write(response.body)
            f.close()

        from PIL import Image
        try:
            im = Image.open("captcha.gif")
            im.show()
            im.close()
        except:
            pass

        captcha = input("输入验证码\n>")

        post_data = response.meta.get("post_data", {})
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data["captcha"] = captcha
        return [scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login
        )]

    def check_login(self, response):
        # 验证服务器的返回数据是否成功
        text_json = json.loads(response.text)
        if "msg" in text_json and text_json["msg"] == "登录成功":
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)






