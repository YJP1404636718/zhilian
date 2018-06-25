# -*- coding: utf-8 -*-
import scrapy
import re
import hashlib
import time

from urllib import parse
from ZhilianSpider.items import ZhilianspiderItem
from ZhilianSpider.untils import utils
from ZhilianSpider.untils import select_data


class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    selecename = '大数据'
    uniquename = parse.quote(selecename)
    print(uniquename)
    # 三个大括号里面要填充  区域  搜索关键字  页数
    url = "http://sou.zhaopin.com/jobs/searchresult.ashx?jl={}&kw={}&p={}&isadv=0"

    def start_requests(self):
        area_data = select_data.parse()
        for i in area_data:
            a = i['area']
            print(a)
            area = parse.quote(a)
            print(area)
            start_urls = self.url.format(area, self.uniquename, 1)
            yield scrapy.Request(url=start_urls, callback=self.parse, meta={'area': area})

    def parse(self, response):
        print(response.body)
        quit()
        page_num = self.get_page_num(response)
        area = response.meta['area.py']
        start_urls = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%B9%BF%E5%B7%9E&kw=%E5%A4%A7%E6%95%B0%E6%8D%AE&p=1&isadv=0'
        yield scrapy.Request(url=start_urls, callback=self.parse0)
        for i in range(1, int(page_num)):
            start_urls = self.url.format(area, self.uniquename, i)
            yield scrapy.Request(url=start_urls, callback=self.parse0)


    # 获取单个页面所有的链接
    def parse0(self, response):
        url = response.css(".zwmc div a::attr(href)").extract()
        for i in url:
            yield scrapy.Request(url=i, callback=self.get_job_info, meta={'url': i})


    @staticmethod
    def get_page_num(response):
        page = response.css(".search_yx_tj em::text")[0].extract()
        if int(page) / 60 >= 90:
            page_num = 90
        else:
            page_num = int(int(page) / 60) + 1
        return page_num

    def get_job_info(self, response):
        item = ZhilianspiderItem()
        url = response.meta['url']
        wenben = []
        money = response.css(".terminalpage-left ul li strong::text")[0].extract().replace("元/月\xa0", "").split("-")
        date = response.css(".terminalpage-left .clearfix li strong span::text")[0].extract()
        job_people = response.css(".terminalpage-left .clearfix li strong::text")[1].extract()
        jin_yan = response.css(".terminalpage-left .clearfix li strong::text")[2].extract()
        xue_li = response.css(".terminalpage-left .clearfix li strong::text")[3].extract()
        job_num = response.css(".terminalpage-left .clearfix li strong::text")[4].extract()
        lei_bie = response.css(".terminalpage-left .clearfix li strong a::text")[1].extract()
        jobplace = response.css(".terminalpage-left .clearfix li strong a::text")[0].extract()
        command = response.css(".tab-cont-box .tab-inner-cont p::text").extract()
        command = str(command)

        wenben.append(command)

        k = re.sub('[\:\'\,\s+]', '', wenben[0])[1:-1]
        info = k.replace('\\xa0', '')
        i = re.sub('[\:r\\\]', '', info)
        h = re.sub('[\:n]', '', i)
        print("i:", str(h))
        if re.findall('岗位职责(.*?)岗位要求', str(h)):
            try:
                what_todo = re.findall('岗位职责(.*?)岗位要求', str(h))
                [0].replace(':', '').replace('：', '')
                print("what_todo", what_todo)
                what_command = re.findall('岗位要求(.*?)工作地址', str(h))
                [0].replace(':', '').replace('：', '')
                print("what_command", what_command)
                work_duty_content = ''
            except Exception as err:
                print(err)
                what_todo = ''
                what_command = ''
                work_duty_content = h[0:500]
        elif re.findall('岗位职责(.*?)任职', str(h)):
            try:
                what_todo = re.findall('岗位职责(.*?)任职', str(h))
                [0].replace(':', '').replace('：', '')
                print("what_todo", what_todo)
                what_command = re.findall('要求(.*?)工作地址', str(h))
                [0].replace(':', '').replace('：', '')
                print("what_command", what_command)
                work_duty_content = ''
            except Exception as err:
                print(err)
        elif re.findall('职责介绍(.*?)岗位', str(h)):
            try:
                what_todo = re.findall(
                    '职责介绍(.*?)岗位',
                    str(h))[0].replace(
                    ':',
                    '').replace(
                    '：',
                    '')
                print("what_todo", what_todo)
            except Exception as err:
                print(err)
                what_todo = ''
                what_command = ''
                work_duty_content = h[0:500]
            except Exception as err:
                print(err)
                what_todo = ''
                what_command = ''
                work_duty_content = h[0:500]
        else:
            what_todo = ''
            what_command = ''
            work_duty_content = h[0:500]
            pass
        if re.findall('工作地址：(\w+)', str(h)):
            totalplace = re.findall('工作地址：(\w+)', str(h))[0]
            print("totalplace", totalplace)
        else:
            totalplace = ''
        if totalplace != '':
            jobarea = jobplace + '-' + totalplace[0]
            print("jobarea", jobarea)
        else:
            jobarea = jobplace
        try:
            date = int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')) * 1000)
        except Exception as err:
            print(err)
            date = '最近or招聘中'
        if len(money) == 2:
            min_salary = utils.change_to_k(int(money[0]))
            max_salary = utils.change_to_k(int(money[1]))
            item['min_salary'] = min_salary
            item['max_salary'] = max_salary
        else:
            item['min_salary'] = money[0]
            item['max_salary'] = money[0]
        item['from_website'] = '智联'
        item['location'] = jobarea
        item['publish_date'] = date
        item['work_type'] = job_people
        item['work_experience'] = jin_yan
        item['limit_degree'] = xue_li
        item['people_count'] = job_num
        item['career_type'] = lei_bie
        item['work_duty'] = what_todo
        item['work_need'] = what_command
        item['work_duty_content'] = work_duty_content
        item['work_info_url'] = url
        company_url = response.css(".fixed-inner-box div h2 a::attr(href)")[0].extract()
        print(company_url)
        yield item


