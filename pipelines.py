# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from MyScrapy import pandasutil
from MyScrapy import settings
import scrapy


class JobPiplines(object):
    def process_item(self, item, spider):
        headers = ["职位", "公司", "薪资(k)", "工作年限要求", "城市", "创建时间","职位优势","公司规模",
                   "公司标签","职位标签","技能标签"]
        dates = item['job_list']
        pandasutil.write_csv_data(headers=headers, dates=dates, file_path=settings.DATA_FILE_PATH)