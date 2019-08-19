# -*- coding: utf-8 -*-
import scrapy
import json
from MyScrapy.items import JobItems


class LagouspiderSpider(scrapy.Spider):
    name = 'lagouspider'
    allowed_domains = \
        ['https://www.lagou.com/jobs/list_数据分析?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput=']

    start_headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://www.lagou.com/jobs/list_%E8%BF%90%E7%BB%B4?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput=',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
    keyword = ""
    page_num = 1
    total_page_num = 30
    total_count = 0

    def start_requests(self):
        # 先访问页面，后调用ajax接口查询职位信息，直接调会被反爬
        login_url = "https://www.lagou.com/jobs/list_数据分析?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput="
        self.keyword = input("输入关键字:")
        yield scrapy.Request(login_url, self.parse, headers=self.start_headers, dont_filter=True)

    def parse(self, response):
        # 查询每页信息
        data_ulr = "https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&first=true&pn={}&kd={}". \
            format(str(self.page_num), str(self.keyword))
        response.headers['Referer'] = 'https://www.lagou.com/jobs/list_%E8%BF%90%E7%BB%B4?city=%E6%88%90%E9%83%BD&cl=fal' \
                                      'se&fromSearch=true&labelWords=&suginput='
        yield scrapy.Request(data_ulr, self.parse_page_content, headers=response.headers, dont_filter=True, method="POST")
        # 判断当前页数，是否还有下一页，是继续调用
        if self.page_num < self.total_page_num:
            self.page_num += 1
            login_url = "https://www.lagou.com/jobs/list_数据分析?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput="
            yield scrapy.Request(login_url, self.parse, headers=self.start_headers, dont_filter=True,method="GET")

    # 解析每页数据
    def parse_page_content(self, response):
        response_json = json.loads(response.text)
        position_result = response_json['content']['positionResult']
        page_size = int(response_json['content']['pageSize'])
        total_count = int(position_result['totalCount'])
        # 计算最大页数（网页实际只显示前三十页）
        # self.total_page_num = int(total_count / page_size)
        results = position_result["result"]
        if len(results) == 0:
            return
        job_dates = []
        for result in results:
            job_date = []
            item = JobItems()
            position_name = result["positionName"]
            company_name = result["companyFullName"]
            salary = result["salary"]
            # avg_salary_data = int(job_avg_salary(salary))
            # avg_salary_scope = salary_scope(avg_salary_data)
            # salary_list.append(salary)
            work_year = result["workYear"]
            city = result["city"]
            create_time = result["createTime"]
            position_dvantage = result["positionAdvantage"]
            company_size = result["companySize"]
            company_label_list = result["companyLabelList"]
            position_lables = result["positionLables"]
            skill_lables  = result["skillLables"]

            """
            item["position_name"] = position_name
            item["company_name"] = company_name
            item["salary"] = salary
            item["work_year"] = work_year
            item["city"] = city
            item["create_time"] = create_time
            """
            job_date = [position_name, company_name, salary, work_year, city, create_time,position_dvantage,
                        company_size,company_label_list,position_lables,skill_lables]
            job_dates.append(job_date)
        item["job_list"] = job_dates
        print("获得数据："+str(len(job_dates))+"条")
        yield item

